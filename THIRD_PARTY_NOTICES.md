# Third-party notices

## Faraday / Kalpa Doggie

Doggie hardware, firmware, name, brand and dog illustration belong to the
original Faraday/Kalpa project. No ownership of those works is claimed here.

- Project: https://github.com/infobyte/doggie
- Artwork: https://github.com/infobyte/doggie/blob/main/docs/res/logo.svg
- Repository license: https://github.com/infobyte/doggie/blob/main/LICENSE
- Copyright notice retained in `assets/FARADAY-LICENSE.txt`.

`assets/pcb-art.svg` corrects the mirrored silkscreen orientation of that resource
for a visual reference board. `assets/doggie-board-art.svg` is a separated dog
variant. They are used only in the viewer/docs; the printable case does not
incorporate Faraday artwork or exterior logo text. Artwork does not imply a
trademark license or certification of the accessory.

## Fonts and generated geometry

Interior workshop-mark geometry is generated from DejaVu Sans Bold using Matplotlib.
The STL/3MF contains outline geometry, not font software. No font files are
redistributed in the repository. PDF output embeds subsets of DejaVu fonts
available through the build environment; DejaVu fonts use their upstream license:
https://dejavu-fonts.github.io/License.html

## Prototype photographs

Three photos in `docs/photos/` document fit checks performed on an earlier workshop prototype.
They depict the prototype, not a printed/validated revision 2. Generated CAD
screenshots in `docs/images/` depict revision 2 and are labelled accordingly.

## Runtime

The viewer uses the browser WebGL API directly, with self-contained geometry
and reference art. It has no bundled Three.js or external CDN dependencies.
Python dependencies are listed separately in the requirements files and retain
their respective upstream licenses.
