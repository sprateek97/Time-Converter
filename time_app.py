import streamlit as st

# ---------- Helpers ----------
def dec_to_hm(dec_hours: float):
    sign = -1 if dec_hours < 0 else 1
    dec_hours = abs(dec_hours)
    hours = int(dec_hours)
    minutes = round((dec_hours - hours) * 60)
    # Handle 60-minute rollover
    if minutes == 60:
        hours += 1
        minutes = 0
    return sign * hours, minutes

def hm_to_dec(hhmm: str):
    hhmm = hhmm.strip()
    neg = hhmm.startswith('-')
    if neg:
        hhmm = hhmm[1:].strip()

    if ':' not in hhmm:
        # Allow plain hours like "6" or "6.5"
        try:
            val = float(hhmm)
            return -val if neg else val
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM or a number like 6.5.")

    parts = hhmm.split(':')
    if len(parts) != 2:
        raise ValueError("Invalid HH:MM format.")
    h, m = parts
    h = int(h)
    if m.strip() == '':
        m = 0
    else:
        m = int(m)
    if m < 0 or m >= 60:
        raise ValueError("Minutes must be between 0 and 59.")
    val = h + m / 60
    return -val if neg else val

def format_hm(hours: int, minutes: int):
    sign = '-' if hours < 0 else ''
    h = abs(hours)
    return f"{sign}{h:02d}:{minutes:02d}"

def round_decimal(val: float, mode: str):
    if mode == "No rounding":
        return val
    if mode == "1 decimal":
        return round(val, 1)
    if mode == "2 decimals":
        return round(val, 2)
    if mode == "3 decimals":
        return round(val, 3)
    return val

def round_minutes(h: int, m: int, mode: str):
    if mode != "Nearest minute":
        return h, m
    # Already in minutes; ensure rollover handled
    if m == 60:
        return h + 1, 0
    return h, m

# ---------- UI ----------
st.set_page_config(page_title="Time Converter", page_icon="⏱️", layout="centered")
st.title("⏱️ Time Converter & Subtractor")

st.markdown("Convert decimal hours ↔ HH:MM and subtract times easily.")

with st.expander("Settings"):
    rounding_choice = st.selectbox(
        "Rounding",
        ["No rounding", "1 decimal", "2 decimals", "3 decimals", "Nearest minute"],
        index=2
    )

tab1, tab2, tab3, tab4 = st.tabs(["Decimal → HH:MM", "HH:MM → Decimal", "Subtract (decimal)", "Subtract (HH:MM)"])

with tab1:
    st.subheader("Decimal to HH:MM")
    dec = st.text_input("Enter decimal hours (e.g., 6.8 or -1.25)", "6.8")
    if st.button("Convert to HH:MM", key="d2hm"):
        try:
            dec_val = float(dec)
            h, m = dec_to_hm(dec_val)
            h, m = round_minutes(h, m, rounding_choice)
            st.success(f"Result: {format_hm(h, m)}")
        except Exception as e:
            st.error(str(e))

with tab2:
    st.subheader("HH:MM to Decimal")
    hm = st.text_input("Enter time HH:MM (e.g., 06:38 or -01:15)", "06:38")
    if st.button("Convert to decimal", key="hm2d"):
        try:
            dec_val = hm_to_dec(hm)
            dec_val = round_decimal(dec_val, rounding_choice)
            st.success(f"Result: {dec_val}")
        except Exception as e:
            st.error(str(e))

with tab3:
    st.subheader("Subtract decimal hours (A − B)")
    a = st.text_input("A (decimal hours)", "6.8")
    b = st.text_input("B (decimal hours)", "6.63")
    if st.button("Compute A − B (decimal)", key="sub_dec"):
        try:
            a_val = float(a)
            b_val = float(b)
            diff = a_val - b_val
            # Show both decimal and HH:MM
            h, m = dec_to_hm(diff)
            h, m = round_minutes(h, m, rounding_choice)
            diff_dec = round_decimal(diff, rounding_choice)
            st.info(f"Decimal: {diff_dec}")
            st.success(f"HH:MM: {format_hm(h, m)}")
        except Exception as e:
            st.error(str(e))

with tab4:
    st.subheader("Subtract HH:MM (A − B)")
    a_hm = st.text_input("A (HH:MM)", "06:48")
    b_hm = st.text_input("B (HH:MM)", "06:38")
    if st.button("Compute A − B (HH:MM)", key="sub_hm"):
        try:
            a_val = hm_to_dec(a_hm)
            b_val = hm_to_dec(b_hm)
            diff = a_val - b_val
            h, m = dec_to_hm(diff)
            h, m = round_minutes(h, m, rounding_choice)
            diff_dec = round_decimal(diff, rounding_choice)
            st.info(f"Decimal: {diff_dec}")
            st.success(f"HH:MM: {format_hm(h, m)}")
        except Exception as e:
            st.error(str(e))

st.caption("Tip: Negative results are supported (e.g., 05:00 − 06:15 = -01:15).")
