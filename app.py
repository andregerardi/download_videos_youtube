import streamlit as st
import regex as re
from pytubefix import YouTube
import os


### primeira parte das funções ###

# Função para processar as legendas
def processa_captions(caption):
    novo_texto = re.sub(r'^\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', '', caption, flags=re.MULTILINE)
    processado = re.sub(r'^\d+$', '', novo_texto, flags=re.MULTILINE)  # Remove números sozinhos
    tex = processado.replace("\n", " ")
    texto_final = " ".join(tex.split())
    return texto_final

# Função para baixar o vídeo e legendas
def baixar_metadados(yt):
    st.subheader("Metadados do vídeo:")
    st.write(f"✔️ Título do vídeo: {yt.title}")
    st.write(f"✔️ Data de publicação: {yt.publish_date}")
    st.write(f"✔️ Total de views do vídeo: {yt.views}")

def baixar_video(yt):
    ys = yt.streams.get_highest_resolution()
    captions_filename = "video.mp4"
    ys.download(filename=captions_filename)    
    with open(captions_filename, "rb") as f:
        st.download_button(
            label="Baixar Vídeo",
            data=f,
            file_name=captions_filename,
            mime="mp4")
    st.success("Vídeo gerado com sucesso!")

#def baixar_legendas(yt):
    #text = processa_captions(yt.captions['a.pt'].generate_srt_captions())
    # Exibe o texto das legendas
    #st.text_area("📝 Legendas", value=text[0:600], height=300)
    # captions_filename = "legendas.txt"
    # if "Baixar Legendas":
    #     with open(captions_filename, "rb") as fl:
    #         st.download_button(
    #             label="Baixar Legendas",
    #             data=fl,
    #             file_name=captions_filename,
    #             mime="plan/text")
    #     st.success("Vídeo gerado com sucesso!")

### segunda parte do código ###

# titulo
st.title("🤖 YouTuber")
st.markdown("#### ⏯️ Download de vídeos e legendas do YouTube")

# Input do link do vídeo
url = st.text_input("Insira a URL do vídeo do YouTube:")

# Processamento
if st.button("Processar"):
    if url:
        # chama aplicação
        yt = YouTube(url)
        baixar_metadados(yt)
        baixar_video(yt)
        #baixar_legendas(yt)
    else:
        st.error("Por favor, insira uma URL válida.")


## rodapé
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 15px; background-color: ##191970;">
    🔗 <a href="https://www.linkedin.com/in/andr%C3%A9-gerardi-ds/" target="_blank">By André Gerardi</a>
</div>
""", unsafe_allow_html=True)
