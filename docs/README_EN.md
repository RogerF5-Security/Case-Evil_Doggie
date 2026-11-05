# Doggie House

**Born on a trip to EKO. Built back home in Guatemala.**

[Español](../README.md) · [Assembly](ASSEMBLY_EN.md) · [Offline 3D viewer](../viewer/index.html)

On a trip to EKO, the Faraday team gave us an EvilDoggie. Back in Guatemala,
we built a little house to take care of it: keep the original dog artwork and
LEDs visible, protect the board and leave its connections accessible.
The first printed prototype revealed several practical fixes. This second
revision brings them together for the community, with thanks to Faraday and Kalpa.

Designed by **RogerF5**. This is a community enclosure for the original hardware,
not a replacement for the [Faraday Doggie repository](https://github.com/infobyte/doggie).

![Front and component cover](images/cover.png)

## Revision 2

- Four releasable PETG snap latches; no screws, nuts or inserts.
- USB opening extended 2 mm at its lower edge through the case thickness,
  preserving the upper edge; larger cable-overmould relief. Board-axis Y remains 35 mm.
- Exterior lettering removed. **RogerF5** engraved inside, approximately 5.4 mm high and 0.5 mm deep.
- 14 roof vents and 8 actual side vents. Roof open area is 2.46 times v1;
  cooling performance has not been measured.
- Original PCB holes locate the board on Ø 2.5 mm pins. No board drilling.
- Open dog window; optional cut 1 mm transparent sheet.

Case: **80 × 110 × 27.8 mm**. Reference PCB: **70 × 100 × 2 mm**, maximum component height 15 mm.

Print the standard [3MF geometry layout](../models/doggie-house-standard.3mf),
or STL `01` + `02` + `03`. Direct-button-access alternative: `01` + `04`.
STLs and 3MF layouts are pre-oriented in millimetres and contain no printer
profile or G-code. Suggested starting setup: unfilled PETG, 0.4 mm nozzle,
0.20 mm layers, 4 walls, 20% infill; use the filament's actual profile.
Check the latch coupon `08` + `09` before printing the complete case.

**v2.0.0-rc1 / 2026-11-04:** v1 was physically printed. The revised geometry has
passed digital checks, including latch engagement and nominal tip travel.
The exact USB displacement was not measured; the 2 mm relief is a proposed
correction. Physical fit, latch force/fatigue, button operation and signature
legibility still need to be checked on v2. Do not mix v1 and v2 halves.

Open `viewer/index.html` locally for the standalone WebGL viewer. No CDN or
Internet connection is required. Case parts come from the actual printable CAD;
PCB graphics and electronic components are visual references.

To rebuild: install `requirements.txt`, run `python cad/build.py`, then
`python tools/build_viewer.py` and `python tools/check_release.py`.
Change values in `cad/parameters.json`; do not scale an STL to reposition USB.

See [assembly](ASSEMBLY_EN.md), [design notes](DESIGN_NOTES.md),
[physical release checklist](RELEASE_CHECKLIST.md) and [contributing](../CONTRIBUTING.md).
New enclosure source: [MIT](../LICENSE). Faraday/Kalpa art and hardware credited
in [third-party notices](../THIRD_PARTY_NOTICES.md).
