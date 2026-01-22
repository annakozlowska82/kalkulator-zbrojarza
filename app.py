import streamlit as st
import math

# 1. Konfiguracja wyglądu
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
    </style>
    """, unsafe_allow_html=True)

# 2. Nagłówek
st.markdown("<h1 style='text-align: center; color: white;'>🏗️ KALKULATOR <span style='color: #ff8c00;'>ZBROJARZA</span></h1>", unsafe_allow_html=True)

opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Wysokość łuku", "Pręt typu L (Realna Wysokość)", "Kąt gięcia"])

def pobierz_wartosc(label, default="0"):
    val = st.text_input(label, value=default).replace(',', '.')
    try:
        return float(val) if val else 0.0
    except ValueError:
        return 0.0

if opcja == "Wysokość łuku":
    st.subheader("Obliczanie wysokości (strzałki) łuku")
    col1, col2 = st.columns(2)
    with col1:
        l = pobierz_wartosc("Długość pręta po łuku L (cm)")
    with col2:
        r = pobierz_wartosc("Promień gięcia R (cm)")
    
    if r > 0 and l > 0:
        # Obliczanie kąta środkowego w radianach
        alfa = l / r
        # Obliczanie wysokości h (strzałki łuku)
        h_luk = r * (1 - math.cos(alfa / 2))
        
        st.markdown("---")
        st.metric("Wysokość łuku (h)", f"{round(h_luk, 2)} cm")
        
        # Weryfikacja gabarytu 240 cm
        if h_luk > 240:
            st.error(f"❌ GABARYT PRZEKROCZONY! Wysokość wynosi {round(h_luk, 2)} cm (Max: 240 cm)")
        else:
            st.success(f"✅ GABARYT OK - Mieści się w skrajni (Wysokość: {round(h_luk, 2)} cm)")

elif opcja == "Pręt typu L (Realna Wysokość)":
    st.subheader("Wymiary pręta
