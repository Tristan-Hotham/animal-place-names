"""Step 7: the paper. Fills code/paper_template.tex from data/results.json, adds tables, compiles with xelatex.
Output: release/paper/Hotham_Where_The_Wolves_Were.pdf and .tex beside the f_*.png figures.
The DOI stays a placeholder: the publisher reruns  DOI=10.5281/zenodo.N python3 code/07_paper.py  then 08_release.py."""
import subprocess
from common import *
from elements import NAMED

R = jload(f"{DATA}/results.json")
OUT = os.path.join(ROOT, "release", "paper"); NAME = "Hotham_Where_The_Wolves_Were"
tex = lambda s: str(s).replace("\\", "").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#").replace("$", "\\$")
assert R["county_top"][0]["county"] == "Northumberland" and R["county_top"][2]["county"] in ("Cumbria", "Highland", "Dumfries and Galloway")
assert R["hotspot_top"]["county"] == "Cumbria" and -3.4 < R["hotspot_top"]["lon"] < -3.0 and 54.25 < R["hotspot_top"]["lat"] < 54.45   # "around Dunnerdale"
assert R["layers"]["norse"] == 3 or R["layers"]["norse"] > 0


def tfmt(v, f):
    if f == "int": return f"{int(round(float(v))):,}"
    if f == "pc": return f"{round(float(v))}\\%"
    if f == "f1": return f"{float(v):.1f}"
    if f == "f2": return f"{float(v):.2f}"
    if f == "f3": return f"{float(v):.3f}"
    return tex(str(v))


A, T = R["animals"], R["elev_test"]
rows = ""
for a in R["order_by_places"]:
    x = A[a]
    t = T.get(a)
    hh = f"{t['median']:.0f} & {t['null_median']:.0f} & {min(t['p_high'], t['p_low']):.3f}{'+' if t['p_high'] < t['p_low'] else '-'}" if t else "& &"
    rows += (f"{x['label']} & {x['places']} & {x['certain']} & {x['layer_english']} & {x['layer_norse']} & {x['layer_welsh']} & {x['layer_gaelic']} & "
             f"{x['layer_irish']} & {x['layer_modern']} & {hh}\\\\\n")
TA = ("\\begin{table}[tbp]\\centering\\footnotesize\\setlength{\\tabcolsep}{4pt}\\caption{Places by animal: total, with a certain reading, by language (Old English, Old Norse, Welsh, "
      "Scottish Gaelic, Irish, later English or Scots), and the median ground height (m) of UK places against that expected for random names of the same "
      "kinds, with the one-sided p-value (+ higher, $-$ lower than expected; 20,000 draws).}\\label{tab:animals}"
      "\\begin{tabular}{lrrrrrrrrrrr}\\toprule Animal & Places & Certain & OE & ON & Wel & Gae & Ir & Later & Height & Expected & p\\\\\\midrule\n" + rows +
      "\\bottomrule\\end{tabular}\\end{table}").replace("-}", "$-$}")
TA = TA.replace("-\\\\", "$-$\\\\")
rows = "".join(f"{tex(f['name'])} & {tex(f['looks'])} & {tex(f['is'])}\\\\\n" for f in R["false_friend_examples"])
TF = ("\\begin{table}[tbp]\\centering\\small\\caption{Some false friends removed by rule or in review.}\\label{tab:ff}"
      "\\begin{tabular}{llp{8.4cm}}\\toprule Name & Looks like & Is\\\\\\midrule\n" + rows + "\\bottomrule\\end{tabular}\\end{table}")
rows = ""
for h, a, L, el, gl, c, cs in NAMED:
    sc = "any" if cs is None else ("England" if cs == "ENGLAND" else ", ".join(cs))
    rows += f"{tex(h)} & {tex(ALAB[a])} & {tex(el)} & {tex(gl)} & {tex(sc)} & {c}\\\\\n"
TN = ("\\begin{small}\\begin{longtable}{R{2.2cm}R{1.3cm}R{2.6cm}R{3.7cm}R{2.7cm}l}\\caption{The named rules: English and Norse settlement names read "
      "with an animal after the standard dictionaries (Mills 2011; Watts 2004; Ekwall 1960), the counties where they apply and the certainty given.}"
      "\\label{tab:named}\\\\\\toprule Name & Animal & Element & Meaning & Counties & Reading\\\\\\midrule\\endhead\n" + rows + "\\bottomrule\\end{longtable}\\end{small}")
t = open(os.path.join(ROOT, "code", "paper_template.tex"), encoding="utf-8").read()
t = t.replace("\\begin{document}", "\\newcolumntype{R}[1]{>{\\raggedright\\arraybackslash}p{#1}}\n\\begin{document}").replace("{{AI}}", AI).replace("{{TABLE_ANIMALS}}", TA).replace("{{TABLE_FF}}", TF).replace("{{TABLE_NAMED}}", TN)
t = re.sub(r"\{\{(?!TABLE_|DOI)([^}|]+)(\|(\w+))?\}\}", lambda m: tfmt(get(R, m.group(1)), m.group(3) or "raw"), t)
DOI = os.environ.get("DOI")
t = t.replace("https://doi.org/10.5281/zenodo.24075293", f"\\url{{https://doi.org/{DOI}}}" if DOI else "\\{\\{DOI\\_URL\\}\\}")
assert "{{" not in t and "--" not in t and "—" not in t and "–" not in t
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, NAME + ".tex"), "w", encoding="utf-8").write(t)
for _ in range(2):
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", NAME + ".tex"], cwd=OUT, capture_output=True, text=True)
log = open(os.path.join(OUT, NAME + ".log"), encoding="utf-8", errors="ignore").read()
print([l for l in log.splitlines() if "Missing character" in l or "undefined" in l.lower() or "Overfull" in l][:12])
for ext in (".aux", ".log", ".out", ".bbl", ".blg"):
    q = os.path.join(OUT, NAME + ext)
    if os.path.exists(q): os.remove(q)
txt = subprocess.run(["pdftotext", os.path.join(OUT, NAME + ".pdf"), "-"], capture_output=True, text=True).stdout
pages = subprocess.run(["pdfinfo", os.path.join(OUT, NAME + ".pdf")], capture_output=True, text=True).stdout
print("paper", r.returncode, len(txt.split()), "words;", [l for l in pages.splitlines() if l.startswith("Pages")], "dashes:", txt.count("—") + txt.count("–") + txt.count("--"))
