"""Streamlit entrypoint for {{ project_name }}."""

from __future__ import annotations

import streamlit as st

from {{ package_name }}.data import sample_metrics

st.set_page_config(page_title="{{ project_name }}", page_icon="📊")
st.title("{{ project_name }}")
st.write("{{ description }}")

metrics = sample_metrics()
for label, value in metrics.items():
    st.metric(label, value)
