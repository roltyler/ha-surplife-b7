"""Offline fixture for the captured EA-81 B7 frame."""
from custom_components.surplife_b7.protocol import parse_status

def test_observed_b7_frame():
    frame = bytes.fromhex("EA 81 02 00 B7 0B 23 25 65 50 F0 B4 64 64 FF 00 1E 00 3D 00 00 00 20 01 00 00 05")
    result = parse_status(frame)
    assert result.signature == "EA-81 / B7"
    assert result.raw_length == 27
    assert result.model_byte == 0xB7
