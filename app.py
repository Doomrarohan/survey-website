import streamlit as st
import plotly.graph_objects as go
import json
from pathlib import Path

st.set_page_config(page_title="Media Industry Report 2025", page_icon="🎬", layout="wide", initial_sidebar_state="collapsed")

PALETTE = ["#CC2936","#1B4965","#2D936C","#E07A2F","#7B2D8E","#6B46C1","#D4526E","#13A8BE","#547AA5","#C4A77D"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700;800&display=swap');
#MainMenu{visibility:hidden}header{visibility:hidden}footer{visibility:hidden}
.block-container{padding-top:0!important;max-width:1060px}

.bain-nav{background:#1a1a1a;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;border-radius:0 0 12px 12px;margin:-1rem -1rem 0 -1rem}
.bain-logo{display:flex;align-items:center;gap:10px}
.bain-logo-mark{width:30px;height:30px;background:#CC2936;border-radius:5px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:600;font-size:15px;font-family:'DM Sans',sans-serif}
.bain-logo-text{color:#fff;font-size:15px;font-weight:500;font-family:'DM Sans',sans-serif}
.bain-logo-text span{color:rgba(255,255,255,.4);font-weight:400;font-size:12px;margin-left:6px}
.bain-auth{font-size:11px;color:rgba(255,255,255,.4);display:flex;align-items:center;gap:5px;font-family:'DM Sans',sans-serif}
.bain-auth-dot{width:6px;height:6px;border-radius:50%;background:#a6e3a1}

.hero{background:#1a1a1a;padding:20px 20px 18px;position:relative;overflow:hidden;margin:0 -1rem 1rem}
.hero::before{content:'';position:absolute;top:-60%;right:-20%;width:500px;height:500px;background:radial-gradient(circle,rgba(204,41,54,.1) 0%,transparent 70%);pointer-events:none}
.hero-ey{display:inline-block;background:#CC2936;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;padding:4px 12px;border-radius:3px;margin-bottom:8px;font-family:'DM Sans',sans-serif}
.hero-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:800;color:#fff;line-height:1.15;margin-bottom:5px;letter-spacing:-.5px}
.hero-desc{color:rgba(255,255,255,.5);font-size:13px;line-height:1.6;max-width:560px;font-family:'DM Sans',sans-serif}

.exec-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#999;margin-bottom:10px;font-family:'DM Sans',sans-serif}
.kpi-card{background:#f5f5f5;border-radius:10px;padding:14px 16px;text-align:center}
.kpi-num{font-size:22px;font-weight:600;color:#212121;font-family:'DM Sans',sans-serif}
.kpi-label{font-size:11px;color:#717171;text-transform:uppercase;letter-spacing:.5px;margin-top:2px;font-family:'DM Sans',sans-serif}

.insight-card{border-left:3px solid #CC2936;padding:8px 12px;background:#f9f9f9;border-radius:0 8px 8px 0;font-size:12px;color:#212121;line-height:1.5;font-family:'DM Sans',sans-serif}

.block-card{border:1px solid #e8e8e8;border-radius:12px;padding:16px 18px;background:#fff;position:relative}
.block-card:hover{box-shadow:0 3px 12px rgba(0,0,0,.05)}
.block-bar{position:absolute;left:0;top:16px;bottom:16px;width:4px;border-radius:2px}
.block-heading{font-size:15px;font-weight:600;color:#212121;padding-left:10px;margin-bottom:2px;font-family:'DM Sans',sans-serif}
.block-subtitle{font-size:12px;color:#717171;padding-left:10px;margin-bottom:2px;line-height:1.4;font-family:'DM Sans',sans-serif}
.block-question{font-size:11px;color:#999;padding-left:10px;margin-bottom:10px;font-style:italic;line-height:1.4;font-family:'DM Sans',sans-serif}
.block-takeaway{font-size:12px;font-weight:500;color:#CC2936;margin-top:8px;padding-left:10px;font-family:'DM Sans',sans-serif}

.chart-note{font-size:11px;color:#717171;background:#f5f5f5;border-radius:6px;padding:7px 10px;margin-top:4px;line-height:1.5;font-family:'DM Sans',sans-serif}

.ph-card{border:1px dashed #ccc;border-radius:12px;padding:16px 18px;background:#fafafa;margin-bottom:8px}
.ph-hdr{display:flex;align-items:center;gap:10px;margin-bottom:4px}
.ph-icon{font-size:20px}
.ph-name{font-size:15px;font-weight:600;color:#212121;font-family:'DM Sans',sans-serif}
.ph-badge{font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;background:#FAEEDA;color:#854F0B;margin-left:auto;font-family:'DM Sans',sans-serif}
.ph-sum{font-size:12px;color:#717171;line-height:1.6;font-family:'DM Sans',sans-serif}

.pw-box{max-width:400px;margin:120px auto;text-align:center}
.pw-logo{width:50px;height:50px;background:#CC2936;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:24px;font-family:'DM Sans',sans-serif;margin:0 auto 16px}
.pw-title{font-family:'Playfair Display',Georgia,serif;font-size:22px;font-weight:700;color:#212121;margin-bottom:4px}
.pw-sub{font-size:13px;color:#717171;margin-bottom:20px;font-family:'DM Sans',sans-serif}
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    p = Path(__file__).parent / "survey_data.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

DATA = load_data()

# ══════════════════════════════════════════
# PASSWORD GATE
# ══════════════════════════════════════════
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div class="pw-box">
        <div class="pw-logo">B</div>
        <div class="pw-title">Media Industry Report 2025</div>
        <div class="pw-sub">This report is confidential. Enter the access code to continue.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Access code", type="password", key="pw_input", label_visibility="collapsed", placeholder="Enter access code...")
        if st.button("Enter", use_container_width=True, type="primary"):
            if pwd == DATA.get("password", "bain2025"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect access code. Please try again.")
    return False

if not check_password():
    st.stop()

# ── DATA ──
verticals = DATA["verticals"]
live_v = [v for v in verticals if v.get("status") == "live"]
total_blocks = sum(len(v.get("blocks", [])) for v in live_v)

# ══════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════
st.markdown("""
<div class="bain-nav">
    <div class="bain-logo">
        <div class="bain-logo-mark">B</div>
        <div class="bain-logo-text">Bain & Company<span>Media Report</span></div>
    </div>
    <div class="bain-auth"><div class="bain-auth-dot"></div>Authenticated</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HERO
# ══════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-ey">Gamer Survey 2025</div>
    <div class="hero-title">{DATA['title']}</div>
    <div class="hero-desc">{DATA['description']}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART BUILDER
# ══════════════════════════════════════════
def build_chart(ch, height=350):
    is_horiz = "horizontal" in ch.get("type", "")
    fig = go.Figure()
    for i, ds in enumerate(ch["datasets"]):
        color = ds.get("color", PALETTE[i % len(PALETTE)])
        kw = dict(
            name=ds["label"], marker_color=color,
            marker_line_color="white", marker_line_width=0.5,
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
    ts = dict(gridwidth=0.5, tickfont=dict(size=10, color="#717171", family="DM Sans"))
    if is_horiz:
        fig.update_xaxes(gridcolor="#f0f0f0", **ts)
        fig.update_yaxes(autorange="reversed", gridcolor="white", **ts)
    else:
        fig.update_xaxes(gridcolor="white", **ts)
        fig.update_yaxes(gridcolor="#f0f0f0", **ts)
    return fig

# ══════════════════════════════════════════
# RENDER VERTICALS
# ══════════════════════════════════════════
for vi, vert in enumerate(verticals):
    is_live = vert.get("status") == "live"
    color = vert.get("color", "#666")

    if not is_live:
        st.markdown(f"""
        <div class="ph-card">
            <div class="ph-hdr">
                <span class="ph-icon">{vert['icon']}</span>
                <span class="ph-name">{vert['name']}</span>
                <span class="ph-badge">Coming soon</span>
            </div>
            <div class="ph-sum">{vert['summary']}</div>
        </div>
        """, unsafe_allow_html=True)
        continue

    # ── LIVE VERTICAL ──
    blocks = vert.get("blocks", [])
    with st.expander(
        f"{vert['icon']}  {vert['name']}  —  {vert.get('respondents','—')} respondents  ·  {len(blocks)} sections",
        expanded=(vi == 0),
    ):
        # Executive summary
        exec_data = vert.get("exec_summary")
        if exec_data:
            st.markdown('<div class="exec-label">Executive summary</div>', unsafe_allow_html=True)

            kpi_cols = st.columns(len(exec_data.get("kpis", [])))
            for col, kpi in zip(kpi_cols, exec_data.get("kpis", [])):
                col.markdown(
                    f'<div class="kpi-card"><div class="kpi-num">{kpi["value"]}</div>'
                    f'<div class="kpi-label">{kpi["label"]}</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            insight_cols = st.columns(2)
            for idx, insight in enumerate(exec_data.get("insights", [])):
                with insight_cols[idx % 2]:
                    st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown("---")

        # ── BLOCKS (2 per row) ──
        for bi in range(0, len(blocks), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = bi + j
                if idx >= len(blocks):
                    break
                block = blocks[idx]
                with col:
                    # Block header
                    question_text = block.get("question", "")
                    st.markdown(
                        f'<div class="block-card">'
                        f'<div class="block-bar" style="background:{color}"></div>'
                        f'<div class="block-heading">{block["heading"]}</div>'
                        f'<div class="block-subtitle">{block["subtitle"]}</div>'
                        f'<div class="block-question">{question_text}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    # Dropdown
                    views = block.get("chart_views", {})
                    view_names = list(views.keys())
                    if len(view_names) > 1:
                        selected_view = st.selectbox(
                            "Split by", view_names,
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
                            st.markdown(f'<div class="chart-note">{ch["note"]}</div>', unsafe_allow_html=True)

                    # Takeaway
                    takeaway = block.get("takeaway", "")
                    if takeaway:
                        st.markdown(f'<div class="block-takeaway">{takeaway}</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:12px;color:#999;padding:.5rem 0;font-family:DM Sans,sans-serif;">'
    'Media Industry Report 2025 &mdash; Bain & Company &mdash; Confidential</div>',
    unsafe_allow_html=True,
)
