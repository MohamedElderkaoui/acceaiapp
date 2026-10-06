# AccessAI Mobile (Reflex)

Aplicación móvil orientada a navegador con Reflex para prototipos multi-device y acceso a cámara del navegador.

## Requisitos

- Python 3.11+
- Node.js 22.22.0 o superior
- Reflex 0.9.12

## Ejecutar

```bash
cd accessai_mobile
python -m reflex run
```

## Nota importante

La app compila correctamente en Python, pero en este equipo la ejecución frontend falló por una versión de Node demasiado antigua (`20.18.0`). Reflex recomienda Node 22.22.0+.

## Uso

- Pantalla responsiva
- cámara del navegador con acceso a `getUserMedia`
- ajuste de confianza
- tarjetas de clases urbanas

## Siguiente paso

Integrar el modelo YOLO real y la lógica de accesibilidad en tiempo real una vez el entorno frontend esté actualizado.
