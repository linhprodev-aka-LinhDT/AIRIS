# AIRIS - Phase 4 Progress (Tiến độ giai đoạn 4)

## Mục tiêu Phase 4

Giai đoạn này tập trung vào tracking khung hình:
- gán `track_id` cho từng người
- giữ `track_id` ổn định qua nhiều frame
- chuẩn bị dữ liệu cho phân tích hành vi theo thời gian
- không chứa logic cảnh báo trong tracker

## File đã thêm

### src/tracker.py
- class `Tracker`
- class `Track`
- mỗi track ghi:
  - `track_id`
  - `class_name`
  - `bbox`
  - `confidence`
  - `age`
  - `hits`
  - `metadata`
- hoạt động đơn giản dựa trên khoảng cách tâm bounding box
- nếu người mới xuất hiện, tạo track mới
- nếu cùng người xuất hiện ở frame sau, giữ lại `track_id`

### tests/test_tracker.py
- test `track_id` duy nhất khi phát hiện nhiều người
- test `track_id` được giữ ổn định trên frame tiếp theo cho cùng một người

## Lưu ý kỹ thuật

- Tracker ở giai đoạn này nhằm mục đích thiết lập contract dữ liệu rõ ràng cho các phase sau.
- Một tracker mạnh hơn như ByteTrack sẽ được thay vào sau này, nhưng kiến trúc hiện tại đã tạo ra tầng abstraction đủ để nâng cấp dễ dàng.

## Kế hoạch tiếp theo

Phase 5 sẽ triển khai:
- `src/temporal_analysis.py`
- state machine hướng tới smoking detection
- logic chống false positive theo nhiều frame liên tiếp

Ngày cập nhật: 2026-09-16
