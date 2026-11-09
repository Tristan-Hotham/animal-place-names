"""Step 8: blog post and meta (release/blog), Zenodo files and metadata (release/zenodo).
10.5281/zenodo.24075293, https://doi.org/10.5281/zenodo.24075293 and https://blog.tristanhotham.com/2026/10/31/animal-place-names/ stay as placeholders for the publisher."""
import shutil, zipfile, importlib.util
from PIL import Image
from common import *

spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "code", "06_build_site.py"))
spec.loader.exec_module(importlib.util.module_from_spec(spec))          # shared fact checks (and rebuilds index.html)
R = jload(f"{DATA}/results.json")
REL = os.path.join(ROOT, "release"); NAME = "Hotham_Where_The_Wolves_Were"
KEEP = {"DOI", "DOI_URL", "BLOG_URL"}
assert R["ex"]["woolpit"]["county"] == "Suffolk" and R["ex"]["arncliffe"]["county"] == "North Yorkshire"

post = fill(open(os.path.join(ROOT, "code", "blog_template.html"), encoding="utf-8").read(), R)
used = re.findall(r"\{\{IMG\|([^|]+)\|", post)
assert 5 <= len(used) <= 8, len(used)
assert all(re.search(r"^\{\{IMG\|" + re.escape(u_), post, re.M) for u_ in used) and "wp:image" not in post
for img in used:
    assert Image.open(f"{REL}/blog/{img}").size[0] == 1800, img
for fn in os.listdir(f"{REL}/blog"):
    if fn.startswith("b_") and fn not in used:
        os.remove(f"{REL}/blog/{fn}")
assert set(re.findall(r"\{\{([^|}]+)\}\}", post)) <= KEEP, set(re.findall(r"\{\{([^|}]+)\}\}", post))
vis = re.sub(r"<!--.*?-->", "", post, flags=re.S)
for bad in ("\u2014", "\u2013", "--", "DSIT", "DCMS", "civil serv"):
    assert bad not in vis, bad
assert AI in post
open(f"{REL}/blog/post.html", "w", encoding="utf-8").write(post)
words = len(re.sub(r"<[^>]+>|\{\{IMG\|[^}]*\}\}", " ", vis).split())
A = R["animals"]
meta = {"title": "Where the wolves were: the animals hiding in British and Irish place names",
        "slug": "animal-place-names",
        "excerpt": f"Wolves, beavers, cranes and wild boar are long gone, but their names are not. I searched every named place and hill in Britain and Ireland for animals, threw out the false friends one by one, and mapped the {R['review']['places']} that are left.",
        "seo_description": f"Animals in British and Irish place names: {A['wolf']['places']} wolf names, high on northern crags, plus cranes, beavers, eagles and boar, checked one by one.",
        "tags": ["maps", "place names", "toponymy", "wolves", "wildlife", "history", "OpenStreetMap", "Gaelic", "Old English", "data visualisation"],
        "header_alt": f"Title card on parchment reading 'Where the wolves were' in black and red lettering beside a map of Britain and Ireland dotted with coloured animal names, with the line {R['review']['places']} places in Britain and Ireland whose names keep an animal."}
assert len(meta["seo_description"]) < 160, len(meta["seo_description"])
jsave(meta, f"{REL}/blog/meta.json", indent=2)

Z = f"{REL}/zenodo"; os.makedirs(Z, exist_ok=True)
for fn in os.listdir(Z):
    os.remove(os.path.join(Z, fn))
shutil.copy(f"{REL}/paper/{NAME}.pdf", f"{Z}/{NAME}.pdf")
zp = f"{Z}/{SLUG}_data_and_code.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for dd in ("code", "js"):
        for fn in sorted(os.listdir(os.path.join(ROOT, dd))):
            if fn.endswith(".pyc") or fn == "__pycache__" or fn.endswith(".png"):
                continue
            z.write(os.path.join(ROOT, dd, fn), f"{SLUG}/{dd}/{fn}")
    for fn in sorted(os.listdir(os.path.join(ROOT, "data"))):
        z.write(os.path.join(ROOT, "data", fn), f"{SLUG}/data/{fn}")
    for fn in ("README.md", "LICENSE", "index.html"):
        z.write(os.path.join(ROOT, fn), f"{SLUG}/{fn}")
    z.write(os.path.join(ROOT, "reddit", "collage.py"), f"{SLUG}/reddit/collage.py")
tex = open(f"{REL}/paper/{NAME}.tex", encoding="utf-8").read()
ab = re.search(r"\\begin\{center\}\\textbf\{Abstract\}\\end\{center\}\n(.*?)\n\n\\textbf\{Keywords", tex, re.S).group(1)
ab = ab.replace("\\%", "%").replace("\\&", "&").replace("\\textdegree{}", "°")
ab = re.sub(r"\\textit\{([^}]*)\}", r"\1", ab)
assert "\\" not in ab and "$" not in ab, ab
zmeta = {"title": "Where the Wolves Were: Animals in the Place Names of Britain and Ireland",
         "upload_type": "publication", "publication_type": "workingpaper",
         "description": f"<p>{ab}</p><p>Interactive page: <a href=\"{PAGE}\">{PAGE}</a>. Data and code: <a href=\"{REPO}\">{REPO}</a>. Blog post: {{https://blog.tristanhotham.com/2026/10/31/animal-place-names/}}.</p><p>Sources: OpenStreetMap contributors (ODbL), queried with QLever; AWS Terrain Tiles; ONS boundaries (OGL v3.0). The name tables are derived from OpenStreetMap and released under the Open Database Licence; text and figures CC BY 4.0; code MIT.</p>",
         "creators": [{"name": "Hotham, Tristan", "affiliation": "Independent researcher", "orcid": "0000-0003-4931-9349"}],
         "keywords": ["place names", "toponymy", "historical ecology", "extinct species", "wolf", "beaver", "crane", "OpenStreetMap", "Old English", "Gaelic", "Welsh"],
         "license": "cc-by-4.0", "language": "eng",
         "notes": "Text and figures CC BY 4.0; code MIT; data/animal_names.csv and data/candidates_review.csv derived from OpenStreetMap, ODbL.",
         "related_identifiers": [{"identifier": REPO, "relation": "isSupplementedBy", "resource_type": "software"},
                                 {"identifier": PAGE, "relation": "isSupplementedBy", "resource_type": "other"},
                                 {"identifier": "https://www.openstreetmap.org/", "relation": "isDerivedFrom", "resource_type": "dataset"}],
         "files": sorted(os.listdir(Z))}
sj = json.dumps(zmeta, ensure_ascii=False) + json.dumps(meta, ensure_ascii=False)
assert "\u2014" not in sj and "\u2013" not in sj and "--" not in sj
jsave(zmeta, f"{Z}/metadata.json", indent=2)
print("blog words", words, "figures", len(used), "; zenodo", sorted(os.listdir(Z)), os.path.getsize(zp) // 1024, "KB zip")
