"""Calendar 2026 — Editorial Edition (Compact, Single-Screen)
Run: streamlit run calendar_pro.py
"""
import calendar
from datetime import date
import streamlit as st

YEAR = 2026

CA_HOLIDAYS = {
    date(2026, 1, 1):  "New Year's Day",
    date(2026, 2, 16): "Family Day",
    date(2026, 4, 3):  "Good Friday",
    date(2026, 4, 6):  "Easter Monday",
    date(2026, 5, 18): "Victoria Day",
    date(2026, 7, 1):  "Canada Day",
    date(2026, 8, 3):  "NB Day",
    date(2026, 9, 7):  "Labour Day",
    date(2026, 9, 30): "Truth & Reconciliation",
    date(2026, 10, 12):"Thanksgiving",
    date(2026, 11, 11):"Remembrance Day",
    date(2026, 12, 25):"Christmas",
    date(2026, 12, 26):"Boxing Day",
}

IN_HOLIDAYS = {
    date(2026, 1, 14): "Makar Sankranti",
    date(2026, 1, 26): "Republic Day",
    date(2026, 2, 15): "Maha Shivaratri",
    date(2026, 3, 4):  "Holi",
    date(2026, 3, 31): "Mahavir Jayanti",
    date(2026, 5, 1):  "Buddha Purnima",
    date(2026, 8, 15): "Independence Day",
    date(2026, 9, 4):  "Janmashtami",
    date(2026, 9, 14): "Ganesh Chaturthi",
    date(2026, 10, 2): "Gandhi Jayanti",
    date(2026, 10, 19):"Navratri",
    date(2026, 10, 20):"Dussehra",
    date(2026, 11, 7): "Dhanteras",
    date(2026, 11, 8): "Diwali",
    date(2026, 11, 24):"Guru Nanak Jayanti",
    date(2026, 12, 25):"Christmas",
}

MONTH_NAMES = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
MONTH_ABBR = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

