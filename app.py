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
# CUSTOM CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700;800&display=swap');
#MainMenu {visibility:hidden} header {visibility:hidden} footer {visibility:hidden}
.block-container {padding-top:0!important;max-width:1000px}

/* Hero */
.hero{background:#1a1a1a;padding:2.5rem 2rem 2rem;border-radius:0 0 16px 16px;margin:-1rem -1rem 1.5rem;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-50%;right:-15%;width:500px;height:500px;background:radial-gradient(circle,rgba(204,41,54,.15) 0%,transparent 70%);pointer-events:none}
.hero-eyebrow{display:inline-block;background:#CC2936;color:#fff;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:4px 12px;border-radius:3px;margin-bottom:.75rem;font-family:'DM Sans',sans-serif}
.hero-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.6rem,4vw,2.5rem);font-weight:800;color:#fff;line-height:1.15;margin-bottom:.5rem;letter-spacing:-.5px}
.hero-desc{color:rgba(255,255,255,.6);font-size:14px;max-width:620px;line-height:1.7;font-family:'DM Sans',sans-serif}
.hero-stats{display:flex;gap:2rem;margin-top:1.25rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,.1);flex-wrap:wrap}
.hero-stat-num{font-size:24px;font-weight:600;color:#fff;font-family:'DM Sans',sans-serif}
.hero-stat-label{font-size:11px;color:rgba(255,255,255,.45);margin-top:2px;font-family:'DM Sans',sans-serif}

/* Vertical cards on landing page */
.vert-card{border:1px solid #e8e8e8;border-radius:14px;padding:20px 24px;margin-bottom:12px;background:#fff;transition:box-shadow .25s;position:relative;overflow:hidden}
.vert-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.08)}
.vert-card-bar{position:absolute;left:0;top:0;bottom:0;width:5px}
.vert-card-header{display:flex;align-items:center;gap:14px;margin-bottom:8px}
.vert-card-icon{font-size:24px}
.vert-card-name{font-size:18px;font-weight:600;color:#212121;font-family:'DM Sans',sans-serif}
.vert-card-badge{font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;margin-left:auto}
.badge-live{background:#EAF3DE;color:#27500A}
.badge-placeholder{background:#FAEEDA;color:#854F0B}
.vert-card-summary{font-size:13px;color:#717171;line-height:1.6;margin-bottom:12px;font-family:'DM Sans',sans-serif}
.vert-card-findings{margin:0;padding:0 0 0 18px;font-size:13px;color:#4a4a4a;line-height:1.8;font-family:'DM Sans',sans-serif}

/* KPI */
.kpi-card{background:#f5f5f5;border-radius:10px;padding:16px 18px;text-align:center}
.kpi-num{font-size:24px;font-weight:600;color:#212121;font-family:'DM Sans',sans-serif}
.kpi-label{font-size:11px;color:#717171;text-transform:uppercase;letter-spacing:.5px;margin-top:2px;font-family:'DM Sans',sans-serif}

/* Chart note */
.chart-note{font-size:12px;color:#717171;background:#f5f5f5;border-radius:8px;padding:10px 14px;margin-top:4px;line-height:1.6;font-family:'DM Sans',sans-serif}
.chart-note-warn{background:#FAEEDA;color:#854F0B}

/* Placeholder banner */
.placeholder-banner{background:#FAEEDA;border:1px solid #F0D4A0;border-radius:10px;padding:14px 18px;margin-bottom:16px;font-size:13px;color:#854F0B;line-height:1.6;font-family:'DM Sans',sans-serif}
.placeholder-banner strong{font-weight:600}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "survey_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

DATA = load_data()
verticals = DATA["verticals"]
live_count = sum(1 for v in verticals if v.get("status") == "live")
total_charts = sum(
    len(ch.get("charts", []))
    for v in verticals
    for ch in v.get("agendas", [])
)


# ═══════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Media Report 2025</div>
    <div class="hero-title">{DATA['title']}</div>
    <div class="hero-desc">{DATA['description']}</div>
    <div class="hero-stats">
        <div><div class="hero-stat-num">{len(verticals)}</div><div class="hero-stat-label">Media verticals</div></div>
        <div><div class="hero-stat-num">{live_count}</div><div class="hero-stat-label">Live datasets</div></div>
        <div><div class="hero-stat-num">{total_charts}</div><div class="hero-stat-label">Visualizations</div></div>
        <div><div class="hero-stat-num">{DATA.get('sample',{}).get('total','—')}</div><div class="hero-stat-label">Gaming respondents</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# CHART BUILDER
# ═══════════════════════════════════════════
def build_chart(ch, height=400):
    is_horiz = "horizontal" in ch.get("type", "")
    fig = go.Figure()

    for i, ds in enumerate(ch["datasets"]):
        color = ds.get("color", PALETTE[i % len(PALETTE)])
        kwargs = dict(
            name=ds["label"],
            marker_color=color,
            marker_line_color="white",
            marker_line_width=0.5,
            text=[f"{v}%" if v > 0 else "" for v in ds["data"]],
            textposition="inside",
            textfont=dict(size=10, color="white", family="DM Sans"),
        )
        if is_horiz:
            fig.add_trace(go.Bar(y=ch["labels"], x=ds["data"], orientation="h", **kwargs))
        else:
            fig.add_trace(go.Bar(x=ch["labels"], y=ds["data"], **kwargs))

    fig.update_layout(
        barmode="stack",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="DM Sans", size=12, color="#4a4a4a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=11)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.25,
        bargroupgap=0.1,
    )

    tick_style = dict(
        gridwidth=0.5,
        tickfont=dict(size=11, color="#717171", family="DM Sans"),
        title_font=dict(size=12, color="#717171"),
    )
    if is_horiz:
        fig.update_xaxes(title_text="", gridcolor="#f0f0f0", **tick_style)
        fig.update_yaxes(autorange="reversed", gridcolor="white", **tick_style)
    else:
        fig.update_xaxes(gridcolor="white", **tick_style)
        fig.update_yaxes(title_text="", gridcolor="#f0f0f0", **tick_style)

    return fig


def render_agenda_charts(agenda, is_placeholder=False):
    """Render charts for a single agenda section."""
    charts = agenda.get("charts", [])
    if not charts:
        st.info("No charts configured for this section.")
        return

    if len(charts) > 1:
        titles = [ch["title"] for ch in charts]
        selected = st.radio(
            "Select view",
            titles,
            horizontal=True,
            key=f"radio_{agenda['id']}",
            label_visibility="collapsed",
        )
        ch = charts[titles.index(selected)]
    else:
        ch = charts[0]

    st.markdown(
        f'<div style="font-size:14px;font-weight:600;color:#212121;margin-bottom:4px;'
        f'font-family:DM Sans,sans-serif;">{ch["title"]}</div>',
        unsafe_allow_html=True,
    )

    is_horiz = "horizontal" in ch.get("type", "")
    h = 50 + len(ch["labels"]) * 38 if is_horiz else 340
    h = max(h, 280)

    fig = build_chart(ch, height=h)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if ch.get("note"):
        note_class = "chart-note chart-note-warn" if is_placeholder else "chart-note"
        st.markdown(f'<div class="{note_class}">{ch["note"]}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════
# NAVIGATION TABS
# ═══════════════════════════════════════════
tab_landing, tab_explore, tab_dashboard = st.tabs([
    "🏠 Overview",
    "🔍 Explore verticals",
    "📊 Dashboard",
])


# ═══════════════════════════════════════════
# TAB 1: LANDING PAGE — expandable vertical cards
# ═══════════════════════════════════════════
with tab_landing:
    for vi, vert in enumerate(verticals):
        is_live = vert.get("status") == "live"
        badge_class = "badge-live" if is_live else "badge-placeholder"
        badge_text = f"{vert.get('respondents', '—')} respondents" if is_live else "Coming soon"
        findings_html = "".join(f"<li>{f}</li>" for f in vert.get("key_findings", []))

        # Card with key info always visible
        st.markdown(f"""
        <div class="vert-card">
            <div class="vert-card-bar" style="background:{vert['color']}"></div>
            <div class="vert-card-header">
                <span class="vert-card-icon">{vert['icon']}</span>
                <span class="vert-card-name">{vert['name']}</span>
                <span class="vert-card-badge {badge_class}">{badge_text}</span>
            </div>
            <div class="vert-card-summary">{vert['summary']}</div>
            <ul class="vert-card-findings">{findings_html}</ul>
        </div>
        """, unsafe_allow_html=True)

        # Expandable agenda sections inside each vertical
        agendas = vert.get("agendas", [])
        agenda_count = len(agendas)
        chart_count = sum(len(a.get("charts", [])) for a in agendas)

        with st.expander(
            f"{'📊' if is_live else '📋'} Explore {vert['name']} — "
            f"{agenda_count} sections, {chart_count} charts",
            expanded=False,
        ):
            if not is_live:
                st.markdown(
                    '<div class="placeholder-banner">'
                    '<strong>⚠️ Placeholder data</strong> — This section shows sample charts to '
                    'illustrate the layout. Replace with actual survey data in '
                    '<code>survey_data.json</code> and update the status to "live".</div>',
                    unsafe_allow_html=True,
                )

            for agenda in agendas:
                st.markdown(
                    f"**{agenda['name']}** — {agenda.get('summary', '')}",
                )
                render_agenda_charts(agenda, is_placeholder=not is_live)
                st.markdown("---")


# ═══════════════════════════════════════════
# TAB 2: EXPLORE — pick a vertical, deep dive
# ═══════════════════════════════════════════
with tab_explore:
    vert_names = [f"{v['icon']} {v['name']}" for v in verticals]
    selected_vi = st.selectbox("Select a media vertical", vert_names, key="explore_select")
    vert = verticals[vert_names.index(selected_vi)]
    is_live = vert.get("status") == "live"

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(
            f'<div style="font-size:20px;font-weight:600;font-family:DM Sans,sans-serif;">'
            f'{vert["icon"]} {vert["name"]}</div>'
            f'<div style="font-size:13px;color:#717171;margin-top:4px;font-family:DM Sans,sans-serif;">'
            f'{vert["summary"]}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        badge_text = f"✅ {vert.get('respondents', '—')} resp." if is_live else "⏳ Coming soon"
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-num" style="font-size:14px;">{badge_text}</div>'
            f'<div class="kpi-label">Status</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        agenda_count = len(vert.get("agendas", []))
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-num">{agenda_count}</div>'
            f'<div class="kpi-label">Sections</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if not is_live:
        st.markdown(
            '<div class="placeholder-banner">'
            '<strong>⚠️ Placeholder data</strong> — Charts below use sample data. '
            'Replace in <code>survey_data.json</code> when your real data is ready.</div>',
            unsafe_allow_html=True,
        )

    # Agenda sections
    for agenda in vert.get("agendas", []):
        with st.expander(f"📌 {agenda['name']}", expanded=True):
            st.markdown(
                f'<div style="font-size:13px;color:#717171;margin-bottom:12px;'
                f'font-family:DM Sans,sans-serif;">{agenda.get("summary","")}</div>',
                unsafe_allow_html=True,
            )
            render_agenda_charts(agenda, is_placeholder=not is_live)


# ═══════════════════════════════════════════
# TAB 3: DASHBOARD — all charts at a glance
# ═══════════════════════════════════════════
with tab_dashboard:
    # KPIs
    sample = DATA.get("sample", {})
    kpis = [
        (len(verticals), "Verticals"),
        (live_count, "Live"),
        (len(verticals) - live_count, "Placeholder"),
        (sample.get("total", 0), "Gaming Resp."),
        (total_charts, "Total Charts"),
    ]
    cols = st.columns(len(kpis))
    for col, (num, label) in zip(cols, kpis):
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-num">{num}</div>'
            f'<div class="kpi-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Filter by vertical
    dash_filter = st.multiselect(
        "Filter by vertical",
        [f"{v['icon']} {v['name']}" for v in verticals],
        default=[f"{v['icon']} {v['name']}" for v in verticals],
        key="dash_filter",
    )
    selected_ids = set()
    for label in dash_filter:
        for v in verticals:
            if f"{v['icon']} {v['name']}" == label:
                selected_ids.add(v["id"])

    # All charts in 2-col grid
    all_charts = []
    for vert in verticals:
        if vert["id"] not in selected_ids:
            continue
        for agenda in vert.get("agendas", []):
            for ch in agenda.get("charts", []):
                all_charts.append((vert, agenda, ch))

    for i in range(0, len(all_charts), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(all_charts):
                break
            vert, agenda, ch = all_charts[idx]
            with col:
                is_live = vert.get("status") == "live"
                status_dot = "🟢" if is_live else "🟡"
                st.markdown(
                    f'<div style="font-size:13px;font-weight:600;font-family:DM Sans,sans-serif;">'
                    f'{status_dot} {vert["icon"]} {vert["name"]} — {agenda["name"]}</div>'
                    f'<div style="font-size:11px;color:#717171;margin-bottom:8px;'
                    f'font-family:DM Sans,sans-serif;">{ch["title"]}</div>',
                    unsafe_allow_html=True,
                )

                is_horiz = "horizontal" in ch.get("type", "")
                h = 40 + len(ch["labels"]) * 28 if is_horiz else 240
                h = max(h, 220)

                fig = build_chart(ch, height=h)
                fig.update_layout(
                    legend=dict(font=dict(size=9)),
                    margin=dict(l=5, r=5, t=5, b=5),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:12px;color:#999;padding:.5rem 0;">'
    'Media Industry Report 2025 — Edit <code>survey_data.json</code> to update. '
    'Push to GitHub to redeploy.</div>',
    unsafe_allow_html=True,
)
