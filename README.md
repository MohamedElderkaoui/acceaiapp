# AccessAI

AccessAI es una aplicación web creada con Streamlit que usa un modelo YOLO26s entrenado para detectar elementos urbanos en imágenes y vídeos y mostrar una estimación heurística de su impacto sobre la accesibilidad.

> Es un prototipo de apoyo visual. Sus estimaciones no sustituyen una auditoría de accesibilidad, una medición arquitectónica ni una norma técnica.

## Funcionalidades

- Analiza imágenes y vídeos cargados desde la interfaz.
- Detecta cuatro grupos: `Obstaculo_Dinamico`, `Obstaculo_Fijo`, `Barrera_Arquitectonica` e `Infraestructura_Peatonal`.
- Estima la distancia a cada detección a partir de su tamaño en la imagen, una altura de referencia por clase y el campo de visión horizontal configurado.
- Calcula un índice de accesibilidad de 0 a 100 usando penalizaciones heurísticas según la clase, la confianza, la proximidad estimada y la posición del elemento en la imagen.
- Permite ajustar la confianza mínima, el tamaño de imagen, el campo de visión, los límites de distancia y el muestreo de fotogramas de vídeo.
- Muestra el vídeo anotado y permite descargarlo junto con los resultados en CSV.

## Requisitos

- Python y las dependencias de este proyecto.
- Una GPU NVIDIA con controladores compatibles y una instalación de PyTorch con CUDA.
- Un checkpoint `best.pt` entrenado para las cuatro clases del proyecto.

La aplicación detiene la inferencia si PyTorch no detecta una GPU NVIDIA con CUDA; no tiene modo de inferencia en CPU.

## Instalación y ejecución

Desde la carpeta del proyecto, crea y activa un entorno virtual en PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Instala primero una versión de PyTorch con CUDA compatible con la GPU y los controladores del equipo. Después instala las dependencias declaradas y Ultralytics:

```powershell
python -m pip install -r requirements.txt
python -m pip install ultralytics
```

`requirements.txt` solo declara Streamlit; Ultralytics y PyTorch son necesarios para ejecutar la detección. Asegúrate de que la instalación de PyTorch tiene soporte CUDA antes de iniciar la aplicación.

Inicia la interfaz:

```powershell
streamlit run streamlit_app.py
```

Streamlit mostrará la dirección local de la aplicación en la terminal y abrirá la interfaz en el navegador.

## Modelo YOLO

La aplicación selecciona automáticamente el checkpoint más reciente que encuentre con esta estructura:

```text
runs/detect/AccessAI_YOLO26s_4clases_RTX4060_*/weights/best.pt
```

Si no encuentra uno, la interfaz permite cargar manualmente un archivo `.pt` entrenado para las cuatro clases. Para aplicar las penalizaciones y alturas de referencia específicas, el checkpoint debe usar los nombres de clase indicados arriba.

## Resultados

Los archivos generados se guardan en `runs/detect/accessibility/`:

- CSV con las detecciones y sus estimaciones cuando el análisis encuentra elementos.
- Vídeo MP4 anotado al analizar un vídeo y CSV con los resultados por fotograma si hay detecciones.

La interfaz también ofrece botones para descargar los resultados.

## Limitaciones

- La distancia se calcula con el tamaño aparente del objeto y alturas de referencia genéricas; no es una medición métrica calibrada.
- El índice de accesibilidad es una heurística del prototipo, no una evaluación conforme a normativa.
- La ausencia de detecciones no demuestra que un espacio sea accesible.
- La calidad de los resultados depende del checkpoint, la imagen, la cámara y los parámetros seleccionados.
