"""AccessAI mobile app for camera-based object detection."""

import reflex as rx


CLASS_NAMES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal",
]


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("AccessAI Mobile", size="9"),
            rx.text(
                "Detección urbana con acceso a cámara",
                size="5",
            ),
            rx.box(
                rx.html(
                    """
                    <style>
                    .accessai-shell {
                        width: 100%;
                        max-width: 880px;
                        border-radius: 24px;
                        overflow: hidden;
                        border: 1px solid rgba(148, 163, 184, 0.4);
                        background: linear-gradient(135deg, #020817 0%, #0f172a 100%);
                        box-shadow: 0 18px 50px rgba(15, 23, 42, 0.35);
                    }
                    .accessai-video-wrap {
                        position: relative;
                        width: 100%;
                        aspect-ratio: 4 / 5;
                        background: #020617;
                    }
                    .accessai-video-wrap video {
                        width: 100%;
                        height: 100%;
                        display: block;
                        object-fit: cover;
                        background: #020617;
                    }
                    .accessai-overlay {
                        position: absolute;
                        inset: 0;
                        display: flex;
                        align-items: flex-end;
                        justify-content: space-between;
                        padding: 16px;
                        pointer-events: none;
                        background: linear-gradient(to top, rgba(2, 6, 23, 0.72), rgba(15, 23, 42, 0.08));
                        font-family: sans-serif;
                    }
                    .accessai-pill {
                        padding: 8px 12px;
                        border-radius: 999px;
                        font-size: 12px;
                        font-weight: 700;
                        letter-spacing: 0.04em;
                        background: rgba(15, 23, 42, 0.75);
                        color: white;
                        border: 1px solid rgba(148, 163, 184, 0.4);
                    }
                    .accessai-button {
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        width: 100%;
                        padding: 14px 18px;
                        margin-top: 14px;
                        font-size: 15px;
                        font-weight: 700;
                        color: white;
                        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                        border: none;
                        border-radius: 14px;
                        cursor: pointer;
                    }
                    .accessai-button:active { opacity: 0.95; }
                    .accessai-status {
                        margin-top: 12px;
                        color: #dbeafe;
                        font-size: 14px;
                        font-family: sans-serif;
                    }
                    </style>
                    <div class="accessai-shell">
                      <div class="accessai-video-wrap">
                        <video id="accessai-video" autoplay playsinline muted></video>
                        <div class="accessai-overlay">
                          <span class="accessai-pill">AccessAI</span>
                          <span class="accessai-pill">LIVE</span>
                        </div>
                      </div>
                      <button id="cameraButton" class="accessai-button">Activar cámara</button>
                      <div id="cameraStatus" class="accessai-status">Cámara no activa.</div>
                    </div>
                    <script>
                      const video = document.getElementById('accessai-video');
                      const button = document.getElementById('cameraButton');
                      const status = document.getElementById('cameraStatus');

                      async function startCamera() {
                        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                          status.textContent = 'Tu navegador no admite acceso a cámara.';
                          return;
                        }

                        try {
                          const stream = await navigator.mediaDevices.getUserMedia({
                            video: { facingMode: 'environment' },
                            audio: false,
                          });
                          video.srcObject = stream;
                          await video.play();
                          button.textContent = 'Cámara activa';
                          status.textContent = 'Cámara habilitada. Se está solicitando detección visual.';
                        } catch (error) {
                          console.error('AccessAI camera error:', error);
                          status.textContent = 'No se pudo acceder a la cámara. Acepta el permiso del navegador.';
                        }
                      }

                      button.addEventListener('click', startCamera);
                    </script>
                    """
                ),
                width="100%",
                margin_top="1em",
                margin_bottom="1em",
            ),
            rx.heading("Clases detectadas", size="6"),
            rx.grid(
                *[
                    rx.box(
                        rx.text(name, weight="bold"),
                        rx.text("Impacto medio / alto", size="2"),
                        padding="1rem",
                        border="1px solid #334155",
                        border_radius="16px",
                        background_color="#0f172a",
                    )
                    for name in CLASS_NAMES
                ],
                columns="2",
                spacing="3",
                width="100%",
            ),
            rx.box(
                rx.text(
                    "La cámara debe activarse desde un clic del usuario para que el navegador permita el permiso.",
                    size="3",
                ),
                padding="1rem",
                border_radius="18px",
                background_color="#111827",
                width="100%",
            ),
            spacing="5",
            justify="center",
            min_height="90vh",
            width="100%",
            padding_bottom="4em",
        ),
        max_width="960px",
        padding_y="2em",
    )


app = rx.App()
app.add_page(index)
