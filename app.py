import streamlit as st
import plotly.graph_objects as go
import json
from pathlib import Path

# ═══════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="Gaming Report 2025",
    page_icon="🎮",
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

/* Hide default Streamlit header/footer */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.block-container { padding-top: 0 !important; max-width: 1000px; }

/* Hero banner */
.hero-banner {
    background: #1a1a1a;
    padding: 2.5rem 2rem 2rem;
    border-radius: 0 0 16px 16px;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -15%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(204,41,54,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-block;
    background: #CC2936;
    color: white;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 3px;
    margin-bottom: 0.75rem;
    font-family: 'DM Sans', sans-serif;
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(1.6rem, 4vw, 2.5rem);
    font-weight: 800;
    color: white;
    line-height: 1.15;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}
.hero-desc {
    color: rgba(255,255,255,0.6);
    font-size: 14px;
    max-width: 600px;
    line-height: 1.7;
    font-family: 'DM Sans', sans-serif;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.25rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    flex-wrap: wrap;
}
.hero-stat-num {
    font-size: 24px;
    font-weight: 600;
    color: white;
    font-family: 'DM Sans', sans-serif;
}
.hero-stat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    margin-top: 2px;
    font-family: 'DM Sans', sans-serif;
}

/* KPI cards */
.kpi-card {
    background: #f5f5f5;
    border-radius: 10px;
    padding: 16px 18px;
    text-align: center;
}
.kpi-num {
    font-size: 26px;
    font-weight: 600;
    color: #212121;
    font-family: 'DM Sans', sans-serif;
}
.kpi-label {
    font-size: 11px;
    color: #717171;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 2px;
    font-family: 'DM Sans', sans-serif;
}

/* Chart note */
.chart-note {
    font-size: 12px;
    color: #717171;
    background: #f5f5f5;
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 4px;
    line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
}

/* Agenda header styling */
.agenda-header {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'DM Sans', sans-serif;
}
.agenda-dot {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    display: inline-block;
    flex-shrink: 0;
}
.agenda-title {
    font-size: 15px;
    font-weight: 600;
    color: #212121;
}
.agenda-subtitle {
    font-size: 13px;
    color: #717171;
    margin-top: 2px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #e8e8e8;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 14px;
    padding: 12px 20px;
}

/* Expander tweaks */
.streamlit-expanderHeader {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}

/* Dashboard card */
.dash-card {
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 16px;
    background: white;
}
.dash-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #212121;
    margin-bottom: 2px;
    font-family: 'DM Sans', sans-serif;
}
.dash-card-sub {
    font-size: 11px;
    color: #717171;
    margin-bottom: 8px;
    font-family: 'DM Sans', sans-serif;
}
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
total_charts = sum(len(a.get("charts", [])) for a in DATA["agendas"])


# ═══════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-eyebrow">Gamer Survey 2025</div>
    <div class="hero-title">{DATA['title']}</div>
    <div class="hero-desc">{DATA['description']}</div>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-num">{len(DATA['agendas'])}</div>
            <div class="hero-stat-label">Questions</div>
        </div>
        <div>
            <div class="hero-stat-num">{total_charts}</div>
            <div class="hero-stat-label">Visualizations</div>
        </div>
        <div>
            <div class="hero-stat-num">{DATA.get('sample', {}).get('total', '—')}</div>
            <div class="hero-stat-label">Respondents</div>
        </div>
        <div>
            <div class="hero-stat-num">2–17</div>
            <div class="hero-stat-label">Age Range</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# CHART BUILDER
# ═══════════════════════════════════════════
def build_chart(ch, height=400):
    """Build a Plotly stacked bar chart from chart config."""
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
            fig.add_trace(go.Bar(
                y=ch["labels"],
                x=ds["data"],
                orientation="h",
                **kwargs,
            ))
        else:
            fig.add_trace(go.Bar(
                x=ch["labels"],
                y=ds["data"],
                **kwargs,
            ))

    fig.update_layout(
        barmode="stack",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="DM Sans", size=12, color="#4a4a4a"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.25,
        bargroupgap=0.1,
    )

    # Axis styling
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


