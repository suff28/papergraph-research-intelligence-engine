import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8030")

st.set_page_config(page_title="PaperGraph", layout="wide")
st.title("PaperGraph: Research Paper Intelligence Engine")


def get(path):
    response = requests.get(f"{API_BASE_URL}{path}", timeout=10)
    response.raise_for_status()
    return response.json()


def post(path):
    response = requests.post(f"{API_BASE_URL}{path}", timeout=30)
    response.raise_for_status()
    return response.json()


if st.button("Ingest Sample Research Corpus", use_container_width=True):
    st.session_state["ingest"] = post("/ingest/sample")

if "ingest" in st.session_state:
    st.caption(st.session_state["ingest"])

metrics = get("/metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Papers", metrics["papers"])
c2.metric("Extracted Entities", metrics["entities"])
c3.metric("Graph Edges", metrics["edges"])
c4.metric("Methods", metrics["methods"])

query = st.text_input("Search papers, methods, datasets, or tasks", value="lung segmentation")
if query:
    results = pd.DataFrame(get(f"/search?q={query}"))
    st.subheader("Search Results")
    st.dataframe(results, use_container_width=True, hide_index=True)

papers = pd.DataFrame(get("/papers"))
if not papers.empty:
    st.subheader("Research Corpus")
    st.dataframe(papers, use_container_width=True, hide_index=True)
    task_counts = papers.groupby("task", as_index=False).size()
    fig = px.bar(task_counts, x="task", y="size", title="Papers by Task")
    st.plotly_chart(fig, use_container_width=True)

leaderboard = pd.DataFrame(get("/leaderboard"))
if not leaderboard.empty:
    st.subheader("Metric Leaderboard")
    st.dataframe(leaderboard, use_container_width=True, hide_index=True)

graph = get("/graph")
edges = pd.DataFrame(graph["edges"])
if not edges.empty:
    st.subheader("Paper Relationship Graph Edges")
    st.dataframe(edges, use_container_width=True, hide_index=True)
