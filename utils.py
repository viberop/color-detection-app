import pandas as pd

def load_colors(csv_path='colors.csv'):
    return pd.read_csv(csv_path)

def get_closest_color_name(R, G, B, colors_df):
    minimum = float('inf')
    closest_color = None
    for _, row in colors_df.iterrows():
        d = abs(R - row["R"]) + abs(G - row["G"]) + abs(B - row["B"])
        if d < minimum:
            minimum = d
            closest_color = row["color_name"]
    return closest_color
