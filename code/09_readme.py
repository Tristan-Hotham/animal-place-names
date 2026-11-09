"""Step 9: README.md, LICENSE and the Reddit post text (reddit/post.md), filled from data/results.json."""
from common import *

R = jload(f"{DATA}/results.json")
A, T, rv = R["animals"], R["elev_test"], R["review"]
readme = f"""# Where the wolves were

Animals in the place names of Britain and Ireland. {R['n']['points']:,} named points from OpenStreetMap (UK places, UK hills, woods, cliffs, springs and bays, and Irish places) searched for animal elements in Old English, Old Norse, Welsh, Scottish Gaelic, Irish and later English and Scots, with a conservative, documented word list and every candidate checked by hand. {rv['places']:,} places kept.

Interactive page: {PAGE}
Paper: {{https://doi.org/10.5281/zenodo.24075293}}
Blog post: {{https://blog.tristanhotham.com/2026/10/31/animal-place-names/}}
Code and data: {REPO}

## Headline results

- {rv['candidates']:,} candidate names; {rv['false_friends']} removed as known false friends and {rv['dropped']} more on reading every one ({rv['corrected_pc']:.1f}%); {rv['places']:,} places after merging repeats within 3 km, {R['certain']} with a certain reading.
- Wolf: {A['wolf']['places']} places ({A['wolf']['certain']} certain: Woolpit, Woolley in West Yorkshire, Ulpha and Welsh Cwm Bleiddiaid). Median ground height {T['wolf']['median']:.0f} m against {T['wolf']['null_median']:.0f} m for random names of the same kinds (20,000 draws, none as high; still higher against other animals' names of the same kinds, p = {R['elev_test_other']['wolf']['p_high']:.3f}). {R['wolf_english']['north_pc']:.0f}% of English-language wolf names lie north of 53.5°N.
- Crane: {A['crane']['places']} places, {R['crane_low']['england_pc']:.0f}% in England (Cranfield, Cranbrook, Cranborne, Tranmere...), not concentrated in the Fens ({R['crane_low']['fen_counties']} in the fen counties) and no lower than expected. Beaver: {A['beaver']['places']} (Beverley, Bevercotes, Beversbrook). Wild boar: {A['boar']['places']}, mostly Gaelic tuirc.
- Eagle: {A['eagle']['places']} places, {R['eagle']['celtic_pc']:.0f}% Gaelic, Welsh or Irish; only {R['eagle']['english']} Old English earn. Otter names lie low ({T['otter']['median']:.0f} m against {T['otter']['null_median']:.0f} m, p = {T['otter']['p_low']:.2f} with only {T['otter']['n']} places), as a river animal should.
- Gaelic madadh alone (dog, fox or wolf) is kept apart: {rv['madadh']} names, never counted. No reliable bear names.

## Files

| File | What it is |
|---|---|
| `index.html`, `js/page.js` | The interactive page: the Inked World map style (loaded from the ink-map study on the same site) with every name, an animal picker, language and certainty filters, search and popups. |
| `header.png` | Social card, 1200 x 630. |
| `data/animal_names.csv` | Every kept name ({rv['kept']:,} rows): OSM id and link, names in each language, animal, language layer, element, meaning, certainty, rule, kind, county, nation, coordinates, ground height, place id (repeats merged), head of place. ODbL. |
| `data/candidates_review.csv` | Every candidate ({rv['candidates'] + rv['madadh']:,}) with its decision and reason: kept, false friend, dropped in review, uncertain. ODbL. |
| `data/elements.csv` | The rule list: named settlements, Welsh, Gaelic and Irish words, English and Scots words, and the false-friend exclusions. |
| `data/county_density.csv` | Animal places per 1,000 named points by county. |
| `data/results.json` | Every number quoted on the page, in the paper, blog, collage and post. |
| `data/names.json`, `data/places.json` | Page data (names for the map; towns and villages for search). |
| `img/` | Figures on the page. |
| `code/` | Numbered scripts, `elements.py` (the rules), `overrides.csv` (the hand review), templates, `qa.js`. |
| `release/` | Paper (`paper/`), blog post and figures (`blog/`), Zenodo files (`zenodo/`). |
| `reddit/` | Collage (`collage.py`, PNG) and post text. |

## Method in brief

- Names: OpenStreetMap via QLever: {R['n']['uk_place']:,} UK place nodes with name, name:cy, name:gd; {R['n']['uk_nature']:,} UK natural features; {R['n']['ie_place']:,} Irish place nodes with name:ga. County and nation from ONS boundaries; ground height from AWS Terrain Tiles (zoom 10).
- Rules (`code/elements.py`): {R['n']['named_rules']} English and Norse settlement names read with an animal by the dictionaries (Mills 2011, Watts 2004, Ekwall 1960), whole names only, in the dictionary's county where known; {R['n']['word_rules']} Welsh, Gaelic and Irish word rules inside each language's area; {R['n']['modern_rules']} English and Scots word rules, only with a landscape word, not on houses, farms or suburbs (always probable); {R['n']['exclude_rules']} false-friend exclusions; {rv['overrides']} hand decisions in `code/overrides.csv`.
- Places: repeats of a name for one animal within 3 km merged. Height test: median ground height of an animal's UK places against 20,000 random draws of UK names of the same kinds.
- Caveats: a name is not a sighting; OpenStreetMap lacks most field and minor names; dictionary readings applied without re-examining early spellings; descriptive English names may honour surnames, inns or stories; Welsh and Gaelic coverage depends on tagging.

## How to rerun

Needs Python 3 with pandas, numpy, geopandas, shapely, pyproj, scipy, matplotlib, Pillow; xelatex, pdftotext, pdfinfo; node with Playwright for `code/qa.js`. Raw inputs are listed in `code/common.py` (not redistributed except as the derived tables); intermediates go to `AP_WORK`.

```
python3 code/01_gazetteer.py   # one gazetteer, counties, heights
python3 code/02_match.py       # rules, false friends, hand review, repeats
python3 code/03_analysis.py    # results.json and data files
python3 code/04_export.py      # page data
python3 code/05_figures.py     # figures
python3 code/06_build_site.py  # index.html
python3 code/07_paper.py       # paper PDF (DOI=10.5281/zenodo.N to fill the DOI)
python3 reddit/collage.py      # collage and header
python3 code/09_readme.py      # README, LICENSE, Reddit post
python3 code/08_release.py     # blog post, Zenodo files
```

## Sources and licences

- OpenStreetMap (https://www.openstreetmap.org/), © OpenStreetMap contributors, Open Database Licence. Queried with QLever (University of Freiburg). `data/animal_names.csv`, `data/candidates_review.csv` and `data/names.json` are derived databases under the ODbL.
- AWS Terrain Tiles (https://registry.opendata.aws/terrain-tiles/) for ground heights; ONS boundaries (Open Government Licence v3.0).
- Place-name dictionaries: Mills (2011), Watts (2004), Ekwall (1960), Owen and Morgan (2007), Watson (1926). Wildlife history: Yalden (1999), Aybes and Yalden (1995), Boisseau and Yalden (1998), Coles (2006), Pluskowski (2006), Hickey (2000), Love (1983). Full references in the paper.
- Map style: the Inked World (ink-map study, MIT code). MapLibre GL JS (BSD 3-Clause). Fonts: MedievalSharp, IM Fell, Fraunces, Source Serif 4, IBM Plex Mono (SIL Open Font License).

## Citation

Hotham, T. (2026) Where the wolves were: animals in the place names of Britain and Ireland. Zenodo. {{https://doi.org/10.5281/zenodo.24075293}}

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

{AI}
"""
for bad in ("—", "–", "--", "DSIT", "DCMS"):
    assert bad not in "\n".join(l for l in readme.replace("```", "").splitlines() if not l.startswith("|---")), bad
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(readme)

