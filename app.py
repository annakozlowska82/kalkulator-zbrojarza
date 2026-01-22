import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Zbrojarza Wrocław", page_icon="🏗️")
st.title("🏗️ Kalkulator Zbrojarski")

# Menu wyboru w pasku bocznym
opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Kąt gięcia", "Wysokość łuku", "Pręt typu L (Transport)"])

def pobierz_wartosc(label):
    val = st.text_input(label, value="0").replace(',', '.')
    return float(val) if val else 0.0

if opcja == "Kąt gięcia":
    st.subheader("Obliczanie kąta gięcia (Trójkąt)")
    try:
        a = pobierz_wartosc("Przyprostokątna (cm)")
        c = pobierz_wartosc("Przeciwprostokątna (cm)")
        if c > a and a > 0:
            kat = math.degrees(math.asin(a/c))
            st.metric("Kąt nachylenia", f"{round(kat, 2)}°")
            st.metric("Kąt gięcia maszynowy", f"{round(90-kat, 2)}°")
    except: st.error("Wpisz poprawne liczby")

elif opcja == "Wysokość łuku":
    st.subheader("Obliczanie wysokości łuku")
    try:
        l = pobierz_wartosc("Długość pręta po łuku L (cm)")
        r = pobierz_wartosc("Promień gięcia R (cm)")
        if r > 0 and l > 0:
            alfa = l / r
            h = r * (1 - math.cos(alfa / 2))
            st.metric("Wysokość łuku (h)", f"{round(h, 2)} cm")
            if h > 240: 
                st.error(f"⚠️ GABARYT PRZEKROCZONY! (Wysokość: {round(h, 2)} cm)")
            else: 
                st.success("✅ Gabaryt OK")
    except: st.error("Wpisz poprawne liczby")

elif opcja == "Pręt typu L (Transport)":
    st.subheader("Weryfikacja pręta typu L")
    st.info("Podaj wymiary ramion. Sprawdzimy wysokość transportową (max 240 cm) oraz odległość między końcami.")
    try:
        ramie1 = pobierz_wartosc("Długość ramienia A (cm)")
        ramie2 = pobierz_wartosc("Długość ramienia B (cm)")
        
        if ramie1 > 0 and ramie2 > 0:
            # Obliczanie przeciwprostokątnej (odległość między końcami)
            skos = math.sqrt(ramie1**2 + ramie2**2)
            
            st.metric("Odleg
