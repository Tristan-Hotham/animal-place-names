"""Step 5: figures for the page (img/*.jpg), the blog (release/blog/b_*.png, 1800 px), the paper (release/paper/f_*.png)."""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from PIL import Image
from figstyle import *

R = jload(f"{DATA}/results.json")
K = pd.read_csv(f"{DATA}/animal_names.csv", keep_default_na=False, low_memory=False)
K["elev"] = pd.to_numeric(K["elev"], errors="coerce")
H = K[K.is_head.astype(str) == "True"].copy()
BLOG, PAPERD = f"{ROOT}/release/blog", f"{ROOT}/release/paper"
for d in (BLOG, PAPERD):
    os.makedirs(d, exist_ok=True)
CRS = 27700
EXT = (-10.6, 1.9, 49.85, 59.0)          # Shetland goes in an inset where needed
LCOL = {"english": "#A3261B", "norse": "#C77A2A", "welsh": "#2F7F4A", "gaelic": "#3D6E9E", "irish": "#5C8F3A", "modern": "#6E604E"}


def out(fig, name, dpi=200):
    fig.savefig(f"{WORK}/{name}.png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    im = Image.open(f"{WORK}/{name}.png").convert("RGB")
    w = 1600; im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).save(f"{IMG}/{name}.jpg", quality=84, optimize=True)
    w = 1800; im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).save(f"{BLOG}/b_{name}.png", optimize=True)
    w = min(2000, im.size[0]); im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).save(f"{PAPERD}/f_{name}.png", optimize=True)
    os.remove(f"{WORK}/{name}.png")


def halo(t, w=3):
    import matplotlib.patheffects as pe
    t.set_path_effects([pe.withStroke(linewidth=w, foreground=PAPER)])
    return t


_base = {}


def basemap(ax, ext=EXT, ripple=(8e3, 20e3), lw=0.6):
    e, f = ink_base(ax, CRS, ext, ripple_m=ripple, coast_lw=lw, countries=False, min_area=2e7)
    return e, f


