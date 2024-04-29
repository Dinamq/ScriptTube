# Tkinter
import tkinter as tk
from tkinter import messagebox as MessageBox
from tkinter import filedialog as fd
import customtkinter

# Path Manegement
import os
from pathlib import Path

# Youtube
from pytube import YouTube


# Functions
def Directory():
    directory_path = fd.askdirectory(title='Directorio')
    pathVar.set(f'Directorio: {directory_path}')


def Update():
    try:
        yt = YouTube(entry.get())
        ytTitleVar.set(f'Titulo: {yt.title}')
        filenameVar.set(yt.title)

        # Reset
        openFolder_button.configure(state='disabled')
        openFile_button.configure(state='disabled')
        progressbar.set(0)
        percentageVar.set('')
    except Exception as error:
        MessageBox.showwarning(title='Advertencia', message='Ha ocurrido un error, revise su URL y la conexión a internet')
        print(f'Error: {error}')


def onProgress(stream, chunk, bytes_remainig):
    total_bytes = stream.filesize
    bytes_dowloaded = total_bytes - bytes_remainig
    percentage_of_compeletion = bytes_dowloaded / total_bytes * 100
    per = str(int(percentage_of_compeletion))
    percentageVar.set(per + '%')

    progressbar.set((float(percentage_of_compeletion)) / 100)
    percentage_label.update()


def OpenFolder():
    path = pathVar.get().replace('Directorio: ', '')
    path = os.path.realpath(path)
    os.startfile(path)


def OpenFile():
    if Path(pathVar.get().replace('Directorio: ', '') + '/' + filenameVar.get() + '.mp3').exists():
        path = pathVar.get().replace('Directorio: ', '') + '/' + filenameVar.get() + '.mp3'
    else:
        path = pathVar.get().replace('Directorio: ', '') + '/' + filenameVar.get() + '.mp4'
    path = os.path.realpath(path)
    os.startfile(path)


def Download():
    # print(Path(pathVar.get().replace('Directorio: ', '') + '/' + filenameVar.get() + '.mp3').is_dir())
    if entry.get() == '': return MessageBox.showwarning(title='Advertencia', message='Inserte URL valida')
    if Path(pathVar.get().replace('Directorio: ', '') + '/' + filenameVar.get() + '.mp4').exists():
        return MessageBox.showwarning(title='Advertencia', message='Archivo ya existente')
    if Path(pathVar.get().replace('Directorio: ', '') + '/' + filenameVar.get() + '.mp3').exists():
        return MessageBox.showwarning(title='Advertencia', message='Archivo ya existente')
    if extensionVar.get() == 'Video':
        yt = YouTube(entry.get(), on_progress_callback=onProgress)
        config = yt.streams.get_highest_resolution()
        config.download(filename=filenameVar.get() + '.mp4', output_path=pathVar.get().replace('Directorio: ', ''))

        # Enabled
        openFolder_button.configure(state='normal')
        openFile_button.configure(state='normal')
    else:
        yt = YouTube(entry.get(), on_progress_callback=onProgress)
        config = yt.streams.get_audio_only()
        config.download(filename=filenameVar.get() + '.mp3', output_path=pathVar.get().replace('Directorio: ', ''))

        # Enabled
        openFolder_button.configure(state='normal')
        openFile_button.configure(state='normal')


# Config
Config = {
    'WindowName': 'Youtube Downloader',
    'WindowSize': '1200x500',
    'extensions': ('Video', 'Audio'),
    'TitleSize': 24,
    'SectionSize': 14
}

# Window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('dark-blue')

window = customtkinter.CTk()
window.title(Config.get('WindowName'))
window.geometry(Config.get('WindowSize'))

# Title
title_label = customtkinter.CTkLabel(master=window, text='Youtube Video Downloader| Audio', font=('Calibri', Config.get('TitleSize'), 'bold'))
title_label.pack(pady=10)

# Input Field
input_frame = customtkinter.CTkFrame(master=window, fg_color='transparent')

url_label = customtkinter.CTkLabel(master=input_frame, text='URL:')

entryString = tk.StringVar()
entry = customtkinter.CTkEntry(master=input_frame, textvariable=entryString, width=600)

update_button = customtkinter.CTkButton(master=input_frame, text='Refresh', command=Update, width=100)

url_label.pack(side='left')
entry.pack(side='left', padx=10)
update_button.pack(side='left', padx=10)

input_frame.pack(pady=10)

# Info Field
info_frame = customtkinter.CTkFrame(master=window, fg_color='transparent')

ytTitleVar = tk.StringVar()
ytTitle_label = customtkinter.CTkLabel(master=info_frame, textvariable=ytTitleVar, font=('Calibri', Config.get('SectionSize'), 'bold'))

extensionVar = tk.StringVar(value=Config.get('extensions')[0])
extension_combo = customtkinter.CTkComboBox(master=info_frame, values=Config.get('extensions'), variable=extensionVar)

extension_label = customtkinter.CTkLabel(master=info_frame, text='Extension type:')

filenameVar = customtkinter.StringVar()
filename_entry = customtkinter.CTkEntry(master=info_frame, textvariable=filenameVar)
filename_label = customtkinter.CTkLabel(master=info_frame, text='File name:')

pathFile = __file__.split('\\')
pathFile.pop(-1)
path = '/'.join(pathFile)

path_button = customtkinter.CTkButton(master=info_frame, text='Change directory', command=Directory)
pathVar = customtkinter.StringVar()
pathVar.set(f'Directorio: {path}')
path_label = customtkinter.CTkLabel(master=info_frame, textvariable=pathVar)

# Grid
info_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
info_frame.rowconfigure((0, 1), weight=1, uniform='a')

ytTitle_label.grid(row=0, column=1, sticky='w', pady=10, padx=10)
filename_entry.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
extension_combo.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)
path_label.grid(row=1, column=2, sticky='nsew', pady=10, padx=10)
path_button.grid(row=2, column=2, sticky='nsew', pady=10, padx=10)
filename_label.grid(row=1, column=0, sticky='e', pady=10, padx=10)
extension_label.grid(row=2, column=0, sticky='e', pady=10, padx=10, )

info_frame.pack(pady=10)

# Output Field
output_frame = customtkinter.CTkFrame(master=window, fg_color='transparent')

percentageVar = customtkinter.StringVar()
percentage_label = customtkinter.CTkLabel(master=output_frame, textvariable=percentageVar, font=('Calibri', 20, 'bold'))

progressbar = customtkinter.CTkProgressBar(master=output_frame, orientation='horizontal', width=800)
progressbar.set(0)

download_button = customtkinter.CTkButton(master=output_frame, text='Download', command=Download, width=20)

# Button Field (Inside)
button_frame = customtkinter.CTkFrame(master=output_frame, fg_color='transparent')
openFolder_button = customtkinter.CTkButton(state='disabled', master=button_frame, text='Open directory file', command=OpenFolder, width=20)
openFile_button = customtkinter.CTkButton(state='disabled', master=button_frame, text='Open file', command=OpenFile, width=20)

percentage_label.pack()
progressbar.pack(pady=30)
download_button.pack()
openFile_button.pack(side='right')
openFolder_button.pack(pady=30, padx=10, side='right')
button_frame.pack()
output_frame.pack(pady=10)

# Run
window.mainloop()
