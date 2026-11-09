"""Step 3: every number quoted anywhere goes into data/results.json. Also writes the derived data files:
data/animal_names.csv (every kept name), data/candidates_review.csv (every candidate with the reason it was kept or dropped),
data/elements.csv (the rule list), data/county_density.csv."""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
from common import *
from elements import NAMED, WORD, MODERN, EXCLUDE

g = pd.read_csv(f"{WORK}/gazetteer.csv.gz", keep_default_na=False, low_memory=False)
g["elev"] = pd.to_numeric(g["elev"], errors="coerce")
C = pd.read_csv(f"{WORK}/matches_all.csv", keep_default_na=False, low_memory=False)
C["elev"] = pd.to_numeric(C["elev"], errors="coerce")
K = C[C.status == "kept"].copy()
H = K[K.is_head.astype(str) == "True"].copy()          # one row per place (repeats of a name within 3 km merged)
R = {}

# ---------- the gazetteer and the review
R["n"] = {"points": len(g), "uk_place": int((g.src == "uk_place").sum()), "uk_nature": int((g.src == "uk_nature").sum()),
          "ie_place": int((g.src == "ie_place").sum()), "named_rules": len(NAMED), "word_rules": len(WORD), "modern_rules": len(MODERN),
          "exclude_rules": len(EXCLUDE)}
nc = len(C[C.animal != "madadh"])
R["review"] = {"candidates": nc, "false_friends": int((C.status == "false friend").sum()), "dropped": int((C.status == "dropped in review").sum()),
               "kept": len(K), "places": len(H), "madadh": int((C.animal == "madadh").sum()),
               "overrides": int(len(pd.read_csv(os.path.join(ROOT, "code", "overrides.csv"))))}
R["review"]["corrected_pc"] = 100 * (R["review"]["false_friends"] + R["review"]["dropped"]) / nc
R["review"]["dropped_pc"] = 100 * R["review"]["dropped"] / nc
R["review"]["repeats_merged"] = len(K) - len(H)
R["certain"] = int((H.certainty == "certain").sum())
R["certain_pc"] = 100 * R["certain"] / len(H)

# ---------- by animal
base_set = g[g.src != "ie_place"]
R["baseline"] = {"median_elev": float(base_set.elev.median()), "upland_pc": float(100 * (base_set.elev >= 250).mean()),
                 "median_elev_places": float(g[g.src == "uk_place"].elev.median()), "median_elev_nature": float(g[g.src == "uk_nature"].elev.median()),
                 "nature_share_pc": float(100 * (base_set.src == "uk_nature").mean())}
A = {}
for a, lab, col in ANIMALS:
    h = H[H.animal == a]
    hu = h[h.nation != "Ireland"]
    d = {"label": lab, "places": len(h), "certain": int((h.certainty == "certain").sum()), "probable": int((h.certainty == "probable").sum()),
         "names": int((K.animal == a).sum())}
    for L, _ in LAYERS:
        d["layer_" + L] = int((h.layer == L).sum())
    for nat in ("England", "Scotland", "Wales", "Northern Ireland", "Ireland"):
        d["nat_" + nat.replace(" ", "_")] = int((h.nation == nat).sum())
    d["median_elev"] = float(hu.elev.median()) if len(hu) else None
    d["upland_pc"] = float(100 * (hu.elev >= 250).mean()) if len(hu) else None
    d["nature_pc"] = float(100 * (hu.src == "uk_nature").mean()) if len(hu) else None
    d["settle_pc"] = float(100 * (h.src != "uk_nature").mean()) if len(h) else None
    d["celtic"] = d["layer_welsh"] + d["layer_gaelic"] + d["layer_irish"]
    d["celtic_pc"] = 100 * d["celtic"] / len(h) if len(h) else None
    d["english_old"] = d["layer_english"] + d["layer_norse"]
    d["examples"] = h.sort_values(["certainty", "kind"]).name.head(6).tolist()
    A[a] = d
R["animals"] = A
R["order_by_places"] = sorted(A, key=lambda a: -A[a]["places"])
R["layers"] = {L: int((H.layer == L).sum()) for L, _ in LAYERS}
R["nations"] = {nat: int((H.nation == nat).sum()) for nat in ("England", "Scotland", "Wales", "Northern Ireland", "Ireland")}

# ---------- uplands: elevation of wolf names against all names, by a permutation test within the same kinds
rng = np.random.default_rng(7)


