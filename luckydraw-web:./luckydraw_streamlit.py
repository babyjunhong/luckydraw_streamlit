from __future__ import annotations
import random
from typing import List
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
def draw_prizes(quantity: int) -> List[str]:
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    rng = random.Random()
    return rng.choices(PRIZES, weights=DEFAULT_WEIGHTS, k=quantity)

# ----- Streamlit Interface -----
st.title("🎁 LUCKYDRAW")

# User input field
quantity = st.number_input("Quantity of prize:", min_value=1, max_value=40, value=1, step=1)

# GO! button
if st.button("GO!"):
    try:
        prizes = draw_prizes(quantity)
        st.success("🎉 Your randomized prizes:")
        # Show prizes in a box
        prize_text = "\n".join(f"{i+1}. {prize}" for i, prize in enumerate(prizes))
        st.text_area("Prizes", value=prize_text, height=200)
    except ValueError as e:
        st.error(f"Error: {e}")
