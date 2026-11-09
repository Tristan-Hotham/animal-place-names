"""Reddit collage (r/dataisbeautiful style) and the 1200 x 630 header card.
Light parchment background; labels on the sea with a halo; full legend; source footer.
Output: reddit/animal_place_names_collage.png (3000 x 2100 px) and header.png. Run after code/05_figures.py."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code"))
import pandas as pd
import matplotlib.patheffects as pe
from figstyle import *

R = jload(f"{DATA}/results.json")
K = pd.read_csv(f"{DATA}/animal_names.csv", keep_default_na=False, low_memory=False)
H = K[K.is_head.astype(str) == "True"].copy()
HALO = [pe.withStroke(linewidth=3, foreground=PAPER)]
OUT = os.path.join(ROOT, "reddit", "animal_place_names_collage.png")
A, T = R["animals"], R["elev_test"]

fig = plt.figure(figsize=(10, 7), dpi=300); parchment(fig, seed=11)
fig.text(0.035, 0.955, "Where the wolves were", fontproperties=HAND, fontsize=31, color=RED, va="center")
fig.text(0.035, 0.912, f"{R['review']['places']} places and hills in Britain and Ireland whose names keep an animal, in English, Norse, Welsh, Gaelic or Irish",
         fontproperties=FELL, fontsize=11.5, color=INKC, va="center")
fig.text(0.035, 0.885, f"Checked one by one: {R['review']['corrected_pc']:.0f}% of {R['review']['candidates']} candidates were false friends (Wolverhampton is Wulfrun's, Swanage is herdsmen's).",
         fontproperties=FELL, fontsize=9.8, color=MUT, va="center")

# ---- the map: every place, coloured by animal
ax = fig.add_axes([0.0, 0.06, 0.50, 0.80])
ext, f = ink_base(ax, 27700, (-10.6, 2.0, 49.85, 59.1), coast_lw=0.5, ripple_m=(6e3, 15e3, 28e3), countries=False, min_area=2e7)
order = [a for a, _, _ in ANIMALS][::-1]
for a in order:
    h = H[H.animal == a]
    x, y = f(h.lon.values, h.lat.values)
    big = (h.certainty == "certain").values
    ax.scatter(x[~big], y[~big], s=5, c=ACOL[a], edgecolors="none", alpha=0.9, zorder=6)
    ax.scatter(x[big], y[big], s=17, c=ACOL[a], edgecolors=INKC, linewidths=0.35, zorder=7)
ax.set_xlim(ext[0] + 0.9e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
# labels on the sea: (name, animal, label lon, lat, ha)
LAB = [("Woolpit", "wolf", 2.0, 52.55, "left", "wolf pit"), ("Beverley", "beaver", 0.7, 54.15, "left", "beaver stream"),
       ("Cranfield", "crane", 1.95, 51.72, "left", "cranes' open land"), ("Wolfhole Crag", "wolf", -3.65, 53.62, "right", "wolves on the fells"),
       ("Ulpha", "wolf", -3.85, 54.66, "right", "Norse: wolves' hill"), ("Creag na h-Iolaire", "eagle", -8.25, 57.55, "right", "eagle's crag"),
       ("Brig o' Turk", "boar", -7.75, 55.72, "right", "Gaelic tuirc: boar's bridge"), ("Hartlepool", "deer", 0.5, 55.0, "left", "hart island pool")]
for nm, a, lx, ly, ha, gl in LAB:
    r = H[(H["name"] == nm) & (H.animal == a)].iloc[0]
    px, py = f(r.lon, r.lat); tx, ty = f(lx, ly)
    ax.annotate(f"{nm}\n{gl}", (px, py), xytext=(tx, ty), fontproperties=FELLIT, fontsize=7.6, color=INKC, ha=ha, va="center", zorder=9,
                path_effects=HALO, arrowprops=dict(arrowstyle="-", color=INKC, lw=0.45, shrinkA=1, shrinkB=2))

# ---- legend: every animal with its count
lx = fig.add_axes([0.505, 0.47, 0.18, 0.40]); lx.axis("off")
lx.text(0, 1.0, "Animal (places)", fontproperties=FELLSC, fontsize=11, color=RED, va="top", transform=lx.transAxes)
for i, (a, lab, c) in enumerate(ANIMALS):
    y = 0.92 - i * 0.064
    lx.scatter([0.04], [y], s=34, c=c, edgecolors=INKC, linewidths=0.4, transform=lx.transAxes)
    lx.text(0.12, y, f"{lab} ({A[a]['places']})", fontproperties=FELL, fontsize=9.6, color=INKC, va="center", transform=lx.transAxes)
y = 0.92 - len(ANIMALS) * 0.064
lx.scatter([0.04], [y], s=17, c="#6E604E", edgecolors=INKC, linewidths=0.35, transform=lx.transAxes)
lx.scatter([0.09], [y], s=5, c="#6E604E", edgecolors="none", transform=lx.transAxes)
lx.text(0.14, y, "certain / probable reading", fontproperties=FELL, fontsize=9, color=MUT, va="center", transform=lx.transAxes)

# ---- panel: wolves stand high
bx = fig.add_axes([0.73, 0.555, 0.24, 0.29])
show = ["wolf", "boar", "deer", "raven", "fox", "crane", "otter"]
for i, a in enumerate(show):
    bx.barh(i, T[a]["median"], color=ACOL[a], edgecolor=INKC, lw=0.4, height=0.62)
    bx.plot([T[a]["null_median"]] * 2, [i - 0.4, i + 0.4], color=RED, lw=1.2, ls=(0, (2, 1)))
bx.set_yticks(range(len(show))); bx.set_yticklabels([ALAB[a] for a in show], fontproperties=FELL, fontsize=9)
bx.invert_yaxis(); bx.tick_params(axis="x", labelsize=7.5)
for t in bx.get_xticklabels(): t.set_fontproperties(FELL); t.set_fontsize(8)
for s in ("top", "right"): bx.spines[s].set_visible(False)
bx.set_xlabel("median ground height (m); red: expected", fontproperties=FELL, fontsize=8.5)
fig.text(0.73, 0.875, "Wolves stood high", fontproperties=FELLSC, fontsize=12, color=RED)
fig.text(0.73, 0.858, f"Wolf names {T['wolf']['median']:.0f} m; similar names {T['wolf']['null_median']:.0f} m", fontproperties=FELL, fontsize=8.2, color=MUT)

# ---- panel: lost dates
cx = fig.add_axes([0.53, 0.09, 0.44, 0.30])
L = [r for r in sorted(R["lost"], key=lambda r: r["year"]) if r["animal"] != "bear"]
cx.set_xlim(1150, 2040); cx.set_ylim(-0.6, len(L) - 0.4)
for i, r in enumerate(L):
    c = ACOL.get(r["animal"], INKC)
    cx.plot([r["year"], 2026], [i, i], color=c, lw=0.8, ls=(0, (1, 1.6)))
    cx.scatter([r["year"]], [i], s=28, c=c, edgecolors=INKC, linewidths=0.4, zorder=3)
    t = cx.text(r["year"] - 12, i, f"{r['label']}: {r['when'].split(';')[0]}", ha="right" if r["year"] > 1400 else "left", va="center", fontproperties=FELL, fontsize=8.2, color=INKC)
    if r["year"] <= 1400:
        t.set_position((r["year"] + 15, i + 0.38))
    t.set_path_effects(HALO)
    cx.text(2034, i, str(r["places"]), va="center", fontproperties=FELL, fontsize=8.5, color=c)
cx.set_yticks([]); cx.set_xticks([1200, 1400, 1600, 1800, 2000])
for t in cx.get_xticklabels(): t.set_fontproperties(FELL); t.set_fontsize(8.5)
for s in ("top", "right", "left"): cx.spines[s].set_visible(False)
fig.text(0.53, 0.415, "The names outlived the animals", fontproperties=FELLSC, fontsize=12, color=RED)
fig.text(0.53, 0.397, "When each was lost in the wild (dot) and the places that keep its name today (right)", fontproperties=FELL, fontsize=8.2, color=MUT)

fig.text(0.035, 0.034, "Data: OpenStreetMap contributors (ODbL), via QLever. Readings: Mills, Watts and Ekwall's place-name dictionaries; Welsh, Gaelic and Irish words.", fontproperties=FELL, fontsize=7.4, color=MUT)
fig.text(0.035, 0.014, "Losses: Yalden 1999, Coles 2006, Boisseau and Yalden 1998, Hickey 2000, Love 1983.", fontproperties=FELL, fontsize=7.4, color=MUT)
fig.text(0.965, 0.022, "maps.tristanhotham.com/animal-place-names", fontproperties=FELL, fontsize=8, color=RED, ha="right")
fig.savefig(OUT, dpi=300, facecolor=fig.get_facecolor())
plt.close(fig)

# ---- header card 1200 x 630
fig = plt.figure(figsize=(12, 6.3), dpi=100); parchment(fig, seed=4)
ax = fig.add_axes([0.53, 0.0, 0.47, 1.0])
ext, f = ink_base(ax, 27700, (-10.6, 2.0, 49.85, 59.1), coast_lw=0.6, ripple_m=(6e3, 15e3), countries=False, min_area=2e7)
for a in [a for a, _, _ in ANIMALS][::-1]:
    h = H[H.animal == a]
    x, y = f(h.lon.values, h.lat.values)
    ax.scatter(x, y, s=10, c=ACOL[a], edgecolors="none", alpha=0.9, zorder=6)
ax.set_xlim(ext[0] + 0.9e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
fig.text(0.05, 0.80, "Where the", fontproperties=FELL, fontsize=44, color=INKC, va="center")
fig.text(0.05, 0.67, "wolves were", fontproperties=HAND, fontsize=50, color=RED, va="center")
fig.text(0.05, 0.50, f"{R['review']['places']} places in Britain and Ireland", fontproperties=FELL, fontsize=19, color=INKC)
fig.text(0.05, 0.44, "whose names keep an animal", fontproperties=FELL, fontsize=19, color=INKC)
fig.text(0.05, 0.33, f"{A['wolf']['places']} wolves, {A['crane']['places']} cranes, {A['eagle']['places']} eagles,", fontproperties=FELL, fontsize=16, color=MUT)
fig.text(0.05, 0.28, f"{A['boar']['places']} wild boar, {A['beaver']['places']} beavers", fontproperties=FELL, fontsize=16, color=MUT)
fig.text(0.05, 0.08, "Dr Tristan Hotham · maps.tristanhotham.com", fontproperties=FELL, fontsize=13, color=MUT)
fig.savefig(os.path.join(ROOT, "header.png"), dpi=100, facecolor=fig.get_facecolor())
plt.close(fig)
from PIL import Image
print(Image.open(OUT).size, Image.open(os.path.join(ROOT, "header.png")).size)
