import streamlit as st
import plotly.graph_objects as go
import json
from pathlib import Path

st.set_page_config(page_title="Gaming Report 2025 | Bain & Company", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

PALETTE = ["#CC2936","#1B4965","#2D936C","#E07A2F","#7B2D8E","#6B46C1","#D4526E","#13A8BE","#547AA5","#C4A77D"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700;800&display=swap');

/* ── FULL WIDTH OVERRIDE ── */
#MainMenu{visibility:hidden}header{visibility:hidden}footer{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
.stApp{background:#fff}
section[data-testid="stSidebar"]{display:none}

/* ── BAIN NAV (white bg, red logo like bain.com) ── */
.bain-nav{background:#fff;padding:14px 40px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #e5e5e5;position:sticky;top:0;z-index:100}
.bain-logo{display:flex;align-items:center;gap:0}
.bain-logo svg{height:22px}
.bain-nav-links{display:flex;gap:24px;align-items:center}
.bain-nav-link{font-size:13px;color:#333;text-decoration:none;font-family:'DM Sans',sans-serif;font-weight:500}
.bain-auth{font-size:11px;color:#999;display:flex;align-items:center;gap:5px;font-family:'DM Sans',sans-serif}
.bain-auth-dot{width:6px;height:6px;border-radius:50%;background:#2D936C}

/* ── HERO (dark, full-width, Bain gaming report style) ── */
.hero-full{background:#1a1a1a;padding:60px 40px 50px;position:relative;overflow:hidden;margin-bottom:0}
.hero-full::before{content:'';position:absolute;top:-40%;right:-10%;width:600px;height:600px;background:radial-gradient(circle,rgba(204,41,54,.12) 0%,transparent 70%);pointer-events:none}
.hero-inner{max-width:900px;position:relative;z-index:1}
.hero-ey{display:inline-block;background:#CC2936;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 14px;border-radius:3px;margin-bottom:12px;font-family:'DM Sans',sans-serif}
.hero-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(2rem,4.5vw,3rem);font-weight:800;color:#fff;line-height:1.12;margin-bottom:10px;letter-spacing:-.5px}
.hero-sub{font-family:'Playfair Display',Georgia,serif;font-size:18px;font-weight:400;color:rgba(255,255,255,.7);margin-bottom:12px;font-style:italic}
.hero-desc{color:rgba(255,255,255,.5);font-size:14px;line-height:1.7;max-width:600px;font-family:'DM Sans',sans-serif}

/* ── CONTENT AREA ── */
.content-area{max-width:1200px;margin:0 auto;padding:32px 40px 48px}

/* ── EXEC SUMMARY ── */
.exec-section{margin-bottom:32px}
.exec-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#CC2936;margin-bottom:14px;font-family:'DM Sans',sans-serif}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.kpi{background:#f8f8f8;border-radius:8px;padding:18px 20px;text-align:center;border:1px solid #f0f0f0}
.kpi-n{font-size:28px;font-weight:600;color:#1a1a1a;font-family:'DM Sans',sans-serif}
.kpi-l{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:.5px;margin-top:3px;font-family:'DM Sans',sans-serif}
.insights-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.insight{border-left:3px solid #CC2936;padding:10px 14px;background:#fafafa;border-radius:0 8px 8px 0;font-size:13px;color:#333;line-height:1.6;font-family:'DM Sans',sans-serif}

/* ── VERTICAL SECTION ── */
.vert-section{margin-bottom:24px}
.vert-header{display:flex;align-items:center;gap:12px;padding:16px 0;border-bottom:2px solid #CC2936;margin-bottom:20px}
.vert-icon{font-size:24px}
.vert-name{font-size:22px;font-weight:600;color:#1a1a1a;font-family:'DM Sans',sans-serif}
.vert-badge{font-size:11px;font-weight:600;padding:4px 12px;border-radius:20px;background:#fef2f2;color:#CC2936;font-family:'DM Sans',sans-serif}
.vert-summary{font-size:14px;color:#666;line-height:1.7;margin-bottom:24px;max-width:800px;font-family:'DM Sans',sans-serif}

/* ── BLOCKS (2-col) ── */
.blocks-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:32px}
.block-card{border:1px solid #e5e5e5;border-radius:10px;padding:20px 22px;background:#fff;position:relative;transition:box-shadow .2s}
.block-card:hover{box-shadow:0 4px 20px rgba(0,0,0,.06)}
.block-bar{position:absolute;left:0;top:20px;bottom:20px;width:4px;border-radius:2px}
.block-heading{font-size:16px;font-weight:600;color:#1a1a1a;padding-left:12px;margin-bottom:3px;font-family:'DM Sans',sans-serif}
.block-subtitle{font-size:12px;color:#888;padding-left:12px;margin-bottom:2px;line-height:1.4;font-family:'DM Sans',sans-serif}
.block-question{font-size:11px;color:#aaa;padding-left:12px;margin-bottom:0;font-style:italic;line-height:1.4;font-family:'DM Sans',sans-serif}
.block-takeaway{font-size:12px;font-weight:600;color:#CC2936;margin-top:10px;padding-left:12px;font-family:'DM Sans',sans-serif}

.chart-note{font-size:11px;color:#888;background:#f8f8f8;border-radius:6px;padding:8px 12px;margin-top:6px;line-height:1.5;font-family:'DM Sans',sans-serif}

/* ── PLACEHOLDER CARDS ── */
.ph-card{border:1px dashed #d0d0d0;border-radius:10px;padding:18px 22px;background:#fafafa;margin-bottom:10px}
.ph-hdr{display:flex;align-items:center;gap:10px;margin-bottom:5px}
.ph-icon{font-size:22px}
.ph-name{font-size:16px;font-weight:600;color:#1a1a1a;font-family:'DM Sans',sans-serif}
.ph-badge{font-size:10px;font-weight:600;padding:3px 12px;border-radius:20px;background:#f0ebe0;color:#8a6d3b;margin-left:auto;font-family:'DM Sans',sans-serif}
.ph-sum{font-size:13px;color:#888;line-height:1.6;font-family:'DM Sans',sans-serif}

/* ── PASSWORD SCREEN ── */
.pw-screen{min-height:80vh;display:flex;align-items:center;justify-content:center}
.pw-box{max-width:380px;text-align:center}
.pw-logo-text{font-family:'Playfair Display',Georgia,serif;font-size:28px;font-weight:800;color:#CC2936;margin-bottom:4px}
.pw-title{font-size:14px;color:#666;margin-bottom:24px;font-family:'DM Sans',sans-serif}
.pw-line{width:40px;height:3px;background:#CC2936;margin:0 auto 20px;border-radius:2px}

/* ── FOOTER ── */
.bain-footer{background:#1a1a1a;padding:24px 40px;text-align:center;margin-top:40px}
.bain-footer p{font-size:12px;color:rgba(255,255,255,.4);font-family:'DM Sans',sans-serif}
.bain-footer a{color:#CC2936;text-decoration:none}

/* ── DIVIDER ── */
.section-divider{height:1px;background:#e5e5e5;margin:32px 0}

/* ── RESPONSIVE ── */
@media(max-width:768px){
  .hero-full{padding:40px 20px 30px}
  .content-area{padding:20px}
  .blocks-grid,.kpi-grid,.insights-grid{grid-template-columns:1fr}
  .bain-nav{padding:12px 16px}
  .bain-nav-links{display:none}
}
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
    <div class="bain-nav">
        <div class="bain-logo">
            <svg viewBox="0 0 100 24" height="22"><text x="0" y="18" font-family="Playfair Display,Georgia,serif" font-weight="800" font-size="22" fill="#CC2936">BAIN</text></svg>
        </div>
    </div>
    <div class="pw-screen">
        <div class="pw-box">
            <div class="pw-logo-text">Bain & Company</div>
            <div class="pw-line"></div>
            <div class="pw-title">Media Industry Report 2025<br>Enter access code to continue</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        pwd = st.text_input("Code", type="password", key="pw_input", label_visibility="collapsed", placeholder="Access code")
        if st.button("Enter", use_container_width=True, type="primary"):
            if pwd == DATA.get("password", "bain2025"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect code.")
    return False

if not check_password():
    st.stop()

# ── DATA ──
verticals = DATA["verticals"]
live_v = [v for v in verticals if v.get("status") == "live"]

# ══════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════
st.markdown("""
<div class="bain-nav">
    <div class="bain-logo">
        <svg viewBox="0 0 100 24" height="22"><text x="0" y="18" font-family="Playfair Display,Georgia,serif" font-weight="800" font-size="22" fill="#CC2936">BAIN</text></svg>
    </div>
    <div class="bain-nav-links">
        <span class="bain-nav-link">Gaming</span>
        <span class="bain-nav-link" style="color:#bbb">Social Media</span>
        <span class="bain-nav-link" style="color:#bbb">Streaming</span>
        <span class="bain-nav-link" style="color:#bbb">Publishing</span>
        <span class="bain-nav-link" style="color:#bbb">Advertising</span>
        <span class="bain-nav-link" style="color:#bbb">Music</span>
    </div>
    <div class="bain-auth"><div class="bain-auth-dot"></div>Authenticated</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HERO (full-width dark banner like Bain gaming report)
# ══════════════════════════════════════════
st.markdown(f"""
<div class="hero-full">
    <div class="hero-inner">
        <div class="hero-ey">Media Report 2025</div>
        <div class="hero-title">{DATA['title']}</div>
        <div class="hero-sub">Breaking boundaries across media verticals</div>
        <div class="hero-desc">{DATA['description']}</div>
    </div>
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
            textfont=dict(size=10, color="white", family="DM Sans"),
        )
        if is_horiz:
            fig.add_trace(go.Bar(y=ch["labels"], x=ds["data"], orientation="h", **kw))
        else:
            fig.add_trace(go.Bar(x=ch["labels"], y=ds["data"], **kw))

    fig.update_layout(
        barmode="stack", height=height,
        margin=dict(l=5, r=5, t=5, b=5),
        font=dict(family="DM Sans", size=12, color="#4a4a4a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=11)),
        plot_bgcolor="white", paper_bgcolor="white",
        bargap=0.25, bargroupgap=0.1,
    )
    ts = dict(gridwidth=0.5, tickfont=dict(size=11, color="#888", family="DM Sans"))
    if is_horiz:
        fig.update_xaxes(gridcolor="#f0f0f0", **ts)
        fig.update_yaxes(autorange="reversed", gridcolor="white", **ts)
    else:
        fig.update_xaxes(gridcolor="white", **ts)
        fig.update_yaxes(gridcolor="#f0f0f0", **ts)
    return fig

# ══════════════════════════════════════════
# CONTENT AREA START
# ══════════════════════════════════════════
st.markdown('<div class="content-area">', unsafe_allow_html=True)

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
        expanded=True,
    ):
        st.markdown(
            f'<div class="vert-summary">{vert["summary"]}</div>',
            unsafe_allow_html=True,
        )

        # ── EXECUTIVE SUMMARY ──
        exec_data = vert.get("exec_summary")
        if exec_data:
            st.markdown('<div class="exec-section">', unsafe_allow_html=True)
            st.markdown('<div class="exec-label">Executive summary</div>', unsafe_allow_html=True)

            kpi_html = '<div class="kpi-grid">'
            for kpi in exec_data.get("kpis", []):
                kpi_html += f'<div class="kpi"><div class="kpi-n">{kpi["value"]}</div><div class="kpi-l">{kpi["label"]}</div></div>'
            kpi_html += '</div>'
            st.markdown(kpi_html, unsafe_allow_html=True)

            insights_html = '<div class="insights-grid">'
            for ins in exec_data.get("insights", []):
                insights_html += f'<div class="insight">{ins}</div>'
            insights_html += '</div>'
            st.markdown(insights_html, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── BLOCKS (2 per row) ──
        for bi in range(0, len(blocks), 2):
            cols = st.columns(2, gap="medium")
            for j, col in enumerate(cols):
                idx = bi + j
                if idx >= len(blocks):
                    break
                block = blocks[idx]
                with col:
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
                        h = 48 + len(ch["labels"]) * 34 if is_horiz else 320
                        h = max(h, 280)
                        h = min(h, 450)

                        fig = build_chart(ch, height=h)
                        st.plotly_chart(
                            fig, use_container_width=True,
                            config={"displayModeBar": False},
                            key=f"chart_{vert['id']}_{block['id']}_{selected_view}",
                        )

                        if ch.get("note"):
                            st.markdown(f'<div class="chart-note">{ch["note"]}</div>', unsafe_allow_html=True)

                    takeaway = block.get("takeaway", "")
                    if takeaway:
                        st.markdown(f'<div class="block-takeaway">{takeaway}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="bain-footer">
    <p>Media Industry Report 2025 &mdash; <a href="https://www.bain.com">Bain & Company</a> &mdash; Confidential</p>
</div>
""", unsafe_allow_html=True)
