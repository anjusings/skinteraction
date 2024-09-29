import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.title("Research")
st.markdown("Even though white people are diagnosed with melanoma at much higher rates than people of color, individuals from racial and ethnic minority groups often experience more severe outcomes. Studies show that people of color are more likely to be diagnosed at later stages of the disease, leading to higher rates of death and poorer prognosis. This disparity is often due to delayed detection, misdiagnosis, or lack of awareness about melanoma risk in non-white populations. While overall incidence rates are lower in people of color, the more advanced stage at diagnosis increases the likelihood of worse outcomes.")

st.title("Melanoma Incidence Rates by Race")

@st.cache_data
def get_data():
    df = pd.read_csv("../app_data/incidence.csv")
    df['Year'] = df['Year'].astype(str).str.replace(',', '')
    return df.set_index("Year")

try:
    df = get_data()
    available_races = list(df.columns)
    races = st.multiselect(
        "Choose race", available_races, default=available_races[:2]
    )
    if not races:
        st.error("Please select at least one race.")
    else:
        data = df[races]
        st.write("### Melanoma Incidence Rates per 100,000 People", data.sort_index())

        data = data.reset_index().melt(id_vars=["Year"], var_name="Race", value_name="Incidence Rate")
        chart = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="Year:T",
                y="Incidence Rate:Q",
                color="Race:N",
                tooltip=["Year:T", "Race:N", "Incidence Rate:Q"]
            )
            .interactive()
        )
        st.altair_chart(chart, use_container_width=True)


    st.markdown("* **Whites** have the highest and steadily increasing incidence rates.")
    st.markdown("* **Blacks** have the lowest and relatively stable rates.")
    st.markdown("* **Asian/Pacific Islanders** show stable rates with minor fluctuations.")
    st.markdown("* **American Indian/Alaska Natives** exhibit some variability but no significant trend changes.")
    st.markdown("* **Hispanics** show a gradual increase in incidence rates.")
except URLError as e:
    st.error(
        f"""
        **This demo requires internet access.**
        Connection error: {e.reason}
        """
    )

st.title("Melanoma Mortality Rates by Race")

@st.cache_data
def get_mortality_data():
    try:
        df = pd.read_csv("../app_data/mortality.csv")
        df['Year'] = df['Year'].astype(str).str.replace(',', '')
        return df.set_index("Year")
    except pd.errors.EmptyDataError:
        st.error("No columns to parse from file. Please check the CSV file.")
        return pd.DataFrame()

try:
    df = get_mortality_data()
    if df.empty:
        st.error("The data could not be loaded. Please check the CSV file.")
    else:
        available_races = list(df.columns)
        races = st.multiselect(
            "Choose race", available_races, default=available_races[:2], key="race_multiselect"
        )
        if not races:
            st.error("Please select at least one race.")
        else:
            data = df[races]
            st.write("### Melanoma Mortality Rates per 100,000 People", data.sort_index())

            data = data.reset_index().melt(id_vars=["Year"], var_name="Race", value_name="Mortality Rate")
            chart = (
                alt.Chart(data)
                .mark_line()
                .encode(
                    x="Year:T",
                    y="Mortality Rate:Q",
                    color="Race:N",
                    tooltip=["Year:T", "Race:N", "Mortality Rate:Q"]
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)


        st.markdown("* **Whites** have the highest mortality rates, with a slight increase over the years.")
        st.markdown("* **Blacks** have the lowest mortality rates, remaining relatively stable.")
        st.markdown("* **Asian/Pacific Islanders** show low and stable mortality rates with minor fluctuations.")
        st.markdown("* **American Indian/Alaska Natives** exhibit some variability but no significant trend changes.")
        st.markdown("* **Hispanics** show low mortality rates with a slight increase over the years.")
except URLError as e:
    st.error(
        f"""
        **This demo requires internet access.**
        Connection error: {e.reason}
        """
    )

st.markdown('<p style="font-size:12px;">The data is sourced by the National Cancer Institute through the SEER Program.</p>\n <a href="https://seer.cancer.gov/archive/csr/1975_2010/browse_csr.php?sectionSEL=16&pageSEL=sect_16_zfig.02" style="font-size:12px;" target="_blank">Melanoma Statistics Link</a>', unsafe_allow_html=True)
