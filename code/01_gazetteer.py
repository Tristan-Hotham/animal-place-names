"""Step 1: one gazetteer of every named point (UK places, UK hills and other natural features, Irish places), with the nation
and county from the ONS boundaries (Ireland: the state), and the ground height from the terrain tiles.
Output: WORK/gazetteer.csv.gz"""
import pandas as pd, numpy as np
import geopandas as gpd
from common import *

rows = []
for r in read_tsv(PL_UK):
    lon, lat = point(r["wkt"])
    rows.append(dict(osm=r["x"].split("openstreetmap.org/")[-1], src="uk_place", kind=r["place"], name=r["name"], name_cy=r["namecy"],
                     name_gd=r["namegd"], name_ga="", lon=lon, lat=lat))
for r in read_tsv(HILLS):
    lon, lat = point(r["wkt"])
    rows.append(dict(osm=r["x"].split("openstreetmap.org/")[-1], src="uk_nature", kind=r["nat"], name=r["name"], name_cy="", name_gd="",
                     name_ga="", lon=lon, lat=lat))
for r in read_tsv(PL_IE):
    lon, lat = point(r["wkt"])
    rows.append(dict(osm=r["x"].split("openstreetmap.org/")[-1], src="ie_place", kind=r["place"], name=r["name"], name_cy="", name_gd="",
                     name_ga=r["namega"], lon=lon, lat=lat))
g = pd.DataFrame(rows)
n_raw = len(g)
g = g.dropna(subset=["lon", "lat"])
g = g[g["name"].str.strip() != ""]
g = g.drop_duplicates(subset=["osm", "src"])
print("rows", n_raw, "kept", len(g), g.src.value_counts().to_dict())

# nation and county
cty = gpd.read_file(f"{GEO}/counties_uk.geojson").to_crs(4326)
pts = gpd.GeoDataFrame(g, geometry=gpd.points_from_xy(g.lon, g.lat), crs=4326)
j = gpd.sjoin(pts, cty[["county", "nation", "geometry"]], how="left", predicate="within")
j = j[~j.index.duplicated()]
g["county"], g["nation"] = j["county"].values, j["nation"].values
# points just off the generalised coast: nearest county within 3 km
miss = g["nation"].isna() & (g.src != "ie_place")
if miss.any():
    c3 = cty.to_crs(27700)
    p3 = pts[miss.values].to_crs(27700)
    nn = gpd.sjoin_nearest(p3, c3[["county", "nation", "geometry"]], how="left", max_distance=3000)
    nn = nn[~nn.index.duplicated()]
    g.loc[nn.index, "county"] = nn["county"].values
    g.loc[nn.index, "nation"] = nn["nation"].values
g.loc[g.src == "ie_place", "nation"] = "Ireland"
g.loc[g.src == "ie_place", "county"] = ""
print("nation", g.nation.value_counts(dropna=False).to_dict())
g["elev"] = np.round(elevations(g.lon.values, g.lat.values), 0)
print("elev missing", int(g.elev.isna().sum()))
g.to_csv(f"{WORK}/gazetteer.csv.gz", index=False)
