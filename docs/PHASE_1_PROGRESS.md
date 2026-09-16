# AIRIS - Phase 1 Progress (Tiến độ giai đoạn 1)

## 1. Mục tiêu giai đoạn 1

Giai đoạn này tập trung vào việc xây dựng nền tảng project và chuẩn bị môi trường phát triển trước khi bắt đầu các module AI/Computer Vision chính.

Các mục tiêu chính:
- tạo cấu trúc thư mục theo kiến trúc dự án
- tạo file cấu hình chung
- chuẩn bị virtual environment
- cài đặt dependency cần thiết
- kiểm tra import và môi trường Python
- sẵn sàng cho các phase sau: video capture, detector, tracker, temporal analysis, alert manager, SQLite logger

## 2. Kiến trúc đã xác định

AIRIS được thiết kế theo hướng modular, rõ ràng theo tầng:

INPUT
  ↓
PERCEPTION (YOLO)
  ↓
TRACKING
  ↓
TEMPORAL REASONING
  ↓
DECISION
  ↓
ALERT
  ↓
LOGGING

Trong đó:
- PERCEPTION = YOLO
- TRACKING = ByteTrack / tracker tương thích
- TEMPORAL REASONING = state machine theo track_id
- DECISION = evidence + threshold + cooldown
- ALERT = snapshot + cảnh báo + interface chuẩn cho ESP32
- LOGGING = SQLite

## 3. Cấu trúc thư mục đã tạo

```text
AIRIS/
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
├── README.md
├── docs/
│   └── PHASE_1_PROGRESS.md
├── models/
│   └── README.md
├── data/
│   ├── input/
│   ├── snapshots/
│   └── database/
├── src/
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_detector.py
│   ├── test_tracker.py
├── scripts/
│   ├── setup.ps1
│   └── run_test.ps1
└── .venv/
```

## 4. File đã tạo và trách nhiệm

### config.py
- định nghĩa cấu hình tập trung cho toàn bộ project
- chứa đường dẫn model, source camera, confidence threshold, IoU, database path, snapshot dir, debug flag
- dùng dataclass để dễ mở rộng

### main.py
- file entrypoint chính
- hỗ trợ CLI arguments cơ bản
- chuẩn bị cấu hình logging và pipeline orchestration trong giai đoạn sau

### requirements.txt
- chứa dependency chính cho AI / CV:
  - ultralytics
  - opencv-python
  - numpy
  - torch
  - torchvision
  - pytest
- giữ nguyên mục tiêu CPU-first để chạy được trên Windows dễ dàng hơn

### README.md
- mô tả dự án, mục tiêu, cấu trúc, setup, chạy ứng dụng
- ghi chú ngắn gọn cho phase đầu tiên

### .gitignore
- loại bỏ file nhạy cảm, cache, môi trường ảo, snapshot tạm thời, model nhạy cảm

### models/README.md
- mô tả nơi lưu model YOLO sẽ thay đổi trong tương lai

### data/*
- khởi tạo thư mục input, snapshots, database
- hỗ trợ lưu hình ảnh cảnh báo và database SQLite sau này

### scripts/setup.ps1
- tự động tạo venv
- nâng cấp pip
- cài requirements
- tạo folder cần thiết
- kiểm tra import các module chính

### scripts/run_test.ps1
- chạy pytest trong môi trường ảo

### tests/*
- tạo test placeholder chuẩn bị cho các phase tiếp theo

## 5. Công việc đã thực hiện

1. Phân tích yêu cầu dự án và cấu trúc sản phẩm.
2. Xác định kiến trúc modular theo pipeline của AIRIS.
3. Tạo root project và các thư mục cần thiết.
4. Tạo file cấu hình `config.py`.
5. Tạo entry point `main.py`.
6. Tạo `requirements.txt` phù hợp với hướng phát triển CPU-first.
7. Tạo `.gitignore` để tránh nhầm lẫn với model và dữ liệu.
8. Tạo `README.md` nền tảng cho documentation ban đầu.
9. Tạo `scripts/setup.ps1` để tự động hóa môi trường Windows.
10. Tạo `docs/PHASE_1_PROGRESS.md` để ghi lại tiến độ.

## 6. Kết quả kiểm tra môi trường

Về mặt kỹ thuật, quá trình đã xác minh rằng môi trường Python hệ thống đang hoạt động, và mục tiêu của Phase 1 là thiết lập được project skeleton và chuẩn bị dependency. Các bước cài đặt và import package chính sẽ được tiếp tục kiểm tra bằng virtual environment trong quá trình phát triển tiếp theo.

## 7. Ghi chú quan trọng

- Dự án hiện đang ở trạng thái skeleton, chưa triển khai pipeline YOLO/thông tin thực sự.
- Chưa bỏ qua việc cài đặt dependencies hoặc import package chính, nhưng project đã được chuẩn bị đúng hướng cho các phase tiếp theo.
- Cần tiếp tục thực hiện theo lộ trình đã đặt: video_capture, detector, tracker, temporal_analysis, alert_manager, event_logger, main pipeline, testing.

## 8. Phase kế tiếp

Phase 2 sẽ bắt đầu với:
- implement `src/video_capture.py`
- kiểm tra webcam / video file
- kiểm tra open/read/release
- validate rõ ràng khi camera không mở được

## 9. Người thực hiện

AIRIS project - Phase 1 setup

Ngày cập nhật: 2026-09-16
