import streamlit as st
import regex as re
from pytubefix import YouTube
import zipfile
import os

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

    # Processa as legendas
    text = processa_captions(yt.captions['a.pt'].generate_srt_captions())

    # Exibe o texto das legendas
    st.text_area("📝 Legendas", value=text, height=300)
  
    # Baixar o vídeo
    ys = yt.streams.get_highest_resolution()
    
    # baixar
    video_filename = "video.mp4"
    ys.download(filename=video_filename)
    st.success("Vídeo gerado com sucesso!")

    # Exibir o botão para baixar o arquivo zip
    with open(video_filename, "rb") as f:
        st.download_button(
            label="Baixar Vídeo",
            data=f,
            file_name=video_filename,
            mime="mp4")
    
    ## deixei para desenvolver posteriormente ##
    # # Salvar as legendas em um arquivo
    # legenda_filename = "legendas.txt"
    # with open(legenda_filename, "w", encoding="utf-8") as f:
    #     f.write(text)
    # st.success("Legendas geradas com sucesso!")
    
    # # Criar um arquivo zip contendo o vídeo e as legendas
    # zip_filename = "video_e_legendas.zip"
    # with zipfile.ZipFile(zip_filename, 'w') as zipf:
    #     zipf.write(video_filename)
    #     zipf.write(legenda_filename)

# Interface Streamlit
left_co, cent_co,last_co, L, M = st.columns(5)
with last_co:
    st.image("./image.png", width=150)
st.title("🤖 YouTuber")
st.subhead("Download de vídeos do YouTube")

# Input do link do vídeo
url = st.text_input("Insira a URL do vídeo do YouTube:")

if st.button("Processar"):
    if url:
        baixar_video(url)
    else:
        st.error("Por favor, insira uma URL válida.")
