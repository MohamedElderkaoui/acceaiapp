[CmdletBinding()]
param(
    [ValidateRange(1, 65535)]
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$AppPath = Join-Path $ProjectRoot "streamlit_app.py"
$LocalPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $AppPath -PathType Leaf)) {
    throw "No se encontró la aplicación: $AppPath"
}

$PythonPath = $null
$PythonArguments = @()

if (Test-Path -LiteralPath $LocalPython -PathType Leaf) {
    $PythonPath = $LocalPython
} else {
    $PythonCommand = Get-Command "python.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($PythonCommand) {
        $PythonPath = $PythonCommand.Source
    } else {
        $PythonLauncher = Get-Command "py.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($PythonLauncher) {
            $PythonPath = $PythonLauncher.Source
            $PythonArguments = @("-3")
        }
    }
}

if (-not $PythonPath) {
    throw "No se encontró Python. Instala Python 3 o crea el entorno del proyecto en .venv."
}

$ImportCheck = "import cv2, pandas, streamlit, torch; from ultralytics import YOLO"
$DependencyOutput = & $PythonPath @PythonArguments -c $ImportCheck 2>&1
$DependencyExitCode = $LASTEXITCODE

if ($DependencyExitCode -ne 0) {
    Write-Host ($DependencyOutput | Out-String)
    throw @"
Faltan dependencias de AccessAI en el Python seleccionado:
  $PythonPath

Consulta la sección de instalación de README.md. Instala primero PyTorch con CUDA compatible
y después las dependencias de requirements.txt. El script no instala paquetes automáticamente.
"@
}

$CudaOutput = & $PythonPath @PythonArguments -c "import torch; print(torch.cuda.is_available())" 2>$null
$CudaExitCode = $LASTEXITCODE
if ($CudaExitCode -eq 0 -and $CudaOutput.Trim() -ne "True") {
    Write-Warning "PyTorch no detecta CUDA. AccessAI requiere una GPU NVIDIA para ejecutar inferencias."
}

Write-Host "Iniciando AccessAI en http://127.0.0.1:$Port"
Write-Host "Pulsa Ctrl+C para detener Streamlit."

& $PythonPath @PythonArguments -m streamlit run $AppPath "--server.address=127.0.0.1" "--server.port=$Port"
exit $LASTEXITCODE