def elev_test(a, n_perm=20000):
    """median ground height of an animal's names against random names of the same kinds (peak, village, locality...)"""
    h = H[(H.animal == a) & (H.nation != "Ireland") & H.elev.notna()]
    obs = h.elev.median()
    bs = base_set[base_set.elev.notna()]
    pool = {k: bs[bs.kind == k].elev.values for k in h.kind.unique()}
    ns = h.kind.value_counts().to_dict()
    sims = np.empty(n_perm)
    for k in range(n_perm):
        x = np.concatenate([rng.choice(pool[s], ns[s]) for s in ns])
        sims[k] = np.median(x)
    return {"n": len(h), "median": float(obs), "null_median": float(np.median(sims)), "p_high": float((sims >= obs).mean()),
            "p_low": float((sims <= obs).mean()), "upland_pc": float(100 * (h.elev >= 250).mean()),
            "modern_median": float(h[h.layer == "modern"].elev.median()) if (h.layer == "modern").any() else None}


R["elev_test"] = {a: elev_test(a) for a in ("wolf", "crane", "eagle", "raven", "boar", "deer", "fox", "badger", "wildcat", "otter")}


def elev_test_other(a, n_perm=20000):
    """a stricter check: against the other animals' kept names of the same kind and the same rule family (old name or
    later English/Scots descriptive name), since the descriptive rules only accept names with a landscape word"""
    hh = H[(H.nation != "Ireland") & H.elev.notna()].copy()
    hh["st"] = np.where(hh.layer == "modern", "modern", "old") + "_" + hh.kind
    h, o = hh[hh.animal == a], hh[hh.animal != a]
    ns = h.st.value_counts().to_dict()
    pool = {s: o[o.st == s].elev.values for s in ns}
    sims = np.array([np.median(np.concatenate([rng.choice(pool[s], ns[s]) for s in ns if len(pool[s])])) for _ in range(n_perm)])
    obs = h.elev.median()
    return {"n": len(h), "median": float(obs), "null_median": float(np.median(sims)), "p_high": float((sims >= obs).mean()),
            "p_low": float((sims <= obs).mean())}


R["elev_test_other"] = {a: elev_test_other(a) for a in ("wolf", "boar", "deer", "otter")}
mod = H[(H.layer == "modern") & (H.nation != "Ireland")]
R["modern_all_median"] = float(mod.elev.median())
# English-language wolf names only (Old English, Old Norse, modern English or Scots)
hw = H[(H.animal == "wolf") & H.layer.isin(["english", "norse", "modern"])]
R["wolf_english"] = {"n": len(hw), "median_elev": float(hw.elev.median()), "upland_pc": float(100 * (hw.elev >= 250).mean()),
                     "north_pc": float(100 * (hw.lat >= 53.5).mean())}
# cranes: low ground and the east
hc = H[H.animal == "crane"]
R["crane_low"] = {"n": len(hc), "below50_pc": float(100 * (hc.elev < 50).mean()), "below100_pc": float(100 * (hc.elev < 100).mean()),
                  "base_below50_pc": float(100 * (g[g.src == "uk_place"].elev < 50).mean()), "base_below100_pc": float(100 * (g[g.src == "uk_place"].elev < 100).mean()),
                  "england_pc": float(100 * (hc.nation == "England").mean()), "south_pc": float(100 * (hc.lat < 52.5).mean()),
                  "base_south_pc": float(100 * (g[(g.src == "uk_place") & (g.nation == "England")].lat < 52.5).mean())}
R["crane_low"]["south_midlands_pc"] = float(100 * (hc.lat < 53.3).mean())
hr = H[(H.animal == "raven") & (H.layer == "modern")]
R["raven_modern"] = {"n": len(hr), "cumbria_nland": int(hr.county.isin(["Cumbria", "Northumberland"]).sum())}
R["raven_modern"]["cumbria_nland_pc"] = 100 * R["raven_modern"]["cumbria_nland"] / len(hr)
FENS = ["Cambridgeshire", "Lincolnshire", "Norfolk", "Suffolk"]
R["crane_low"]["fen_counties"] = int(hc.county.isin(FENS).sum())
# eagles by language: Highlands and islands vs elsewhere
he = H[H.animal == "eagle"]
R["eagle"] = {"gaelic": int((he.layer == "gaelic").sum()), "welsh": int((he.layer == "welsh").sum()), "irish": int((he.layer == "irish").sum()),
              "english": int(he.layer.isin(["english", "norse"]).sum()), "modern": int((he.layer == "modern").sum()), "n": len(he),
              "scotland_pc": float(100 * (he.nation == "Scotland").mean())}
