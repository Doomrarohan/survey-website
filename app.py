import streamlit as st
import plotly.graph_objects as go
import json
from pathlib import Path

# ═══════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="Media Industry Report 2025",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PALETTE = [
    "#CC2936", "#1B4965", "#2D936C", "#E07A2F", "#7B2D8E",
    "#6B46C1", "#D4526E", "#13A8BE", "#547AA5", "#C4A77D",
]

# ═══════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700;800&display=swap');
#MainMenu {visibility:hidden} header {visibility:hidden} footer {visibility:hidden}
.block-container {padding-top:0!important;max-width:1060px}

.hero{background:#1a1a1a;padding:2.5rem 2rem 2rem;border-radius:0 0 16px 16px;margin:-1rem -1rem 1.5rem;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-50%;right:-15%;width:500px;height:500px;background:radial-gradient(circle,rgba(204,41,54,.15) 0%,transparent 70%);pointer-events:none}
.hero-eyebrow{display:inline-block;background:#CC2936;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:4px 12px;border-radius:3px;margin-bottom:.75rem;font-family:'DM Sans',sans-serif}
.hero-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.6rem,4vw,2.5rem);font-weight:800;color:#fff;line-height:1.15;margin-bottom:.5rem;letter-spacing:-.5px}
.hero-desc{color:rgba(255,255,255,.6);font-size:14px;max-width:620px;line-height:1.7;font-family:'DM Sans',sans-serif}
.hero-stats{display:flex;gap:2rem;margin-top:1.25rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,.1);flex-wrap:wrap}
.hero-stat-num{font-size:24px;font-weight:600;color:#fff;font-family:'DM Sans',sans-serif}
.hero-stat-label{font-size:11px;color:rgba(255,255,255,.45);margin-top:2px;font-family:'DM Sans',sans-serif}

.placeholder-card{border:1px dashed #ccc;border-radius:12px;padding:20px;background:#fafafa;margin-bottom:8px}
.placeholder-card .ph-hdr{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.placeholder-card .ph-icon{font-size:22px}
.placeholder-card .ph-name{font-size:16px;font-weight:600;color:#212121;font-family:'DM Sans',sans-serif}
.placeholder-card .ph-badge{font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;background:#FAEEDA;color:#854F0B;margin-left:auto}
.placeholder-card .ph-sum{font-size:13px;color:#717171;line-height:1.6;font-family:'DM Sans',sans-serif}

.block-card{border:1px solid #e8e8e8;border-radius:12px;padding:18px 20px;background:#fff;position:relative;height:100%}
.block-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.06)}
.block-bar{position:absolute;left:0;top:12px;bottom:12px;width:4px;border-radius:2px}
.block-heading{font-size:16px;font-weight:600;color:#212121;margin-bottom:2px;font-family:'DM Sans',sans-serif;padding-left:10px}
.block-subtitle{font-size:12px;color:#717171;margin-bottom:12px;line-height:1.5;font-family:'DM Sans',sans-serif;padding-left:10px}

.chart-note{font-size:11px;color:#717171;background:#f5f5f5;border-radius:6px;padding:8px 12px;margin-top:6px;line-height:1.5;font-family:'DM Sans',sans-serif}

.section-label{font-size:12px;font-weight:600;color:#717171;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;font-family:'DM Sans',sans-serif}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════
@st.cache_data
def load_data():
    p = Path(__file__).parent / "survey_data.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

DATA = load_data()
verticals = DATA["verticals"]

# ═══════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════
live_v = [v for v in verticals if v.get("status") == "live"]
total_blocks = sum(len(v.get("blocks", [])) for v in live_v)
total_resp = sum(v.get("respondents", 0) or 0 for v in live_v)

st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Media Report 2025</div>
    <div class="hero-title">{DATA['title']}</div>
    <div class="hero-desc">{DATA['description']}</div>
    <div class="hero-stats">
        <div><div class="hero-stat-num">{len(verticals)}</div><div class="hero-stat-label">Media verticals</div></div>
        <div><div class="hero-stat-num">{len(live_v)}</div><div class="hero-stat-label">Live datasets</div></div>
        <div><div class="hero-stat-num">{total_blocks}</div><div class="hero-stat-label">Survey sections</div></div>
        <div><div class="hero-stat-num">{total_resp:,}</div><div class="hero-stat-label">Respondents</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# CHART BUILDER
# ═══════════════════════════════════════════
def build_chart(ch, height=350):
    is_horiz = "horizontal" in ch.get("type", "")
    fig = go.Figure()
    for i, ds in enumerate(ch["datasets"]):
        color = ds.get("color", PALETTE[i % len(PALETTE)])
        kw = dict(
            name=ds["label"],
            marker_color=color,
            marker_line_color="white",
            marker_line_width=0.5,
            text=[f"{v}%" if v > 0 else "" for v in ds["data"]],
            textposition="inside",
            textfont=dict(size=9, color="white", family="DM Sans"),
        )
        if is_horiz:
            fig.add_trace(go.Bar(y=ch["labels"], x=ds["data"], orientation="h", **kw))
        else:
            fig.add_trace(go.Bar(x=ch["labels"], y=ds["data"], **kw))

    fig.update_layout(
        barmode="stack", height=height,
        margin=dict(l=5, r=5, t=5, b=5),
        font=dict(family="DM Sans", size=11, color="#4a4a4a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=10)),
        plot_bgcolor="white", paper_bgcolor="white",
        bargap=0.25, bargroupgap=0.1,
    )
    tick_s = dict(gridwidth=0.5, tickfont=dict(size=10, color="#717171", family="DM Sans"))
    if is_horiz:
        fig.update_xaxes(gridcolor="#f0f0f0", **tick_s)
        fig.update_yaxes(autorange="reversed", gridcolor="white", **tick_s)
    else:
        fig.update_xaxes(gridcolor="white", **tick_s)
        fig.update_yaxes(gridcolor="#f0f0f0", **tick_s)
    return fig


# ═══════════════════════════════════════════
# RENDER VERTICALS
# ═══════════════════════════════════════════
for vi, vert in enumerate(verticals):
    is_live = vert.get("status") == "live"
    color = vert.get("color", "#666")

    if not is_live:
        # Placeholder card — not expandable
        st.markdown(f"""
        <div class="placeholder-card">
            <div class="ph-hdr">
                <span class="ph-icon">{vert['icon']}</span>
                <span class="ph-name">{vert['name']}</span>
                <span class="ph-badge">Coming soon</span>
            </div>
            <div class="ph-sum">{vert['summary']}</div>
        </div>
        """, unsafe_allow_html=True)
        continue

    # Live vertical — expandable
    blocks = vert.get("blocks", [])
    block_count = len(blocks)

    with st.expander(
        f"{vert['icon']}  {vert['name']}  —  {vert.get('respondents','—')} respondents  ·  {block_count} sections",
        expanded=(vi == 0),
    ):
        st.markdown(
            f'<div style="font-size:13px;color:#717171;margin-bottom:20px;line-height:1.6;'
            f'font-family:DM Sans,sans-serif;">{vert["summary"]}</div>',
            unsafe_allow_html=True,
        )

        # Render blocks 2 per row
        for bi in range(0, len(blocks), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = bi + j
                if idx >= len(blocks):
                    break
                block = blocks[idx]
                with col:
                    # Block card header
                    st.markdown(
                        f'<div class="block-card">'
                        f'<div class="block-bar" style="background:{color}"></div>'
                        f'<div class="block-heading">{block["heading"]}</div>'
                        f'<div class="block-subtitle">{block["subtitle"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    # Dropdown filter for this block
                    views = block.get("chart_views", {})
                    view_names = list(views.keys())

                    if len(view_names) > 1:
                        selected_view = st.selectbox(
                            "Split by",
                            view_names,
                            key=f"sel_{vert['id']}_{block['id']}",
                            label_visibility="collapsed",
                        )
                    else:
                        selected_view = view_names[0] if view_names else None

                    if selected_view and selected_view in views:
                        ch = views[selected_view]
                        is_horiz = "horizontal" in ch.get("type", "")
                        h = 45 + len(ch["labels"]) * 32 if is_horiz else 300
                        h = max(h, 260)
                        h = min(h, 420)

                        fig = build_chart(ch, height=h)
                        st.plotly_chart(
                            fig, use_container_width=True,
                            config={"displayModeBar": False},
                            key=f"chart_{vert['id']}_{block['id']}_{selected_view}",
                        )

                        if ch.get("note"):
                            st.markdown(
                                f'<div class="chart-note">{ch["note"]}</div>',
                                unsafe_allow_html=True,
                            )

        st.markdown("")  # spacing


# ═══════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:12px;color:#999;padding:.5rem 0;font-family:DM Sans,sans-serif;">'
    'Media Industry Report 2025 — Edit <code>survey_data.json</code> to update. '
    'Push to GitHub to redeploy.</div>',
    unsafe_allow_html=True,
)
