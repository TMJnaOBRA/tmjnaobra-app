from PIL import Image
import streamlit as st
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="TMJnaOBRA | Automatizador de Conteúdo", page_icon="⚡")
st.title("🚀 TMJ | Fábrica de Conteúdos")

# Tenta carregar a chave dos Secrets automaticamente
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.sidebar.success("✅ Conectado com sucesso!")
else:
    st.sidebar.error("❌ Chave API não encontrada nos Secrets.")
    api_key = None

# Agora o seletor de modelo inclui as versões que você viu no AI Studio
modelo_selecionado = st.sidebar.selectbox(
    "Escolha o cérebro da obra:", 
    ["gemini-3-flash-preview", "gemini-3-pro-preview", "gemini-1.5-pro", "gemini-1.5-flash"]
)

if api_key:
    genai.configure(api_key=api_key)
    
    # Seleção do Modo
    modo = st.radio("O que vamos fazer hoje?", ["Reels ➡️ Carrossel", "Carrossel ➡️ Reels"])

    if modo == "Reels ➡️ Carrossel":
        upload = st.file_uploader("Suba o arquivo de vídeo (Reels)", type=["mp4", "mov", "avi"])
        prompt_especifico = "Analise este vídeo e gere um roteiro de carrossel de 7 a 10 slides, seguindo minha System Instruction de estrategista."
        
    else:
        upload = st.file_uploader("Suba as imagens do carrossel ou o texto base", type=["png", "jpg", "txt"], accept_multiple_files=True)
        prompt_especifico = "Com base nestes materiais, crie um roteiro de Reels dinâmico com ganchos, roteiro de fala e sugestão de cortes visuais."

    if upload and st.button("✨ Gerar Mágica"):
        with st.spinner("O Gemini está processando seu conteúdo..."):
            try:
                model = genai.GenerativeModel(modelo_selecionado)
                
                # Preparando a "lista de entrega" para a IA
                conteudo_para_ia = [prompt_especifico]
                
                # Se forem vários arquivos (Carrossel)
                if isinstance(upload, list):
                    for f in upload:
                        if f.type.startswith('image'):
                            conteudo_para_ia.append(Image.open(f))
                        else:
                            conteudo_para_ia.append({"mime_type": f.type, "data": f.read()})
                else:
                    # Se for arquivo único (Reels ou Imagem única)
                    if upload.type.startswith('image'):
                        conteudo_para_ia.append(Image.open(upload))
                    else:
                        # Para vídeos, enviamos os dados puros com o tipo do arquivo
                        conteudo_para_ia.append({"mime_type": upload.type, "data": upload.read()})

                response = model.generate_content(conteudo_para_ia)
                
                st.markdown("---")
                st.success("Conteúdo Gerado!")
                st.markdown(response.text)
                
                st.download_button("Baixar Roteiro", response.text, file_name="roteiro_gerado.txt")
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
else:

    st.warning("Por favor, insira sua API Key na barra lateral para começar.")

