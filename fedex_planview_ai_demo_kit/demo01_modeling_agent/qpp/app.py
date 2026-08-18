import json
from pathlib import Path
import streamlit as st
from agents import run_modeling_workflow

st.set_page_config(page_title='Planview Logbook Modeling Agent', layout='wide')
st.title('Planview Logbook Modeling Agent — GCP Demo')
st.caption('Synthetic data only. Demonstrates art-of-the-possible for agentic AI on a future-state GCP data platform.')

sample_path = Path(__file__).resolve().parents[2] / 'common' / 'data' / 'raw_logbook_sample.json'
default_sample = sample_path.read_text() if sample_path.exists() else '[]'

with st.sidebar:
    st.header('Demo Controls')
    st.write('Set `OFFLINE_MODE=false` and configure PROJECT_ID/REGION to use Vertex AI Gemini.')
    run_btn = st.button('Run modeling workflow', type='primary')

sample = st.text_area('Raw Planview-like Logbook JSON sample', default_sample, height=220)

if run_btn:
    source, model, quality, review = run_modeling_workflow(sample)
    tabs = st.tabs(['1. Source Analysis', '2. Model Recommendation', '3. Quality Rules', '4. Architecture Review'])
    with tabs[0]: st.markdown(source)
    with tabs[1]: st.markdown(model)
    with tabs[2]: st.markdown(quality)
    with tabs[3]: st.markdown(review)
else:
    st.info('Click **Run modeling workflow** to generate the demo outputs.')
