import streamlit as st
import math

# 1. Konfiguracja barw i wyglądu (Granat + Pomarańcz)
st.set_page_config(page_title="Kalkulator Zbrojarza", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #001f3f; 
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #00152b !important;
    }
    h1, h2, h3, p, label {
        color: white !important;
    }
    .stMetricValue {
        color: #ff8c00 !important;
    }
    div[data-baseweb="input"] {
        background-color: #002b56 !important;
        color: white !important;
    }
    .stAlert {
        background-color: #002b56 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Nagłówek aplikacji
st.markdown("<h1 style='text-align: center; color: white;'>🏗️ KALKULATOR <span style='color: #ff8c00;'>ZBROJARZA</span></h1>", unsafe_allow_html=True)

opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Wysokość łuku", "Pręt typu L (Realna Wysokość)", "Kąt gięcia"])

def pobierz_wartosc(label, default="0"):
    val = st.text_input(label, value=default).replace(',', '.')
    try:
        return float(val) if val else 0.0
    except ValueError:
        return 0.0

# --- SEKCJA 1: ŁUKI ---
if opcja == "Wysokość łuku":
    st.subheader("Obliczanie wysokości (strzałki) łuku")
    col1, col2 = st.columns(2)
    with col1:
        l = pobierz_wartosc("Długość pręta po łuku L (cm)")
    with col2:
        r = pobierz_wartosc("Promień gięcia R (cm)")
    
    if r > 0 and l > 0:
        alfa = l / r
        h_luk = r * (1 - math.cos(alfa / 2))
        
        st.markdown("---")
        st.metric("Wysokość łuku (h)", f"{round(h_luk, 2)} cm")
        
        if h_luk > 240:
            st.error(f"❌ GABARYT PRZEKROCZONY! Wysokość {round(h_luk, 2)} cm przekracza 240 cm.")
        else:
            st.success(f"✅ GABARYT OK - Mieści się w skrajni (Wysokość: {round(h_luk, 2)} cm)")

# --- SEKCJA 2: PRĘTY L ---
elif opcja == "Pręt typu L (Realna Wysokość)":
    st.subheader("Weryfikacja pręta L (z łukiem gięcia)")
    col1, col2 = st.columns(2)
    with col1:
        fi = pobierz_wartosc("Średnica pręta FI (mm)", "12")
        a = pobierz_wartosc("Ramię A - po zewnątrz (cm)")
    with col2:
        r_wew = pobierz_wartosc("Promień trzpienia R (cm)", str((2 * float(fi if fi else 12))/10))
        b = pobierz_wartosc("Ramię B - po zewnątrz (cm)")
    
    if a > 0 and b > 0:
        c = math.sqrt(a**2 + b**2)
        h_teo = (a * b) / c
        r_zew = r_wew + (fi / 10)
        # Realna wysokość mierzona do krawędzi łuku
        h_real = h_teo - (r_zew * (math.sqrt(2) - 1) / math.sqrt(2))

        st.markdown("---")
        res1, res2 = st.columns(2)
        res1.metric("Odległość końców (skos)", f"{round(c, 2)} cm")
        res2.metric("REALNA WYSOKOŚĆ (h)", f"{round(h_real, 2)} cm")
        
        if h_real > 240:
            st.error(f"❌ GABARYT PRZEKROCZONY! ({round(h_real, 2)} cm)")
        else:
            st.success(f"✅ GABARYT OK")

# --- SEKCJA 3: KĄTY ---
elif opcja == "Kąt gięcia":
    st.subheader("Obliczanie kątów (Trójkąt)")
    col1, col2 = st.columns(2)
    with col1:
        a_kat = pobierz_wartosc("Przyprostokątna - pion (cm)")
    with col2:
        c_kat = pobierz_wartosc("Przeciwprostokątna - skos (cm)")
        
    if c_kat > a_kat and a_kat > 0:
        kat = math.degrees(math.asin(a_kat/c_kat))
        st.metric("Kąt nachylenia", f"{round(kat, 2)}°")
        st.metric("Kąt gięcia maszynowy", f"{round(90-kat, 2)}°")
