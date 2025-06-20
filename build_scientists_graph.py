#!/usr/bin/env python3
# chronological_scientists_graph.py
from pathlib import Path
import pandas as pd, numpy as np, networkx as nx
from pyvis.network import Network

# ---------- paths -----------------------------------------------------------
PORTRAIT_DIR   = Path("portraits")
FALLBACK_IMAGE = PORTRAIT_DIR / "Unknown_person.jpg"
NAMES_TXT      = Path("names.txt")
BIRTH_TXT      = Path("birth_years.txt")
ADJ_CSV        = Path("person_reference_matrix.csv")
HTML_OUT       = "index.html"

# ---------- load data -------------------------------------------------------
names  = [ln.strip() for ln in NAMES_TXT.open(encoding="utf-8") if ln.strip()]
births = [int(ln.strip()) for ln in BIRTH_TXT.open() if ln.strip()]
adj    = pd.read_csv(ADJ_CSV).values[:, 1:]

assert len(names) == len(births) == adj.shape[0] == adj.shape[1], "length mismatch"

# importance = number of inbound links
in_deg = adj.sum(axis=0)
lo, hi = 5, 100
scale  = lambda v: lo if in_deg.max()==in_deg.min() else lo+(hi-lo)*(v-in_deg.min())/(in_deg.max()-in_deg.min())

# chronological levels (older = smaller level number)
min_year = min(births)
levels   = [(by - min_year) / 10 for by in births]   # 1473 → 0, 1890 → 417, …

# ---------- build NetworkX --------------------------------------------------

def safe_filename(text: str) -> str:
    """Turn a slug or name into a filesystem-friendly filename."""
    keep = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    return "".join(c if c in keep else "_" for c in text)

G = nx.DiGraph()
for idx, (name, imp, lvl) in enumerate(zip(names, in_deg, levels)):
    slug = safe_filename(name)
    possible_exts = [".jpg", ".jpeg", ".JPG", ".png", ".PNG"]
    for ext in possible_exts:
        portrait = PORTRAIT_DIR / f"{slug}{ext}"
        if portrait.exists() and portrait.stat().st_size > 0:
            break
    else:                                   # no break -> no valid file found
        portrait = FALLBACK_IMAGE

    G.add_node(
        idx,
        label=name,
        title=f"{name}, Inbound links: {int(imp)}",
        shape="circularImage",
        image=str(portrait),
        value=scale(imp),
        level=lvl                     # ← key for hierarchical layout
    )

rows, cols = np.where(adj == 1)
for s, d in zip(rows, cols):
    G.add_edge(int(s), int(d), arrows="to", color="rgba(140,140,140,0.25)")

# ---------- visualise -------------------------------------------------------
net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")
net.from_nx(G)

# chronological top-→-down layout
# give vis.js a hierarchical layout block via set_options
net.set_options("""
{
  "layout": {
    "hierarchical": {
      "enabled": true,
      "direction": "UD",
      "sortMethod": "directed"
    }
  },
  "physics": {
    "solver": "hierarchicalRepulsion",
    "hierarchicalRepulsion": {
      "nodeDistance": 250,
      "springLength": 500
    }
  }
}
""")
net.show(HTML_OUT)
print(f"✓ graph written to {HTML_OUT}")

