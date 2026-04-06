"""
Transsion Kenya Sentiment Report — Streamlit Viewer
=====================================================
Pulls the latest HTML report from GitHub Releases (or raw GitHub)
and renders it as a full-page iframe.

Deploy on Streamlit Cloud:
  1. Push this file + requirements.txt to a GitHub repo
  2. Go to share.streamlit.io → New app → point to app.py
  3. Set REPORT_URL in Streamlit Secrets (or .streamlit/secrets.toml)
"""

import streamlit as st
import requests
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Transsion Kenya — Market Sentiment Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Where to pull the report from ────────────────────────────────────────────
# Option A — GitHub raw file (simplest, public repo)
REPORT_URL = st.secrets.get(
    "REPORT_URL",
    "https://raw.githubusercontent.com/nderitumwangi/sentiment/master/reports/transsion_report_latest.html"
)

# Option B — GitHub Releases asset URL (better for large files / private)
# REPORT_URL = "https://github.com/YOUR_USERNAME/YOUR_REPO/releases/latest/download/transsion_report_latest.html"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/320px-Flag_of_Kenya.svg.png",
        width=120,
    )
    st.markdown("## 📊 Report Viewer")
    st.markdown("**Transsion Kenya**  \nMarket Sentiment Monitor")
    st.divider()

    # Manual refresh button
    if st.button("🔄 Refresh Report", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.caption(f"Last refreshed: {datetime.now().strftime('%d %b %Y %H:%M')}")
    st.divider()

    # Report source info
    st.markdown("**Report source**")
    st.code(REPORT_URL, language=None)

    st.markdown("**Pipeline**")
    st.markdown("""
- 🕷 GSMArena scraper (Kaggle)
- 🛒 Jumia price scraper (Kaggle)
- 🤖 Claude AI sentiment (Kaggle)
- 📄 HTML report → GitHub
- 🌐 This viewer (Streamlit)
    """)

# ── Fetch the HTML report ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600)  # cache for 1 hour, auto-refresh
def fetch_report(url: str) -> tuple[str, bool]:
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        return resp.text, True
    except Exception as e:
        return str(e), False


# ── Main content ──────────────────────────────────────────────────────────────
st.markdown(
    "<h2 style='margin:0 0 4px;'>Transsion Kenya Market Sentiment Report</h2>"
    "<p style='color:gray;margin:0;'>Powered by GSMArena · Jumia KE · Claude AI</p>",
    unsafe_allow_html=True,
)
st.divider()

html_content, success = fetch_report(REPORT_URL)

if not success:
    st.error(f"❌ Could not load report: {html_content}")
    st.info("Make sure REPORT_URL is set correctly in Streamlit Secrets.")
else:
    # Inject base target so links inside the report open in new tab
    html_content = html_content.replace(
        "<head>",
        "<head><base target='_blank'>",
        1,
    )

    # Render the full HTML report in an iframe
    st.components.v1.html(
        html_content,
        height=900,
        scrolling=True,
    )

    # Download button so users can save the report
    st.download_button(
        label="⬇ Download Report HTML",
        data=html_content,
        file_name=f"transsion_report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        use_container_width=False,
    )