# ---------- 1. small multiples: eight animals
show = ["wolf", "beaver", "crane", "boar", "eagle", "raven", "deer", "wildcat"]
fig = plt.figure(figsize=(13, 9.4)); parchment(fig)
fig.text(0.03, 0.962, "Where the wolves were, and the rest of the lost menagerie", fontproperties=FELL, fontsize=23, color=INKC, va="center")
fig.text(0.03, 0.928, "Place and hill names with an animal in them, in English, Norse, Welsh, Gaelic or Irish. Large dots: etymology certain; small: probable.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
W, Hh = 0.235, 0.385
for k, a in enumerate(show):
    x0, y0 = 0.02 + (k % 4) * 0.243, 0.47 - (k // 4) * 0.44
    ax = fig.add_axes([x0, y0, W, Hh])
    ext, f = basemap(ax)
    h = H[H.animal == a]
    x, y = f(h.lon.values, h.lat.values)
    big = (h.certainty == "certain").values
    ax.scatter(x[~big], y[~big], s=9, c=ACOL[a], edgecolors="none", alpha=0.85, zorder=6)
    ax.scatter(x[big], y[big], s=34, c=ACOL[a], edgecolors=PAPER, linewidths=0.7, zorder=7)
    A = R["animals"][a]
    fig.text(x0 + 0.004, y0 + Hh + 0.008, ALAB[a], fontproperties=FELLSC, fontsize=17, color=RED, va="bottom")
    fig.text(x0 + W - 0.004, y0 + Hh + 0.01, f"{A['places']} places, {A['certain']} certain", fontproperties=FELL, fontsize=11, color=INKC, va="bottom", ha="right")
    ax.set_xlim(ext[0] + 1.5e5, ext[1]); ax.set_ylim(ext[2], ext[3] - 0.4e5)
fig.text(0.03, 0.012, "Names: OpenStreetMap (places, hills, woods, cliffs, springs, bays), matched against a curated list of animal words with false friends removed by hand. Shetland not shown.",
         fontproperties=FELL, fontsize=10, color=MUT)
out(fig, "animals")

# ---------- 2. the wolves, labelled
fig = plt.figure(figsize=(10, 12)); parchment(fig)
ax = fig.add_axes([0.0, 0.04, 1, 0.86])
ext, f = basemap(ax, ripple=(8e3, 20e3, 36e3), lw=0.8)
h = H[H.animal == "wolf"].copy()
x, y = f(h.lon.values, h.lat.values)
h["x"], h["y"] = x, y
for lay, mk in (("modern", "o"), ("english", "s"), ("norse", "s"), ("welsh", "D"), ("gaelic", "D"), ("irish", "D")):
    s = h[h.layer == lay]
    if len(s):
        ax.scatter(s.x, s.y, s=[90 if c == "certain" else 46 for c in s.certainty], marker=mk, c=LCOL[lay], edgecolors=INKC, linewidths=0.6, zorder=7)
LAB = {"Woolpit": (60, -25), "Ulpha": (-120, 10), "Woolley": (60, 10), "Wolfhole Crag": (-150, -5), "Wolf's Castle": (-110, -45), "Wolfelee": (30, 35),
       "Wolf Craig": (40, 10), "Wolfhill": (-110, 20), "Cwm Bleiddiaid": (-140, 18), "Wolf Stones": (55, -10), "Wolf Island": (-120, -20), "Wolfcleugh": (40, -30)}
done = set()
for _, r in h.iterrows():
    nm = r["name"]
    if nm in LAB and nm not in done and not (nm == "Woolley" and r.county != "West Yorkshire"):
        dx, dy = LAB[nm]
        t = ax.annotate(nm, (r.x, r.y), xytext=(r.x + dx * 400, r.y + dy * 400), fontproperties=FELLIT, fontsize=12.5, color=INKC, zorder=9,
                        arrowprops=dict(arrowstyle="-", lw=0.5, color=MUT), va="center")
        halo(t); done.add(nm)
ax.set_xlim(ext[0] + 1.0e5, ext[1]); ax.set_ylim(ext[2], ext[3])
fig.text(0.05, 0.955, "Where the wolves were", fontproperties=FELL, fontsize=27, color=INKC, va="center")
fig.text(0.05, 0.922, f"{R['animals']['wolf']['places']} places named for wolves: Old English wulf and Norse ulfr, Welsh blaidd, and the later\nEnglish and Scots wolf of the crags. Median ground height {R['elev_test']['wolf']['median']:.0f} m, against {R['elev_test']['wolf']['null_median']:.0f} m for names of the same kinds.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
lx = fig.add_axes([0.66, 0.56, 0.3, 0.16]); lx.axis("off")
items = [("s", LCOL["english"], "Old English or Norse (dictionary)"), ("D", LCOL["welsh"], "Welsh blaidd"), ("o", LCOL["modern"], "English or Scots 'wolf' (later)")]
for i, (mk, c, l) in enumerate(items):
    lx.scatter([0.05], [0.85 - i * 0.25], marker=mk, s=70, c=c, edgecolors=INKC, linewidths=0.6, transform=lx.transAxes)
    lx.text(0.13, 0.85 - i * 0.25, l, transform=lx.transAxes, fontproperties=FELL, fontsize=12, color=INKC, va="center")
lx.text(0.0, 1.08, "Language of the name", transform=lx.transAxes, fontproperties=FELLSC, fontsize=13, color=RED)
fig.text(0.05, 0.012, "Larger symbols: etymology certain. Names: OpenStreetMap. Shetland not shown (no wolf names).", fontproperties=FELL, fontsize=10, color=MUT)
out(fig, "wolves")

# ---------- 3. language layers by animal
order = [a for a in R["order_by_places"] if R["animals"][a]["places"] >= 3]
fig = plt.figure(figsize=(12, 7.6)); parchment(fig)
ax = fig.add_axes([0.16, 0.12, 0.8, 0.72])
left = np.zeros(len(order))
for L, lab in LAYERS:
    v = np.array([R["animals"][a]["layer_" + L] for a in order])
    ax.barh(range(len(order)), v, left=left, color=LCOL[L], edgecolor=INKC, lw=0.4, height=0.68, label=lab)
    left += v
for i, a in enumerate(order):
    ax.text(left[i] + 1.5, i, f"{R['animals'][a]['places']}", va="center", fontproperties=FELL, fontsize=11.5, color=INKC)
ax.set_yticks(range(len(order))); ax.set_yticklabels([ALAB[a] for a in order], fontproperties=FELL, fontsize=13)
ax.invert_yaxis()
ax.set_xlabel("Places (repeats of one name within 3 km counted once)", fontproperties=FELL, fontsize=12)
for s in ("top", "right"): ax.spines[s].set_visible(False)
leg = ax.legend(prop=FELL, fontsize=12, frameon=False, loc="lower right")
for t in leg.get_texts(): t.set_fontproperties(FELL); t.set_fontsize(12)
fig.text(0.03, 0.94, "Each animal's names, by the language they are in", fontproperties=FELL, fontsize=21, color=INKC, va="center")
fig.text(0.03, 0.902, "Eagles and boar live on mainly in Gaelic; deer, fox and raven in later English and Scots names of crags and hills.", fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
out(fig, "layers")

# ---------- 4. ground height by animal, against names of the same kinds
T = R["elev_test"]
order2 = sorted(T, key=lambda a: -T[a]["median"])
fig = plt.figure(figsize=(12, 7.4)); parchment(fig)
ax = fig.add_axes([0.14, 0.12, 0.82, 0.72])
rng = np.random.default_rng(2)
for i, a in enumerate(order2):
    h = H[(H.animal == a) & (H.nation != "Ireland")]
    yy = i + rng.uniform(-0.22, 0.22, len(h))
    ax.scatter(h.elev.clip(0, 1000), yy, s=10, c=ACOL[a], alpha=0.55, edgecolors="none", zorder=3)
    ax.plot([T[a]["median"]] * 2, [i - 0.34, i + 0.34], color=INKC, lw=2.6, zorder=5)
    ax.plot([T[a]["null_median"]] * 2, [i - 0.34, i + 0.34], color=RED, lw=1.6, ls=(0, (2, 1.4)), zorder=5)
ax.set_yticks(range(len(order2))); ax.set_yticklabels([ALAB[a] for a in order2], fontproperties=FELL, fontsize=13)
ax.invert_yaxis(); ax.set_xlim(-10, 1000)
ax.set_xlabel("Ground height of the named point (m, from 90 m terrain)", fontproperties=FELL, fontsize=12)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.plot([], [], color=INKC, lw=2.6, label="median of the animal's names")
ax.plot([], [], color=RED, lw=1.6, ls=(0, (2, 1.4)), label="median expected for names of the same kinds")
leg = ax.legend(frameon=False, loc="lower right")
for t in leg.get_texts(): t.set_fontproperties(FELL); t.set_fontsize(12)
fig.text(0.03, 0.94, "Wolf, boar and deer names stand high; otter names lie low", fontproperties=FELL, fontsize=21, color=INKC, va="center")
fig.text(0.03, 0.902, "Each dot is one place (UK). Expected: the median of random UK names of the same kinds (peak, village, locality...), 20,000 draws.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
out(fig, "height")

# ---------- 5. when they were lost
L = R["lost"]
fig = plt.figure(figsize=(12, 6.4)); parchment(fig)
ax = fig.add_axes([0.05, 0.16, 0.9, 0.62])
ax.set_xlim(700, 2060); ax.set_ylim(-0.5, len(L) - 0.3)
for yv in range(800, 2001, 200):
    ax.axvline(yv, color="#E2D3AE", lw=0.8, zorder=0)
ax.axvspan(450, 1066, color="#EFE1BC", zorder=0)
ax.text(760, len(L) - 0.55, "Old English\nnames formed", fontproperties=FELLIT, fontsize=11, color=MUT, va="top")
for i, r in enumerate(sorted(L, key=lambda r: r["year"])):
    c = ACOL.get(r["animal"], INKC) if r["animal"] in ACOL else "#7A6A52"
    ax.plot([r["year"], 2026], [i, i], color=c, lw=1.2, ls=(0, (1, 2)), zorder=2)
    ax.scatter([r["year"]], [i], s=90, c=c, edgecolors=INKC, zorder=4, marker="X" if r["animal"] in ("bear",) else "o")
    left_side = r["year"] > 1000
    t = ax.text(r["year"] + (-18 if left_side else 18), i + (0 if left_side else 0.32), f"{r['label']}: {r['when']}", ha="right" if left_side else "left", va="center", fontproperties=FELL, fontsize=12, color=INKC)
    halo(t)
    ax.text(2034, i, f"{r['places']}", va="center", fontproperties=FELL, fontsize=12, color=c if r["places"] else MUT)
ax.text(2034, len(L) - 0.4, "names\ntoday", fontproperties=FELLIT, fontsize=10.5, color=MUT, va="bottom")
ax.set_yticks([]); ax.set_xticks(range(800, 2001, 200)); ax.set_xticklabels([str(v) for v in range(800, 2001, 200)], fontproperties=FELL, fontsize=12)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
fig.text(0.03, 0.93, "The names outlived the animals", fontproperties=FELL, fontsize=22, color=INKC, va="center")
fig.text(0.03, 0.885, "When each animal was lost as a wild breeding animal, from the histories cited in the paper, and how many place names keep it.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
fig.text(0.03, 0.02, "Sources: Yalden (1999), Pluskowski (2006), Coles (2006), Boisseau and Yalden (1998), Hickey (2000), Love (1983). Bear: no reliable place names found.",
         fontproperties=FELL, fontsize=10, color=MUT)
out(fig, "lost")

# ---------- 6. eagles by language, and ravens
fig = plt.figure(figsize=(13, 9)); parchment(fig)
for k, a in enumerate(["eagle", "raven"]):
    ax = fig.add_axes([0.02 + k * 0.49, 0.04, 0.47, 0.82])
    ext, f = basemap(ax, lw=0.7)
    h = H[H.animal == a]
    for lay in ("modern", "english", "norse", "welsh", "irish", "gaelic"):
        s = h[h.layer == lay]
        if not len(s): continue
        x, y = f(s.lon.values, s.lat.values)
        ax.scatter(x, y, s=[60 if c == "certain" else 26 for c in s.certainty], c=LCOL[lay], edgecolors=INKC, linewidths=0.5, zorder=7,
                   label=f"{LLAB[lay]} ({len(s)})")
    ax.set_xlim(ext[0] + 1.3e5, ext[1]); ax.set_ylim(ext[2], ext[3] - 0.3e5)
    ax.text(0.03, 0.98, ALAB[a], transform=ax.transAxes, fontproperties=FELLSC, fontsize=20, color=RED, va="top")
    leg = ax.legend(loc="upper right", frameon=True, facecolor=PAPER, edgecolor=MUT, framealpha=0.95)
    for t in leg.get_texts(): t.set_fontproperties(FELL); t.set_fontsize(11.5)
fig.text(0.03, 0.955, "Two languages, two landscapes", fontproperties=FELL, fontsize=22, color=INKC, va="center")
fig.text(0.03, 0.918, f"Eagle names are {R['eagle']['celtic_pc']:.0f}% Gaelic, Welsh or Irish: Gaelic iolair on Highland crags, English earn in a few old English villages.",
         fontproperties=FELL, fontsize=12.5, color=MUT, va="center")
out(fig, "eagles")
print("figures done")
