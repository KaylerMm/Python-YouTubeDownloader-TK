import tkinter
import customtkinter
from pytube import YouTube
import threading
from PIL import Image, ImageTk
from urllib.request import urlopen
import io

def start_download_thread():
    thread = threading.Thread(target=start_download)
    thread.start()

def start_download():
    try:
        youtube_link = link.get()
        youtube_object = YouTube(youtube_link, on_progress_callback=on_progress)
        
        audio = youtube_object.streams.get_audio_only()

        # Atualiza o título do vídeo e a thumbnail
        update_video_thumbnail(youtube_object.title, youtube_object.thumbnail_url)

        title.configure(text=youtube_object.title)  # Shows video title being downloaded
        title.update()
        download_label.configure(text='')  # Resets download status label

        audio.download()  # type: ignore
        download_label.configure(text="Download is complete!", text_color="white")
    except Exception as e:
        download_label.configure(text='Invalid YouTube link!', text_color="red")
    
def update_video_thumbnail(video_title, thumbnail_url):
    # Atualiza o título do vídeo
    title.configure(text=video_title)

    # Atualiza a thumbnail do vídeo
    image_bytes = urlopen(thumbnail_url).read()  # Lê os bytes da imagem da URL
    image_data = io.BytesIO(image_bytes)  # Converte para um buffer de bytes

    pil_image = Image.open(image_data)  # Abre a imagem usando PIL
    tk_image = customtkinter.CTkImage(pil_image, size= (192, 108))  # Converte a imagem para um formato suportado por tkinter

    image_label.configure(image=tk_image, pady= 15)  # Atualiza a imagem no label (thumbnail)
    image_label.update()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    completion_percentage = bytes_downloaded / total_size * 100

    progress_percentage.configure(text=f'{str(int(completion_percentage))} %')  # Updates download percentage on screen
    progress_percentage.update()

    progress_bar.set(completion_percentage / 100)

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Music Downloader")

# UI elements

# Thumbnail
image_label = customtkinter.CTkLabel(app, text= " ", pady= 15)
image_label.pack()

# Main text
main_text = 'Paste or insert a YouTube link below'
title = customtkinter.CTkLabel(app, text=main_text)
title.pack(padx=10, pady=10)

# Link input
url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url)
link.pack()

# Download button
download = customtkinter.CTkButton(app, text="Download", command=start_download_thread)
download.pack(padx=15, pady=15)

# Download status label
download_label = customtkinter.CTkLabel(app, text='')
download_label.pack(padx=10, pady=10)

# Download status progress bar
progress_percentage = customtkinter.CTkLabel(app, text='0%')
progress_percentage.pack()

progress_bar = customtkinter.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

# Runs app
app.mainloop()
