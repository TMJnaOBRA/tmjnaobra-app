import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuração da página (Sempre no topo!)
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
    .stCodeBlock { border: 1px solid #FFD700; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 TMJnaOBRA: Content Lab")

# Sidebar com logo e config
try:
    st.sidebar.image("logo_tmj_branco.png")
except:
    pass

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("✅ Conectado")
else:
    st.sidebar.error("❌ API Key não configurada.")

modelo_opcoes = ["gemini-3-flash-preview", "gemini-1.5-flash", "gemini-1.5-pro"]
modelo_selecionado = st.sidebar.selectbox("Cérebro:", modelo_opcoes)

modo = st.radio("O que vamos fazer?", ["Reels ➡️ Carrossel", "Carrossel ➡️ Reels"])
upload = st.file_uploader("Suba seus arquivos", accept_multiple_files=True)

if upload and st.button("✨ Gerar Mágica"):
    with st.spinner("Analisando a obra..."):
        try:
            model = genai.GenerativeModel(modelo_selecionado)
            
            # --- DEFINIÇÃO DO PROMPT DINÂMICO ---
            if modo == "Reels ➡️ Carrossel":
                prompt = f"""
                Analise este vídeo e transforme-o em um CARROSSEL estratégico de 7 a 10 slides.
                Siga exatamente estes 3 blocos:
                
                ---ESTRATEGIA---
                (Explique por que escolheu esses pontos do vídeo para os slides e qual a lógica de retenção)
                
                ---SLIDES---
                (Para cada slide, forneça: 
                Título do Slide:
                Conteúdo/Texto do Slide:
                Sugestão de Imagem/Visual: )
                
                ---LEGENDA---
                (Escreva a legenda do Instagram com CTAs e estas hashtags: {HASHTAGS})
                """
            else:
                prompt = f"""
                Analise estas imagens/textos e transforme-os em um roteiro de REELS dinâmico.
                Siga exatamente estes 3 blocos:
                
                ---ESTRATEGIA---
                (Explique os ganchos e a lógica visual aqui)
                
                ---CAPCUT---
                (Escreva APENAS a locução/fala limpa para ser colada no Script to Video do CapCut)
                
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

            # --- EXIBIÇÃO INTELIGENTE ---
            
            # 1. Estratégia (Comum aos dois)
            if "---ESTRATEGIA---" in res_text:
                st.subheader("📐 Estratégia da Obra")
                estrategia = res_text.split("---ESTRATEGIA---")[1].split("---")[0]
                st.write(estrategia.strip())

            # 2. Conteúdo Principal (Diferencia se é Slide ou CapCut)
            if modo == "Reels ➡️ Carrossel":
                if "---SLIDES---" in res_text:
                    st.subheader("🗂️ Estrutura dos Slides (Carrossel)")
                    slides = res_text.split("---SLIDES---")[1].split("---")[0]
                    st.write(slides.strip())
            else:
                if "---CAPCUT---" in res_text:
                    st.subheader("🎬 Roteiro para o CapCut")
                    st.info("Copie e cole no 'Script to Video' do CapCut.")
                    roteiro = res_text.split("---CAPCUT---")[1].split("---")[0]
                    st.code(roteiro.strip(), language="text")

            # 3. Legenda (Comum aos dois)
            if "---LEGENDA---" in res_text:
                st.subheader("📝 Legenda do Post")
                legenda = res_text.split("---LEGENDA---")[1]
                st.code(legenda.strip(), language="text")

        except Exception as e:
            st.error(f"Erro na obra: {e}")



