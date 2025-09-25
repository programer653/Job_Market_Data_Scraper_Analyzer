import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import csv
import scraper
import cleaner
import analyzer
import visualizer

#!/usr/bin/python

# Get theme colors from Streamlit config
primary = st.get_option("theme.primaryColor")
bg = st.get_option("theme.backgroundColor")
secondary_bg = st.get_option("theme.secondaryBackgroundColor")
text_color = st.get_option("theme.textColor")



def skills_graph(job_title_filter, nb_skills):
    df = pd.read_csv(f'./data/skills_count_{job_title_filter}.csv') 
    df = df.sort_values("count", ascending=False).head(nb_skills)

    #df_top = df.head(nb_skills)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(df["skill"], df["count"], color=primary)
    ax.set_xlabel("Count", color=text_color)
    ax.set_ylabel("Skill", color=text_color)
    ax.set_title(f"Top {nb_skills} Skills for {job_title_filter}")

    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.set_facecolor(bg)
    fig.patch.set_facecolor(bg)

    ax.invert_yaxis()

    fig_plot = st.pyplot(fig)
    #my_table = st.dataframe(df_top)

    

def wordcloud_graph(job_title_filter, nb_skills, use_mask):
    df = pd.read_csv(f'./data/skills_count_{job_title_filter}.csv') 
    frequencies = dict(zip(df["skill"], df["count"]))
    mask = np.array(Image.open("./assets/cloud.png")) if use_mask else None

    wordcloud = WordCloud(
        width=800,
        height=600,
        background_color=bg,
        max_words=nb_skills,
        #colormap=colormap,
        mask=mask,
        contour_width=2 if use_mask else 0,
        contour_color=primary if use_mask else None
    ).generate_from_frequencies(frequencies)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(bg)

    st.pyplot(fig)
    





#skills count
st.set_page_config(layout="wide")
job_title = st.sidebar.selectbox("Choose Job Role", ["All", "Data Scientist", "Software Engineer", "Web Developer", "Data Engineer"])
nb_skills = st.sidebar.selectbox("Choose number of skills to be displayed", [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

st.header("Job Market Skill Analyzer ")


st.write(f"📊 Top {nb_skills} Skills for {job_title or 'All Jobs'}")
if job_title == "Web Developer":
    job_title = "Web"
elif job_title == "All":
    job_title = " "


new_scrape = st.sidebar.button("Run New Scrape")
if new_scrape:
    scraper.run_scraper()
    cleaner.run_cleaner()
    analyzer.run_analyzer(job_title)
    #st.experimental_rerun()



data = pd.read_csv(f'./data/clean_jobs.csv') 
df = pd.DataFrame(data)
df_display = df[['job_title', 'company', 'link']]

keyword = st.sidebar.text_input("Search a skill or keyword")
data2 = pd.read_csv("./data/clean_jobs.csv") 
df2 = pd.DataFrame(data2)
filtered_df = df2[df2['description'].str.contains(keyword, case=False)]
df_display = filtered_df[['job_title', 'company', 'link']].head(10)

st.sidebar.download_button("Download Results", df_display.to_csv(index=False), file_name="skills.csv")


col1, col2 = st.columns([1,1])
with col1:
    st.header("")
    topskills_png = skills_graph(job_title, nb_skills)
with col2:
    st.header("")
    wordcloud_png = wordcloud_graph(job_title, nb_skills, False)
    #wordcloud_png = Image.open(f'./charts/skills_wordcloud_for_{job_title}.png')
    #st.image(wordcloud_png)
    st.write("Sample Job Postings")
    st.write(df_display)
    
    



