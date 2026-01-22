import streamlit as st
import math

# 1. Konfiguracja wyglądu i barw
st.set_page_config(page_title="Kalkulator Zbrojarza", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    /* Granatowe tło całej aplikacji */
    .stApp {
        background-color: #001f3f; 
        color: white;
    }
    /* Stylizacja bocznego menu */
    section[data-testid="stSidebar"] {
        background-color: #00152b !important;
    }
    /* Białe napisy i pomarańczowe akcenty */
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

# 2. Nagłówek z logo (Pomarańczowo-Granatowy styl)
st.markdown("<h1 style='text-align: center; color: white;'>🏗️ KALKULATOR <span style='color: #ff8c00;'>ZBROJARZA</span></h1>", unsafe_allow_html=True)

opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Pręt typu L (Realna Wysokość)", "Kąt gięcia", "Wysokość łuku"])

def pobierz_wartosc(label, default="0"):
    val = st.text_input(label, value=default).replace(',', '.')
    try:
        return float(val) if val else 0.0
    except ValueError:
        return 0.0

if opcja == "Pręt typu L (Realna Wysokość)":
    st.subheader("Wymiary pręta L z uwzględnieniem łuku")
    col1, col2 = st.columns(2)
    with col1:
        fi = pobierz_wartosc("Średnica pręta FI (mm)", "12")
        a = pobierz_wartosc("Ramię A - po zewnątrz (cm)")
    with col2:
        r_wew = pobierz_wartosc("Promień gięcia R (cm)", str((2 * float(fi if fi else 12))/10))
        b = pobierz_wartosc("Ramię B - po zewnątrz (cm)")
    
    if a > 0 and b > 0:
        c = math.sqrt(a**2 + b**2)
        h_teo = (a * b) / c
        r_zew = r_wew + (fi / 10)
        # Korekta o łuk (najdalszy punkt zewnętrzny)
        h_real = h_teo - (r_zew * (math.sqrt(2) - 1) / math.sqrt(2))

        st.markdown("---")
        res1, res2 = st.columns(2)
        res1.metric("Skos (cm)", round(c, 2))
        res2.metric("REALNA WYSOKOŚĆ (cm)", round(h_real, 2))
        
        if h_real > 240:
            st.error(f"❌ GABARYT PRZEKROCZONY! ({round(h_real, 2)} cm)")
        else:
            st.success(f"✅ GABARYT OK (Mniej niż 240 cm)")

elif opcja == "Kąt gięcia":
    st.subheader("Kąt gięcia")
    a = pobierz_wartosc("Przyprostokątna - pion (cm)")
    c = pobierz_wartosc("Przeciwprostokątna - skos (cm)")
    if c > a and a > 0:
        kat = math.degrees(math.asin(a/c))
        st.metric("Kąt nachylenia", f"{round(kat, 2)}°")
        st.metric("Kąt gięcia maszynowy", f"{round(90-kat, 2)}°")

elif opcja == "Wysokość łuku":
    st.subheader("Wysokość łuku")
    l = pobierz_wartosc("Długość po łuku (cm)")
    r = pobierz_wartosc("Promień R (cm)")
    if r > 0 and l > 0:
        alfa = l / r
        h_luk = r * (1 - math.cos(alfa / 2))
        st.metric("Wysokość łuku (h)", f"{round(h_luk, 2)} cm")