st.set_page_config(
    page_title=f"Calendar {YEAR}",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    .block-container {
        padding: 0.75rem 1.5rem 0.5rem !important;
        max-width: 100% !important;
    }
    html, body, .stApp { background: #FAF9F6; color: #1A1A1A; overflow-x: hidden; }
    [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #1A2332;
        padding-bottom: 0.5rem;
        margin-bottom: 0.6rem;
    }
    .brand {
        font-family: 'Fraunces', serif;
        font-size: 1.85rem;
        font-weight: 400;
        color: #1A2332;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    .brand-sub {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #6B6B6B;
        margin-top: 2px;
    }
    .inline-stats {
        display: flex;
        gap: 1.5rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #6B6B6B;
    }
    .inline-stat { text-align: right; line-height: 1.3; }
    .inline-stat .v {
        font-family: 'Fraunces', serif;
        font-size: 1.25rem;
        color: #1A2332;
        text-transform: none;
        letter-spacing: 0;
        font-weight: 400;
        display: block;
    }

    .dow-row {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 3px;
        margin-bottom: 3px;
    }
    .dow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #8B8680;
        padding: 4px 8px 3px;
    }
    .dow.weekend { color: #C6485F; }

    .cal-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 3px;
    }
    .day {
        background: #FFFFFF;
        border: 1px solid #E8E4DA;
        border-radius: 2px;
        padding: 6px 8px;
        height: 62px;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
    }
    .day.muted { background: #F5F2EB; border-color: #EDE8DC; }
    .day.weekend { background: #F5F2EB; }
    .day.ca { background: #FCEFE8; border-color: #E8C8B5; }
    .day.ind { background: #FAF1DC; border-color: #E8D4A0; }
    .day.both { background: #ECEDE0; border-color: #C8CFA8; }
    .day.today { border: 2px solid #1A2332; padding: 5px 7px; }
    .day-num {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.95rem;
        color: #1A1A1A;
        line-height: 1;
    }
    .day.muted .day-num { color: #B8B2A6; }
    .day-num.weekend-num { color: #C6485F; }
    .holiday-tag {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.62rem;
        line-height: 1.15;
        margin-top: auto;
        padding-top: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .holiday-tag.ca { color: #8B2C3F; }
    .holiday-tag.ind { color: #8B5A0F; }
    .today-pill {
        position: absolute;
        top: 4px; right: 6px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #1A2332;
        font-weight: 500;
    }

    .panel-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #1A2332;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #1A2332;
        margin-bottom: 0.5rem;
    }
    .h-row {
        padding: 0.4rem 0;
        border-bottom: 1px solid #E8E4DA;
    }
    .h-row:last-child { border-bottom: none; }
    .h-meta {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.58rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6B6B6B;
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.1rem;
    }
    .h-name {
        font-family: 'Fraunces', serif;
        font-size: 0.9rem;
        color: #1A1A1A;
        line-height: 1.2;
    }
    .h-region {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.55rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin-top: 2px;
    }
    .h-region.ca { color: #C6485F; }
    .h-region.ind { color: #C8841F; }

    .stButton > button {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.62rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        background: transparent !important;
        color: #6B6B6B !important;
        border: 1px solid #D4D0C8 !important;
        border-radius: 2px !important;
        padding: 4px 2px !important;
        height: 26px !important;
        min-height: 26px !important;
    }
    .stButton > button:hover {
        background: #1A2332 !important;
        color: #FAF9F6 !important;
        border-color: #1A2332 !important;
    }
    .stButton > button[kind="primary"] {
        background: #1A2332 !important;
        color: #FAF9F6 !important;
        border-color: #1A2332 !important;
    }

    .month-head {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin: 0.4rem 0 0.35rem;
    }
    .month-head h2 {
        font-family: 'Fraunces', serif;
        font-weight: 400;
        font-size: 1.4rem;
        color: #1A2332;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .month-head .meta {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #8B8680;
    }

    div[data-testid="stHorizontalBlock"] { gap: 0.4rem !important; }
    div[data-testid="column"] { padding: 0 !important; }
    .element-container { margin-bottom: 0 !important; }
    div[data-testid="stMarkdownContainer"] > * { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

today = date.today()
default_month = today.month if today.year == YEAR else 1
if "month" not in st.session_state:
    st.session_state.month = default_month

total_days = 366 if calendar.isleap(YEAR) else 365
weekend_days = sum(1 for m in range(1,13) for d in range(1, calendar.monthrange(YEAR, m)[1]+1)
                    if date(YEAR, m, d).weekday() >= 5)
working_days = total_days - weekend_days - sum(1 for d in CA_HOLIDAYS if d.weekday() < 5)

st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="brand">The Calendar · {YEAR}</div>
        <div class="brand-sub">Canada · India · Edition I</div>
    </div>
    <div class="inline-stats">
        <div class="inline-stat"><span class="v">{total_days}</span>Total Days</div>
        <div class="inline-stat"><span class="v">{working_days}</span>Working Days</div>
        <div class="inline-stat"><span class="v">{len(CA_HOLIDAYS)}</span>CA Holidays</div>
        <div class="inline-stat"><span class="v">{len(IN_HOLIDAYS)}</span>IN Holidays</div>
        <div class="inline-stat"><span class="v" style="font-size:0.85rem;">{today.strftime('%a · %b %d')}</span>Today</div>
    </div>
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns(12, gap="small")
for i, mname in enumerate(MONTH_ABBR, start=1):
    with nav_cols[i-1]:
        is_active = (st.session_state.month == i)
        if st.button(mname, key=f"m{i}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.month = i
            st.rerun()

m = st.session_state.month
left, right = st.columns([3, 1], gap="medium")

with left:
    cal_obj = calendar.Calendar(firstweekday=0)
    weeks = cal_obj.monthdatescalendar(YEAR, m)
    first_day = date(YEAR, m, 1)
    last_day = date(YEAR, m, calendar.monthrange(YEAR, m)[1])

    st.markdown(f"""
    <div class="month-head">
        <h2>{MONTH_NAMES[m-1]}</h2>
        <span class="meta">{first_day.strftime('%b %d').upper()} — {last_day.strftime('%b %d').upper()} · {calendar.monthrange(YEAR, m)[1]} DAYS</span>
    </div>
    """, unsafe_allow_html=True)

    dow_html = '<div class="dow-row">'
    for i, dn in enumerate(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):
        cls = "dow weekend" if i >= 5 else "dow"
        dow_html += f'<div class="{cls}">{dn}</div>'
    dow_html += '</div>'
    st.markdown(dow_html, unsafe_allow_html=True)

    grid_html = '<div class="cal-grid">'
    for week in weeks:
        for day in week:
            in_month = day.month == m
            is_weekend = day.weekday() >= 5
            is_ca = day in CA_HOLIDAYS
            is_in = day in IN_HOLIDAYS
            is_today = (day == today)

            classes = ["day"]
            if not in_month: classes.append("muted")
            elif is_ca and is_in: classes.append("both")
            elif is_ca: classes.append("ca")
            elif is_in: classes.append("ind")
            elif is_weekend: classes.append("weekend")
            if is_today and in_month: classes.append("today")

            num_class = "day-num"
            if in_month and is_weekend and not (is_ca or is_in):
                num_class += " weekend-num"

            cell = f'<div class="{" ".join(classes)}">'
            if is_today and in_month:
                cell += '<div class="today-pill">Today</div>'
            cell += f'<div class="{num_class}">{day.day:02d}</div>'

            if in_month:
                if is_ca:
                    cell += f'<div class="holiday-tag ca">{CA_HOLIDAYS[day]}</div>'
                if is_in and not is_ca:
                    cell += f'<div class="holiday-tag ind">{IN_HOLIDAYS[day]}</div>'
                elif is_in and is_ca:
                    cell += f'<div class="holiday-tag ind" style="font-size:0.55rem;">+ {IN_HOLIDAYS[day]}</div>'
            cell += '</div>'
            grid_html += cell
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel-title">Observances · This Month</div>', unsafe_allow_html=True)

    month_hols = []
    for d, n in CA_HOLIDAYS.items():
        if d.month == m: month_hols.append((d, n, "ca", "Canada"))
    for d, n in IN_HOLIDAYS.items():
        if d.month == m: month_hols.append((d, n, "ind", "India"))
    month_hols.sort(key=lambda x: x[0])

    if month_hols:
        for d, name, region_cls, region_label in month_hols[:4]:
            st.markdown(f"""
            <div class="h-row">
                <div class="h-meta"><span>{d.strftime('%b %d').upper()}</span><span>{d.strftime('%a').upper()}</span></div>
                <div class="h-name">{name}</div>
                <div class="h-region {region_cls}">— {region_label}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="h-row" style="font-style:italic;color:#8B8680;font-family:Fraunces,serif;">None this month.</div>',
                    unsafe_allow_html=True)

    st.markdown('<div style="height:0.6rem;"></div><div class="panel-title">Next Up</div>', unsafe_allow_html=True)
    all_h = [(d, n, "ca", "Canada") for d, n in CA_HOLIDAYS.items()] + \
            [(d, n, "ind", "India") for d, n in IN_HOLIDAYS.items()]
    upcoming = sorted([h for h in all_h if h[0] >= today])[:2]

    for d, name, region_cls, region_label in upcoming:
        days_away = (d - today).days
        away = "Today" if days_away == 0 else "Tomorrow" if days_away == 1 else f"In {days_away}d"
        st.markdown(f"""
        <div class="h-row">
            <div class="h-meta"><span>{d.strftime('%b %d').upper()}</span><span>{away.upper()}</span></div>
            <div class="h-name">{name}</div>
            <div class="h-region {region_cls}">— {region_label}</div>
        </div>
        """, unsafe_allow_html=True)
