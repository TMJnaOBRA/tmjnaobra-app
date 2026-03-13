import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTE PRECISA SER O PRIMEIRO COMANDO DO STREAMLIT!
st.set_page_config(
    page_title="TMJnaOBRA | Content Lab", 
    page_icon="⚡", 
    layout="wide"
)

# --- HASHTAGS ---
HASHTAGS = "#TMJnaOBRA #MetodoDono #ObrasdeSucesso #Arquitetura #GestaoDeObras #ObrasSemCaos"

# --- ESTILO TMJnaOBRA ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    [data-testid="stSidebar"] { background-color: #1E1E1E; border-right: 3px solid #FFD700; }
    h1, h2, h3, b, strong { color: #FFD700 !important; }
    div.stButton > button:first-child {
        background-color: #FFD700; color: black; font-weight: bold; width: 100%; border-radius: 10px;
    }
    /* Estilo para facilitar a visualização do código */
    .stCodeBlock { border: 1px solid #FFD700; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 TMJnaOBRA: Content Lab")
st.sidebar.image("logo_tmj_branco.png")

# Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("✅ Conectado")
else:
    st.sidebar.error("❌ API Key não configurada.")

modelo = st.sidebar.selectbox("Cérebro:", ["gemini-3-flash-preview", "gemini-1.5-flash", "gemini-1.5-pro"])

modo = st.radio("O que vamos fazer?", ["Reels ➡️ Carrossel", "Carrossel ➡️ Reels"])

upload = st.file_uploader("Suba seus arquivos", accept_multiple_files=True)

if upload and st.button("✨ Gerar Mágica"):
    with st.spinner("Analisando a obra..."):
        try:
            model = genai.GenerativeModel(modelo)
            
            # Prompt ultra-detalhado para garantir a separação
            prompt = f"""
            Analise os arquivos e gere o conteúdo seguindo estes exatos 3 blocos:
            
            ---ESTRATEGIA---
            (Explique os ganchos e a lógica visual aqui)
            
            ---CAPCUT---
            (Escreva apenas a locução/fala limpa para o CapCut aqui)
            
            ---LEGENDA---
            (Escreva a legenda do Instagram com CTAs e estas hashtags: {HASHTAGS})
            """
            
            conteudo = [prompt]
            for f in upload:
                if f.type.startswith('image'):
                    conteudo.append(Image.open(f))
                else:
                    conteudo.append({"mime_type": f.type, "data": f.read()})

            response = model.generate_content(conteudo)
            res_text = response.text

            # --- LÓGICA DE EXIBIÇÃO COM BOTÕES DE COPIAR ---
            
            # 1. Estratégia
            if "---ESTRATEGIA---" in res_text:
                st.subheader("📐 Estratégia da Obra")
                estratégia = res_text.split("---ESTRATEGIA---")[1].split("---")[0]
                st.write(estratégia.strip())

            # 2. Roteiro CapCut (Com botão de copiar)
            if "---CAPCUT---" in res_text:
                st.subheader("🎬 Roteiro para o CapCut")
                st.info("Passe o mouse no quadro abaixo e clique no ícone de copiar no canto direito.")
                roteiro = res_text.split("---CAPCUT---")[1].split("---")[0]
                st.code(roteiro.strip(), language="text")

            # 3. Legenda Instagram (Com botão de copiar)
            if "---LEGENDA---" in res_text:
                st.subheader("📝 Legenda do Post")
                legenda = res_text.split("---LEGENDA---")[1]
                st.code(legenda.strip(), language="text")

        except Exception as e:
            st.error(f"Erro na obra: {e}")


