# SPDX-FileCopyrightText: 2023 Alessandro Guttrof
#
# SPDX-License-Identifier: MIT

"""
`ili9488`
====================================================

Display driver for ILI9488

* Author(s): Alessandro Guttrof

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import struct

from micropython import const
from adafruit_rgb_display.rgb import DisplaySPI

_NOP = const(0x00)
_SWRESET = const(0x01)
_RDDID = const(0x04)
_RDDST = const(0x09)

_SLPIN = const(0x10)
_SLPOUT = const(0x11)
_PTLON = const(0x12)
_NORON = const(0x13)

_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)

_PTLAR = const(0x30)


class ILI9488(DisplaySPI):
    """
    A simple driver for the ILI9488-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import ili9488
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = ili9488.ILI9488(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15), rst=digitalio.DigitalInOut(board.GPIO16))
    >>> display.fill(0x7521)
    >>> display.pixel(64, 64, 0)
    """

    _COLUMN_SET = _CASET
    _PAGE_SET = _RASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD
    _INIT = (
        (const(0xE0), b"\x0F\x13\x1D\x09\x18\x0A\x43\x66\x4F\x07\x0F\x0E\x18\x1A\x03"),
        (const(0xE1), b"\x0F\x1A\x1D\x04\x0F\x04\x31\x14\x43\x03\x0D\x0C\x26\x29\x00"),
        # Memory Access
        (const(0x36), b"\x08"),
        # Interface Pixel Format 
        (const(0x3A), b"\x66"), #66:18Bit,55:18Bit
        # Power Control 1 
        (const(0xC0), b"\x14\x0E"), #Vreg1out #Vreg2out
        # Power Control 2
        (const(0xC1), b"\x43"), #VGH,VGL 
        # Power Control 3
        (const(0xC5), b"\x00\x36\x80"), #Vcom
        # Interface Mode Control
        (const(0xB0), b"\x80"), #SDA_EN 
        # Frame rate 
        (const(0xB1), b"\xA0\x11"), #60Hz
        # Display Inversion Control 
        (const(0xB4), b"\x02"), #2-dot
        # RGB/MCU Interface Control 
        (const(0xB6), b"\x02\x02\x3B"), #RGB 22, MCU 02 #Source,Gate scan direction
        # Set Image Function
        (const(0xE9), b"\x00"), #Disable 24 bit data input 
        (const(0xF7), b"\xA9\x51\x2C\x82"),

        (_SLPOUT, None),
        (_DISPON, None),
    )
    _ENCODE_PIXEL = ">I"
    _ENCODE_POS = ">HH"
    
    def _encode_pixel(self, color):
        """Encode a pixel color into bytes."""
        return struct.pack(self._ENCODE_PIXEL, color)[1:]

    # pylint: disable-msg=useless-super-delegation, too-many-arguments
    def __init__(
        self,
        spi,
        dc,
        cs,
        rst=None,
        width=320,
        height=480,
        baudrate=16000000,
        polarity=0,
        phase=0,
        *,
        x_offset=0,
        y_offset=0,
        rotation=0
    ):
        super().__init__(
            spi,
            dc,
            cs,
            rst,
            width,
            height,
            baudrate=baudrate,
            polarity=polarity,
            phase=phase,
            x_offset=x_offset,
            y_offset=y_offset,
            rotation=rotation,
        )
