import streamlit as st
import plotly.graph_objects as go
import json
from pathlib import Path

st.set_page_config(page_title="Media Report 2025 | Bain & Company", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

PALETTE = ["#CC2936","#1B4965","#2D936C","#E07A2F","#7B2D8E","#6B46C1","#D4526E","#13A8BE"]

# ══════════════════════════════════════════
# CSS
# ══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700;800&display=swap');
#MainMenu{visibility:hidden}header{visibility:hidden}footer{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
.stApp{background:#fff}
section[data-testid="stSidebar"]{display:none}
div[data-testid="stVerticalBlockBorderWrapper"]{gap:0}

/* ── NAV ── */
.bain-nav{background:#fff;padding:0 5vw;display:flex;align-items:center;border-bottom:1px solid #e5e5e5;position:sticky;top:0;z-index:999;height:54px}
.bain-logo-area{display:flex;align-items:center;margin-right:40px}
.bain-logo-area svg{height:20px}
.nav-links{display:flex;gap:0;flex:1;height:100%}
.nav-link{font-size:13px;color:#666;text-decoration:none;font-family:'DM Sans',sans-serif;font-weight:500;padding:0 16px;display:flex;align-items:center;height:100%;border-bottom:2px solid transparent;cursor:pointer;transition:all .15s}
.nav-link:hover{color:#1a1a1a;background:#fafafa}
.nav-link.active{color:#CC2936;border-bottom-color:#CC2936}
.nav-link.disabled{color:#bbb;cursor:default}
.nav-link.disabled:hover{background:transparent;color:#bbb}
.nav-right{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:11px;color:#999;font-family:'DM Sans',sans-serif}
.nav-right-dot{width:6px;height:6px;border-radius:50%;background:#2D936C}

/* ── HERO ── */
.hero-full{background:#1a1a1a;padding:56px 5vw 48px;position:relative;overflow:hidden}
.hero-full::before{content:'';position:absolute;top:-40%;right:-5%;width:600px;height:600px;background:radial-gradient(circle,rgba(204,41,54,.12) 0%,transparent 70%);pointer-events:none}
.hero-inner{max-width:860px;position:relative;z-index:1}
.hero-ey{display:inline-block;background:#CC2936;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 14px;border-radius:3px;margin-bottom:14px;font-family:'DM Sans',sans-serif}
.hero-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;color:#fff;line-height:1.12;margin-bottom:8px;letter-spacing:-.5px}
.hero-sub{font-family:'Playfair Display',Georgia,serif;font-size:17px;color:rgba(255,255,255,.6);font-style:italic;margin-bottom:12px}
.hero-desc-text{color:rgba(255,255,255,.45);font-size:13px;line-height:1.7;max-width:620px;font-family:'DM Sans',sans-serif}

/* ── CONTENT WRAPPER ── */
.content{max-width:900px;margin:0 auto;padding:36px 5vw 48px}

/* ── EXEC SUMMARY ── */
.exec-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#CC2936;margin-bottom:14px;font-family:'DM Sans',sans-serif}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.kpi{background:#f8f8f8;border-radius:8px;padding:18px;text-align:center;border:1px solid #f0f0f0}
.kpi-n{font-size:26px;font-weight:600;color:#1a1a1a;font-family:'DM Sans',sans-serif}
.kpi-l{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:.5px;margin-top:3px;font-family:'DM Sans',sans-serif}
.insights-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:24px}
.insight{border-left:3px solid #CC2936;padding:10px 14px;background:#fafafa;border-radius:0 8px 8px 0;font-size:13px;color:#333;line-height:1.6;font-family:'DM Sans',sans-serif}

/* ── BODY TEXT ── */
.body-text{font-size:15px;color:#444;line-height:1.8;margin-bottom:32px;font-family:'DM Sans',sans-serif;max-width:800px}

/* ── VERTICAL CARDS (overview page) ── */
.vert-cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:32px}
.vert-card{border:1px solid #e5e5e5;border-radius:10px;padding:24px;background:#fff;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}
.vert-card:hover{box-shadow:0 6px 24px rgba(0,0,0,.07);transform:translateY(-2px)}
.vert-card-bar{position:absolute;top:0;left:0;right:0;height:4px}
.vert-card-icon{font-size:28px;margin-bottom:10px;display:block}
.vert-card-name{font-size:16px;font-weight:600;color:#1a1a1a;margin-bottom:6px;font-family:'DM Sans',sans-serif}
.vert-card-desc{font-size:12px;color:#888;line-height:1.6;font-family:'DM Sans',sans-serif}
.vert-card-status{font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;position:absolute;top:16px;right:16px;font-family:'DM Sans',sans-serif}
.status-live{background:#fef2f2;color:#CC2936}
.status-soon{background:#f0ebe0;color:#8a6d3b}

/* ── BLOCK CARDS (single column) ── */
.block-card{border:1px solid #e5e5e5;border-radius:10px;padding:22px 24px;background:#fff;position:relative;margin-bottom:20px;max-width:900px}
.block-card:hover{box-shadow:0 3px 14px rgba(0,0,0,.04)}
.block-bar{position:absolute;left:0;top:22px;bottom:22px;width:4px;border-radius:2px}
.block-heading{font-size:17px;font-weight:600;color:#1a1a1a;padding-left:14px;margin-bottom:3px;font-family:'DM Sans',sans-serif}
.block-subtitle{font-size:13px;color:#888;padding-left:14px;margin-bottom:3px;line-height:1.4;font-family:'DM Sans',sans-serif}
.block-question{font-size:11px;color:#aaa;padding-left:14px;margin-bottom:0;font-style:italic;line-height:1.4;font-family:'DM Sans',sans-serif}
.block-takeaway{font-size:12px;font-weight:600;color:#CC2936;margin-top:10px;padding-left:14px;font-family:'DM Sans',sans-serif}

.chart-note{font-size:11px;color:#888;background:#f8f8f8;border-radius:6px;padding:8px 12px;margin-top:6px;line-height:1.5;font-family:'DM Sans',sans-serif}

/* ── COMING SOON ── */
.coming-soon{text-align:center;padding:80px 20px}
.coming-soon-icon{font-size:48px;margin-bottom:16px}
.coming-soon-title{font-size:22px;font-weight:600;color:#1a1a1a;margin-bottom:8px;font-family:'DM Sans',sans-serif}
.coming-soon-text{font-size:14px;color:#888;font-family:'DM Sans',sans-serif}
.coming-soon-bar{width:50px;height:3px;background:#CC2936;margin:20px auto 0;border-radius:2px}

/* ── SECTION DIVIDER ── */
.divider{height:1px;background:#e5e5e5;margin:28px 0}

/* ── FOOTER ── */
.bain-footer{background:#1a1a1a;padding:28px 5vw;text-align:center}
.bain-footer p{font-size:12px;color:rgba(255,255,255,.4);font-family:'DM Sans',sans-serif}
.bain-footer a{color:#CC2936;text-decoration:none}

/* ── PASSWORD ── */
.pw-screen{min-height:80vh;display:flex;align-items:center;justify-content:center}
.pw-box{max-width:380px;text-align:center}
.pw-logo-text{font-family:'Playfair Display',Georgia,serif;font-size:28px;font-weight:800;color:#CC2936;margin-bottom:4px}
.pw-title{font-size:14px;color:#666;margin-bottom:24px;font-family:'DM Sans',sans-serif}
.pw-line{width:40px;height:3px;background:#CC2936;margin:0 auto 20px;border-radius:2px}

/* ── RESPONSIVE ── */
@media(max-width:768px){
  .hero-full{padding:36px 20px 30px}
  .content{padding:24px 16px 36px}
  .kpi-grid{grid-template-columns:1fr 1fr}
  .insights-grid{grid-template-columns:1fr}
  .vert-cards{grid-template-columns:1fr}
  .bain-nav{padding:0 16px}
  .nav-links{overflow-x:auto}
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
    <div class="bain-nav"><div class="bain-logo-area"><svg viewBox="0 0 80 22" height="20"><text x="0" y="17" font-family="Playfair Display,Georgia,serif" font-weight="800" font-size="20" fill="#CC2936">BAIN</text></svg></div></div>
    <div class="pw-screen"><div class="pw-box">
        <div class="pw-logo-text">Bain & Company</div>
        <div class="pw-line"></div>
        <div class="pw-title">Media Industry Report 2025<br>Enter access code to continue</div>
    </div></div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c2:
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

# ── ROUTING ──
verticals = DATA["verticals"]
NAV_ITEMS = ["Overview"] + [v["name"] for v in verticals]

if "page" not in st.session_state:
    st.session_state.page = "Overview"

def nav_to(page):
    st.session_state.page = page

# ══════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════
current = st.session_state.page
nav_html_links = ""
for item in NAV_ITEMS:
    is_active = "active" if item == current else ""
    vert_match = next((v for v in verticals if v["name"] == item), None)
    is_disabled = ""
    if vert_match and vert_match.get("status") != "live" and item != "Overview":
        is_disabled = ""  # still clickable, shows coming soon page
    nav_html_links += f'<span class="nav-link {is_active}" id="nav-{item.replace(" ","_").replace("&","")}">{item}</span>'

st.markdown(f"""
<div class="bain-nav">
    <div class="bain-logo-area"><svg viewBox="0 0 80 22" height="20"><text x="0" y="17" font-family="Playfair Display,Georgia,serif" font-weight="800" font-size="20" fill="#CC2936">BAIN</text></svg></div>
    <div class="nav-links">{nav_html_links}</div>
    <div class="nav-right"><div class="nav-right-dot"></div>Authenticated</div>
</div>
""", unsafe_allow_html=True)

# Nav buttons (hidden visual, functional routing)
cols_nav = st.columns(len(NAV_ITEMS))
for i, item in enumerate(NAV_ITEMS):
    with cols_nav[i]:
        if st.button(item, key=f"navbtn_{item}", use_container_width=True, type="secondary"):
            nav_to(item)
            st.rerun()

# Hide the ugly buttons but keep them functional
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    position: absolute; top: 54px; left: 5vw; right: 5vw; z-index: 1000;
    display: flex; gap: 0; height: 54px; opacity: 0;
}
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button {
    height: 54px !important; border: none !important; background: transparent !important;
}
</style>
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
        plot_bgcolor="white", paper_bgcolor="white", bargap=0.25, bargroupgap=0.1,
    )
    ts = dict(gridwidth=0.5, tickfont=dict(size=11, color="#888", family="DM Sans"))
    if is_horiz:
        fig.update_xaxes(gridcolor="#f0f0f0", **ts)
        fig.update_yaxes(autorange="reversed", gridcolor="white", **ts)
    else:
        fig.update_xaxes(gridcolor="white", **ts)
        fig.update_yaxes(gridcolor="#f0f0f0", **ts)
    return fig


def render_block(block, vert_color, prefix=""):
    """Render a single block card with dropdown and chart — single column."""
    question_text = block.get("question", "")
    st.markdown(
        f'<div class="block-card">'
        f'<div class="block-bar" style="background:{vert_color}"></div>'
        f'<div class="block-heading">{block["heading"]}</div>'
        f'<div class="block-subtitle">{block["subtitle"]}</div>'
        f'<div class="block-question">{question_text}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    views = block.get("chart_views", {})
    view_names = list(views.keys())
    if len(view_names) > 1:
        selected = st.selectbox("Split by", view_names, key=f"sel_{prefix}{block['id']}", label_visibility="collapsed")
    else:
        selected = view_names[0] if view_names else None

    if selected and selected in views:
        ch = views[selected]
        is_horiz = "horizontal" in ch.get("type", "")
        h = 48 + len(ch["labels"]) * 34 if is_horiz else 320
        h = max(h, 280)
        h = min(h, 450)
        fig = build_chart(ch, height=h)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"ch_{prefix}{block['id']}_{selected}")
        if ch.get("note"):
            st.markdown(f'<div class="chart-note">{ch["note"]}</div>', unsafe_allow_html=True)

    takeaway = block.get("takeaway", "")
    if takeaway:
        st.markdown(f'<div class="block-takeaway">{takeaway}</div>', unsafe_allow_html=True)
    st.markdown("")


# ══════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════
if current == "Overview":
    # Hero
    st.markdown(f"""
    <div class="hero-full">
        <div class="hero-inner">
            <div class="hero-ey">Media Report 2025</div>
            <div class="hero-title">{DATA['title']}</div>
            <div class="hero-sub">Breaking boundaries across media verticals</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content">', unsafe_allow_html=True)

    # Exec summary
    ex = DATA.get("overview_exec", {})
    if ex:
        st.markdown('<div class="exec-label">Executive summary</div>', unsafe_allow_html=True)
        kpi_html = '<div class="kpi-grid">'
        for k in ex.get("kpis", []):
            kpi_html += f'<div class="kpi"><div class="kpi-n">{k["value"]}</div><div class="kpi-l">{k["label"]}</div></div>'
        kpi_html += '</div>'
        st.markdown(kpi_html, unsafe_allow_html=True)

        ins_html = '<div class="insights-grid">'
        for ins in ex.get("insights", []):
            ins_html += f'<div class="insight">{ins}</div>'
        ins_html += '</div>'
        st.markdown(ins_html, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Body description
    st.markdown(f'<div class="body-text">{DATA["description"]}</div>', unsafe_allow_html=True)

    # Vertical cards
    st.markdown('<div class="exec-label">Explore by vertical</div>', unsafe_allow_html=True)
    cards_html = '<div class="vert-cards">'
    for v in verticals:
        is_live = v.get("status") == "live"
        status_class = "status-live" if is_live else "status-soon"
        status_text = f'{v.get("respondents","")} respondents' if is_live else "Coming soon"
        cards_html += f'''
        <div class="vert-card" id="card-{v['id']}">
            <div class="vert-card-bar" style="background:{v['color']}"></div>
            <div class="vert-card-status {status_class}">{status_text}</div>
            <span class="vert-card-icon">{v['icon']}</span>
            <div class="vert-card-name">{v['name']}</div>
            <div class="vert-card-desc">{v.get('card_desc', v.get('summary',''))}</div>
        </div>'''
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Card buttons (invisible, overlaid)
    card_cols = st.columns(3)
    for i, v in enumerate(verticals):
        with card_cols[i % 3]:
            if st.button(f"Open {v['name']}", key=f"card_{v['id']}", use_container_width=True):
                nav_to(v["name"])
                st.rerun()

    # Placeholder gaming preview charts on overview
    gaming = next((v for v in verticals if v["id"] == "gaming"), None)
    if gaming and gaming.get("blocks"):
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="exec-label">Gaming highlights</div>', unsafe_allow_html=True)
        for block in gaming["blocks"][:3]:
            render_block(block, gaming["color"], prefix="ov_")

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE: LIVE VERTICAL (Gaming)
# ══════════════════════════════════════════
elif current in [v["name"] for v in verticals if v.get("status") == "live"]:
    vert = next(v for v in verticals if v["name"] == current)

    st.markdown(f"""
    <div class="hero-full">
        <div class="hero-inner">
            <div class="hero-ey">{vert['icon']} {vert['name']}</div>
            <div class="hero-title">{vert['name']} Report</div>
            <div class="hero-sub">{vert.get('respondents','')} respondents &mdash; Ages 2&ndash;17</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content">', unsafe_allow_html=True)

    # Exec summary
    ex = vert.get("exec_summary", {})
    if ex:
        st.markdown('<div class="exec-label">Executive summary</div>', unsafe_allow_html=True)
        kpi_html = '<div class="kpi-grid">'
        for k in ex.get("kpis", []):
            kpi_html += f'<div class="kpi"><div class="kpi-n">{k["value"]}</div><div class="kpi-l">{k["label"]}</div></div>'
        kpi_html += '</div>'
        st.markdown(kpi_html, unsafe_allow_html=True)

        ins_html = '<div class="insights-grid">'
        for ins in ex.get("insights", []):
            ins_html += f'<div class="insight">{ins}</div>'
        ins_html += '</div>'
        st.markdown(ins_html, unsafe_allow_html=True)

    st.markdown(f'<div class="body-text">{vert.get("summary","")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Blocks — single column
    for block in vert.get("blocks", []):
        render_block(block, vert["color"], prefix="pg_")

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# PAGE: COMING SOON
# ══════════════════════════════════════════
else:
    vert = next((v for v in verticals if v["name"] == current), None)
    icon = vert["icon"] if vert else "📋"
    color = vert["color"] if vert else "#666"
    desc = vert.get("card_desc", "") if vert else ""

    st.markdown(f"""
    <div class="hero-full" style="padding:40px 5vw 36px">
        <div class="hero-inner">
            <div class="hero-ey">{icon} {current}</div>
            <div class="hero-title">{current}</div>
        </div>
    </div>
    <div class="content">
        <div class="coming-soon">
            <div class="coming-soon-icon">{icon}</div>
            <div class="coming-soon-title">Work in progress &mdash; Coming soon</div>
            <div class="coming-soon-text">{desc}</div>
            <div class="coming-soon-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("← Back to Overview", use_container_width=True, type="primary"):
            nav_to("Overview")
            st.rerun()


# ── FOOTER ──
st.markdown("""
<div class="bain-footer">
    <p>Media Industry Report 2025 &mdash; <a href="https://www.bain.com">Bain & Company</a> &mdash; Confidential</p>
</div>
""", unsafe_allow_html=True)
