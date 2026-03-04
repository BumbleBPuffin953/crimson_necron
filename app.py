import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

st.title("Crimson vs Necron Heatmap")

stats = np.array([[120,80],[152,100],[192,128],[240,160],[304,200]])
necron = np.array([176,132])
tiers = ['Base', 'Hot', 'Burning', 'Fiery', 'Infernal']

def get_bonus(tier_index, stars):
    return stats[tier_index] * (1 + stars * 0.02)

tier = st.selectbox("Select Armor Tier", options=range(len(tiers)), format_func=lambda x: tiers[x])
if tier == len(tiers) - 1:
    max_stars = 15
else:
    max_stars = 10
stars = st.slider("Stars", 0, max_stars, 0)

base_stats_crimson = get_bonus(tier, stars)
s_diff, c_diff = necron - base_stats_crimson

cd_range = np.arange(base_stats_crimson[0], 1510, 10) 
str_range = np.arange(base_stats_crimson[1], 1510, 10)
add_range = np.arange(1.88, 10.04, 0.04)

cd_b = cd_range[:, None, None]
str_b = str_range[None, :, None] 
add_b = add_range[None, None, :]    

res = (1 + (str_b + s_diff)/100) * (1 + (cd_b + c_diff)/100) - \
      (1 + str_b/100) * (1 + cd_b/100) * (1 + 1.5/add_b)

positive_mask = res > 0  
positive_counts = positive_mask.sum(axis=2) 
heatmap_fraction = positive_counts / len(add_range)

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