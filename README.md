# AIRIS

AIRIS is a modular Python project for smoke detection and smoking-behavior monitoring with a privacy-first web dashboard layer.

## Architecture overview

Camera / Webcam / Video
  ↓
VideoCapture
  ↓
YOLO Detection
  ↓
Object Tracking
  ↓
Temporal Analysis
  ↓
Smoking / Smoke Decision
  ↓
Alert Manager
  ↓
Snapshot + Log
  ↓
FastAPI dashboard backend
  ↓
Privacy-safe web dashboard

## Project structure

```text
AIRIS/
├── config.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── models/
│   └── README.md
├── data/
│   ├── input/
│   ├── snapshots/
│   └── database/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── app.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── demo_data.py
│   │   └── privacy.py
│   ├── video_capture.py
│   ├── detector.py
│   ├── tracker.py
│   ├── temporal_analysis.py
│   ├── alert_manager.py
│   └── event_logger.py
├── web/
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
├── scripts/
│   ├── setup.ps1
│   ├── run_test.ps1
│   └── start_web.ps1
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_detector.py
│   ├── test_tracker.py
│   ├── test_temporal_analysis.py
│   └── test_event_logger.py
└── .venv/
```

## Setup

Open PowerShell in the project root and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For the web layer, install frontend dependencies in the `web` folder:

```powershell
cd web
npm install
```

## Run the core detection pipeline

```powershell
python main.py --source 0
python main.py --source data/input/test.mp4
```

## Run the API backend

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Then check:

```powershell
curl http://127.0.0.1:8000/api/health
```

## Run the dashboard

From the project root:

```powershell
cd web
npm run dev -- --host 0.0.0.0 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

## Quick launcher

A convenience script is available to start both backend and frontend together:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_web.ps1
```

## Demo mode and privacy layer

AIRIS includes a demo dashboard mode that exposes aggregated, privacy-safe school data without revealing personal identity. The web app intentionally does not store or expose face images, names, ID numbers, or person-level tracking paths.

The privacy page in the dashboard documents:
- what AIRIS records
- what AIRIS does not record
- retention and monitoring safeguards

## Run with the public Roboflow smoking model

The project can use the public Roboflow model `smoking-detection-3gefl/4` through the Serverless Inference API. Set the API key only in the current terminal session:

```powershell
$env:ROBOFLOW_API_KEY = "your-roboflow-api-key"
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe main.py --backend roboflow --source data/input/test.mp4 --show
```

For a webcam, replace the source with `0`:

```powershell
& .\.venv\Scripts\python.exe main.py --backend roboflow --source 0 --show
```

The Roboflow backend sends each frame to the inference API, converts returned predictions to AIRIS `Detection` objects, and then reuses the existing tracking, temporal analysis, alert, and SQLite logging pipeline.

## Model configuration

The YOLO model path is defined in `config.py`. Replace the default path with a custom model when available.

## Notes

- This project targets CPU-first execution.
- GPU acceleration can be added later if supported by the installed PyTorch build.
- The web layer is an additive extension on top of the existing AI pipeline, not a replacement.
- The dashboard uses demo data for UI simulation and privacy-safe aggregated monitoring data.
