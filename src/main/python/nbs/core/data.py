from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Instrument:
    name: str
    color: Tuple[int, int, int]
    pitch: int = 45
    press: bool = False
    sound_path: Optional[str] = None
    icon_path: Optional[str] = None


default_instruments = [
    Instrument(
        name="Harp",
        sound_path="harp.ogg",
        icon_path="harp.png",
        color=(25, 100, 172),
        press=True,
    ),
    Instrument(
        name="Double Bass",
        sound_path="double_bass.ogg",
        icon_path="double_bass.png",
        color=(60, 142, 72),
        press=False,
    ),
    Instrument(
        name="Bass Drum",
        sound_path="bass_drum.ogg",
        icon_path="bass_drum.png",
        color=(190, 107, 107),
        press=False,
    ),
    Instrument(
        name="Snare Drum",
        sound_path="snare_drum.ogg",
        icon_path="snare_drum.png",
        color=(190, 190, 25),
        press=False,
    ),
    Instrument(
        name="Click",
        sound_path="click.ogg",
        icon_path="click.png",
        color=(157, 90, 152),
        press=True,
    ),
    Instrument(
        name="Guitar",
        sound_path="guitar.ogg",
        icon_path="guitar.png",
        color=(77, 60, 152),
        press=True,
    ),
    Instrument(
        name="Flute",
        sound_path="flute.ogg",
        icon_path="flute.png",
        color=(190, 182, 92),
        press=True,
    ),
    Instrument(
        name="Bell",
        sound_path="bell.ogg",
        icon_path="bell.png",
        color=(190, 25, 190),
        press=True,
    ),
    Instrument(
        name="Chime",
        sound_path="chime.ogg",
        icon_path="chime.png",
        color=(82, 142, 157),
        press=True,
    ),
    Instrument(
        name="Xylophone",
        sound_path="xylophone.ogg",
        icon_path="xylophone.png",
        color=(190, 190, 190),
        press=True,
    ),
    Instrument(
        name="Iron Xylophone",
        sound_path="iron_xylophone.ogg",
        icon_path="iron_xylophone.png",
        color=(25, 145, 190),
        press=True,
    ),
    Instrument(
        name="Cow Bell",
        sound_path="cow_bell.ogg",
        icon_path="cow_bell.png",
        color=(190, 35, 40),
        press=True,
    ),
    Instrument(
        name="Didgeridoo",
        sound_path="didgeridoo.ogg",
        icon_path="didgeridoo.png",
        color=(190, 87, 40),
        press=True,
    ),
    Instrument(
        name="Bit",
        sound_path="bit.ogg",
        icon_path="bit.png",
        color=(25, 190, 25),
        press=True,
    ),
    Instrument(
        name="Banjo",
        sound_path="banjo.ogg",
        icon_path="banjo.png",
        color=(190, 25, 87),
        press=True,
    ),
    Instrument(
        name="Pling",
        sound_path="pling.ogg",
        icon_path="pling.png",
        color=(87, 87, 87),
        press=True,
    ),
]
