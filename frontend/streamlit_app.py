import os
import sys
import uuid
from html import escape
from typing import Any, Dict, List, Optional

import streamlit as st
from langgraph.types import Command


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.graph.travel_graph import travel_graph  


st.set_page_config(
    page_title="TravelMind AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --tm-bg-0: #0E1E1B;
  --tm-bg-1: #14302A;
  --tm-paper: #FBF8F1;
  --tm-paper-dim: #F1EDE1;
  --tm-ink: #1C2420;
  --tm-muted: #5D6660;
  --tm-border: #E1DAC6;
  --tm-red: #B5473C;
  --tm-blue: #3D6E8C;
  --tm-gold: #C79A46;
  --tm-serif: "Fraunces", Georgia, serif;
  --tm-sans: "Inter", -apple-system, sans-serif;
  --tm-mono: "IBM Plex Mono", ui-monospace, monospace;
}

/* -- app shell ------------------------------------------------------- */
.stApp {
  background: radial-gradient(1400px 800px at 15% -10%, #1B3A32 0%, transparent 60%),
              linear-gradient(180deg, var(--tm-bg-0), #0B1815 90%);
}
.block-container { padding-top: 1.4rem; max-width: 1180px; }
html, body, [class*="css"] { font-family: var(--tm-sans); }

/* -- sidebar ---------------------------------------------------------- */
[data-testid="stSidebar"] {
  background: #0F211D;
  border-right: 1px solid rgba(199,154,70,0.18);
}
[data-testid="stSidebar"] * { color: var(--tm-paper) !important; }
.tm-side-label {
  font-family: var(--tm-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  color: var(--tm-gold) !important;
  text-transform: uppercase;
  margin-bottom: 0.2rem;
}
.tm-side-thread {
  font-family: var(--tm-mono);
  font-size: 0.78rem;
  color: #C9D6CF !important;
  background: rgba(255,255,255,0.05);
  border: 1px dashed rgba(199,154,70,0.35);
  border-radius: 4px;
  padding: 0.35rem 0.5rem;
  word-break: break-all;
}
.tm-side-note {
  font-size: 0.78rem;
  color: #9FB0A8 !important;
  line-height: 1.5;
  margin-top: 0.6rem;
}
.tm-side-note code {
  background: rgba(255,255,255,0.08);
  color: var(--tm-gold) !important;
  padding: 0.05rem 0.3rem;
  border-radius: 3px;
}

/* -- signature motif: airmail stripe ---------------------------------- */
.tm-airmail-strip {
  height: 7px;
  background: repeating-linear-gradient(
    45deg,
    var(--tm-red) 0 9px,
    var(--tm-paper) 9px 12px,
    var(--tm-blue) 12px 21px,
    var(--tm-paper) 21px 24px
  );
}

/* -- hero --------------------------------------------------------------- */
.tm-hero {
  position: relative;
  background: linear-gradient(155deg, #1B3A32 0%, #10241F 100%);
  border: 1px solid rgba(199,154,70,0.3);
  border-radius: 6px;
  padding: 0;
  overflow: hidden;
  margin-bottom: 1.4rem;
  box-shadow: 0 18px 40px rgba(0,0,0,0.35);
}
.tm-hero-body { padding: 1.6rem 2rem 1.7rem; }
.tm-hero-eyebrow {
  font-family: var(--tm-mono);
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  color: var(--tm-gold);
  text-transform: uppercase;
}
.tm-hero h1 {
  font-family: var(--tm-serif);
  font-weight: 600;
  font-size: 2.1rem;
  color: var(--tm-paper);
  margin: 0.25rem 0 0.4rem 0;
  letter-spacing: -0.01em;
}
.tm-hero p {
  color: #C9D6CF;
  font-size: 0.95rem;
  margin: 0;
  max-width: 46rem;
}
.tm-hero-stamp {
  position: absolute;
  top: 1.1rem;
  right: 1.4rem;
  border: 2px dashed rgba(199,154,70,0.55);
  border-radius: 3px;
  padding: 0.4rem 0.6rem;
  transform: rotate(4deg);
  text-align: center;
  color: var(--tm-gold);
  font-family: var(--tm-mono);
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  line-height: 1.3;
}

/* -- section headers ------------------------------------------------- */
.tm-section-head { margin: 0.4rem 0 1rem 0; }
.tm-eyebrow {
  font-family: var(--tm-mono);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--tm-gold);
}
.tm-h2 {
  font-family: var(--tm-serif);
  font-weight: 600;
  font-size: 1.5rem;
  color: var(--tm-paper);
  margin: 0.2rem 0 0.25rem 0;
}
.tm-lede { color: #B8C6BE; font-size: 0.9rem; margin: 0; }

/* -- ticket / card ----------------------------------------------------- */
.tm-card {
  background: var(--tm-paper);
  border: 1px solid var(--tm-border);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 12px 28px rgba(0,0,0,0.28);
  margin-bottom: 1rem;
}
.tm-card-head {
  padding: 0.85rem 1.1rem 0.7rem;
  border-bottom: 1px dashed rgba(28,36,32,0.22);
  position: relative;
}
.tm-card-body { padding: 0.85rem 1.1rem 1.05rem; }
.tm-card-title {
  font-family: var(--tm-serif);
  font-weight: 600;
  font-size: 1.15rem;
  color: var(--tm-ink);
}
.tm-card-meta {
  font-family: var(--tm-mono);
  font-size: 0.7rem;
  letter-spacing: 0.06em;
  color: var(--tm-muted);
  margin-top: 0.15rem;
}
.tm-card-text {
  font-size: 0.88rem;
  color: var(--tm-ink);
  line-height: 1.55;
  margin: 0 0 0.5rem 0;
}
.tm-card-sublabel {
  font-family: var(--tm-mono);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--tm-blue);
  margin: 0.6rem 0 0.3rem 0;
}
.tm-card-list { margin: 0; padding-left: 1.1rem; }
.tm-card-list li { color: var(--tm-ink); font-size: 0.86rem; margin-bottom: 0.2rem; }

.tm-card-accent .tm-card-head { background: #FDF3E7; }

/* stamp-style pill, used for prices / ratings / status */
.tm-stamp {
  display: inline-block;
  font-family: var(--tm-mono);
  font-size: 0.72rem;
  border: 1.5px dashed rgba(181,71,60,0.55);
  color: var(--tm-red);
  border-radius: 3px;
  padding: 0.12rem 0.45rem;
  transform: rotate(-1deg);
  margin: 0.1rem 0.3rem 0.1rem 0;
}
.tm-stamp.blue { border-color: rgba(61,110,140,0.55); color: var(--tm-blue); transform: rotate(1deg); }
.tm-stamp.gold { border-color: rgba(199,154,70,0.6); color: #8a6a1f; transform: rotate(-0.5deg); }

.tm-list-label {
  font-family: var(--tm-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--tm-gold);
  margin: 0.2rem 0 0.4rem 0.1rem;
}

.tm-empty {
  background: rgba(255,255,255,0.04);
  border: 1px dashed rgba(199,154,70,0.4);
  border-radius: 6px;
  padding: 0.9rem 1.1rem;
  color: #D8CBAE;
  font-size: 0.88rem;
}

.tm-final-label {
  font-family: var(--tm-mono);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--tm-blue);
}
.tm-final-value { font-family: var(--tm-serif); font-size: 1.1rem; color: var(--tm-ink); margin: 0.15rem 0 0.2rem 0; }
.tm-final-sub { font-family: var(--tm-mono); font-size: 0.78rem; color: var(--tm-muted); }
.tm-final-price { font-family: var(--tm-mono); font-size: 0.95rem; color: var(--tm-red); margin-top: 0.35rem; }

.tm-divider {
  border: none;
  border-top: 1px dashed rgba(199,154,70,0.35);
  margin: 1.3rem 0 1.1rem 0;
}

/* -- native widgets, restyled to match the ticket language ------------- */
.stButton>button, .stDownloadButton>button, [data-testid="stFormSubmitButton"] button {
  font-family: var(--tm-mono) !important;
  letter-spacing: 0.04em;
  border-radius: 4px !important;
  border: 1px solid var(--tm-gold) !important;
  background: linear-gradient(180deg, #1B3A32, #143028) !important;
  color: var(--tm-paper) !important;
}
.stButton>button:hover, .stDownloadButton>button:hover { border-color: var(--tm-red) !important; color: var(--tm-paper) !important; }

[data-testid="stRadio"] {
  background: var(--tm-paper);
  border: 1px solid var(--tm-border);
  border-radius: 6px;
  padding: 0.5rem 0.8rem;
}
[data-testid="stRadio"] label { color: var(--tm-ink) !important; font-family: var(--tm-mono); font-size: 0.85rem; }
[data-testid="stRadio"] div[role="radiogroup"] > label {
  border-bottom: 1px dashed rgba(28,36,32,0.15);
  padding: 0.4rem 0.1rem;
}
[data-testid="stRadio"] div[role="radiogroup"] span,
[data-testid="stRadio"] div[role="radiogroup"] p,
[data-testid="stRadio"] div[role="radiogroup"] div {
  color: var(--tm-ink) !important;
}

[data-testid="stTextArea"] textarea, [data-testid="stTextArea"] label {
  font-family: var(--tm-mono) !important;
  background: var(--tm-paper) !important;
  color: var(--tm-ink) !important;
  border-radius: 6px !important;
}
[data-testid="stTextArea"] textarea::placeholder {
  color: #6B736D !important;
  opacity: 1 !important;
}
[data-testid="stTextArea"] textarea {
  caret-color: var(--tm-ink) !important;
}
.stTextArea label p { color: var(--tm-paper) !important; }

[data-testid="stSelectbox"] label p { color: var(--tm-paper) !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: var(--tm-paper) !important;
  color: var(--tm-ink) !important;
  border-color: var(--tm-border) !important;
}

[data-testid="stForm"] {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(199,154,70,0.25);
  border-radius: 8px;
  padding: 1.2rem 1.3rem;
}

[data-testid="stJson"] {
  background: var(--tm-paper) !important;
  border-radius: 6px;
  border: 1px solid var(--tm-border);
}

.stMarkdown p, .stMarkdown li, .stMarkdown, .stCaption, [data-testid="stCaptionContainer"] {
  color: #D8E2DC;
}

/* Ensure content inside ticket cards stays dark and readable */
.stMarkdown .tm-card .tm-card-text,
.stMarkdown .tm-card .tm-card-title,
.stMarkdown .tm-card .tm-card-meta,
.stMarkdown .tm-card .tm-card-list li,
.stMarkdown .tm-card .tm-final-label,
.stMarkdown .tm-card .tm-final-value,
.stMarkdown .tm-card .tm-final-sub,
.stMarkdown .tm-card .tm-final-price {
  color: var(--tm-ink) !important;
}

/* generic page label used ahead of the trip-description textarea */
.tm-form-label {
  font-family: var(--tm-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--tm-gold);
  margin-bottom: 0.4rem;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    defaults = {
        "thread_id": f"streamlit_{uuid.uuid4().hex[:10]}",
        "result": None,
        "pending_interrupt": None,
        "trip_started": False,
        "trip_text": "",
        "messages": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def graph_config() -> Dict[str, Any]:
    return {"configurable": {"thread_id": st.session_state.thread_id}}


def summarize_flight_option(flight: Dict[str, Any]) -> str:
    stops = flight.get("num_stops", 0)
    stops_txt = "Direct" if stops == 0 else f"{stops} stop(s)"
    arrival = flight.get("arrival_airport", "N/A")
    return (
        f"{flight.get('airline', 'Unknown')} -> {arrival} | "
        f"EUR {flight.get('price', 'N/A')} | "
        f"{flight.get('total_duration', 'N/A')} mins | {stops_txt}"
    )


def summarize_hotel_option(hotel: Dict[str, Any]) -> str:
    return (
        f"{hotel.get('name', 'Unknown')} | EUR {hotel.get('total_price', 'N/A')} | "
        f"Rating {hotel.get('rating', 'N/A')}"
    )


def safe_text(value: Any) -> str:
  if value is None:
    return ""
  if isinstance(value, dict):
    parts = []
    recommendation = value.get("recommendation")
    reason = value.get("reason")
    if recommendation:
      parts.append(str(recommendation))
    if reason:
      parts.append(str(reason))
    if not parts:
      return str(value)
    return "\n\n".join(parts)
  if isinstance(value, list):
    return "\n".join(str(item) for item in value)
  return str(value)


def default_hotel_selection() -> Dict[str, Any]:
  """Fallback hotel payload when no hotel options are returned."""
  return {
    "name": "No hotel selected (auto-continued)",
    "price_per_night": 0,
    "total_price": 0,
    "rating": 0,
    "amenities": [],
  }


def invoke_graph(payload: Any) -> Dict[str, Any]:
    return travel_graph.invoke(payload, config=graph_config())


def process_result_loop(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Auto-resume only non-user decisions.
    Keep user decisions (flight/hotel/budget) as pending interrupts.
    """
    while "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0].value

        # Auto-continue after destination preview has been shown to the user.
        if "destinations" in interrupt_data and st.session_state.get("dest_preview_continue"):
            st.session_state.dest_preview_continue = False
            result = invoke_graph(Command(resume=True))
            continue

        # If hotels list is empty, safely continue without manual selection.
        if "hotels" in interrupt_data and not interrupt_data.get("hotels"):
            st.warning("No hotels were returned for this destination. Continuing automatically.")
            result = invoke_graph(Command(resume=default_hotel_selection()))
            continue

        st.session_state.pending_interrupt = interrupt_data
        st.session_state.result = result
        return result

    st.session_state.pending_interrupt = None
    st.session_state.result = result
    return result


def start_trip(trip_text: str) -> None:
    st.session_state.trip_text = trip_text
    st.session_state.trip_started = True
    st.session_state.pending_interrupt = None
    st.session_state.result = None
    st.session_state.messages = []
    st.session_state.dest_preview_continue = False

    initial_state = {
        "user_input": trip_text,
        "budget_adjustment_attempted": False,
    }
    result = invoke_graph(initial_state)
    process_result_loop(result)


def render_follow_up(interrupt_data: Dict[str, Any]) -> None:
    message = interrupt_data.get("message", "Please provide missing details.")
    missing_fields = interrupt_data.get("missing_fields", [])

    st.markdown(
        """
        <div class='tm-section-head'>
          <span class='tm-eyebrow'>Required details</span>
          <h2 class='tm-h2'>Need a bit more info</h2>
          <p class='tm-lede'>Add the missing trip fields so the planner can continue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    missing_html = ""
    if missing_fields:
        chips = "".join(
            f"<span class='tm-stamp blue'>{escape(str(field))}</span>" for field in missing_fields
        )
        missing_html = f"<div style='margin-bottom:0.55rem;'>{chips}</div>"

    st.markdown(
        f"""
        <div class='tm-card tm-card-accent'>
          <div class='tm-airmail-strip'></div>
          <div class='tm-card-head'>
            <div class='tm-card-title'>Follow-up question</div>
            <div class='tm-card-meta'>MISSING TRIP FIELDS</div>
          </div>
          <div class='tm-card-body'>
            {missing_html}
            <p class='tm-card-text'>{escape(str(message))}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("follow_up_form", clear_on_submit=False):
        user_reply = st.text_area(
            "Provide missing details",
            placeholder="Example: Start date is 2026-08-10 and end date is 2026-08-14.",
            height=120,
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Continue planning →", type="primary", use_container_width=True)

    if submitted:
        if not user_reply.strip():
            st.warning("Please provide the missing details so planning can continue.")
            return
        result = invoke_graph(Command(resume=user_reply.strip()))
        process_result_loop(result)
        st.rerun()


def render_destination_preview(interrupt_data: Dict[str, Any]) -> None:
    st.markdown(
        """
        <div class='tm-section-head'>
          <span class='tm-eyebrow'>Step 1 · Preview</span>
          <h2 class='tm-h2'>Recommended destinations</h2>
          <p class='tm-lede'>Review each destination and its highlights before selecting flights.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    destinations = interrupt_data.get("destinations", [])
    cols = st.columns(2)
    for idx, dest in enumerate(destinations):
        col = cols[idx % 2]
        with col:
            acts = dest.get("activities", [])[:4]
            acts_html = "".join(f"<li>{escape(a.get('name', 'Activity'))}</li>" for a in acts)
            activities_block = (
                f"<div class='tm-card-sublabel'>Top activities</div><ul class='tm-card-list'>{acts_html}</ul>"
                if acts
                else ""
            )
            card_html = f"""
            <div class='tm-card'>
              <div class='tm-airmail-strip'></div>
              <div class='tm-card-head'>
                <div class='tm-card-title'>{escape(dest.get('name', 'Destination'))}</div>
                <div class='tm-card-meta'>NEAREST AIRPORT &middot; {escape(str(dest.get('airport_city', 'N/A'))).upper()}</div>
              </div>
              <div class='tm-card-body'>
                <p class='tm-card-text'>{escape(dest.get('reason', ''))}</p>
                {activities_block}
              </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<hr class='tm-divider' />", unsafe_allow_html=True)
    if st.button("Continue to flight selection →", type="primary", use_container_width=True):
        st.session_state.dest_preview_continue = True
        result = invoke_graph(Command(resume=True))
        process_result_loop(result)
        st.rerun()


def render_flight_selection(interrupt_data: Dict[str, Any]) -> None:
    rec = interrupt_data.get("recommended_flight", {})
    st.markdown(
        f"""
        <div class='tm-section-head'>
          <span class='tm-eyebrow'>Step 2 · Flights</span>
          <h2 class='tm-h2'>Select your flight</h2>
        </div>
        <div class='tm-card tm-card-accent'>
          <div class='tm-airmail-strip'></div>
          <div class='tm-card-head'>
            <div class='tm-card-title'>AI recommendation</div>
            <div class='tm-card-meta'>{escape(str(rec.get('airline', 'N/A'))).upper()} &rarr; {escape(str(rec.get('arrival_airport', 'N/A'))).upper()}</div>
          </div>
          <div class='tm-card-body'>
            <p class='tm-card-text'>{escape(rec.get('reason', ''))}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    flights = interrupt_data.get("flights", [])
    if not flights:
        st.markdown(
            "<div class='tm-empty'>No flights returned. Please try a different trip description.</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown("<div class='tm-list-label'>Available flights</div>", unsafe_allow_html=True)
    options = [summarize_flight_option(f) for f in flights]
    selected_label = st.radio(
        "Available flights", options, key="flight_choice_radio", label_visibility="collapsed"
    )

    if st.button("Confirm flight →", type="primary", use_container_width=True):
        selected_idx = options.index(selected_label)
        selected_flight = flights[selected_idx]
        result = invoke_graph(Command(resume=selected_flight))
        process_result_loop(result)
        st.rerun()


def render_hotel_selection(interrupt_data: Dict[str, Any]) -> None:
    rec = interrupt_data.get("recommended", {})
    st.markdown(
        f"""
        <div class='tm-section-head'>
          <span class='tm-eyebrow'>Step 3 · Hotels</span>
          <h2 class='tm-h2'>Select your primary hotel</h2>
        </div>
        <div class='tm-card tm-card-accent'>
          <div class='tm-airmail-strip'></div>
          <div class='tm-card-head'>
            <div class='tm-card-title'>AI recommendation</div>
            <div class='tm-card-meta'>{escape(str(rec.get('hotel_name', 'N/A'))).upper()} &middot; {escape(str(rec.get('city', 'N/A'))).upper()}</div>
          </div>
          <div class='tm-card-body'>
            <p class='tm-card-text'>{escape(rec.get('reason', ''))}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    hotels = interrupt_data.get("hotels", [])
    if not hotels:
        st.markdown(
            "<div class='tm-empty'>No hotels available for selection. The workflow will continue automatically.</div>",
            unsafe_allow_html=True,
        )
        if st.button("Continue →", use_container_width=True):
            result = invoke_graph(Command(resume=default_hotel_selection()))
            process_result_loop(result)
            st.rerun()
        return

    st.markdown("<div class='tm-list-label'>Available hotels</div>", unsafe_allow_html=True)
    options = [summarize_hotel_option(h) for h in hotels]
    selected_label = st.radio(
        "Available hotels", options, key="hotel_choice_radio", label_visibility="collapsed"
    )

    if st.button("Confirm hotel →", type="primary", use_container_width=True):
        selected_idx = options.index(selected_label)
        selected_hotel = hotels[selected_idx]
        result = invoke_graph(Command(resume=selected_hotel))
        process_result_loop(result)
        st.rerun()


def render_budget_decision(interrupt_data: Dict[str, Any]) -> None:
    advisor_payload = interrupt_data.get("advisor_recommendation", {})
    advisor_text = safe_text(advisor_payload)

    st.markdown(
        f"""
        <div class='tm-section-head'>
          <span class='tm-eyebrow'>Step 4 · Budget</span>
          <h2 class='tm-h2'>Budget decision</h2>
        </div>
        <div class='tm-card'>
          <div class='tm-airmail-strip'></div>
          <div class='tm-card-head'>
            <div class='tm-card-title'>Advisor recommendation</div>
          </div>
          <div class='tm-card-body'>
            <p class='tm-card-text'>{escape(advisor_text)}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='tm-list-label'>Budget summary</div>", unsafe_allow_html=True)
    st.json(interrupt_data.get("budget_summary", {}))

    suggestions = interrupt_data.get("suggestions", [])
    if suggestions:
        rows = "".join(
            f"<li>{escape(str(s.get('type', 'option')))} &mdash; "
            f"<span class='tm-stamp blue'>Saves EUR {escape(str(s.get('savings', 'N/A')))}</span></li>"
            for s in suggestions
        )
        st.markdown(
            f"""
            <div class='tm-card' style='margin-top:0.8rem;'>
              <div class='tm-card-head'><div class='tm-card-title' style='font-size:1rem;'>Savings suggestions</div></div>
              <div class='tm-card-body'><ul class='tm-card-list'>{rows}</ul></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='tm-list-label'>Choose action</div>", unsafe_allow_html=True)
    action = st.radio(
        "Choose action",
        ["keep_current", "switch_hotel", "switch_flight"],
        format_func=lambda x: {
            "keep_current": "Keep current",
            "switch_hotel": "Switch hotel",
            "switch_flight": "Switch flight",
        }[x],
        key="budget_action_radio",
        label_visibility="collapsed",
    )

    decision: Dict[str, Any] = {"action": action}

    if action in {"switch_hotel", "switch_flight"}:
        relevant = [s for s in suggestions if s.get("type") == action.split("_")[1]]
        if not relevant:
            st.markdown(
                "<div class='tm-empty'>No cheaper alternatives available for this action.</div>",
                unsafe_allow_html=True,
            )
            decision = {"action": "keep_current"}
        else:
            labels = []
            for s in relevant:
                opt = s.get("option", {})
                if action == "switch_hotel":
                    labels.append(f"{opt.get('name', 'Hotel')} | EUR {opt.get('total_price', 'N/A')}")
                else:
                    labels.append(f"{opt.get('airline', 'Flight')} | EUR {opt.get('price', 'N/A')}")
            selected_label = st.selectbox("Choose replacement", labels, key="budget_swap_select")
            selected_idx = labels.index(selected_label)
            decision = {"action": action, "option": relevant[selected_idx].get("option")}

    if st.button("Apply budget decision →", type="primary", use_container_width=True):
        result = invoke_graph(Command(resume=decision))
        process_result_loop(result)
        st.rerun()


def render_final_result(result: Dict[str, Any]) -> None:
    st.markdown(
        """
        <div class='tm-section-head'>
          <span class='tm-eyebrow'>Complete</span>
          <h2 class='tm-h2'>Your final plan</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        flight = result.get("selected_flight")
        if flight:
            body = f"""
            <div class='tm-final-label'>Flight</div>
            <div class='tm-final-value'>{escape(str(flight.get('airline', 'N/A')))}</div>
            <div class='tm-final-sub'>{escape(str(flight.get('departure_airport', 'N/A')))} &rarr; {escape(str(flight.get('arrival_airport', 'N/A')))}</div>
            <div class='tm-final-price'>EUR {escape(str(flight.get('price', 'N/A')))}</div>
            """
        else:
            body = "<div class='tm-final-label'>Flight</div><div class='tm-final-sub'>Not selected</div>"
        st.markdown(f"<div class='tm-card'><div class='tm-airmail-strip'></div><div class='tm-card-body'>{body}</div></div>", unsafe_allow_html=True)

    with c2:
        hotel = result.get("selected_hotel")
        if hotel:
            body = f"""
            <div class='tm-final-label'>Primary hotel</div>
            <div class='tm-final-value'>{escape(str(hotel.get('name', 'N/A')))}</div>
            <div class='tm-final-sub'>Rating: {escape(str(hotel.get('rating', 'N/A')))}</div>
            <div class='tm-final-price'>EUR {escape(str(hotel.get('total_price', 'N/A')))}</div>
            """
        else:
            body = "<div class='tm-final-label'>Primary hotel</div><div class='tm-final-sub'>Not selected</div>"
        st.markdown(f"<div class='tm-card'><div class='tm-airmail-strip'></div><div class='tm-card-body'>{body}</div></div>", unsafe_allow_html=True)

    with c3:
        budget = result.get("budget_summary")
        if budget:
            body = f"""
            <div class='tm-final-label'>Budget</div>
            <div class='tm-final-value'>EUR {escape(str(budget.get('total_cost', 'N/A')))}</div>
            <div class='tm-final-sub'>Remaining: EUR {escape(str(budget.get('remaining_budget', 'N/A')))}</div>
            <span class='tm-stamp gold'>{escape(str(budget.get('budget_status', ''))).upper()}</span>
            """
        else:
            body = "<div class='tm-final-label'>Budget</div><div class='tm-final-sub'>No budget summary</div>"
        st.markdown(f"<div class='tm-card'><div class='tm-airmail-strip'></div><div class='tm-card-body'>{body}</div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='tm-divider' />", unsafe_allow_html=True)
    st.markdown("<div class='tm-list-label'>Itinerary</div>", unsafe_allow_html=True)
    formatted = result.get("formatted_itinerary", "")
    if formatted:
        st.text_area("", value=formatted, height=420, label_visibility="collapsed")
        st.download_button(
            "Download itinerary",
            data=formatted,
            file_name="travelmind_itinerary.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.markdown("<div class='tm-empty'>No formatted itinerary returned.</div>", unsafe_allow_html=True)


def reset_app() -> None:
    for key in [
        "result",
        "pending_interrupt",
        "trip_started",
        "trip_text",
        "messages",
        "dest_preview_continue",
    ]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.thread_id = f"streamlit_{uuid.uuid4().hex[:10]}"


def main() -> None:
    apply_theme()
    init_state()

    st.markdown(
        f"""
        <div class='tm-hero'>
          <div class='tm-airmail-strip'></div>
          <div class='tm-hero-body'>
            <span class='tm-hero-eyebrow'>Boarding pass &middot; draft itinerary</span>
            <h1>TravelMind AI Planner</h1>
            <p>Build complete multi-city trips with AI-assisted flight and hotel decisions.</p>
          </div>
          <div class='tm-hero-stamp'>✈<br/>THREAD<br/>{escape(st.session_state.thread_id[-8:])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("<div class='tm-side-label'>Session</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tm-side-thread'>{escape(st.session_state.thread_id)}</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='tm-side-note'><code>SERP_API_KEY</code> and Gemini credentials must be configured in your environment.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
        if st.button("Start new trip", use_container_width=True):
            reset_app()
            st.rerun()

    if not st.session_state.trip_started:
        st.markdown("<div class='tm-form-label'>Describe your trip</div>", unsafe_allow_html=True)
        with st.form("trip_form", clear_on_submit=False):
            trip_text = st.text_area(
                "Describe your trip",
                placeholder=(
                    "Example: I want to travel to India for a 7-day trip from Frankfurt from 1st August till 7th August."
                    "Budget is EUR 4000. My interests are food, culture and nature. Plan a trip for me."
                ),
                height=140,
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Generate plan →", type="primary", use_container_width=True)

        if submitted:
            if not trip_text.strip():
                st.warning("Please enter your trip details.")
            else:
                with st.spinner("Planning your trip..."):
                    start_trip(trip_text.strip())
                st.rerun()
        return

    pending = st.session_state.pending_interrupt
    result = st.session_state.result

    if pending:
      if pending.get("type") == "follow_up":
        render_follow_up(pending)
      elif "destinations" in pending:
        render_destination_preview(pending)
      elif "flights" in pending:
        render_flight_selection(pending)
      elif "hotels" in pending:
        render_hotel_selection(pending)
      elif "valid_actions" in pending:
        render_budget_decision(pending)
      else:
        st.warning("Unhandled interrupt payload. Check graph interrupt schema.")
        st.json(pending)
    elif result:
      render_final_result(result)
    else:
      st.info("No result yet. Start a new trip from the sidebar.")


if __name__ == "__main__":
    main()