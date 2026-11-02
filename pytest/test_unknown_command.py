import pytest

@pytest.mark.parametrize("command", [
    "HELLO",       # Unknown word
    "12345678",    # Numeric text
    "###",         # Symbols
])
def test_unknown_command(device, command):
    response = device.command(command)

    assert response["status"] == "ERROR"
    assert response["code"] == "UNKNOWN_COMMAND"

###check that device still works after unknown command
def test_device_handles_unknown_command(device):
    response = device.command("HELLO")

    assert response["status"] == "ERROR"
    assert response["code"] == "UNKNOWN_COMMAND"

    response = device.command("SET LED ON")
    assert response["status"] == "OK"
    assert response["led"] is True