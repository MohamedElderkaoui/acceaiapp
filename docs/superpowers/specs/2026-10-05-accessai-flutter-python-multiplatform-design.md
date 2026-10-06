# AccessAI multiplatform: Flutter client and Python GPU service

Date: 2026-10-05
Status: Draft for user review

## Goal

Replace the current Streamlit interface with a Spanish-language Flutter application for web/PWA, Android, iOS, Windows, macOS, and Linux. Keep the existing Python/YOLO accessibility analysis on a network-accessible NVIDIA GPU server.

The first release preserves the existing image and video workflows, parameter controls, accessibility scores, detections, annotated outputs, CSV downloads, and explanatory limitations. The mobile and desktop clients are user interfaces; they do not run YOLO locally.

## Agreed decisions

- Flutter is the sole user interface across supported targets; Streamlit is retired after the new clients preserve its functionality.
- The Python backend exposes a FastAPI HTTPS API.
- A single GPU worker processes video jobs through a queue, one at a time, and keeps the YOLO model loaded between jobs.
- Image analysis is request/response. Video analysis is asynchronous and reports progress to Flutter.
- Supabase Auth provides email/password accounts. There is no public registration; an administrator invites users.
- The API verifies each user's access token and authorizes every job and artifact against that user.
- Uploaded media and generated artifacts are temporary, isolated per user, and removed after 24 hours. There is no permanent analysis history.
- File type, file size, and per-account request limits are configurable.
- The web build is installable as a PWA. Inference requires an internet connection to the GPU service; the offline experience is limited to the app shell.
- Add a Windows development launcher named start.ps1. During the migration it launches the existing Streamlit entrypoint; after Flutter and FastAPI replace Streamlit, update it to start the local API, queue/worker dependencies, and Flutter client. It is not a production deployment command.
- Deploy the Flutter web bundle as static assets and the API/worker on a GPU server behind HTTPS. Secrets stay in server-side environment configuration; no administrative secret is included in a client build.

## User flows

### Sign-in and invitations

An administrator invites users through Supabase Auth. Users accept the invite, set a password, sign in, sign out, and can request a password reset from any Flutter client. The client sends its access token to the Python API. The API verifies the token and uses its subject as the owner identity for jobs and downloads.

There is no self-registration or in-app administration console in the first release.

### Image analysis

A signed-in user selects an image, adjusts confidence, image size, camera field of view, and distance limits, then submits the analysis. The client displays the annotated image, summary score and level, detection table, and CSV download. Results without detections retain the existing explanatory message that an empty result does not establish accessibility.

### Video analysis

A signed-in user selects a supported video, sets the same analysis options plus frame sampling, and submits it. The API creates a job and returns its identifier. Flutter polls job status and progress, then displays the average and worst frame scores, detections by frame, annotated MP4 playback/download, and CSV download when processing completes.

### Project information

The client retains the existing project description, class names, heuristic distance explanation, current model/runtime information that is safe to expose, and prototype limitations. It does not expose server secrets or local filesystem paths.

## System design

### Flutter clients

One Flutter codebase provides responsive layouts for web/PWA, Android, iOS, Windows, macOS, and Linux. The web client is delivered as a static bundle. The PWA may cache public shell assets and show an offline message, but must not cache uploaded media, private results, or authentication secrets.

The client receives API and Supabase public configuration from environment-specific build configuration. The private Supabase admin key and any backend credentials remain on the server.

### Python API and inference worker

The API accepts multipart file uploads and validated analysis parameters. It returns structured JSON for image results and job identifiers for video work. Video status exposes queued/running/completed/failed states and progress. Output download routes require a valid token and an ownership match.

The worker loads the existing YOLO model once on CUDA, processes one video job at a time to bound GPU memory, and reuses the existing distance, impact, scoring, and annotation logic. The API and worker are versioned so client and server changes can be coordinated.

### Queue and temporary artifacts

The queue stores video job state and progress. Source uploads, annotated outputs, and CSVs are associated with an authenticated user and job identifier. A cleanup task removes expired inputs, outputs, and job metadata after 24 hours. The initial design targets a single GPU server; horizontal scaling is outside the first release.

### Authentication and access control

FastAPI validates Supabase-issued access tokens and rejects missing, invalid, or expired tokens. Every job lookup, status response, and output download checks ownership. Rate limits and upload limits apply per authenticated user. CORS allows only configured web app origins. HTTPS is required for production.

### Deployment

The web client is hosted as static files on an HTTPS origin. FastAPI and the GPU worker run on the selected GPU server behind an HTTPS reverse proxy. Redis is the proposed queue broker; backend, worker, queue, Supabase URL, allowed origins, upload limits, and retention duration are configured outside source control. Provide safe example configuration without real credentials.

The development start.ps1 script is for Windows. In the current migration stage it launches streamlit_app.py on localhost after checking Python dependencies and warning if CUDA is unavailable. Once the Flutter and FastAPI projects exist, update it to check prerequisites, start local API/queue/worker services, and launch Flutter in a selected target (web by default). It prints clear setup guidance when required tooling is missing. It does not create cloud resources or publish any build.

## Existing project mapping

- Reuse the existing Python calculations and YOLO inference behavior while separating them from Streamlit rendering.
- Move server-side code into a backend package and declare its Python dependencies.
- Add a Flutter project for all client targets.
- Replace Streamlit installation and launch instructions in the README with client, API, authentication, and deployment setup.
- Keep the existing model checkpoint and accessible result warnings.
- Do not commit secrets, uploaded user media, or generated analysis artifacts.

## Constraints and open deployment inputs

- A production API URL, Supabase project, email delivery configuration, domain, and GPU host credentials are not present in this repository. The implementation must use configuration placeholders and document how an administrator supplies them.
- The current Windows environment has Python but Flutter was not found on PATH during read-only inspection. Builds cannot be confirmed until Flutter tooling is installed.
- iOS/macOS and Linux release builds need their respective supported build environments. Source support does not imply all release binaries can be produced from this Windows host.
- Model weights and inference still require an NVIDIA CUDA environment. The app does not fall back to CPU.

## Acceptance criteria

- Users invited by an administrator can sign in on supported Flutter clients; uninvited users cannot create accounts.
- Image analysis preserves the current adjustable parameters and returns a score, detections, annotated image, and CSV.
- Video analysis uses queued processing, reports progress, and returns summary, detections, annotated MP4, and CSV.
- A user cannot inspect another user's job or download another user's artifacts.
- Expired media and job artifacts are removed automatically after the configured 24-hour period.
- Flutter Web installs as a PWA over HTTPS and presents an offline state without implying that inference works offline.
- start.ps1 starts the local Windows development stack and reports missing prerequisites without exposing secrets.
- README documents local development and the production deployment boundary.

