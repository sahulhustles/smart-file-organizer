import shutil
import mimetypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


# ----------------------------
# File Categorization Logic
# ----------------------------
def get_category(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        return "Others"

    main_type = mime_type.split("/")[0]

    if main_type == "image":
        return "Images"
    elif main_type == "video":
        return "Videos"
    elif main_type == "audio":
        return "Audio"
    elif main_type == "text":
        return "Text_Files"
    elif mime_type == "application/pdf":
        return "PDFs"
    elif "word" in mime_type:
        return "Word_Documents"
    elif "excel" in mime_type or "spreadsheet" in mime_type:
        return "Excel_Sheets"
    elif "presentation" in mime_type or "powerpoint" in mime_type:
        return "Presentations"
    elif "zip" in mime_type or "compressed" in mime_type:
        return "Archives"
    elif "executable" in mime_type:
        return "Executables"
    else:
        return "Others"


def get_unique_destination(destination: Path):
    counter = 1
    new_destination = destination

    while new_destination.exists():
        new_destination = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        counter += 1

    return new_destination


# ----------------------------
# Main Organizing Logic
# ----------------------------
def organize_files(target_folder, progress_bar, status_label, root):

    files = [f for f in target_folder.iterdir() if f.is_file()]
    total_files = len(files)

    if total_files == 0:
        messagebox.showinfo("Info", "No files found to organize.")
        root.destroy()
        return

    progress_bar["maximum"] = total_files

    moved_count = 0
    skipped_count = 0

    for index, file in enumerate(files):

        try:
            category = get_category(str(file))
            category_folder = target_folder / category
            category_folder.mkdir(exist_ok=True)

            destination = category_folder / file.name
            destination = get_unique_destination(destination)

            shutil.move(str(file), str(destination))
            moved_count += 1

        except Exception:
            skipped_count += 1

        progress_bar["value"] = index + 1
        percent = int(((index + 1) / total_files) * 100)
        status_label.config(text=f"Organizing... {percent}%")
        root.update_idletasks()

    messagebox.showinfo(
        "Completed",
        f"✅ Files Organized!\n\nMoved: {moved_count}\nSkipped: {skipped_count}"
    )

    root.destroy()


# ----------------------------
# Splash Screen
# ----------------------------
def show_splash():

    splash = tk.Tk()
    splash.title("Smart File Organizer")
    splash.geometry("400x200")
    splash.configure(bg="#1e1e1e")
    splash.resizable(False, False)

    tk.Label(
        splash,
        text="Smart File Organizer",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack(pady=40)

    tk.Label(
        splash,
        text="Initializing...",
        font=("Arial", 10),
        fg="lightgray",
        bg="#1e1e1e"
    ).pack()

    splash.after(2000, splash.destroy)  # 2 second splash
    splash.mainloop()


# ----------------------------
# App Start
# ----------------------------
if __name__ == "__main__":

    show_splash()

    # Folder selection
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder to Organize")
    root.destroy()

    if not folder_selected:
        exit()

    target_folder = Path(folder_selected)

    # Progress Window
    app = tk.Tk()
    app.title("Smart File Organizer")
    app.geometry("400x160")
    app.resizable(False, False)

    tk.Label(app, text="Organizing Files...", font=("Arial", 12)).pack(pady=10)

    progress = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    status = tk.Label(app, text="Starting...", font=("Arial", 10))
    status.pack(pady=5)

    app.after(100, organize_files, target_folder, progress, status, app)
    app.mainloop()