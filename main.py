import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, PngImagePlugin, JpegImagePlugin
from mutagen.mp3 import MP3, ID3, TIT2, TPE1, TALB
from hurry.filesize import size as filesize


class SEOMetadataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("SEO Metadata Editor")
        self.file_list = []

        self.create_widgets()

    def create_widgets(self):
        self.add_file_button = tk.Button(self.root, text="Add Files", command=self.add_files)
        self.add_file_button.pack()

        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack()

        self.save_button = tk.Button(self.root, text="Save Metadata", command=self.save_metadata)
        self.save_button.pack()

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
                self.display_file(file)

    def display_file(self, file):
        file_label = tk.Label(self.file_frame, text=file)
        file_label.pack()

        metadata_frame = tk.Frame(self.file_frame)
        metadata_frame.pack()

        title_label = tk.Label(metadata_frame, text="Title")
        title_label.pack(side="left")
        title_entry = tk.Entry(metadata_frame)
        title_entry.pack(side="left")

        artist_label = tk.Label(metadata_frame, text="Artist")
        artist_label.pack(side="left")
        artist_entry = tk.Entry(metadata_frame)
        artist_entry.pack(side="left")

        album_label = tk.Label(metadata_frame, text="Album")
        album_label.pack(side="left")
        album_entry = tk.Entry(metadata_frame)
        album_entry.pack(side="left")

        # Store the entries for later use
        metadata_frame.entries = (title_entry, artist_entry, album_entry)
        file_label.metadata_frame = metadata_frame

    def save_metadata(self):
        for file in self.file_list:
            file_label = self.file_frame.children[str(self.file_list.index(file))]
            metadata_frame = file_label.metadata_frame
            title, artist, album = metadata_frame.entries

            if file.endswith('.mp3'):
                self.save_mp3_metadata(file, title.get(), artist.get(), album.get())
            elif file.endswith(('.jpg', '.jpeg', '.png')):
                self.save_image_metadata(file, title.get(), artist.get(), album.get())
            # Add more formats as needed

        messagebox.showinfo("Success", "Metadata saved successfully!")

    def save_mp3_metadata(self, file, title, artist, album):
        audio = MP3(file, ID3=ID3)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TALB"] = TALB(encoding=3, text=album)
        audio.save(filename=f"{file[:-4]}_optimized.mp3")

    def save_image_metadata(self, file, title, artist, album):
        with Image.open(file) as img:
            metadata = PngImagePlugin.PngInfo() if file.endswith('.png') else JpegImagePlugin.get_jpeg_header(img)

            metadata.add_text("Title", title)
            metadata.add_text("Artist", artist)
            metadata.add_text("Album", album)

            optimized_file = f"{file[:-4]}_optimized{file[-4:]}"
            img.save(optimized_file, "png" if file.endswith('.png') else "jpeg",
                     pnginfo=metadata if file.endswith('.png') else None)


if __name__ == "__main__":
    root = tk.Tk()
    app = SEOMetadataEditor(root)
    root.mainloop()
