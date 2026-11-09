"""Step 4: page data. data/names.json (every kept name, compact rows for the map) and data/places.json (towns and villages
for the search box)."""
import pandas as pd, numpy as np
from common import *

K = pd.read_csv(f"{DATA}/animal_names.csv", keep_default_na=False, low_memory=False)
R = jload(f"{DATA}/results.json")
AK = [a[0] for a in ANIMALS]
LK = [l[0] for l in LAYERS]
KINDS = sorted(K.kind.unique())
rows = []
for r in K.itertuples():
    alt = " / ".join(x for x in (r.name_cy, r.name_gd, r.name_ga) if x and x != r.name)
    rows.append([round(float(r.lon), 5), round(float(r.lat), 5), r.name, AK.index(r.animal), LK.index(r.layer), 1 if r.certainty == "certain" else 0,
                 KINDS.index(r.kind), r.county or r.nation, r.element, r.gloss, r.osm, None if r.elev == "" else int(float(r.elev)), alt,
                 1 if str(r.is_head) == "True" else 0])
out = {"animals": [[a, l, c] for a, l, c in ANIMALS], "layers": [[k, l] for k, l in LAYERS], "kinds": KINDS,
       "cols": ["lon", "lat", "name", "animal", "layer", "certain", "kind", "county", "element", "gloss", "osm", "elev", "alt", "head"], "rows": rows,
       "lost": R["lost"]}
jsave(out, f"{DATA}/names.json")
g = pd.read_csv(f"{WORK}/gazetteer.csv.gz", keep_default_na=False, low_memory=False)
g = g[g.kind.isin(["city", "town", "village"])]
pri = {"city": 0, "town": 1, "village": 2}
g = g.assign(p=g.kind.map(pri)).sort_values(["p", "name"])
pl = [[r.name, round(float(r.lon), 4), round(float(r.lat), 4), r.p, r.county or r.nation] for r in g.itertuples()]
jsave({"cols": ["name", "lon", "lat", "rank", "county"], "places": pl}, f"{DATA}/places.json")
print(len(rows), "names;", len(pl), "places;", os.path.getsize(f"{DATA}/names.json") // 1024, "KB,", os.path.getsize(f"{DATA}/places.json") // 1024, "KB")
