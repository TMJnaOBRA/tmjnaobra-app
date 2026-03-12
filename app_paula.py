import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- BIBLIOTECA DE HASHTAGS TMJnaOBRA ---
HASHTAGS_PADRAO = "#TMJnaOBRA #MetodoDono #Arquitetura #GestaoDeObras #ObrasSemCaos #ObrasdeSucesso"

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
    code { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="TMJnaOBRA | Automatizador de Conteúdo", page_icon="⚡")
st.title("🚀 TMJnaOBRA: Content Lab")

# Conexão via Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.sidebar.success("✅ Conectado!")
else:
    st.sidebar.error("❌ Configure a API Key.")
    api_key = None

modelo_selecionado = st.sidebar.selectbox(
    "Escolha o cérebro da obra:", 
    [
        "gemini-3-flash-preview", 
        "gemini-3-pro-preview", 
        "gemini-2.0-flash", # Caso o Google já tenha estabilizado a 2.0
        "gemini-1.5-pro"    # Mantemos como backup se ainda existir
    ]
)

if api_key:
    modo = st.radio("O que vamos fazer hoje?", ["Reels ➡️ Carrossel", "Carrossel ➡️ Reels"])

    if modo == "Reels ➡️ Carrossel":
        upload = st.file_uploader("Suba o arquivo de vídeo (Reels)", type=["mp4", "mov", "avi"])
        prompt_especifico = f"""
        Analise este vídeo e gere um roteiro de carrossel (7-10 slides).
        Para cada slide: Título, Texto Curto e Sugestão de Imagem.
        AO FINAL, escreva uma LEGENDA para o Instagram que gere engajamento, usando este grupo de hashtags: {HASHTAGS_PADRAO}.
        """
    else:
        upload = st.file_uploader("Suba as imagens ou texto", type=["png", "jpg", "txt", "jpeg"], accept_multiple_files=True)
        prompt_especifico = f"""
        Crie um roteiro de Reels dinâmico. Divida em:
        1. ESTRATÉGIA VISUAL: Ganchos e cenas.
        2. ROTEIRO PARA CAPCUT: Apenas a locução/narração limpa.
        3. LEGENDA DO POST: Uma legenda curta e impactante com CTAs e estas hashtags: {HASHTAGS_PADRAO}.
        """

    if upload and st.button("✨ Gerar Mágica"):
        with st.spinner("O Gemini está finalizando o conteúdo..."):
            try:
                model = genai.GenerativeModel(modelo_selecionado)
                conteudo_para_ia = [prompt_especifico]
                
                if isinstance(upload, list):
                    for f in upload:
                        conteudo_para_ia.append(Image.open(f) if f.type.startswith('image') else {"mime_type": f.type, "data": f.read()})
                else:
                    conteudo_para_ia.append(Image.open(upload) if upload.type.startswith('image') else {"mime_type": upload.type, "data": upload.read()})

                response = model.generate_content(conteudo_para_ia)
                st.markdown("---")
                
                # Organização da Saída
                texto_total = response.text
                
                if "LEGENDA DO POST" in texto_total:
                    partes = texto_total.split("LEGENDA DO POST")
                    st.subheader("📝 Roteiro e Estratégia")
                    st.write(partes[0])
                    
                    st.subheader("📸 Legenda para o Instagram")
                    st.info("Pronta para copiar e colar no post!")
                    st.code(partes[1].strip(), language="text")
                else:
                    st.markdown(texto_total)

            except Exception as e:
                st.error(f"Erro: {e}")
