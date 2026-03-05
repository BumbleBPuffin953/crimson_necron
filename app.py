import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

st.title("Crimson vs Necron Heatmap")

tiers = ['Base', 'Hot', 'Burning', 'Fiery', 'Infernal']
tier = st.selectbox("Select Armor Tier", options=range(len(tiers)), format_func=lambda x: tiers[x])
if tier == len(tiers) - 1:
    max_stars = 15
else:
    max_stars = 10
stars = st.slider("Stars", 0, max_stars, 0)

@st.cache_data
def load_data():
    data = np.load("precomputed_heatmaps.npz", allow_pickle=True)
    return data["data"].item()

all_heatmaps = load_data()

heatmap_fraction, cd_range, str_range = all_heatmaps[(tier, stars)]

fig, ax = plt.subplots(figsize=(10,8))
cmap = plt.cm.viridis.copy()
cmap.set_under('black') 

im = ax.imshow(
    heatmap_fraction.T,
    origin='lower',
    extent=[cd_range[0], cd_range[-1], str_range[0], str_range[-1]],
    aspect='auto',
    cmap=cmap,
    norm=colors.Normalize(vmin=0.0001, vmax=heatmap_fraction.max())
)
ax.set_xlabel('cd')
ax.set_ylabel('str')
fig.colorbar(im, ax=ax, label='Fraction of positive points')

st.pyplot(fig)