import os
import difflib
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Set page title and layout
st.set_page_config(page_title="Competitor Tracker UI", page_icon="🔍", layout="wide")

st.title("🔍 Competitor Page Tracker Dashboard")
st.markdown("Monitor rival websites for changes in copy, pricing, or strategic positioning.")

# Ensure directory exists for snapshots
STORAGE_DIR = "snapshots"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# Helper function to clean raw HTML
def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style', 'iframe', 'noscript', 'svg']):
        element.decompose()
    text = soup.get_text()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

# Sidebar for controls
st.sidebar.header("Add Competitor")
comp_name = st.sidebar.text_input("Competitor Name", placeholder="e.g. Stripe")
comp_url = st.sidebar.text_input("Page URL", placeholder="https://example.com/pricing")
comp_id = st.sidebar.text_input("Tracker ID", placeholder="e.g. stripe-pricing")

if st.sidebar.button("Run Tracker"):
    if not comp_url or not comp_id:
        st.sidebar.error("Please provide both a URL and a Tracker ID.")
    else:
        st.info(f"Fetching latest data from: {comp_url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        try:
            response = requests.get(comp_url, headers=headers, timeout=10)
            current_text = sanitize_html(response.text)
            snapshot_file = os.path.join(STORAGE_DIR, f"{comp_id}.txt")

            if not os.path.exists(snapshot_file):
                with open(snapshot_file, 'w', encoding='utf-8') as f:
                    f.write(current_text)
                st.success(f"Baseline snapshot saved for **{comp_name or comp_id}**. Run again later to detect changes.")
            else:
                with open(snapshot_file, 'r', encoding='utf-8') as f:
                    previous_text = f.read()

                prev_lines = previous_text.splitlines()
                curr_lines = current_text.splitlines()
                diff = list(difflib.unified_diff(prev_lines, curr_lines, lineterm=''))

                if not diff:
                    st.success("No changes detected since last check.")
                else:
                    st.warning(f"Changes detected for {comp_name or comp_id}!")
                    
                    added = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
                    removed = [line[1:] for line in diff if line.startswith('-') and not line.startswith('---')]

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("🟢 Added Content")
                        st.code("\n".join(added) if added else "None")
                    with col2:
                        st.subheader("🔴 Removed Content")
                        st.code("\n".join(removed) if removed else "None")

                    # Update snapshot baseline
                    with open(snapshot_file, 'w', encoding='utf-8') as f:
                        f.write(current_text)
                    st.info("Snapshot baseline updated to latest version.")

        except Exception as e:
            st.error(f"Error fetching URL: {e}")

st.markdown("---")
st.subheader("Stored Baselines")
snapshots = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.txt')]
if snapshots:
    st.write(f"Active tracked pages: `{', '.join(snapshots)}`")
else:
    st.write("No saved page baselines found.")
import os
import difflib
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Set page title and layout
st.set_page_config(page_title="Competitor Tracker UI", page_icon="🔍", layout="wide")

st.title("🔍 Competitor Page Tracker Dashboard")
st.markdown("Monitor rival websites for changes in copy, pricing, or strategic positioning.")

# Ensure directory exists for snapshots
STORAGE_DIR = "snapshots"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# Helper function to clean raw HTML
def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style', 'iframe', 'noscript', 'svg']):
        element.decompose()
    text = soup.get_text()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

# Sidebar for controls
st.sidebar.header("Add Competitor")
comp_name = st.sidebar.text_input("Competitor Name", placeholder="e.g. Stripe")
comp_url = st.sidebar.text_input("Page URL", placeholder="https://example.com/pricing")
comp_id = st.sidebar.text_input("Tracker ID", placeholder="e.g. stripe-pricing")

if st.sidebar.button("Run Tracker"):
    if not comp_url or not comp_id:
        st.sidebar.error("Please provide both a URL and a Tracker ID.")
    else:
        st.info(f"Fetching latest data from: {comp_url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        try:
            response = requests.get(comp_url, headers=headers, timeout=10)
            current_text = sanitize_html(response.text)
            snapshot_file = os.path.join(STORAGE_DIR, f"{comp_id}.txt")

            if not os.path.exists(snapshot_file):
                with open(snapshot_file, 'w', encoding='utf-8') as f:
                    f.write(current_text)
                st.success(f"Baseline snapshot saved for **{comp_name or comp_id}**. Run again later to detect changes.")
            else:
                with open(snapshot_file, 'r', encoding='utf-8') as f:
                    previous_text = f.read()

                prev_lines = previous_text.splitlines()
                curr_lines = current_text.splitlines()
                diff = list(difflib.unified_diff(prev_lines, curr_lines, lineterm=''))

                if not diff:
                    st.success("No changes detected since last check.")
                else:
                    st.warning(f"Changes detected for {comp_name or comp_id}!")
                    
                    added = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
                    removed = [line[1:] for line in diff if line.startswith('-') and not line.startswith('---')]

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("🟢 Added Content")
                        st.code("\n".join(added) if added else "None")
                    with col2:
                        st.subheader("🔴 Removed Content")
                        st.code("\n".join(removed) if removed else "None")

                    # Update snapshot baseline
                    with open(snapshot_file, 'w', encoding='utf-8') as f:
                        f.write(current_text)
                    st.info("Snapshot baseline updated to latest version.")

        except Exception as e:
            st.error(f"Error fetching URL: {e}")

st.markdown("---")
st.subheader("Stored Baselines")
snapshots = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.txt')]
if snapshots:
    st.write(f"Active tracked pages: `{', '.join(snapshots)}`")
else:
    st.write("No saved page baselines found.")
