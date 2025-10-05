import streamlit as st

# ---------- Helpers ----------
def dec_to_hm(dec_hours: float):
    sign = -1 if dec_hours < 0 else 1
    dec_hours = abs(dec_hours)
    hours = int(dec_hours)
    minutes = round((dec_hours - hours) * 60)
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
        try:
            val = float(hhmm)
            return -val if neg else val
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM or a number like 6.5.")

    parts = hhmm.split(':')
    if len(parts) not in (2, 3):
        raise ValueError("Invalid time format. Use HH:MM or HH:MM:SS.")

    h = int(parts[0])
    m = int(parts[1]) if parts[1] else 0
    s = int(parts[2]) if len(parts) == 3 else 0

    if m < 0 or m >= 60 or s < 0 or s >= 60:
        raise ValueError("Minutes/seconds must be between 0 and 59.")

    val = h + m / 60 + s / 3600
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
    if m == 60:
        return h + 1, 0
    return h, m

# ---------- UI ----------
st.set_page_config(page_title="Time Tools", page_icon="⏱️", layout="centered")
st.title("⏱️ Time Conversion & Calculation Suite")

with st.expander("Settings"):
    rounding_choice = st.selectbox(
        "Rounding",
        ["No rounding", "1 decimal", "2 decimals", "3 decimals", "Nearest minute"],
        index=2
    )

tab1, tab2, tab3 = st.tabs([
    "Decimal → HH:MM",
    "HH:MM → Decimal",
    "Multi-time Average"
])

# --- Decimal to HH:MM ---
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

# --- HH:MM to Decimal ---
with tab2:
    st.subheader("HH:MM to Decimal")
    hm = st.text_input("Enter time HH:MM or HH:MM:SS", "06:38")
    if st.button("Convert to decimal", key="hm2d"):
        try:
            dec_val = hm_to_dec(hm)
            dec_val = round_decimal(dec_val, rounding_choice)
            st.success(f"Result: {dec_val}")
        except Exception as e:
            st.error(str(e))

# --- Multi-time Average ---
with tab3:
    st.subheader("Time to Decimal Converter & Average Calculator")
    st.write("Enter times in `HH:MM` or `HH:MM:SS` format, one per line:")
    time_input = st.text_area("Times", placeholder="e.g.\n2:30\n3:45\n1:15\n4:00")
    if st.button("Convert & Calculate Average", key="avg_calc"):
        if time_input.strip():
            times = time_input.strip().split("\n")
            decimal_times = []
            try:
                for t in times:
                    decimal_times.append(hm_to_dec(t))
                average_decimal = sum(decimal_times) / len(decimal_times)
                avg_hours = int(average_decimal)
                avg_minutes = int((average_decimal - avg_hours) * 60)
                avg_seconds = int((((average_decimal - avg_hours) * 60) - avg_minutes) * 60)

                st.subheader("Results")
                st.write("**Decimal times:**", [round(d, 4) for d in decimal_times])
                st.write(f"**Average (decimal):** {round(average_decimal, 4)} hours")
                st.write(f"**Average (HH:MM:SS):** {avg_hours:02d}:{avg_minutes:02d}:{avg_seconds:02d}")
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Please enter at least one time value.")





