def test_temperature_response(device):
    r = device.command("GET TEMP")

    assert r["status"] in {"OK", "ERROR"}

    if r["status"] == "OK":
        assert -40 <= r["temperature"] <= 80
    else:
        assert r["code"] == "SENSOR_UNAVAILABLE"