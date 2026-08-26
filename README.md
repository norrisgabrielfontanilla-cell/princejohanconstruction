# Prince Johan Iron Works and Construction, Inc. — Website

Official company website. A single self-contained `index.html` — inline CSS and JS,
no build step, no framework, no runtime dependencies. The only external request is
Google Fonts.

**Live:** https://norrisgabrielfontanilla-cell.github.io/princejohanconstruction/

---

## Company details on the site

All content comes from verified company records:

| | |
|---|---|
| Legal name | Prince Johan Iron Works and Construction, Inc. |
| SEC registration | 21 May 2009 |
| PCAB licence | Category D, General Building |
| Procurement | PhilGEPS Platinum (government bidding eligible) |
| Head office | 11-A Meleguas St., Torres Subdivision, Tandang Sora District 6, Quezon City 1116 |
| Phone | 0917-812-7146 |
| Email | princejohan2009@gmail.com |
| Completed contracts | 40+ |
| Contract value range on file | ₱636,133 – ₱14,722,050 |

Individual project cards deliberately show **"Value on file"** rather than per-project
figures — only the aggregate range above is verified, so no per-project numbers were
invented.

---

## Repository layout

```
index.html                          the entire website
README.md                           this file
tools/
  generate-hero-scene.py            generates the isometric hero SVG
docs/
  screenshots/                      reference renders of each section
.github/workflows/
  deploy-pages.yml                  auto-deploys to GitHub Pages on push to main
```

---

## The hero scene

The hero background is a hand-built isometric construction site in inline SVG —
no photography, no 3D render, no external asset. It is **generated**, not
hand-authored, by `tools/generate-hero-scene.py`.

The script projects 3D grid coordinates to 2D:

```
screen_x = (x - y) * 30
screen_y = (x + y) * 15 - z * 26
```

Every building is drawn as three shaded faces from that projection — top lightest,
right face mid, left face darkest — which is what gives the solids their depth.

The scene contains a concrete skeleton frame with floor slabs and columns,
scaffolding, a dark residential tower, a cream apartment block with accent panels,
a glass podium, a timber site office, three lattice tower cranes, material stacks,
site hoarding, road markings and vehicles.

### Regenerating it

```bash
python3 tools/generate-hero-scene.py
```

This writes an SVG fragment. Paste it inside the `<svg>` in the `.hero-bg` block of
`index.html`, replacing the previous `<g id="scene">…</g>`. Edit the palette
constants or building coordinates near the top of the script to change the scene.

---

## Motion

Fourteen CSS animations drive the hero:

| Element | Motion |
|---|---|
| Crane hooks (×3) | Raise and lower. The rope `scaleY`s from its top anchor while the hook block `translateY`s on the same keyframe timing, so the two stay attached instead of the rope stretching past the block. |
| Hoist cage | Climbs the skeleton frame and descends. |
| Crane beacons (×3) | Blink, each on its own offset. |
| Vehicles (×4) | Drive along the isometric road axis, fading in and out at both ends so the loop never visibly snaps. |

Everything is disabled under `prefers-reduced-motion: reduce`.

---

## Accessibility and SEO

- Skip link, semantic landmarks, `<address>` for NAP data
- Visible focus rings; all interactive targets ≥ 44px
- Trend indicators pair an icon **and** a label with colour, never colour alone
- `schema.org` `GeneralContractor` JSON-LD with address, service area and credentials
- Location-specific copy naming Quezon City, Ilocos Sur, Metro Manila and Cavite

---

## Known limitation

**The contact form is not wired to a backend.** It validates on the client only —
nothing is sent anywhere on submit. This is stated plainly on the form itself, which
directs visitors to phone or email instead. Connecting it to a form service
(Formspree, Netlify Forms, Google Apps Script) is a small change to the submit
handler at the bottom of `index.html`.

---

## Deployment

Pushing to `main` triggers `.github/workflows/deploy-pages.yml`, which publishes the
repository root to GitHub Pages. No build, no install step.

Pages must be set to **Settings → Pages → Source: GitHub Actions** — this is already
configured and only ever needs doing once.
