from src.sensors import AirQualityReading, SensorVerifier


def test_sensor_verifier_correlates_abnormal_air_quality() -> None:
    verifier = SensorVerifier()
    verifier.ingest(AirQualityReading.now("sensor-1", "ct1a-floor5", pm25=48.0, co_ppm=2.0))

    result = verifier.verify("ct1a-floor5")

    assert result["status"] == "corroborated"
    assert result["zone_id"] == "ct1a-floor5"


def test_sensor_verifier_reports_missing_reading() -> None:
    assert SensorVerifier().verify("unknown")["status"] == "unverified"