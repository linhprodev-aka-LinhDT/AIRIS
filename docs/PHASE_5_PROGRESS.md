# AIRIS - Phase 5 Progress (Tiến độ giai đoạn 5)

## Mục tiêu Phase 5

Giai đoạn này tập trung vào phân tích theo thời gian và state machine cho từng `track_id`:
- `UNKNOWN`
- `POSSIBLE_SMOKING`
- `SMOKING`
- `COOLDOWN`
- tránh cảnh báo sai nhờ nhiều frame liên tiếp
- isolation theo track_id, không ảnh hưởng giữa người này và người khác

## File đã thêm

### src/temporal_analysis.py
- class `TemporalAnalyzer`
- enum `TemporalState`
- dataclass `TemporalDecision`
- logic cộng dồn evidence theo thời gian
- logic cooldown để tránh alert liên tục
- trạng thái riêng biệt theo từng track_id

### tests/test_temporal_analysis.py
- test transition qua nhiều state
- test cảnh báo chỉ khi đủ evidence
- test trạng thái không ảnh hưởng giữa track khác nhau

## Lưu ý kỹ thuật

- Phase này chưa liên kết với MediaPipe hoặc hand-mouth analysis.
- Đây là tầng cơ sở để sau này có thể tích hợp đánh giá tay-miệng, thuốc lá hoặc khói.
- Việc tách theo `track_id` là rất quan trọng để tránh trộn state của người này với người khác.

## Kế hoạch tiếp theo

Phase 6 sẽ triển khai:
- `src/alert_manager.py`
- snapshot
- cooldown cảnh báo
- giao diện chuẩn cho ESP32 sau này

Ngày cập nhật: 2026-09-16
