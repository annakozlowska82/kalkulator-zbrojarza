import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Zbrojarza Wrocław", page_icon="🏗️")
st.title("🏗️ Kalkulator Zbrojarski Pro")

opcja = st.sidebar.selectbox("Wybierz obliczenia:", 
    ["Kąt gięcia", "Wysokość łuku", "Pręt typu L (Realna Wysokość)"])

def pobierz_wartosc(label, default="0"):
    val = st.text_input(label, value=default).replace(',', '.')
    try:
        return float(val) if val else 0.0
    except ValueError:
        return 0.0

if opcja == "Pręt typu L (Realna Wysokość)":
    st.subheader("Wymiary pręta L z uwzględnieniem łuku gięcia")
    
    col_a, col_b = st.columns(2)
    with col_a:
        fi = pobierz_wartosc("Średnica pręta FI (mm)", "12")
        a = pobierz_wartosc("Ramię A - po zewnątrz (cm)")
    with col_b:
        r_trzypien = pobierz_wartosc("Promień gięcia R (cm)", str((2 * float(fi if fi else 12))/10))
        b = pobierz_wartosc("Ramię B - po zewnątrz (cm)")
    
    if a > 0 and b > 0 and r_trzypien > 0:
        # 1. Obliczamy skos (przeciwprostokątną)
        c = math.sqrt(a**2 + b**2)
        
        # 2. Obliczamy wysokość teoretyczną do kąta prostego
        h_teoretyczna = (a * b) / c
        
        # 3. Korekta o łuk gięcia (odsuniecie od wierzchołka)
        # Odległość od wierzchołka do początku łuku to R * tan(45/2)
        # Przy kącie 90 stopni, wierzchołek łuku jest przesunięty o R * (sqrt(2)-1)
        # Dodajemy promień zewnętrzny (R_wew + FI)
        r_zew = r_trzypien + (fi / 10)
        odsuniecie = r_zew * (math.sqrt(2) - 1)
        h_realna = h_teoretyczna - (odsuniecie / math.sqrt(2)) # uproszczony model geometryczny

        st.markdown("---")
        c1, c2 = st.columns(2)
        c1.metric("Skos (końce pręta)", f"{round(c, 2)} cm")
        c2.metric("REALNA WYSOKOŚĆ (h)", f"{round(h_realna, 2)} cm")
        
        st.info(f"Obliczenia uwzględniają promień gięcia R={r_trzypien} cm oraz grubość pręta.")

        if h_realna > 240:
            st.error(f"❌ GABARYT! Wysokość {round(h_realna, 2)} cm przekracza limit.")
        else:
            st.success(f"✅ OK! Pręt mieści się w skrajni.")

# ... (reszta kodu dla kąta i łuku pozostaje bez zmian)
