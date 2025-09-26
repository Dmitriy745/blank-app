import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng




df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])
st.line_chart(df)



age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years old")


option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
    index=None,
    placeholder="Select contact method...",
)
st.write("You selected:", option)




