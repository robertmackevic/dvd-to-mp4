import subprocess
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, messagebox
from tkinter.ttk import Progressbar


class DVDConverterGUI:
    def __init__(self, main: Tk):
        self.main = main
        self.main.title("DVD to MP4 Converter")
        self.main.geometry("640x320")

        self.label = Label(main, text="Select a DVD folder", font=("Arial", 12))
        self.label.pack(pady=10)

        self.select_button = Button(main, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.convert_button = Button(main, text="Convert", command=self.convert, state="disabled")
        self.convert_button.pack(pady=10)

        self.progress_label = Label(main, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)

        self.progress_bar = Progressbar(main, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.selected_folder = None

    def select_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select DVD Folder")

        if folder:
            self.selected_folder = Path(folder)
            self.label.config(text=f"Selected Folder: {folder}")
            self.convert_button.config(state="normal")

    def convert(self):
        if not self.selected_folder or not self.selected_folder.is_dir():
            messagebox.showerror("Error", "The selected folder is invalid.")
            return

        mp4_folder = self.selected_folder.parent / f"{self.selected_folder.name}_MP4"
        mp4_folder.mkdir(parents=True, exist_ok=True)

        vob_files = list(self.selected_folder.rglob("*.vob"))
        if not vob_files:
            messagebox.showinfo("No Files Found", "No VOB files were found in the selected folder.")
            return

        self.progress_bar["maximum"] = len(vob_files)
        self.progress_bar["value"] = 0
        self.progress_label.config(text=f"Converting 0/{len(vob_files)} files...")

        for i, vob_file in enumerate(vob_files, start=1):
            base_name = vob_file.stem
            output_file = mp4_folder / f"{base_name}.mp4"

            command = [
                "ffmpeg", "-i", str(vob_file),
                "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental",
                str(output_file)
            ]

            try:
                subprocess.run(command, check=True)
                self.progress_bar["value"] = i
                self.progress_label.config(text=f"Converting {i}/{len(vob_files)} files...")
                self.main.update_idletasks()

            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to convert {vob_file}. Error: {e}")
                return

        self.progress_label.config(text="Conversion completed!")


if __name__ == "__main__":
    root = Tk()
    app = DVDConverterGUI(root)
    root.mainloop()