# ═══════════════════════════════════════════
# PAGE TABS
# ═══════════════════════════════════════════
tab_survey, tab_dashboard = st.tabs(["📋 Survey", "📊 Dashboard"])


# ═══════════════════════════════════════════
# SURVEY PAGE
# ═══════════════════════════════════════════
with tab_survey:
    for ai, agenda in enumerate(DATA["agendas"]):
        color = agenda.get("color", "#CC2936")
        icon = agenda.get("icon", "📄")
        chart_count = len(agenda.get("charts", []))

        with st.expander(
            f"{icon}  {agenda['name']}  —  {chart_count} chart{'s' if chart_count != 1 else ''}",
            expanded=(ai == 0),
        ):
            st.markdown(
                f'<div style="font-size:13px;color:#717171;margin-bottom:16px;line-height:1.6;">'
                f'{agenda.get("summary", "")}</div>',
                unsafe_allow_html=True,
            )

            # Chart selector if multiple charts
            charts = agenda.get("charts", [])
            if len(charts) > 1:
                chart_titles = [ch["title"] for ch in charts]
                selected = st.radio(
                    "Select view",
                    chart_titles,
                    horizontal=True,
                    key=f"radio_{agenda['id']}",
                    label_visibility="collapsed",
                )
                ch = charts[chart_titles.index(selected)]
            elif len(charts) == 1:
                ch = charts[0]
            else:
                st.info("No charts configured for this section.")
                continue

            # Title
            st.markdown(
                f'<div style="font-size:14px;font-weight:600;color:#212121;margin-bottom:4px;'
                f'font-family:DM Sans,sans-serif;">{ch["title"]}</div>',
                unsafe_allow_html=True,
            )

            # Build chart
            is_horiz = "horizontal" in ch.get("type", "")
            h = 50 + len(ch["labels"]) * 38 if is_horiz else 340
            h = max(h, 280)

            fig = build_chart(ch, height=h)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Note
            if ch.get("note"):
                st.markdown(
                    f'<div class="chart-note">{ch["note"]}</div>',
                    unsafe_allow_html=True,
                )


# ═══════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════
with tab_dashboard:
    # KPI row
    sample = DATA.get("sample", {})
    kpi_data = [
        (sample.get("total", 0), "Total Respondents"),
        (sample.get("age_2_12", 0), "Age 2–12"),
        (sample.get("age_13_17", 0), "Age 13–17"),
        (sample.get("immersive", 0), "Immersive Gamers"),
        (sample.get("non_immersive", 0), "Non-Immersive"),
    ]
    cols = st.columns(len(kpi_data))
    for col, (num, label) in zip(cols, kpi_data):
        col.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-num">{num:,}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # All charts in 2-column grid
    all_charts = []
    for agenda in DATA["agendas"]:
        for ch in agenda.get("charts", []):
            all_charts.append((agenda, ch))

    for i in range(0, len(all_charts), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(all_charts):
                break
            agenda, ch = all_charts[idx]
            with col:
                st.markdown(
                    f'<div class="dash-card">'
                    f'<div class="dash-card-title">'
                    f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
                    f'background:{agenda.get("color","#CC2936")};margin-right:6px;"></span>'
                    f'{agenda["name"]}</div>'
                    f'<div class="dash-card-sub">{ch["title"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                is_horiz = "horizontal" in ch.get("type", "")
                h = 40 + len(ch["labels"]) * 28 if is_horiz else 260
                h = max(h, 240)

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
    '<div style="text-align:center;font-size:12px;color:#999;padding:1rem 0;">'
    'Gaming Report 2025 — Edit <code>survey_data.json</code> to update content. '
    'Push to GitHub and the app auto-refreshes.</div>',
    unsafe_allow_html=True,
)