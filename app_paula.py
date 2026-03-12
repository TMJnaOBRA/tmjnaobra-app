import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- ESTILIZAÇÃO TMJnaOBRA ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    [data-testid="stSidebar"] { background-color: #1E1E1E; border-right: 3px solid #FFD700; }
    h1, h2, h3, b, strong { color: #FFD700 !important; font-family: 'Helvetica', sans-serif; }
    div.stButton > button:first-child {
        background-color: #FFD700; color: #000000; border-radius: 10px;
        font-weight: bold; height: 3em; width: 100%; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #E6C200; border: 1px solid #000000; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #262730; color: white; border: 1px solid #FFD700;
    }
    /* Estilo para o bloco de código do CapCut */
    code { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# Configuração da Página
st.set_page_config(page_title="TMJnaOBRA | Automatizador de Conteúdo", page_icon="⚡")
st.title("🚀 TMJnaOBRA: Content Lab")

# Conexão com a API via Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.sidebar.success("✅ Conectado com sucesso!")
else:
    st.sidebar.error("❌ Configure a GOOGLE_API_KEY nos Secrets.")
    api_key = None

modelo_selecionado = st.sidebar.selectbox(
    "Escolha o cérebro da obra:", 
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-3-flash-preview", "gemini-3-pro-preview"]
)

if api_key:
    modo = st.radio("O que vamos fazer hoje?", ["Reels ➡️ Carrossel", "Carrossel ➡️ Reels"])

    if modo == "Reels ➡️ Carrossel":
        upload = st.file_uploader("Suba o arquivo de vídeo (Reels)", type=["mp4", "mov", "avi"])
        prompt_especifico = "Analise este vídeo e gere um roteiro de carrossel de 7 a 10 slides, seguindo minha System Instruction. Para cada slide, dê: Título, Texto Curto e Sugestão de Imagem."
    else:
        upload = st.file_uploader("Suba as imagens do carrossel ou o texto base", type=["png", "jpg", "txt", "jpeg"], accept_multiple_files=True)
        # PROMPT OTIMIZADO PARA CAPCUT
        prompt_especifico = """
        Com base nestes materiais, crie um roteiro de Reels dinâmico. 
        IMPORTANTE: Divida sua resposta em duas partes:
        1. ESTRATÉGIA VISUAL: Detalhe os ganchos e o que deve aparecer em cada cena.
        2. ROTEIRO PARA CAPCUT: Escreva apenas a narração (locução) de forma fluida, sem colchetes ou instruções técnicas. 
        Este segundo bloco deve ser curto (máximo 60 segundos de fala).
        """

    if upload and st.button("✨ Gerar Mágica"):
        with st.spinner("O Gemini está analisando a obra..."):
            try:
                model = genai.GenerativeModel(modelo_selecionado)
                conteudo_para_ia = [prompt_especifico]
                
                # Tratamento de arquivos para a IA
                if isinstance(upload, list):
                    for f in upload:
                        if f.type.startswith('image'):
                            conteudo_para_ia.append(Image.open(f))
                        else:
                            conteudo_para_ia.append({"mime_type": f.type, "data": f.read()})
                else:
                    if upload.type.startswith('image'):
                        conteudo_para_ia.append(Image.open(upload))
                    else:
                        conteudo_para_ia.append({"mime_type": upload.type, "data": upload.read()})

                response = model.generate_content(conteudo_para_ia)
                
                st.markdown("---")
                
                # Se for Carrossel para Reels, vamos tentar separar o código do CapCut
                if modo == "Carrossel ➡️ Reels":
                    partes = response.text.split("2. ROTEIRO PARA CAPCUT")
                    
                    st.subheader("📋 Estratégia de Conteúdo")
                    st.write(partes[0])
                    
                    if len(partes) > 1:
                        st.subheader("🎬 Roteiro Pronto para o CapCut")
                        st.info("Copie o texto abaixo e cole na função 'Script para Vídeo' do CapCut.")
                        st.code(partes[1].strip(), language="text") # Bloco de fácil cópia
                else:
                    st.success("Conteúdo Gerado!")
                    st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar: {e}")


