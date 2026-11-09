"""Step 6: index.html from code/page_template.html, filled from data/results.json, with the facts stated in words checked.
10.5281/zenodo.24075293, https://doi.org/10.5281/zenodo.24075293 and https://blog.tristanhotham.com/2026/10/31/animal-place-names/ stay as placeholders for the publisher."""
import time
from common import *

R = jload(f"{DATA}/results.json")
A, T = R["animals"], R["elev_test"]
# ---- facts stated in words (page, blog, paper)
assert {e["name"] for e in R["ex"].values()} >= {"Woolpit", "Ulpha", "Beverley", "Bevercotes", "Cranfield", "Arncliffe", "Eversley", "Wildboarclough"}
assert all(R["ex"][k]["certainty"] == "certain" for k in ("woolpit", "ulpha", "beverley", "bevercotes", "cranfield", "arncliffe", "eversley"))
assert R["ex"]["wolfhole"]["county"] == "Lancashire" and R["ex"]["brigoturk"]["county"] == "Stirling"
assert T["wolf"]["p_high"] < 0.001 and T["boar"]["p_high"] < 0.001 and T["deer"]["p_high"] < 0.001          # "much higher"
assert T["raven"]["p_high"] < 0.05 and T["wildcat"]["p_high"] < 0.05                                       # "a little higher"
assert min(T[a]["p_high"] for a in ("fox", "badger", "eagle", "crane")) > 0.1 and min(T[a]["p_low"] for a in ("fox", "badger", "eagle", "crane")) > 0.1  # "about where expected"
assert 0.03 < T["otter"]["p_low"] < 0.1 and T["otter"]["median"] < T["otter"]["null_median"]                 # "low, at the edge of chance"
assert R["elev_test_other"]["wolf"]["p_high"] < 0.01 and R["elev_test_other"]["otter"]["p_low"] < 0.05
assert T["wolf"]["p_high"] == 0.0                                                                           # "none was as high"
assert R["crane_low"]["england_pc"] > 90 and R["crane_low"]["fen_counties"] == 1
assert T["crane"]["p_low"] > 0.1 and T["crane"]["p_high"] > 0.1
assert A["fox"]["layer_modern"] / A["fox"]["places"] > 0.5 and A["deer"]["layer_modern"] / A["deer"]["places"] > 0.5   # "mostly in later English"
assert A["eagle"]["layer_gaelic"] > A["eagle"]["layer_english"] and A["boar"]["layer_gaelic"] > A["boar"]["places"] / 2  # eagles and boar "mainly in Gaelic"
assert R["eagle"]["english"] == 6 or R["eagle"]["english"] >= 3
assert R["hotspot_top"]["county"] == "Cumbria" and R["county_top"][0]["county"] == "Northumberland"
assert 1250 < 2026 - 400 and all(400 <= 2026 - r["year"] <= 800 for r in R["lost"] if r["animal"] in ("boar", "wolf", "beaver", "crane") and r["label"] != "Wolf, Ireland" and r["label"] != "Wolf, Scotland")
assert A["wolf"]["nat_England"] > A["wolf"]["nat_Scotland"]
CHIPS = '<button class="chip" data-a="all" aria-pressed="true">All</button>' + "".join(
    f'<button class="chip" data-a="{a}" aria-pressed="false"><span class="sw" style="background:{c}"></span>{l}</button>' for a, l, c in ANIMALS if A[a]["places"] >= 3)
LANG = "".join(f'<label><input type="checkbox" data-l="{k}" checked> {l}</label>' for k, l in LAYERS)
t = open(os.path.join(ROOT, "code", "page_template.html"), encoding="utf-8").read()
css = open(os.path.join(ROOT, "code", "page.css"), encoding="utf-8").read()
fs = open(os.path.join(ROOT, "code", "fullscreen_snippet.html"), encoding="utf-8").read()
t = t.replace("{{CSS}}", css).replace("{{CHIPS}}", CHIPS).replace("{{LANG_BOXES}}", LANG).replace("{{FULLSCREEN}}", fs)
t = t.replace("{{BYLINE}}", BYLINE).replace("{{AI}}", AI).replace("{{VERSION}}", time.strftime("%Y%m%d"))
t = fill(t, R)
assert set(re.findall(r"\{\{([^}]+)\}\}", t)) <= {"DOI", "DOI_URL", "BLOG_URL"}, set(re.findall(r"\{\{([^}]+)\}\}", t))
vis = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", "", t, flags=re.S)
for bad in ("—", "–", "--", "DSIT", "DCMS", "civil serv"):
    assert bad not in vis, bad
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(t)
js = open(os.path.join(ROOT, "js", "page.js"), encoding="utf-8").read()
assert "—" not in js and "–" not in js
print("index.html", len(t) // 1024, "KB")
