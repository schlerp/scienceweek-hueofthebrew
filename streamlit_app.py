from PIL.Image import Image
import streamlit as st
from streamlit_gsheets import GSheetsConnection

import string

import pandas as pd
import plotly.express as px
import nltk

# Download the 'stopwords' corpus if it's not already present
nltk.data.find("corpora/stopwords")
from nltk.corpus import stopwords
from wordcloud import WordCloud


S1_COL_NAME = "How would you describe the first beer?"
S2_COL_NAME = "How would you describe the second beer?"

COMMON_WORDS = [
    "beer",
    "think",
    "thought",
    "like",
    "taste",
    "tasted",
    "flavour",
    "flavor",
    "flavours",
    "flavors",
    "hue",
    "colour",
    "color",
    "colourful",
    "colorful",
    "tasting",
    "little",
    "bit",
]


def load_data():
    """
    Load the experiment data from a CSV file.

    Returns:
        A DataFrame containing the experiment data.
    """
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=st.secrets["public_gsheets_url"])
    return df


def build_wordcloud(text: str) -> Image:
    # Sample text for the word cloud
    text.replace("\n", " ")
    text = text.strip()
    text = text.lower()
    text = "".join(char for char in text if char not in string.punctuation)
    stop_words = set(stopwords.words("english"))
    text = " ".join(
        w for w in text.split(" ") if w not in stop_words and w not in COMMON_WORDS
    )

    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white").generate(text)

    return wordcloud.to_image()


if __name__ == "__main__":
    # Set the page configuration
    st.set_page_config(
        page_title="Hue of the Brew",
        page_icon="🍻",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Add a custom CSS style to the app
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f0f2f5;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # print the title first
    st.title("🍻 :blue[Science Week 2025] - Hue of the Brew")

    # load the data
    df = load_data()
    if df.empty:
        st.error(
            "No data available! Has the audience responded yet? Or is patty shit at coding? 🫠"
        )
    else:
        st.table(df)

        # lets anylyse teh first sample
        st.header("The first sample...")
        st.text("This beer appeared darker in colour")
        s1_text = "\n".join(df[S1_COL_NAME].values)
        s1_wordcloud = build_wordcloud(s1_text)
        st.image(s1_wordcloud)

        # lets anylyse teh first sample
        st.header("The second sample...")
        st.text("This beer appeared lighter in colour")
        s2_text = "\n".join(df[S2_COL_NAME].values)
        s2_wordcloud = build_wordcloud(s1_text)
        st.image(s1_wordcloud)
