import streamlit as st
import google.generativeai as genai

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="YouTube Script Gen", page_icon="🎬", layout="wide")

st.title("🎬 Generator Scripturi YouTube (Gemini Edition)")
st.markdown("Transformă ideile în scripturi structurate folosind **Google Gemini**.")

# --- SIDEBAR (CONFIGURĂRI) ---
with st.sidebar:
    st.header("⚙️ Setări")
    
    # Input pentru API Key
    api_key = st.text_input("Introdu Google API Key", type="password", help="Ia cheia gratuit de pe aistudio.google.com")
    
    if not api_key:
        st.warning("⚠️ Introdu cheia API pentru a începe.")
    else:
        # Configurare model doar când avem cheia
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            st.success("API Conectat! ✅")
        except Exception as e:
            st.error("Cheie invalidă.")

    st.markdown("---")
    st.info("Sfat: Un script bun începe cu un titlu bun.")

# --- INTERFAȚA PRINCIPALĂ ---
col1, col2 = st.columns(2)

with col1:
    nisa = st.selectbox("Nișa Canalului", ["Tech & Gadgets", "Educațional", "Vlog/Lifestyle", "Gaming", "Business", "Sănătate", "Istorie"])
    durata = st.select_slider("Durata Estimată", options=["Shorts (<60s)", "Scurt (2-5 min)", "Mediu (5-10 min)", "Lung (>10 min)"])

with col2:
    ton = st.selectbox("Tonul Vocii", ["Entuziast & Rapid", "Serios & Analitic", "Umoristic & Relaxat", "Dramatic & Storytelling"])
    subiect = st.text_area("Despre ce e videoclipul?", height=100, placeholder="Ex: De ce iPhone 15 nu merită cumpărat...")

generate_btn = st.button("✨ Generează Scriptul", type="primary")

# --- LOGICA DE GENERARE ---
if generate_btn:
    if not api_key:
        st.error("Te rog introdu API Key-ul în meniul din stânga!")
    elif not subiect:
        st.error("Te rog scrie un subiect!")
    else:
        # PROMPT DE SISTEM AVANSAT
        system_instruction = """
        Ești un Scenarist YouTube Expert (Retention Specialist).
        
        SARCINA:
        Creează un script video optimizat pentru 'Average View Duration'.
        
        REGULI STRICTE:
        1. Formatare Markdown curată.
        2. Tabel OBLIGATORIU pentru script: Coloana [VIZUAL] (stânga) și [AUDIO] (dreapta).
        3. Vizualul trebuie să fie specific (B-roll, grafice, text pe ecran).
        4. Hook-ul (primele 15 secunde) trebuie să fie exploziv.
        
        OUTPUT CERUT:
        - 3 Titluri Virale (Clickable).
        - 1 Idee clară de Thumbnail.
        - Scriptul complet tabelar.
        """
        
        user_request = f"""
        Scrie scriptul pentru:
        - Nișa: {nisa}
        - Subiect: {subiect}
        - Ton: {ton}
        - Durata: {durata}
        - Limba: Română
        """
        
        full_prompt = system_instruction + "\n\n" + user_request

        with st.spinner('Gemini scrie scenariul... 🤖'):
            try:
                # Folosim modelul configurat anterior
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.subheader("📝 Rezultatul Tău")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"A apărut o eroare. Verifică API Key-ul. Detalii: {e}")
