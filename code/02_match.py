"""Step 2: match every name in the gazetteer against the element list (code/elements.py), drop false friends, apply the
hand review (code/overrides.csv), and group repeats of one name into one place.
Output: WORK/matches_all.csv (every candidate, with why it was kept or dropped), data/animal_names.csv (kept)."""
import unicodedata, warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
from common import *
from elements import NAMED, PRE, POST, WORD, MADADH, MODERN, EXCLUDE, LANDWORD

g = pd.read_csv(f"{WORK}/gazetteer.csv.gz", keep_default_na=False, low_memory=False)
g["elev"] = pd.to_numeric(g["elev"], errors="coerce")
g.loc[g.nation == "", "nation"] = "Other"


def norm(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("`", "'")).strip()


for c in ("name", "name_cy", "name_gd", "name_ga"):
    g["n_" + c] = g[c].map(norm)
SETTLE = {"city", "town", "village", "hamlet", "suburb", "neighbourhood", "quarter", "locality"}
HOUSE = {"farm", "isolated_dwelling"}
excl = [(re.compile(p), why) for p, why in EXCLUDE]

cands = []


def add(i, r, rule, animal, layer, element, gloss, cert, auth, field):
    cands.append(dict(idx=i, rule=rule, animal=animal, layer=layer, element=element, gloss=gloss, certainty=cert, auth=auth, field=field))


# NAMED
named = {}
for head, animal, layer, el, gloss, cert, counties in NAMED:
    rx = re.compile("^" + PRE + re.escape(norm(head)) + POST + "$")
    named.setdefault(norm(head), []).append((rx, animal, layer, el, gloss, cert, counties, head))
for i, r in g.iterrows():
    if r.kind not in SETTLE:
        continue
    n = r.n_name
    for key, rules in named.items():
        if key not in n:
            continue
        # a county-specific rule wins over a general one for the same head name
        hit = None
        for rx, animal, layer, el, gloss, cert, counties, head in sorted(rules, key=lambda x: x[6] is None):
            if rx.match(n) and (counties is None or (counties == "ENGLAND" and r.nation == "England") or r.county in counties or (head == "Leixlip" and r.nation == "Ireland")):
                hit = (animal, layer, el, gloss, cert, head); break
        if hit:
            add(i, r, "named:" + hit[5], hit[0], hit[1], hit[2], hit[3], hit[4], "MILLS WATTS EKWALL", "name")
# WORD
FIELDS = {"n": "n_name", "cy": "n_name_cy", "gd": "n_name_gd", "ga": "n_name_ga"}
for wid, animal, layer, rx, nations, fields, gloss, cert, auth in WORD:
    c = re.compile(rx)
    for f in fields.split():
        col = FIELDS[f]
        m = g[col].str.contains(c, regex=True) & g.nation.isin(nations)
        for i in g.index[m]:
            add(i, g.loc[i], "word:" + wid, animal, layer, gloss.split(",")[0], gloss, cert, auth, f)
# madadh alone: dog, fox or wolf
cm = re.compile(MADADH)
for f in ("n", "gd"):
    m = g[FIELDS[f]].str.contains(cm, regex=True) & (g.nation == "Scotland")
    for i in g.index[m]:
        add(i, g.loc[i], "word:gd_madadh", "madadh", "gaelic", "madadh", "madadh: dog, fox or wolf", "uncertain", "DICT", f)
# MODERN (England, Scotland, Wales, Northern Ireland, Isle of Man; descriptive English or Scots words)
for mid, animal, rx, cert in MODERN:
    c = re.compile(rx)
    m = g.n_name.str.contains(c, regex=True) & (g.nation != "Ireland") & ~g.kind.isin(HOUSE | {"suburb", "neighbourhood", "quarter"})
    for i in g.index[m]:
        add(i, g.loc[i], "modern:" + mid, animal, "modern", animal + " (English or Scots word)", "descriptive name with the English or Scots word", cert, "-", "name")

