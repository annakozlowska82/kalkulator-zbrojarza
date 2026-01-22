import streamlit as st
import math

# 1. Ustawienia wyglądu (Granat + Pomarańcz)
st.set_page_config(page_title="Kalkulator Zbrojarza", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: white; }
    section[data-testid="stSidebar"] { background-color: #00152b !important; }
    h1, h2, h3, p, label { color: white !important; }
    .stMetricValue { color: #ff8c00 !important; }
    div[data-baseweb="input"] { background-color: #002b56 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>🏗️ KALKULATOR <span style='color: #ff8c00;'>ZBROJARZA</span></h1>", unsafe_allow_html=True)

opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Kąt gięcia", "Wysokość łuku", "Pręt typu L (Realna Wysokość)"])

def pobierz_wartosc(label, default="0", klucz=None):
    val = st.text_input(label, value=default, key=klucz).replace(',', '.')
    try:
        return float(val) if val else 0.0
    except ValueError:
        return 0.0

# --- SEKCJA: KĄT GIĘCIA ---
if opcja == "Kąt gięcia":
    st.subheader("Obliczanie kątów (Trójkąt)")
    col1, col2 = st.columns(2)
    with col1:
        a = pobierz_wartosc("Przyprostokątna - pion (cm)", klucz="kat_a")
    with col2:
        c = pobierz_wartosc("Przeciwprostokątna - skos (cm)", klucz="kat_c")
        
    if a > 0 and c > 0:
        if c > a:
            kat_rad = math.asin(a / c)
            kat_stopnie = math.degrees(kat_rad)
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Kąt nachylenia", f"{round(kat_stopnie, 2)}°")
            c2.metric("Kąt gięcia maszynowy", f"{round(90 - kat_stopnie, 2)}°")
        else:
            st.error("⚠️ BŁĄD: Skos (przeciwprostokątna) musi być DŁUŻSZY niż pion!")

# --- SEKCJA: WYSOKOŚĆ ŁUKU ---
elif opcja == "Wysokość łuku":
    st.subheader("Obliczanie wysokości łuku")
    col1, col2 = st.columns(2)
    with col1:
        l_luk = pobierz_wartosc("Długość po łuku L (cm)", klucz="luk_l")
    with col2:
        r_luk = pobierz_wartosc("Promień R (cm)", klucz="luk_r")
    
    if r_luk > 0 and l_luk > 0:
        h = r_luk * (1 - math.cos(l_luk / (2 * r_luk)))
        st.metric("Wysokość łuku (h)", f"{round(h, 2)} cm")
        if h > 240:
            st.error(f"❌ GABARYT PRZEKROCZONY! ({round(h, 2)} cm)")
        else:
            st.success("✅ Gabaryt OK")

# --- SEKCJA: PRĘT L ---
elif opcja == "Pręt typu L (Realna Wysokość)":
    st.subheader("Wymiary pręta L z uwzględnieniem łuku")
    fi = pobierz_wartosc("Średnica FI (mm)", "12", klucz="l_fi")
    a_l = pobierz_wartosc("Ramię A (cm)", klucz="l_a")
    b_l = pobierz_wartosc("Ramię B (cm)", klucz="l_b")
    
    if a_l > 0 and b_l > 0:
        skos_l = math.sqrt(a_l**2 + b_l**2)
        r_trzpien = (2 * fi) / 10 # standardowy promień
        r_zew = r_trzpien + (fi / 10)
        h_teo = (a_l * b_l) / skos_l
        h_real = h_teo - (r_zew * (math.sqrt(2) - 1) / math.sqrt(2))
        
        st.metric("REALNA WYSOKOŚĆ (h)", f"{round(h_real, 2)} cm")
        if h_real > 240:
            st.error("❌ GABARYT PRZEKROCZONY!")
        else:
            st.success("✅ Gabaryt OK")
