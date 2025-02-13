import streamlit as st
import re
from pytubefix import YouTube

# Função para processar as legendas
def processa_captions(caption):
    novo_texto = re.sub(r'^\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', '', caption, flags=re.MULTILINE)
    processado = re.sub(r'^\d+$', '', novo_texto, flags=re.MULTILINE)  # Remove números sozinhos
    tex = processado.replace("\n", " ")
    texto_final = " ".join(tex.split())
    return texto_final

# Função para baixar o vídeo e legendas
def baixar_video(url):
    yt = YouTube(url)
    st.subheader("Metadados do vídeo:")
    st.write(f"✔️ Título do vídeo: {yt.title}")
    st.write(f"✔️ Data de publicação: {yt.publish_date}")
    st.write(f"✔️ Total de views do vídeo: {yt.views}")
    
    caption = yt.captions['a.pt'].generate_srt_captions()  # Pega a legenda no idioma português
    text = processa_captions(caption)
    
    # Exibe o texto das legendas
    st.text_area("📝 Legendas", value=text, height=300)
    st.download_button(label="Baixar Legendas", data=text, file_name="legendas.txt", mime="text/plain"):
    st.success("Legendas geradas com sucesso!")
    
    # Baixar o vídeo
    ys = yt.streams.get_highest_resolution()
    ys.download(filename="video.mp4")
    st.success("Vídeo baixado com sucesso!")

# Interface Streamlit
st.title("🤖 Download de Vídeos do YouTube")

# Input do link do vídeo
url = st.text_input("Insira a URL do vídeo do YouTube:")

if st.button("Processar", ):
    if url:
        baixar_video(url)
    else:
        st.error("Por favor, insira uma URL válida.")
