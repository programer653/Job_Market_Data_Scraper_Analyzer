import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from wordcloud import WordCloud
import operator
import numpy as np
from PIL import Image

def run_visualizer(job_title_filter, nb_skills):
    data = pd.read_csv(f'./data/skills_count_{job_title_filter}.csv') 
    df = pd.DataFrame(data)
    #sort skills by frequency
    df = df.sort_values(['count'], ascending=False)

    #df.sort_values(by="skill", ascending=False)

    df.to_csv(f'./data/skills_count_{job_title_filter}.csv', index=False)

    #print(df)

    #Plot top N skills as a bar chart

    df_first_20 = df.head(nb_skills)

    X = list(df_first_20.iloc[:, 0])
    Y = list(df_first_20.iloc[:, 1])

    plt.barh(X, Y, color='g')
    #plt.title("Skills researched")
    plt.xlabel("skills")
    plt.ylabel("count")

    plt.savefig(f"./charts/top_skills_for_{job_title_filter}.png")

    #tuples = [tuple(x) for x in df.values]
    #frequencies = dict(tuples)

    frequencies = dict(zip(df['skill'], df['count']))

    mask = np.array(Image.open("./assets/cloud.png"))  # <-- put a cloud silhouette in assets/

    wordcloud = WordCloud(
        width=800,
        height=600,
        background_color="white",
        mask=mask,
        contour_width=2,
        contour_color='steelblue',
        colormap="viridis"  # you can try "plasma", "cool", etc.
    ).generate_from_frequencies(frequencies)

    # Save wordcloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"./charts/skills_wordcloud_for_{job_title_filter}.png")
    plt.close()

run_visualizer("software engineer", 10)