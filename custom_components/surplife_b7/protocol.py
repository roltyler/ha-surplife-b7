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

def parse_status(raw: bytes) -> ControllerStatus:
    """Validate an observed B7 frame; other fields are not yet decoded."""
    if len(raw) != 27 or raw[:2] != b"\xea\x81":
        raise ValueError(f"Unexpected status frame: {raw.hex('-').upper()}")
    if raw[4] != 0xB7:
        raise ValueError(f"Unsupported model byte 0x{raw[4]:02X}")
    return ControllerStatus(raw.hex('-').upper(), len(raw), raw[4], "EA-81 / B7")

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