lic = """MIT License (code)

Copyright (c) 2026 Tristan Hotham

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Text and figures: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), Tristan Hotham, 2026.
Name data (data/animal_names.csv, data/candidates_review.csv, data/names.json, data/places.json): derived from OpenStreetMap, © OpenStreetMap contributors, Open Database Licence 1.0 (https://opendatacommons.org/licenses/odbl/1-0/).
Other derived data (results.json, elements.csv, county_density.csv): CC BY 4.0.
The map engine is loaded from the ink-map study (MIT code; credits in its README). Fonts under the SIL Open Font License.
"""
open(os.path.join(ROOT, "LICENSE"), "w", encoding="utf-8").write(lic)

post = f"""**Title:** [OC] Where the wolves were: {rv['places']} places in Britain and Ireland whose names keep an animal. Wolf names sit at a median {T['wolf']['median']:.0f} m up, against {T['wolf']['null_median']:.0f} m for similar names

**Body:**

Wolves, beavers, cranes and wild boar have been gone from Britain for centuries, but their names have not. Woolpit in Suffolk is a wolf pit, Beverley a beaver stream, Cranfield the cranes' open land, Arncliffe the eagles' cliff.

I searched {R['n']['points']:,} named places and hills from OpenStreetMap for animal words in Old English, Norse, Welsh, Gaelic, Irish and later English and Scots, then read every candidate by hand to throw out false friends (Wolverhampton is named after a woman, Wulfrun; Eagle in Lincolnshire is an oak wood; Swanage is herdsmen, not swans). {rv['corrected_pc']:.0f}% of candidates went.

- {A['wolf']['places']} wolf names, mostly on northern crags: median height {T['wolf']['median']:.0f} m vs {T['wolf']['null_median']:.0f} m expected.
- {A['crane']['places']} crane names, almost all in England, and not where I expected (the Fens).
- {R['eagle']['celtic_pc']:.0f}% of the {A['eagle']['places']} eagle names are Gaelic, Welsh or Irish.
- Sanity check: otter names sit low, {T['otter']['median']:.0f} m vs {T['otter']['null_median']:.0f} m (only {T['otter']['n']} of them, so a weak check).

Interactive map (pick an animal, tap any name for its meaning): {PAGE}

**Source comment:**

Data: OpenStreetMap contributors (ODbL), via QLever; ground heights from AWS Terrain Tiles. Readings: the standard place-name dictionaries (Mills, Watts, Ekwall) for English names, the ordinary Welsh, Gaelic and Irish words otherwise. Loss dates: Yalden 1999, Coles 2006, Boisseau and Yalden 1998, Hickey 2000, Love 1983. Tools: Python (pandas, geopandas, matplotlib), MapLibre. Every rule and hand decision is in the repo: {REPO}
"""
for bad in ("—", "–", "--"):
    assert bad not in post, bad
open(os.path.join(ROOT, "reddit", "post.md"), "w", encoding="utf-8").write(post)
print("README, LICENSE, post written")
