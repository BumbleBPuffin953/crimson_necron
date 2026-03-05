import numpy as np

stats = np.array([[120,80],[152,100],[192,128],[240,160],[304,200]])
necron = np.array([176,132])
tiers = ['Base', 'Hot', 'Burning', 'Fiery', 'Infernal']

all_maps = {}

for tier_index in range(len(tiers)):
    max_stars = 15 if tier_index == len(tiers) - 1 else 10

    for stars in range(max_stars + 1):
        base_stats_crimson = stats[tier_index] * (1 + stars * 0.02)
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

        all_maps[(tier_index, stars)] = {
            "heatmap": heatmap_fraction,
            "cd_range": cd_range,
            "str_range": str_range
        }

np.savez("precomputed_heatmaps.npz", data=all_maps)