R["eagle"]["celtic_pc"] = 100 * (R["eagle"]["gaelic"] + R["eagle"]["welsh"] + R["eagle"]["irish"]) / len(he)
# share of Celtic-language names among all kept places in Scotland, by animal family (lost vs living)
LOST = ["wolf", "beaver", "crane", "boar"]
R["lost_places"] = int(H.animal.isin(LOST).sum())
R["lost_certain"] = int((H.animal.isin(LOST) & (H.certainty == "certain")).sum())

# ---------- what is in the hills: kinds of feature
H["is_nature"] = H.src == "uk_nature"
R["nature_pc"] = float(100 * H.is_nature.mean())
R["settle_n"] = int((~H.is_nature).sum())
R["settle_n_named_old"] = int(((~H.is_nature) & H.layer.isin(["english", "norse"])).sum())

# ---------- hot spots: 10 km squares (British National Grid, Irish Grid ignored: Ireland is sparse) with most animals
import pyproj
tr = pyproj.Transformer.from_crs(4326, 27700, always_xy=True)
hu = H[H.nation != "Ireland"].copy()
hu["E"], hu["N"] = tr.transform(hu.lon.values, hu.lat.values)
hu["sq"] = (hu.E // 10000).astype(int).astype(str) + "_" + (hu.N // 10000).astype(int).astype(str)
sq = hu.groupby("sq").agg(n=("animal", "size"), k=("animal", "nunique"), animals=("animal", lambda s: sorted(set(s))),
                          lon=("lon", "mean"), lat=("lat", "mean"), names=("name", lambda s: list(s)[:12]), county=("county", lambda s: s.mode().iloc[0]))
sq = sq.sort_values(["k", "n"], ascending=False)
R["hotspots"] = [{"sq": i, "k": int(r.k), "n": int(r.n), "animals": r.animals, "lon": float(r.lon), "lat": float(r.lat), "names": r.names, "county": r.county}
                 for i, r in sq.head(8).iterrows()]
R["hotspot_top"] = R["hotspots"][0]

# ---------- county density (UK counties only)
gc = g[g.src != "ie_place"].groupby("county").size()
hc2 = H[H.nation != "Ireland"].groupby("county").size()
dens = pd.DataFrame({"points": gc, "animal_places": hc2}).fillna(0)
dens["per_1000"] = 1000 * dens.animal_places / dens.points
dens = dens[dens.points >= 1000].sort_values("per_1000", ascending=False)
dens.to_csv(f"{DATA}/county_density.csv")
R["county_top"] = [{"county": c, "per_1000": float(r.per_1000), "places": int(r.animal_places), "points": int(r.points)} for c, r in dens.head(6).iterrows()]
R["county_bottom"] = [{"county": c, "per_1000": float(r.per_1000), "places": int(r.animal_places)} for c, r in dens.tail(4).iterrows()]
R["uk_per_1000"] = float(1000 * len(H[H.nation != "Ireland"]) / len(g[g.src != "ie_place"]))

# ---------- the animals lost, when (sources in the paper)
R["lost"] = [
    {"animal": "bear", "label": "Brown bear", "when": "early medieval at the latest", "year": 800, "src": "Yalden (1999)", "places": 0},
    {"animal": "boar", "label": "Wild boar", "when": "13th century in the wild; park herds into the 17th", "year": 1250, "src": "Yalden (1999)", "places": A["boar"]["places"]},
    {"animal": "wolf", "label": "Wolf, England", "when": "around 1500", "year": 1500, "src": "Yalden (1999); Pluskowski (2006)", "places": A["wolf"]["nat_England"]},
    {"animal": "beaver", "label": "Beaver", "when": "by the 16th century (debated)", "year": 1550, "src": "Coles (2006)", "places": A["beaver"]["places"]},
    {"animal": "crane", "label": "Crane, as a breeding bird", "when": "around 1600", "year": 1600, "src": "Boisseau and Yalden (1998)", "places": A["crane"]["places"]},
    {"animal": "wolf", "label": "Wolf, Scotland", "when": "late 17th or 18th century", "year": 1700, "src": "Yalden (1999)", "places": A["wolf"]["nat_Scotland"]},
    {"animal": "wolf", "label": "Wolf, Ireland", "when": "1786", "year": 1786, "src": "Hickey (2000)", "places": A["wolf"]["nat_Ireland"] + A["wolf"]["nat_Northern_Ireland"]},
    {"animal": "eagle", "label": "White-tailed eagle", "when": "1918 (reintroduced from 1975)", "year": 1918, "src": "Love (1983)", "places": A["eagle"]["places"]},
]
R["oldest_gap"] = 2026 - 1250

# ---------- examples quoted in words: check they are kept, with the reading given
def ex(name, animal):
    r = H[(H.name == name) & (H.animal == animal)]
    assert len(r) >= 1, (name, animal)
    r = r.iloc[0]
    return {"name": name, "county": r.county, "certainty": r.certainty, "gloss": r.gloss, "element": r.element, "elev": float(r.elev), "kind": r.kind}


R["ex"] = {k: ex(*v) for k, v in {"woolpit": ("Woolpit", "wolf"), "ulpha": ("Ulpha", "wolf"), "beverley": ("Beverley", "beaver"), "bevercotes": ("Bevercotes", "beaver"),
                                  "cranfield": ("Cranfield", "crane"), "tranmere": ("Tranmere", "crane") if (H.name == "Tranmere").any() else ("Lower Tranmere", "crane"),
                                  "arncliffe": ("Arncliffe", "eagle"), "eversley": ("Eversley", "boar"), "wildboarclough": ("Wildboarclough", "boar"),
                                  "wolfhole": ("Wolfhole Crag", "wolf"), "leixlip": ("Leixlip", "salmon"), "hartlepool": ("Hartlepool", "deer"),
                                  "brigoturk": ("Brig o' Turk", "boar"), "catford": ("Catford", "wildcat"), "earnley": ("Earnley", "eagle"),
                                  "wildboarfell": ("Wild Boar Fell", "boar"), "craigentinny": ("Craigentinny", "fox"), "ibrox": ("Ibrox", "badger")}.items()}
R["false_friend_examples"] = [
    {"name": "Wolverhampton", "looks": "wolf", "is": "Wulfrun's high farm, after a woman's name"},
    {"name": "Eagle (Lincolnshire)", "looks": "eagle", "is": "Old English ac-leah, oak wood"},
    {"name": "Eaglesham", "looks": "eagle", "is": "Gaelic eaglais, a church"},
    {"name": "Swanage", "looks": "swan", "is": "Old English swan, herdsmen"},
    {"name": "Roedean", "looks": "roe deer", "is": "Old English ruh denu, rough valley"},
    {"name": "Brockley", "looks": "badger", "is": "a brook, or a personal name"},
    {"name": "Cranagh", "looks": "crane", "is": "Irish crann, a tree"},
    {"name": "Donnybrook", "looks": "badger", "is": "Domhnach Broc, St Broc's church"},
]
for f in R["false_friend_examples"]:
    nm = f["name"].split(" (")[0]
    if nm in ("Wolverhampton", "Swanage", "Eaglesham", "Brockley", "Cranagh", "Donnybrook"):
        st = C[C.name == nm].status
        if len(st):
            assert (st != "kept").all(), nm
jsave(R, f"{DATA}/results.json", indent=1)

# ---------- data files
cols = ["place_id", "is_head", "osm", "name", "name_cy", "name_gd", "name_ga", "animal", "layer", "element", "gloss", "certainty", "rule",
        "kind", "src", "county", "nation", "lon", "lat", "elev"]
K2 = K[cols].sort_values(["animal", "place_id", "is_head"], ascending=[True, True, False])
K2["osm_url"] = "https://www.openstreetmap.org/" + K2.osm
K2.to_csv(f"{DATA}/animal_names.csv", index=False)
C[["osm", "name", "name_cy", "name_gd", "name_ga", "animal", "rule", "certainty", "status", "why", "kind", "county", "nation", "lon", "lat"]].sort_values(
    ["status", "animal", "name"]).to_csv(f"{DATA}/candidates_review.csv", index=False)
rows = [dict(kind="named", id=h, animal=a, layer=L, element=e, gloss=gl, certainty=c, scope=";".join(cs) if isinstance(cs, list) else (cs or "any")) for h, a, L, e, gl, c, cs in NAMED]
rows += [dict(kind="word", id=w[0], animal=w[1], layer=w[2], element=w[6], gloss=w[3], certainty=w[7], scope=";".join(w[4])) for w in WORD]
rows += [dict(kind="modern", id=m[0], animal=m[1], layer="modern", element="", gloss=m[2], certainty=m[3], scope="UK") for m in MODERN]
rows += [dict(kind="exclude", id="", animal="", layer="", element=why, gloss=p, certainty="", scope="") for p, why in EXCLUDE]
pd.DataFrame(rows).to_csv(f"{DATA}/elements.csv", index=False)
print(json.dumps({k: R[k] for k in ("review", "certain", "layers", "nations", "elev_test", "wolf_english", "crane_low", "eagle", "hotspot_top", "county_top")}, indent=1, ensure_ascii=False)[:6000])
for a in A: print(a, {k: A[a][k] for k in ("places", "certain", "median_elev", "upland_pc", "celtic", "english_old", "layer_modern")})
