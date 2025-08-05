import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Relatos de Padrões de Fraudadores", page_icon="🕵️‍♀️", layout="centered")

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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="gpt-box">', unsafe_allow_html=True)
st.markdown('<span class="gpt-label">🕵️‍♀️ Relate um novo padrão de fraude ou comportamento suspeito:</span>', unsafe_allow_html=True)

relato = st.text_area("", placeholder="Digite aqui o novo padrão ou relato suspeito do cliente...", height=120)
vendedor = st.text_input("Seu nome (opcional):")

if st.button("Enviar"):
    if relato.strip():
        novo = pd.DataFrame([{
            'Relato': relato,
            'Vendedor': vendedor,
            'Data': datetime.now().strftime("%d/%m/%Y %H:%M")
        }])
        try:
            df = pd.read_csv("relatos_fraudes.csv")
            df = pd.concat([df, novo], ignore_index=True)
        except FileNotFoundError:
            df = novo
        df.to_csv("relatos_fraudes.csv", index=False)
        st.success("Relato salvo! Obrigado por contribuir.")
    else:
        st.warning("Por favor, escreva algo antes de enviar.")

st.markdown("</div>", unsafe_allow_html=True)
