import streamlit as st
import base64
from cogniflow_utils import cogniflow_request

st.set_page_config(
    page_title="Cogniflow Text Classification",
    page_icon="https://uploads-ssl.webflow.com/60510407e7726b268293da1c/60ca08f7a2abc9c7c79c4dac_logo_ico256x256.png",
)

def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

st.title('Text Classification')
st.markdown("Powered by [Cogniflow](https://www.cogniflow.ai)")

model = st.secrets["model_url"]
api_key = st.secrets["api_key"]

if not "text/classification/predict/" in model:
    st.error("Error validating model url. Please make sure you are using a text classification model")
    st.stop()

inputtext = st.text_input("input text here")

st.session_state['enableBtn'] = not (inputtext is not None and model != "" and api_key != "")

click = st.button("✨ Get prediction from AI", disabled=st.session_state.enableBtn)

if click:
    if inputtext is not None and model != "" and api_key != "":
        with st.spinner("Predicting..."):
            result = cogniflow_request(model, api_key, inputtext)

        score_str = "Between 0 and 1, the higher the better"

        col1, col2 = st.columns(2, gap="large")

        col1.write("Text:")
        col1.write(inputtext)

        col2.write("Prediction:")
        col2.metric(label="Result", value=result['result'])
        col2.metric(label="Score", value=result['confidence_score'], help=score_str)

        st.balloons()                
    else:
        st.warning("fill every input")

