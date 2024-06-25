import tkinter
import customtkinter
from pytube import YouTube
import threading
from PIL import Image, ImageTk
from urllib.request import urlopen
import io

# Threads a new download
def start_download_thread():
    thread = threading.Thread(target=start_download)
    thread.start()

# Handles all the download process and calls for on-screen updates
def start_download():
    try:
        youtube_link = link.get()
        youtube_object = YouTube(youtube_link, on_progress_callback=on_progress)
        
        # Updates title and thumbnail based on video link info
        update_video_thumbnail(youtube_object.title, youtube_object.thumbnail_url)
        
        choice = combobox.get()  # Gets the dropdown menu choice

        if choice == 'Audio':
            audio = youtube_object.streams.get_audio_only()
            audio.download(output_path="./Audio Downloads") # type: ignore
            download_label.configure(text="Audio download completed!", text_color="white")
        
        elif choice == 'Video':
            video = youtube_object.streams.get_highest_resolution()
            video.download(output_path="Video Downloads") # type: ignore
            download_label.configure(text="Video download completed!", text_color="white")

        title.configure(text=youtube_object.title)  # Mostra o título do vídeo sendo baixado
        title.update()
        progress_percentage.configure(text='100%')  # Updates final percentage to 100%
        progress_bar.set(1.0) # Sets progress bar as complete
    except Exception as e:
        download_label.configure(text='Invalid Youtube link', text_color="red")

# Sets new thumbnail on display
def update_video_thumbnail(video_title, thumbnail_url):
    # Atualiza o título do vídeo
    title.configure(text=video_title)

    # Atualiza a thumbnail do vídeo
    image_bytes = urlopen(thumbnail_url).read()  # Read bytes from url
    image_data = io.BytesIO(image_bytes)  # Buffer bytes

    pil_image = Image.open(image_data)  # Abre a imagem usando PIL
    tk_image = customtkinter.CTkImage(pil_image, size=(192, 108))  # Converts image to supported format

    image_label.configure(image=tk_image, pady=15)  # Updates image label (thumbnail)
    image_label.update()

# Updates on-screen download progress info
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    completion_percentage = bytes_downloaded / total_size * 100

    progress_percentage.configure(text=f'{int(completion_percentage)} %')  # Updates percentage bar display
    progress_percentage.update()

    progress_bar.set(completion_percentage / 100)  # Updates progress bar percentage

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("860x520")
app.title("Youtube Downloader")

# UI elements

# Thumbnail
image_label = customtkinter.CTkLabel(app, text=" ", pady=15)
image_label.pack()

# Main text
main_text = 'Paste or type a YouTube link below'
title = customtkinter.CTkLabel(app, text=main_text)
title.pack(padx=10, pady=10)

# Link input
url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url)
link.pack()
# Combobox menu label
combobox_label = customtkinter.CTkLabel(app, text="Select which you want to download", padx= 15, pady= 15)
combobox_label.pack()

# Combobox menu
combobox = customtkinter.CTkOptionMenu(app, values= ['Video', 'Audio'])
combobox.set('Audio') # Initial value
combobox.pack(pady=15)

# download button
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

# Roda o loop principal
app.mainloop()
