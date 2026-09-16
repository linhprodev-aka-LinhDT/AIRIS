# AIRIS - Phase 6 Progress (Tiến độ giai đoạn 6)

## Mục tiêu Phase 6

Giai đoạn này tập trung vào cảnh báo và snapshot:
- AlertManager chịu trách nhiệm quyết định cảnh báo
- lưu snapshot khi có sự kiện
- cooldown để tránh cảnh báo lặp lại liên tục
- chuẩn bị cho việc gửi tới ESP32/loa sau này

## File đã thêm

### src/alert_manager.py
- class `AlertManager`
- `should_trigger()` kiểm tra cooldown
- `create_alert()` lưu ảnh snapshot vào thư mục `data/snapshots`
- `draw_alert_overlay()` vẽ chữ cảnh báo trực tiếp lên frame
- tách hoàn toàn khỏi detector và tracking

### tests/test_alert_manager.py
- test lưu snapshot
- test cooldown hoạt động như mong đợi
- test không gây cảnh báo liên tục khi chưa hết cooldown

## Lưu ý kỹ thuật

- Đây là tầng decision/alert ở cuối pipeline.
- Detector không tự phát alert; alert manager chỉ kích hoạt sau khi temporal reasoning xác nhận đủ điều kiện.
- Mục tiêu là chuẩn bị interface rõ ràng cho việc tích hợp hardware sau này.

## Kế hoạch tiếp theo

Phase 7 sẽ triển khai:
- `src/event_logger.py`
- SQLite
- ghi event dạng `SMOKING_DETECTED`, `SMOKE_DETECTED`

Ngày cập nhật: 2026-09-16