C = pd.DataFrame(cands)
C = C.join(g[["osm", "src", "kind", "name", "name_cy", "name_gd", "name_ga", "lon", "lat", "county", "nation", "elev", "n_name"]], on="idx")
# one candidate per (point, animal): the strongest rule wins (named > word > modern; certain > probable)
rank = {"named": 0, "word": 1, "modern": 2}
C["r1"] = C.rule.str.split(":").str[0].map(rank)
C["r2"] = C.certainty.map({"certain": 0, "probable": 1, "uncertain": 2})
C = C.sort_values(["idx", "animal", "r1", "r2"]).drop_duplicates(["idx", "animal"])
# madadh is dropped where the same point is a fox (madadh-ruadh) or wolf (madadh-allaidh)
fw = set(C.idx[C.animal.isin(["fox", "wolf"])])
C = C[~((C.animal == "madadh") & C.idx.isin(fw))]
C["status"], C["why"] = "kept", ""
for i, r in C.iterrows():
    nm = " | ".join(x for x in (r.n_name, norm(r.name_cy), norm(r.name_gd)) if x)
    for rx, why in excl:
        if rx.search(nm):
            if r.rule.startswith("named:") and why.startswith("a medieval deer park"):
                continue
            C.at[i, "status"], C.at[i, "why"] = "false friend", why
            break
C.loc[C.animal == "madadh", ["status", "why"]] = ["uncertain", "madadh alone can be dog, fox or wolf"]
# the hand review of every candidate
ov = pd.read_csv(os.path.join(ROOT, "code", "overrides.csv"), keep_default_na=False) if os.path.exists(os.path.join(ROOT, "code", "overrides.csv")) else pd.DataFrame(columns=["osm", "animal", "action", "reason"])
n_over = 0
for o in ov.itertuples():
    sel = (C.osm == o.osm) & ((C.animal == o.animal) | (o.animal == "*"))
    if not sel.any():
        print("override not used:", o.osm, o.animal); continue
    n_over += 1
    if o.action == "drop":
        C.loc[sel, ["status", "why"]] = ["dropped in review", o.reason]
    elif o.action in ("certain", "probable"):
        C.loc[sel, "certainty"] = o.action
        C.loc[sel, "why"] = "certainty set in review: " + o.reason
    elif o.action.startswith("animal="):
        C.loc[sel, "animal"] = o.action.split("=")[1]
        C.loc[sel, "why"] = "animal changed in review: " + o.reason
    else:
        raise ValueError(o.action)
print("overrides applied", n_over)

# repeats: the same name (or its parts, Woolpit and Woolpit Heath) for one animal within 3 km is one place
K = C[C.status == "kept"].copy().sort_values(["animal", "r1", "r2"])
K["place_id"] = -1
pid = 0
xs, ys = np.radians(K.lon.values), np.radians(K.lat.values)
idx = list(K.index)
base = K.n_name.str.replace(r"^(great|little|upper|lower|nether|north|south|east|west|high|old|new) ", "", regex=True).str.split(" ").str[0].values
cmp_ = K.n_name.str.replace(r"[\s'’-]", "", regex=True).values
for a in K.animal.unique():
    ii = [k for k, j in enumerate(idx) if K.at[j, "animal"] == a]
    for k in ii:
        j = idx[k]
        if K.at[j, "place_id"] >= 0: continue
        K.at[j, "place_id"] = pid
        for k2 in ii:
            j2 = idx[k2]
            if K.at[j2, "place_id"] >= 0: continue
            d = km(K.at[j, "lat"], K.at[j, "lon"], K.at[j2, "lat"], K.at[j2, "lon"])
            # names compared without spaces and apostrophes, so Wolf Hope and Wolfhope Bush, Crane Dale and Cranedale Spout merge
            if d < 3.0 and (base[k] == base[k2] or cmp_[k] in cmp_[k2] or cmp_[k2] in cmp_[k]):
                K.at[j2, "place_id"] = pid
        pid += 1
for head, *_ in NAMED:
    if not (C.rule == "named:" + head).any(): print("NAMED not found:", head)
C = C.join(K["place_id"]).fillna({"place_id": -1})
C["place_id"] = C.place_id.astype(int)
# the head of each place: a settlement before a hill, larger kinds first
KO = {"city": 0, "town": 1, "village": 2, "suburb": 3, "hamlet": 4, "quarter": 5, "neighbourhood": 6, "locality": 7}
C["is_head"] = False
for p, grp in C[C.place_id >= 0].groupby("place_id"):
    j = grp.assign(o=grp.kind.map(KO).fillna(8), L=grp.name.str.len()).sort_values(["r1", "r2", "o", "L"]).index[0]
    C.at[j, "is_head"] = True
C.drop(columns=["r1", "r2"]).to_csv(f"{WORK}/matches_all.csv", index=False)
print(C.status.value_counts().to_dict())
k = C[C.is_head]
print("places", len(k), k.groupby("animal").size().to_dict())
print(k.groupby(["animal", "certainty"]).size().unstack(fill_value=0))
