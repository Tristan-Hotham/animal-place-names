# Where the wolves were

Animals in the place names of Britain and Ireland. 145,934 named points from OpenStreetMap (UK places, UK hills, woods, cliffs, springs and bays, and Irish places) searched for animal elements in Old English, Old Norse, Welsh, Scottish Gaelic, Irish and later English and Scots, with a conservative, documented word list and every candidate checked by hand. 662 places kept.

Interactive page: https://maps.tristanhotham.com/animal-place-names/
Paper: https://doi.org/10.5281/zenodo.24075293
Blog post: https://blog.tristanhotham.com/2026/10/31/animal-place-names/
Code and data: https://github.com/Tristan-Hotham/animal-place-names

## Headline results

- 800 candidate names; 30 removed as known false friends and 26 more on reading every one (7.0%); 662 places after merging repeats within 3 km, 189 with a certain reading.
- Wolf: 33 places (4 certain: Woolpit, Woolley in West Yorkshire, Ulpha and Welsh Cwm Bleiddiaid). Median ground height 256 m against 103 m for random names of the same kinds (20,000 draws, none as high; still higher against other animals' names of the same kinds, p = 0.003). 73% of English-language wolf names lie north of 53.5°N.
- Crane: 23 places, 91% in England (Cranfield, Cranbrook, Cranborne, Tranmere...), not concentrated in the Fens (1 in the fen counties) and no lower than expected. Beaver: 3 (Beverley, Bevercotes, Beversbrook). Wild boar: 22, mostly Gaelic tuirc.
- Eagle: 41 places, 68% Gaelic, Welsh or Irish; only 6 Old English earn. Otter names lie low (36 m against 73 m, p = 0.05 with only 15 places), as a river animal should.
- Gaelic madadh alone (dog, fox or wolf) is kept apart: 23 names, never counted. No reliable bear names.

## Files

| File | What it is |
|---|---|
| `index.html`, `js/page.js` | The interactive page: the Inked World map style (loaded from the ink-map study on the same site) with every name, an animal picker, language and certainty filters, search and popups. |
| `header.png` | Social card, 1200 x 630. |
| `data/animal_names.csv` | Every kept name (744 rows): OSM id and link, names in each language, animal, language layer, element, meaning, certainty, rule, kind, county, nation, coordinates, ground height, place id (repeats merged), head of place. ODbL. |
| `data/candidates_review.csv` | Every candidate (823) with its decision and reason: kept, false friend, dropped in review, uncertain. ODbL. |
| `data/elements.csv` | The rule list: named settlements, Welsh, Gaelic and Irish words, English and Scots words, and the false-friend exclusions. |
| `data/county_density.csv` | Animal places per 1,000 named points by county. |
| `data/results.json` | Every number quoted on the page, in the paper, blog, collage and post. |
| `data/names.json`, `data/places.json` | Page data (names for the map; towns and villages for search). |
| `img/` | Figures on the page. |
| `code/` | Numbered scripts, `elements.py` (the rules), `overrides.csv` (the hand review), templates, `qa.js`. |
| `release/` | Paper (`paper/`), blog post and figures (`blog/`), Zenodo files (`zenodo/`). |
| `reddit/` | Collage (`collage.py`, PNG) and post text. |

## Method in brief

- Names: OpenStreetMap via QLever: 106,905 UK place nodes with name, name:cy, name:gd; 24,964 UK natural features; 14,065 Irish place nodes with name:ga. County and nation from ONS boundaries; ground height from AWS Terrain Tiles (zoom 10).
- Rules (`code/elements.py`): 69 English and Norse settlement names read with an animal by the dictionaries (Mills 2011, Watts 2004, Ekwall 1960), whole names only, in the dictionary's county where known; 37 Welsh, Gaelic and Irish word rules inside each language's area; 22 English and Scots word rules, only with a landscape word, not on houses, farms or suburbs (always probable); 23 false-friend exclusions; 28 hand decisions in `code/overrides.csv`.
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

Hotham, T. (2026) Where the wolves were: animals in the place names of Britain and Ireland. Zenodo. https://doi.org/10.5281/zenodo.24075293

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped prepare the analysis code. I reviewed and checked all text and results.
