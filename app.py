import streamlit as st
import plotly.graph_objects as go
import json
from pathlib import Path

st.set_page_config(page_title="Media Report 2026 | Bain & Company", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

PALETTE = ["#CC2936","#1B4965","#2D936C","#E07A2F","#7B2D8E","#6B46C1","#D4526E","#13A8BE"]
PAD = "calc(max(24px, (100vw - 1100px) / 2))"
NPAD = "calc(-1 * max(24px, (100vw - 1100px) / 2))"

@st.cache_data
def load_data():
    p = Path(__file__).parent / "survey_data.json"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

DATA = load_data()
verticals = DATA["verticals"]

# ══════════════════════════════════════════
# CSS
# ══════════════════════════════════════════
def inject_css():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
    #MainMenu{{visibility:hidden}}header{{visibility:hidden}}footer{{visibility:hidden}}
    .stApp{{background:#fff}}
    section[data-testid="stSidebar"]{{display:none}}
    .block-container{{
        padding-top:0!important;padding-bottom:0!important;
        padding-left:{PAD}!important;padding-right:{PAD}!important;
        max-width:100%!important;
    }}

    /* ── NAV BAR (row of st.page_link) ── */
    div[data-testid="stHorizontalBlock"].nav-row {{
        border-bottom:1px solid #e5e5e5;
        margin-left:{NPAD};margin-right:{NPAD};
        padding:0 {PAD};
        background:#fff;
    }}
    div[data-testid="stHorizontalBlock"].nav-row a[data-testid="stPageLink-NavLink"] {{
        font-family:'Avenir Next','Avenir','Segoe UI',sans-serif!important;
        font-size:13px!important;font-weight:500!important;
        color:#666!important;padding:14px 12px!important;
        border-bottom:2px solid transparent;border-radius:0!important;
        text-decoration:none!important;
    }}
    div[data-testid="stHorizontalBlock"].nav-row a[data-testid="stPageLink-NavLink"]:hover {{
        color:#1a1a1a!important;background:#fafafa!important;
    }}
    div[data-testid="stHorizontalBlock"].nav-row a[data-testid="stPageLink-NavLink"][aria-current="page"] {{
        color:#CC2936!important;border-bottom-color:#CC2936;
    }}

    /* ── CARD LINKS (st.page_link styled as cards) ── */
    .card-grid a[data-testid="stPageLink-NavLink"] {{
        border:1px solid #e5e5e5!important;border-radius:10px!important;
        padding:22px!important;background:#fff!important;
        text-decoration:none!important;color:#1a1a1a!important;
        transition:all .2s!important;display:block!important;
        font-family:'Avenir Next','Avenir','Segoe UI',sans-serif!important;
    }}
    .card-grid a[data-testid="stPageLink-NavLink"]:hover {{
        box-shadow:0 6px 24px rgba(0,0,0,.07)!important;transform:translateY(-2px);
    }}

    /* ── HERO ── */
    .hero-media{{
        margin-left:{NPAD};margin-right:{NPAD};
        padding:0;position:relative;overflow:hidden;
        background:linear-gradient(135deg, #1a1a1a 0%, #2a1215 30%, #CC2936 100%);
        min-height:320px;display:flex;align-items:center;
    }}
    .hero-media::before{{
        content:'';position:absolute;inset:0;
        background:
            radial-gradient(ellipse 500px 400px at 90% 50%, rgba(204,41,54,.25) 0%, transparent 70%),
            radial-gradient(ellipse 300px 300px at 70% 80%, rgba(204,41,54,.15) 0%, transparent 70%);
        pointer-events:none;
    }}
    .hero-media-inner{{position:relative;z-index:1;padding:56px {PAD} 48px;max-width:100%}}
    .hero-media-ey{{display:inline-block;background:rgba(204,41,54,.8);color:#fff;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 14px;border-radius:3px;margin-bottom:16px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .hero-media-title{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(2rem,4.5vw,3rem);font-weight:800;color:#fff;line-height:1.1;margin-bottom:14px;letter-spacing:-.5px}}
    .hero-media-desc{{color:rgba(255,255,255,.7);font-size:15px;line-height:1.8;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif;max-width:800px}}

    .hero-full{{
        background:#1a1a1a;padding:52px {PAD} 44px;position:relative;overflow:hidden;
        margin-left:{NPAD};margin-right:{NPAD};
    }}
    .hero-full::before{{content:'';position:absolute;top:-40%;right:0;width:500px;height:500px;background:radial-gradient(circle,rgba(204,41,54,.12) 0%,transparent 70%);pointer-events:none}}
    .hero-inner{{max-width:760px;position:relative;z-index:1}}
    .hero-ey{{display:inline-block;background:#CC2936;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:5px 14px;border-radius:3px;margin-bottom:14px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .hero-title{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;color:#fff;line-height:1.12;margin-bottom:8px;letter-spacing:-.5px}}
    .hero-sub{{font-family:'Playfair Display',Georgia,serif;font-size:16px;color:rgba(255,255,255,.6);font-style:italic}}

    .exec-label{{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#CC2936;margin-bottom:14px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}}
    .kpi{{background:#f8f8f8;border-radius:8px;padding:16px;text-align:center;border:1px solid #f0f0f0}}
    .kpi-n{{font-size:24px;font-weight:600;color:#1a1a1a;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .kpi-l{{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:.5px;margin-top:3px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .insights-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:24px}}
    .insight{{border-left:3px solid #CC2936;padding:10px 14px;background:#fafafa;border-radius:0 8px 8px 0;font-size:13px;color:#333;line-height:1.6;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .body-text{{font-size:15px;color:#444;line-height:1.8;margin-bottom:28px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif;max-width:800px}}

    .block-card{{border:1px solid #e5e5e5;border-radius:10px;padding:20px 22px;background:#fff;position:relative;margin-bottom:20px}}
    .block-card:hover{{box-shadow:0 3px 14px rgba(0,0,0,.04)}}
    .block-bar{{position:absolute;left:0;top:20px;bottom:20px;width:4px;border-radius:2px}}
    .block-heading{{font-size:16px;font-weight:600;color:#1a1a1a;padding-left:12px;margin-bottom:3px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .block-subtitle{{font-size:13px;color:#888;padding-left:12px;margin-bottom:3px;line-height:1.4;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .block-question{{font-size:11px;color:#aaa;padding-left:12px;font-style:italic;line-height:1.4;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .block-takeaway{{font-size:12px;font-weight:600;color:#CC2936;margin-top:10px;padding-left:12px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .chart-note{{font-size:11px;color:#888;background:#f8f8f8;border-radius:6px;padding:8px 12px;margin-top:6px;line-height:1.5;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}

    .coming-soon{{text-align:center;padding:80px 20px}}
    .coming-soon-icon{{font-size:48px;margin-bottom:16px}}
    .coming-soon-title{{font-size:22px;font-weight:600;color:#1a1a1a;margin-bottom:8px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .coming-soon-text{{font-size:14px;color:#888;max-width:500px;margin:0 auto;line-height:1.7;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .coming-soon-bar{{width:50px;height:3px;background:#CC2936;margin:20px auto 0;border-radius:2px}}

    .divider{{height:1px;background:#e5e5e5;margin:28px 0}}

    .bain-footer{{
        background:#1a1a1a;padding:28px {PAD};text-align:center;
        margin-left:{NPAD};margin-right:{NPAD};
    }}
    .bain-footer p{{font-size:12px;color:rgba(255,255,255,.4);font-family:'Avenir Next','Avenir','Segoe UI',sans-serif}}
    .bain-footer a{{color:#CC2936;text-decoration:none}}

    @media(max-width:1200px){{.hero-full,.hero-media,.bain-footer{{padding-left:24px;padding-right:24px}}}}
    @media(max-width:768px){{.kpi-grid{{grid-template-columns:1fr 1fr}}.insights-grid{{grid-template-columns:1fr}}}}
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# SHARED FUNCTIONS
# ══════════════════════════════════════════
@st.cache_data
def build_chart_figure(labels, datasets_json, chart_type, height):
    is_horiz = "horizontal" in chart_type
    datasets = json.loads(datasets_json)
    fig = go.Figure()
    for i, ds in enumerate(datasets):
        color = ds.get("color", PALETTE[i % len(PALETTE)])
        kw = dict(name=ds["label"], marker_color=color, marker_line_color="white", marker_line_width=0.5,
                  text=[f"{v}%" if v > 0 else "" for v in ds["data"]], textposition="inside",
                  textfont=dict(size=10, color="white", family="Avenir Next, Avenir, Segoe UI"))
        if is_horiz:
            fig.add_trace(go.Bar(y=list(labels), x=ds["data"], orientation="h", **kw))
        else:
            fig.add_trace(go.Bar(x=list(labels), y=ds["data"], **kw))
    fig.update_layout(barmode="stack", height=height, margin=dict(l=5, r=5, t=5, b=5),
        font=dict(family="Avenir Next, Avenir, Segoe UI", size=12, color="#4a4a4a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=11)),
        plot_bgcolor="white", paper_bgcolor="white", bargap=0.25, bargroupgap=0.1)
    ts = dict(gridwidth=0.5, tickfont=dict(size=11, color="#888", family="Avenir Next, Avenir, Segoe UI"))
    if is_horiz:
        fig.update_xaxes(gridcolor="#f0f0f0", **ts)
        fig.update_yaxes(autorange="reversed", gridcolor="white", **ts)
    else:
        fig.update_xaxes(gridcolor="white", **ts)
        fig.update_yaxes(gridcolor="#f0f0f0", **ts)
    return fig


@st.fragment
def render_block(block, color, prefix=""):
    st.markdown(
        f'<div class="block-card"><div class="block-bar" style="background:{color}"></div>'
        f'<div class="block-heading">{block["heading"]}</div>'
        f'<div class="block-subtitle">{block["subtitle"]}</div>'
        f'<div class="block-question">{block.get("question","")}</div></div>',
        unsafe_allow_html=True)
    views = block.get("chart_views", {})
    vnames = list(views.keys())
    if len(vnames) > 1:
        sel = st.selectbox("Split by", vnames, key=f"s_{prefix}{block['id']}", label_visibility="collapsed")
    else:
        sel = vnames[0] if vnames else None
    if sel and sel in views:
        ch = views[sel]
        is_h = "horizontal" in ch.get("type", "")
        h = 48 + len(ch["labels"]) * 34 if is_h else 320
        h = min(max(h, 280), 450)
        fig = build_chart_figure(tuple(ch["labels"]), json.dumps(ch["datasets"]), ch.get("type", ""), h)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        if ch.get("note"):
            st.markdown(f'<div class="chart-note">{ch["note"]}</div>', unsafe_allow_html=True)
    if block.get("takeaway"):
        st.markdown(f'<div class="block-takeaway">{block["takeaway"]}</div>', unsafe_allow_html=True)


def render_exec(ex):
    st.markdown('<div class="exec-label">Executive summary</div>', unsafe_allow_html=True)
    khtml = '<div class="kpi-grid">'
    for k in ex.get("kpis", []):
        khtml += f'<div class="kpi"><div class="kpi-n">{k["value"]}</div><div class="kpi-l">{k["label"]}</div></div>'
    st.markdown(khtml + '</div>', unsafe_allow_html=True)
    ihtml = '<div class="insights-grid">'
    for ins in ex.get("insights", []):
        ihtml += f'<div class="insight">{ins}</div>'
    st.markdown(ihtml + '</div>', unsafe_allow_html=True)


def render_nav(all_pages):
    """Render navbar using st.page_link for proper internal navigation."""
    cols = st.columns(len(all_pages) + 1)
    for i, pg in enumerate(all_pages):
        with cols[i]:
            st.page_link(pg, label=pg.title)
    with cols[-1]:
        st.markdown('<div style="text-align:right;font-size:11px;color:#999;padding:14px 0;font-family:Avenir Next,Avenir,Segoe UI,sans-serif"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#2D936C;margin-right:5px;vertical-align:middle"></span>Authenticated</div>', unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="bain-footer"><p>Media Report 2026 &mdash; <a href="https://www.bain.com">Bain & Company</a> &mdash; Confidential</p></div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# PASSWORD CHECK
# ══════════════════════════════════════════
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    inject_css()
    st.markdown("""
    <div style="min-height:80vh;display:flex;align-items:center;justify-content:center">
        <div style="max-width:380px;text-align:center">
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:28px;font-weight:800;color:#CC2936;margin-bottom:4px">Bain & Company</div>
            <div style="width:40px;height:3px;background:#CC2936;margin:0 auto 20px;border-radius:2px"></div>
            <div style="font-size:14px;color:#666;margin-bottom:24px;font-family:'Avenir Next','Avenir','Segoe UI',sans-serif">Media Report 2026<br>Enter access code to continue</div>
        </div>
    </div>
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


# ══════════════════════════════════════════
# PAGE FUNCTIONS
# ══════════════════════════════════════════
def page_overview():
    inject_css()
    render_nav(ALL_PAGES)

    st.markdown(f"""
    <div class="hero-media"><div class="hero-media-inner">
        <div class="hero-media-ey">Media Report 2026</div>
        <div class="hero-media-title">Media Report 2026</div>
        <div class="hero-media-desc">{DATA["description"]}</div>
    </div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    ex = DATA.get("overview_exec", {})
    if ex:
        render_exec(ex)

    gaming = next((v for v in verticals if v["id"] == "gaming"), None)
    if gaming and gaming.get("blocks"):
        st.markdown('<div class="exec-label">Gaming highlights</div>', unsafe_allow_html=True)
        for block in gaming["blocks"][:2]:
            render_block(block, gaming["color"], prefix="ov_")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Vertical cards as page_link buttons
    st.markdown('<div class="exec-label">Explore by vertical</div>', unsafe_allow_html=True)
    row1 = st.columns(3)
    row2 = st.columns(3)
    for i, pg in enumerate(ALL_PAGES[1:]):  # skip overview
        v = verticals[i]
        is_live = v.get("status") == "live"
        status = f"✅ {v.get('respondents','')} respondents" if is_live else "🔜 Coming soon"
        label = f"{v['icon']} **{v['name']}**\n\n{v.get('card_desc','')}\n\n{status}"
        col = row1[i] if i < 3 else row2[i - 3]
        with col:
            st.page_link(pg, label=label, use_container_width=True)

    render_footer()


def make_live_page(vert):
    """Factory: returns a page function for a live vertical."""
    def page_fn():
        inject_css()
        render_nav(ALL_PAGES)

        st.markdown(f"""
        <div class="hero-full"><div class="hero-inner">
            <div class="hero-ey">{vert['icon']} {vert['name']}</div>
            <div class="hero-title">{vert['name']}</div>
            <div class="hero-sub">{vert.get('respondents','')} respondents</div>
        </div></div>
        """, unsafe_allow_html=True)

        ex = vert.get("exec_summary", {})
        if ex:
            render_exec(ex)
        st.markdown(f'<div class="body-text">{vert.get("summary","")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        for block in vert.get("blocks", []):
            render_block(block, vert["color"], prefix="pg_")

        st.page_link(ALL_PAGES[0], label="← Back to Overview")
        render_footer()
    return page_fn


def make_coming_soon_page(vert):
    """Factory: returns a page function for a placeholder vertical."""
    def page_fn():
        inject_css()
        render_nav(ALL_PAGES)

        st.markdown(f"""
        <div class="hero-full"><div class="hero-inner">
            <div class="hero-ey">{vert['icon']} {vert['name']}</div>
            <div class="hero-title">{vert['name']}</div>
        </div></div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="coming-soon">
            <div class="coming-soon-icon">{vert['icon']}</div>
            <div class="coming-soon-title">Work in progress &mdash; Coming soon</div>
            <div class="coming-soon-text">{vert.get('card_desc','')}</div>
            <div class="coming-soon-bar"></div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(ALL_PAGES[0], label="← Back to Overview")
        render_footer()
    return page_fn


# ══════════════════════════════════════════
# BUILD ALL PAGES
# ══════════════════════════════════════════
ALL_PAGES = [
    st.Page(page_overview, title="Overview", url_path="overview", default=True),
]

for vert in verticals:
    if vert.get("status") == "live":
        ALL_PAGES.append(st.Page(
            make_live_page(vert),
            title=vert["name"],
            url_path=vert["id"],
        ))
    else:
        ALL_PAGES.append(st.Page(
            make_coming_soon_page(vert),
            title=vert["name"],
            url_path=vert["id"],
        ))


# ══════════════════════════════════════════
# RUN
# ══════════════════════════════════════════
if not check_password():
    st.stop()

pg = st.navigation(ALL_PAGES, position="hidden")
pg.run()
