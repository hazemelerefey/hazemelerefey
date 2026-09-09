# Hazem Elerefy asset maintenance

The profile is ordinary GitHub Markdown with self-contained SVG images. No JavaScript, external fonts, statistics endpoints or scheduled jobs are required.

## Edit

- Edit profile copy, project destinations and credentials in `README.md`.
- Edit labels, colors and animation in `tools/build_cinema.py`.
- Run `python tools/build_cinema.py` to regenerate all 20 SVG assets. Dependencies: Pillow and fonttools. The default font is DejaVu Sans; set `CINEMA_FONT` to a TrueType font path on other systems.
- Keep the seven `-mobile.svg` variants paired with their desktop assets. The README selects them at viewport widths of 640px or less.

The PNGs in `assets/cinema/source/` are the original AI-generated movie key art, made for this profile using the image-generation tool. They are retained as editable production inputs. The SVGs embed optimized JPEG copies, so visitors do not need to download the full-resolution PNGs. Project posters are symbolic key art. SIGNAL is an editorial title for the existing n8n projects, not a separate product.

## Motion

The hero has a one-time light-ribbon ident, followed by looping energy traces and particles. DAFEsteel has an inspection sweep. NeuroScope has network pulses. SIGNAL has flowing paths. Nebula has a floating wireframe world; JobPulse has a moving chart highlight. All animations are decorative and respect `prefers-reduced-motion`. The essential content is visible when CSS animation is unavailable or disabled.

## Content provenance

Roles follow the owner's current instruction. Project facts and technologies come from the owner's public project READMEs, public profile and existing public CV. DAFEsteel is credited as a team project. Its 81.98% mAP@0.5 figure is explicitly labeled as a repository-reported result on NEU-DET, with the documented split. There are no invented skill percentages, ratings or audience counts.

Existing assets and certificate files are preserved. This update does not need the older snake workflow to run.
