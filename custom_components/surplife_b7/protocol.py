"""Read-only protocol support for EA-81 Surplife controller responses."""
from __future__ import annotations
import asyncio
from dataclasses import dataclass
from .const import STATUS_REQUEST

@dataclass(frozen=True)
class ControllerStatus:
    raw_hex: str
    raw_length: int
    model_byte: int
    signature: str
    power_state: str
    reported_level: int | None
    reported_level_hex: str
    mode_byte: str

def parse_status(raw: bytes) -> ControllerStatus:
    """Parse only empirically observed fields of this B7 controller."""
    if len(raw) != 27 or raw[:2] != b"\xea\x81":
        raise ValueError(f"Unexpected status frame: {raw.hex('-').upper()}")
    if raw[4] != 0xB7:
        raise ValueError(f"Unsupported model byte 0x{raw[4]:02X}")
    power = {0x23: "on", 0x24: "off"}.get(raw[6], "unknown")
    # Observed 0x18 at 25% and 0x64 at 100% in one mode only.
    # 0x00 during a scene is NOT evidence of zero brightness.
    reported_level = raw[15] if raw[15] in range(1, 101) else None
    return ControllerStatus(
        raw.hex('-').upper(), len(raw), raw[4], "EA-81 / B7",
        power, reported_level, f"0x{raw[15]:02X}", f"0x{raw[7]:02X}"
    )

async def read_status(host: str, port: int) -> ControllerStatus:
    """Send a read-only Magic Home status request."""
    reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
    try:
        writer.write(STATUS_REQUEST)
        await asyncio.wait_for(writer.drain(), timeout=3)
        raw = await asyncio.wait_for(reader.readexactly(27), timeout=5)
        return parse_status(raw)
    finally:
        writer.close()
        await writer.wait_closed()

async def write_power(host: str, port: int, on: bool) -> None:
    """Send verified B7 power command; caller refreshes state afterwards."""
    command = bytes((0x71, 0x23 if on else 0x24, 0x0F))
    _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
    try:
        writer.write(command)
        await asyncio.wait_for(writer.drain(), timeout=3)
    finally:
        writer.close()
        await writer.wait_closed()
