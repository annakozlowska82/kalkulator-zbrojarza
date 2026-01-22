import streamlit as st
import math

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Zbrojarski Wrocław", page_icon="🏗️")

st.title("🏗️ System Wspierania Produkcji Zbrojeń")
st.markdown("---")

# Menu wyboru w pasku bocznym
opcja = st.sidebar.selectbox(
    "Co chcesz obliczyć?",
    ("Kąt gięcia (Trójkąt)", "Parametry łuku (Strzałka)")
)

if opcja == "Kąt gięcia (Trójkąt)":
    st.header("📐 Obliczanie kąta gięcia")
    col1, col2 = st.columns(2)
    
    with col1:
        a = st.number_input("Przyprostokątna - Wysokość (cm)", min_value=0.1, value=20.0, step=0.1)
    with col2:
        c = st.number_input("Przeciwprostokątna - Skos (cm)", min_value=0.1, value=40.0, step=0.1)

    if c <= a:
        st.error("Błąd: Skos (przeciwprostokątna) musi być dłuższy niż wysokość!")
    else:
        kat_rad = math.asin(a / c)
        kat_deg = math.degrees(kat_rad)
        
        st.success(f"**Kąt nachylenia:** {round(kat_deg, 2)}°")
        st.info(f"**Kąt gięcia maszynowy:** {round(90 - kat_deg, 2)}°")

elif opcja == "Parametry łuku (Strzałka)":
    st.header("🏹 Obliczanie wysokości łuku")
    
    col1, col2 = st.columns(2)
    with col1:
        l = st.number_input("Długość pręta po łuku L (cm)", min_value=0.1, value=150.0, step=0.1)
    with col2:
        r = st.number_input("Promień gięcia R (cm)", min_value=0.1, value=300.0, step=0.1)

    # Obliczenia
    alfa_rad = l / r
    h = r * (1 - math.cos(alfa_rad / 2))
    s = 2 * r * math.sin(alfa_rad / 2)
    kat_srodkowy = math.degrees(alfa_rad)

    # Wyniki
    st.markdown("### Wyniki obliczeń:")
    c1, c2, c3 = st.columns(3)
    c1.metric("Wysokość (h)", f"{round(h, 2)} cm")
    c2.metric("Rozpiętość (s)", f"{round(s, 2)} cm")
    c3.metric("Kąt środkowy", f"{round(kat_srodkowy, 2)}°")

    # Sprawdzenie gabarytu
    if h > 240:
        st.warning("⚠️ **GABARYT:** Wysokość łuku przekracza 240 cm! Sprawdź transport.")
    else:
        st.success("✅ **TRANSPORT:** Wysokość mieści się w skrajni (do 240 cm).")

st.markdown("---")
st.caption("Aplikacja dedykowana dla inżynierów produkcji zbrojeń. Jednostki: cm. Standard transportowy: 240 cm.")