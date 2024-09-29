import streamlit as st


st.set_page_config(
    page_title ="Multipage App",
    

)
st.title("Skinteraction")
st.text("Take action against skin cancer")

st.header("What is Skin Cancer?")
st.markdown("Skin cancer is a type of cancer that begins in the cells of the skin. It occurs when the skin cells start to grow uncontrollably due to DNA damage, often caused by exposure to ultraviolet (UV) radiation from the sun or tanning beds. There are several types of skin cancer, but the most common ones are basal cell carcinoma (BCC), squamous cell carcinoma (SCC), and melanoma.")

st.header("What causes skin cancer?")
st.markdown("Skin cancer is caused primarily by ultraviolet (UV) radiation from the sun or tanning beds, which damages the DNA in skin cells. Key risk factors include:")
st.markdown("* **UV Exposure:** Sunlight and tanning beds.")
st.markdown("* **Fair Skin**: Less melanin means higher risk.")
st.markdown ("* **History of Sunburns**: Especially severe burns in youth.")
st.markdown("* **Family or Personal History**: A genetic predisposition or previous skin cancer.")
st.markdown("* **Weakened Immune System**: Conditions like HIV/AIDS or immunosuppressive medications.")
st.markdown("* **Toxic Exposure**: Arsenic and radiation.")
st.markdown("* **Age**: Risk increases with cumulative sun exposure.")
st.markdown("* **Moles**: Atypical or congenital moles may become cancerous.")

st.header("How does this affect people of color?")
st.markdown("Skin cancer disparities in people of color include:")
st.markdown("* **Delayed Diagnosis**: People of color are often diagnosed at later stages, leading to worse outcomes.")
st.markdown("* **Misdiagnosis**: Skin cancer can appear in less obvious areas, like the palms or soles, and may be harder to detect in darker skin tones.")
st.markdown("* **Lower Survival Rates**: Particularly for melanoma, due to late detection.")
st.markdown("* **Limited Access to Care**: Economic, geographic, and systemic barriers reduce access to screenings and treatment.")
st.markdown("* **Lack of Awareness**: Many believe darker skin is not at risk, leading to fewer preventive measures.")