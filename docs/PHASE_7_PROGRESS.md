# AIRIS - Phase 7 Progress (Tiến độ giai đoạn 7)

## Mục tiêu Phase 7

Giai đoạn này tập trung vào logging sự kiện bằng SQLite:
- tạo database tự động nếu chưa có
- lưu event không chứa dữ liệu cá nhân nhạy cảm
- lưu thông tin kỹ thuật cần thiết: timestamp, event_type, track_id, confidence, snapshot_path, duration, metadata
- chuẩn bị cho việc tổng hợp sự kiện sau này

## File đã thêm

### src/event_logger.py
- class `EventLogger`
- tạo database SQLite nếu chưa tồn tại
- khởi tạo schema `events`
- method `log_event()` ghi sự kiện
- method `get_events()` đọc log mới nhất
- method `clear_events()` xóa dữ liệu nếu cần

### tests/test_event_logger.py
- kiểm tra database được tạo
- kiểm tra sự kiện được lưu đúng trường và kiểu dữ liệu

## Lưu ý kỹ thuật

- Không lưu thông tin nhận dạng cá nhân lâu dài, không lưu khuôn mặt, không lưu tên người.
- Chỉ lưu thông tin kỹ thuật phục vụ giám sát và kiểm tra hệ thống.

## Kế hoạch tiếp theo

Phase 8 sẽ nối toàn bộ pipeline trong `main.py`:
- VideoCapture
- YOLODetector
- Tracker
- TemporalAnalyzer
- AlertManager
- EventLogger

Ngày cập nhật: 2026-09-16
