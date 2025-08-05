import streamlit as st
from datetime import datetime
import requests
import base64

# ==================== CONFIGURAÇÕES GITHUB ====================
GITHUB_TOKEN = 'SEU_TOKEN_AQUI'                                      # Seu token de acesso pessoal do GitHub
REPO = 'usuario/repositorio'                                         # Exemplo: 'jairosousa194/minha-pasta'
ARQUIVO = 'relatos.txt'                                              # Nome do arquivo .txt no seu github
API_URL = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"

def salva_no_github(relato_linha):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(API_URL, headers=headers)
    if resp.status_code == 200:
        conteudo = base64.b64decode(resp.json()["content"]).decode("utf-8")
        sha = resp.json()["sha"]
    else:
        conteudo = ""
        sha = None
    texto_novo = conteudo + relato_linha
    mensagem = "Novo relato adicionado"
    data = {
        "message": mensagem,
        "content": base64.b64encode(texto_novo.encode("utf-8")).decode("utf-8"),
    }
    if sha:
        data["sha"] = sha
    res = requests.put(API_URL, headers=headers, json=data)
    return res.ok

# ==================== DESIGN CUSTOMIZADO ====================
st.set_page_config(page_title="Relatos de Padrões de Fraudadores", 
                   page_icon="🕵️‍♀️", 
                   layout="centered")

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

st.markdown('<span class="gpt-label">🕵️‍♀️ Chat de Relatos de Fraude:</span>', unsafe_allow_html=True)
st.write("Envie um relato de um novo padrão de fraude observado ou comportamento suspeito no atendimento.")

if "chat" not in st.session_state:
    st.session_state.chat = []

# --- ENTRADA DO RELATO ---
relato = st.text_area(
    "Digite seu relato de fraude ou padrão suspeito:",
    placeholder="Exemplo: Cliente usando documentos inconsistentes, telefone não corresponde ao cadastro, etc.",
    height=120,
    key="relato_input"
)
vendedor = st.text_input("Seu nome (opcional):", key="nome_input")

if st.button("Enviar"):
    if relato.strip():
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        mensagem = {
            "autor": vendedor.strip() if vendedor else "Anônimo",
            "relato": relato.strip(),
            "data": data_atual
        }
        # Salva no chat de sessão
        st.session_state.chat.append(mensagem)
        # Monta linha do relato para Github
        relato_linha = f"{data_atual} | {mensagem['autor']} | {mensagem['relato']}\n"
        # Salva no arquivo do Github
        sucesso = salva_no_github(relato_linha)
        if sucesso:
            st.success("Relato enviado e armazenado no GitHub com sucesso!")
        else:
            st.error("Falha ao armazenar relato no GitHub. Tente novamente.")
        # Limpa os campos para a próxima mensagem
        st.session_state.relato_input = ""
        st.session_state.nome_input = ""
    else:
        st.warning("Por favor, escreva um relato antes de enviar.")

# --- CAIXA DE MENSAGENS (ESTILO CHAT) ---
st.markdown("---")
st.markdown('<span class="gpt-label">📋 Histórico de Relatos nesta sessão:</span>', unsafe_allow_html=True)
if st.session_state.chat:
    for mensagem in reversed(st.session_state.chat):
        st.markdown(f"""
        <div style="background-color:#2F3B49;border-radius:8px;padding:12px;margin-bottom:6px;">
        <b>{mensagem['autor']} <span style='color:#F1C40F;font-size:13px'>({mensagem['data']})</span></b>
        <br>
        {mensagem['relato']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Nenhum relato enviado nesta sessão ainda.")

st.markdown("</div>", unsafe_allow_html=True)

