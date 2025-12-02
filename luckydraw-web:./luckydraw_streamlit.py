from __future__ import annotations
import random
from collections import Counter
from typing import List, Optional
import streamlit as st

# ----- Prize Data -----
PRIZES: List[str] = [
    "photo frame",
    "slogan",
    "sticker set",
    "notebook",
    "pin button",
    "postcard",
]

DEFAULT_WEIGHTS: List[float] = [1.0, 3.0, 6.0, 10.0, 20.0, 30.0]

# ----- Weighted sampling without replacement -----
def weighted_sample_without_replacement(population: List[str], weights: List[float], k: int, rng: random.Random) -> List[str]:
    pop = population[:]
    w = weights[:]
    result: List[str] = []
    for _ in range(k):
        total = sum(w)
        if total <= 0:
            idx = rng.randrange(len(pop))
            result.append(pop.pop(idx))
            w.pop(idx)
            continue
        r = rng.random() * total
        cum = 0.0
        for i, wi in enumerate(w):
            cum += wi
            if r <= cum:
                result.append(pop.pop(i))
                w.pop(i)
                break
    return result

# ----- Prize Draw Function -----
def draw_prizes(quantity: int, unique: bool = False, seed: Optional[int] = None, tiered: bool = True, weights: Optional[List[float]] = None) -> List[str]:
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    rng = random.Random(seed)
    if weights is None:
        weights = DEFAULT_WEIGHTS

    if unique:
        if quantity > len(PRIZES):
            raise ValueError(f"quantity must be <= {len(PRIZES)} when drawing unique prizes")
        return weighted_sample_without_replacement(PRIZES, weights, quantity, rng) if tiered else rng.sample(PRIZES, k=quantity)
    else:
        if tiered:
            return rng.choices(PRIZES, weights=weights, k=quantity)
        else:
            return [rng.choice(PRIZES) for _ in range(quantity)]

# ----- Streamlit Interface -----
st.title("🎁 Lucky Draw Simulator")

# User input field
quantity = st.number_input("Quantity of prize:", min_value=1, max_value=10, value=1, step=1)

# Optional: Unique & Tiered toggles
unique = st.checkbox("Draw unique prizes (no duplicates)")
tiered = st.checkbox("Use tiered (weighted) draw", value=True)

# Seed input (optional)
seed_input = st.text_input("Optional seed for reproducible results", "")
seed = int(seed_input) if seed_input.isdigit() else None

# GO! button
if st.button("GO!"):
    try:
        prizes = draw_prizes(quantity, unique=unique, seed=seed, tiered=tiered)
        st.success("🎉 Your randomized prizes:")
        # Show prizes in a box
        prize_text = "\n".join(f"{i+1}. {prize}" for i, prize in enumerate(prizes))
        st.text_area("Prizes", value=prize_text, height=200)
    except ValueError as e:
        st.error(f"Error: {e}")