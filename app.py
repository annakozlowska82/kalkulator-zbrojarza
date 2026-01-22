import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Zbrojarza Wrocław", page_icon="🏗️")
st.title("🏗️ Kalkulator Zbrojarski")

opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Kąt gięcia", "Wysokość łuku", "Pręt typu L (Transport)"])

def pobierz_wartosc(label):
    val = st.text_input(label, value="0").replace(',', '.')
    try:
        return float(val) if val else 0.0
    except ValueError:
        return 0.0

if opcja == "Kąt gięcia":
    st.subheader("Obliczanie kąta gięcia (Trójkąt)")
    try:
        a = pobierz_wartosc("Przyprostokątna - pion (cm)")
        c = pobierz_wartosc("Przeciwprostokątna - skos (cm)")
        if c > a and a > 0:
            kat = math.degrees(math.asin(a/c))
            st.metric("Kąt nachylenia", f"{round(kat, 2)}°")
            st.metric("Kąt gięcia maszynowy", f"{round(90-kat, 2)}°")
    except Exception: st.error("Błąd danych")

elif opcja == "Wysokość łuku":
    st.subheader("Obliczanie wysokości łuku")
    try:
        l = pobierz_wartosc("Długość pręta po łuku L (cm)")
        r = pobierz_wartosc("Promień gięcia R (cm)")
        if r > 0 and l > 0:
            alfa = l / r
            h_luk = r * (1 - math.cos(alfa / 2))
            st.metric("Wysokość łuku (h)", f"{round(h_luk, 2)} cm")
            if h_luk > 240: st.error("⚠️ GABARYT!")
            else: st.success("✅ OK")
    except Exception: st.error("Błąd danych")

elif opcja == "Pręt typu L (Transport)":
    st.subheader("Weryfikacja wymiarów pręta L")
    try:
        a = pobierz_wartosc("Długość ramienia A (cm)")
        b = pobierz_wartosc("Długość ramienia B (cm)")
        
        if a > 0 and b > 0:
            c = math.sqrt(a**2 + b**2)
            # Wysokość trójkąta prostokątnego opuszczona na przeciwprostokątną
            h_trojkata = (a * b) / c
            
            st.markdown("### Wymiary konstrukcyjne:")
            col1, col2 = st.columns(2)
            col1.metric("Odległość końców (skos)", f"{round(c, 2)} cm")
            col2.metric("Wysokość po skosie (h)", f"{round(h_trojkata, 2)} cm")
            
            st.markdown("---")
            st.subheader("Analiza transportowa (max 240 cm):")
            
            # Sprawdzenie czy da się przewieźć
            if a <= 240 or b <= 240 or h_trojkata <= 240:
                st.success("✅ Pręt da się zmieścić w skrajni!")
                if h_trojkata <= 240 and (a > 240 and b > 240):
                    st.info(f"💡 Uwaga: Pręt musi leżeć na skosie. Wysokość transportowa wyniesie: {round(h_trojkata, 2)} cm.")
            else:
                st.error("❌ GABARYT: Nawet po skosie pręt przekracza 240 cm!")
    except Exception: st.error("Wpisz poprawne liczby")
