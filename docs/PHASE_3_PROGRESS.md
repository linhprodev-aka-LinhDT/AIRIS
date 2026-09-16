# AIRIS - Phase 3 Progress (Tiến độ giai đoạn 3)

## Mục tiêu Phase 3

Giai đoạn này tập trung vào module nhận diện ban đầu bằng YOLO:
- load model YOLO
- chạy inference trên frame
- trả về định dạng chuẩn cho tracker và phân tích thời gian
- đảm bảo code hoạt động cả khi model chưa có sẵn

## File đã thêm

### src/detector.py
- class `YOLODetector`
- load model bằng Ultralytics
- dùng `detect(frame)` để trả về danh sách `Detection`
- định dạng chuẩn gồm:
  - `class_id`
  - `class_name`
  - `confidence`
  - `bbox`
- nếu không tìm thấy file model, tự động fallback sang `yolo11n.pt` để kiểm tra kiến trúc mà không phá vỡ pipeline

### tests/test_detector.py
- kiểm tra output của detector có đúng định dạng và kiểu dữ liệu
- không mock logic nhận diện; test theo kiểu dữ liệu thực tế

## Lưu ý kỹ thuật

- Module detector chỉ chịu trách nhiệm perception, không chứa logic tracking hoặc alert.
- Mục tiêu là giữ detector dễ thay model sau này bằng smoking_model hoặc smoke_model mà không phải refactor lớn.

## Kế hoạch tiếp theo

Phase 4 sẽ triển khai:
- `src/tracker.py`
- tracking theo `track_id`
- dữ liệu format rõ ràng cho từng người

Ngày cập nhật: 2026-09-16
