#!/usr/bin/env python3
"""Rend chaque guide de rôle (.md) en PDF, dans l'identité visuelle du site.

Usage : python3 build.py <dossier_source> <dossier_sortie>

Les .md sont la source de vérité et vivent dans CIASETIN-Documentation-Dump,
sous « Event Guides/Staffing Guides/ ». Les PDF sont des artefacts de build :
ne les modifiez pas à la main, modifiez le markdown.
"""

import pathlib
import sys

import markdown
from playwright.sync_api import sync_playwright

GABARIT = """<!doctype html>
<html lang="fr-CA"><head><meta charset="utf-8"><style>
@page {{ size: letter; margin: 18mm 17mm 20mm; }}

:root {{
  --encre: #142433;
  --ambre: #E39A33;
  --gris: #5A6875;
  --trait: #C7CFD6;
}}

* {{ box-sizing: border-box; }}

body {{
  margin: 0;
  font-family: "Liberation Serif", "DejaVu Serif", Georgia, serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: var(--encre);
}}

h1, h2, h3, th {{
  font-family: "Liberation Sans", "DejaVu Sans", Arial, sans-serif;
}}

h1 {{
  margin: 0 0 0.35em;
  padding-bottom: 0.35em;
  border-bottom: 3px solid var(--ambre);
  font-size: 23pt;
  font-weight: 700;
  letter-spacing: -0.015em;
  line-height: 1.1;
}}

/* Le bloc d'identification juste sous le titre. */
h1 + p {{
  margin: 0 0 1.6em;
  font-family: "Liberation Sans", "DejaVu Sans", Arial, sans-serif;
  font-size: 9pt;
  line-height: 1.45;
  color: var(--gris);
}}

h2 {{
  margin: 1.9em 0 0.5em;
  font-size: 12.5pt;
  font-weight: 700;
  page-break-after: avoid;
  break-after: avoid;
}}

p {{ margin: 0 0 0.8em; }}
strong {{ font-weight: 700; }}

ul {{ margin: 0 0 0.9em; padding-left: 1.1em; }}
li {{ margin-bottom: 0.4em; }}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 0.6em 0 1.2em;
  font-size: 9.5pt;
  page-break-inside: avoid;
  break-inside: avoid;
}}

th, td {{
  padding: 0.5em 0.7em 0.5em 0;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid var(--trait);
}}

th {{
  font-size: 8.5pt;
  font-weight: 700;
  border-bottom: 2px solid var(--encre);
}}

/* Colonne d'heures : étroite, chiffres alignés. */
td:first-child {{ white-space: nowrap; }}
table td:first-child {{ font-variant-numeric: tabular-nums; }}

</style></head>
<body>
{corps}
</body></html>"""

PIED = """<div style="width:100%;margin:0 17mm;padding-top:2mm;
  border-top:1px solid #C7CFD6;font-family:Arial,sans-serif;font-size:7pt;
  color:#5A6875;display:flex;justify-content:space-between;">
  <span>Club IA &times; ASETIN &middot; Hackathon du 28 novembre 2026</span>
  <span class="pageNumber"></span>
</div>"""


def construire(dossier_src: pathlib.Path, dossier_out: pathlib.Path) -> None:
    sources = sorted(dossier_src.glob("*.md"))
    if not sources:
        sys.exit(f"Aucun fichier .md dans {dossier_src}")

    dossier_out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        navigateur = pw.chromium.launch()
        page = navigateur.new_page()

        for source in sources:
            corps = markdown.markdown(
                source.read_text(encoding="utf-8"),
                extensions=["tables", "sane_lists"],
            )
            page.set_content(GABARIT.format(corps=corps), wait_until="load")
            cible = dossier_out / f"{source.stem}.pdf"
            page.pdf(
                path=str(cible),
                format="Letter",
                print_background=True,
                display_header_footer=True,
                header_template="<div></div>",
                footer_template=PIED,
                margin={
                    "top": "18mm",
                    "right": "17mm",
                    "bottom": "20mm",
                    "left": "17mm",
                },
            )
            print(f"{source.name} -> {cible.name}")

        navigateur.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    construire(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
