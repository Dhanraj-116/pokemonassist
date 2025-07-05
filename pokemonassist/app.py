import streamlit as st
import pandas as pd
import os
import ast  # to safely convert string lists to Python lists

st.set_page_config(page_title="Pokémon Data Explorer", layout="centered")

@st.cache_data
def load_data():
    file_path = os.path.join("dataset", "Pokemon_data.csv")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # Safely parse stringified lists in 'types' column
    if df['types'].dtype == object:
        df['types'] = df['types'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [x])
    return df

# Load dataset
try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 'Pokemon_data.csv' not found in the 'dataset' folder.")
    st.stop()

st.title("🧬 Pokémon Data Explorer")

# Show all columns
st.sidebar.markdown("### Dataset Columns:")
st.sidebar.write(df.columns.tolist())

# Show raw data
if st.checkbox("Show Full Dataset"):
    st.dataframe(df)

# Search by Pokémon name
name_search = st.text_input("🔍 Search Pokémon by name")
if name_search:
    results = df[df['name'].str.contains(name_search, case=False, na=False)]
    st.write(f"Found {len(results)} Pokémon:")
    st.dataframe(results)

# Extract all unique types
all_types = sorted({t for types_list in df['types'] for t in types_list})
selected_type = st.selectbox("🌀 Filter by Type", ["All"] + all_types)

if selected_type != "All":
    filtered = df[df['types'].apply(lambda lst: selected_type in lst)]
    st.write(f"Showing {len(filtered)} Pokémon of Type: {selected_type}")
    st.dataframe(filtered)

# Summary stats
if st.checkbox("📊 Show Summary Statistics"):
    st.write(df.describe())
