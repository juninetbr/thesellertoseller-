import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Relatos de Padrões de Fraudadores", page_icon="🕵️‍♀️", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
body, .stApp {background-color: #101824 !important; color: #E0E6EC;}
.gpt-box {
  background-color: #232d36;
  border-radius: 16px;
  padding: 24px;
  max-width: 630px;
  margin: 32px auto;
}
input, textarea, .stTextArea, .stTextInput {
  border: 1.5px solid #F1C40F !important;
  background-color: #2F3B49 !important;
  color: #E0E6EC !important;
}
.gpt-label {
  color: #F1C40F;
  font-size: 21px;
  font-family: 'Consolas', monospace;
}
button.stButton>button {
  background: linear-gradient(90deg, #008B8B 0%, #00596d 100%) !important;
  border: 1px solid #F1C40F;
  color: white !important;
  font-weight: bold;
  font-size: 18px;
  padding: 0.4em 2em !important;
  border-radius: 12px;
}
button.stButton>button:hover {
  background: linear-gradient(90deg, #00b0a2 0%, #008170 100%) !important;
}
.stTextInput>div>input, .stTextArea>div>textarea {
  color: #F1C40F !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="gpt-box">', unsafe_allow_html=True)
st.markdown('<span class="gpt-label">🕵️‍♀️ Relate um padrão de fraude ou comportamento suspeito:</span>', unsafe_allow_html=True)

# Variável global para armazenar relatos (dura enquanto o app está ativo)
if "historico_fraude" not in st.session_state:
    st.session_state.historico_fraude = []

def enviar_relato():
    relato = st.session_state.get("relato_input", "").strip()
    vendedor = st.session_state.get("nome_input", "").strip()
    if relato:
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.session_state.historico_fraude.append({
            "data": data,
            "autor": vendedor if vendedor else "Anônimo",
            "relato": relato
        })
        st.session_state.relato_input = ""
        st.session_state.nome_input = ""
        st.success("Relato enviado!")
    else:
        st.warning("Por favor, escreva um relato antes de enviar.")

st.text_area("Relato", key="relato_input", placeholder="Descreva o novo padrão suspeito ou fraude...", height=120)
st.text_input("Seu nome (opcional):", key="nome_input")
st.button("Enviar", on_click=enviar_relato)

st.markdown("---")
st.markdown('<span class="gpt-label">📋 Histórico de Relatos:</span>', unsafe_allow_html=True)

if st.session_state.historico_fraude:
    for item in reversed(st.session_state.historico_fraude):
        st.markdown(f"""
        <div style="background-color:#2F3B49;border-radius:8px;padding:12px;margin-bottom:6px;">
        <b>{item['autor']} <span style='color:#F1C40F;font-size:13px'>({item['data']})</span></b>
        <br>
        {item['relato']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Nenhum relato cadastrado ainda.")

st.markdown("</div>", unsafe_allow_html=True)
