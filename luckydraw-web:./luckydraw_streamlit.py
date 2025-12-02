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

# Custom CSS for fonts, button, and cards
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');

.title {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 0;
}
.sub-title {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 32px;
    color: #555555;
    margin-top: 0;
    margin-bottom: 20px;
}
.stButton>button {
    width: 100% !important;
    background-color: #FFC0CB;
    color: black;
    height: 40px;
    font-size: 16px;
}
.prize-card {
    display: inline-block;
    width: 80px;
    height: 80px;
    border-radius: 10px;
    background-color: #FFDEE9;
    margin: 5px;
    text-align: center;
    line-height: 80px;
    font-weight: bold;
    font-family: 'Roboto Condensed', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Titles
st.markdown('<div class="title">🎁 LUCKYDRAW</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🎁 럭키드로우</div>', unsafe_allow_html=True)

# User input field
quantity = st.number_input("Quantity of prize:", min_value=1, max_value=40, value=1, step=1)

# GO! button
if st.button("GO!"):
    try:
        prizes = draw_prizes(quantity)
        st.success("🎉 Your randomized prizes:")

        # Display prizes as cards
        prize_cards_html = ''.join([f'<div class="prize-card">{prize}</div>' for prize in prizes])
        st.markdown(f'<div>{prize_cards_html}</div>', unsafe_allow_html=True)

    except ValueError as e:
        st.error(f"Error: {e}")
