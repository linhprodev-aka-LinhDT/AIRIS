# AIRIS - Phase 2 Progress (Tiến độ giai đoạn 2)

## Mục tiêu Phase 2

Giai đoạn này tập trung vào module xử lý đầu vào video:
- hỗ trợ webcam
- hỗ trợ video file
- mở/đọc/giải phóng capture
- xử lý lỗi khi nguồn không mở được
- chuẩn bị pipeline cho các phase sau

## File đã thêm

### src/video_capture.py
- lớp `VideoCapture` đóng gói `cv2.VideoCapture`
- hỗ trợ `open()`, `read()`, `release()`
- có `__enter__` và `__exit__` để sử dụng dễ dàng hơn
- log rõ ràng khi mở và đóng nguồn video
- ném `RuntimeError` khi không mở được camera hoặc file video

### tests/test_video_capture.py
- tạo video test thực tế bằng OpenCV
- kiểm tra khởi tạo và đọc frame
- kiểm tra trường hợp source không hợp lệ

## Lưu ý kỹ thuật

- Module này vẫn là nền tảng cho việc sau này đổi sang RTSP/IP camera mà không làm thay đổi phần logic pipeline chính.
- Việc lê thiết bị webcam thật không được thực hiện trong test vì mục tiêu test core logic không cần hardware.

## Kế hoạch tiếp theo

Phase 3 sẽ triển khai:
- `src/detector.py`
- YOLO loading và inference
- output format chuẩn cho tracker

Ngày cập nhật: 2026-09-16
