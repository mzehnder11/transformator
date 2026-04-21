import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import pillow_avif  # Ensures AVIF support in Pillow
import moviepy as mp
from fpdf import FPDF
import uuid

# --- UI Configuration - Modern Dark Pro Theme ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") # We will override colors manually for a more custom feel

class FileTransformerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Transformator Pro")
        self.geometry("1200x800")
        
        # Windows-specific window centering
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        # Colors & Styles
        self.colors = {
            "bg": "#0f172a",          # slate-900
            "sidebar": "#1e293b",      # slate-800
            "sidebar_hover": "#334155",# slate-700
            "accent": "#6366f1",       # indigo-500
            "accent_hover": "#4f46e5", # indigo-600
            "success": "#10b981",      # emerald-500
            "success_hover": "#059669",# emerald-600
            "danger": "#ef4444",       # red-500
            "text_main": "#f8fafc",    # slate-50
            "text_muted": "#94a3b8",   # slate-400
            "card_bg": "#1e293b",
            "border": "#334155"
        }

        # Data state
        self.current_category = "image"
        self.staged_files = [] # List of dicts: {"path": str, "ui_item": CTkFrame}
        self.output_folder = os.path.join(os.getcwd(), "converted")
        os.makedirs(self.output_folder, exist_ok=True)

        self.format_options = {
            "image": ["PNG", "JPG", "WEBP", "GIF", "BMP", "TIFF", "AVIF"],
            "video": ["MP4", "MOV", "AVI", "MKV", "GIF"],
            "text": ["TXT", "PDF", "MD"],
            "audio": ["MP3", "WAV", "OGG", "FLAC"]
        }

        self.setup_ui()

    def setup_ui(self):
        # Configure Grid
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Area
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=self.colors["sidebar"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Logo / Branding
        self.logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=30, pady=(50, 60))
        
        self.logo_label = ctk.CTkLabel(self.logo_frame, text="TRANSFORMATOR", 
                                      font=ctk.CTkFont(size=22, weight="bold", family="Inter"),
                                      text_color=self.colors["text_main"])
        self.logo_label.pack()
        
        self.sublogo_label = ctk.CTkLabel(self.logo_frame, text="Professional File Suite", 
                                         font=ctk.CTkFont(size=12, family="Inter"),
                                         text_color=self.colors["accent"])
        self.sublogo_label.pack(pady=(2, 0))

        # Category Buttons
        categories = [
            ("Bilder", "image", "🖼️"),
            ("Videos", "video", "🎬"),
            ("Text / Docs", "text", "📄"),
            ("Audio", "audio", "🎵")
        ]

        self.sidebar_buttons = {}
        for i, (name, tag, icon) in enumerate(categories):
            btn = ctk.CTkButton(self.sidebar_frame, text=f"  {icon}   {name}", 
                               font=ctk.CTkFont(size=15, family="Inter"),
                               anchor="w",
                               height=55,
                               corner_radius=10,
                               fg_color="transparent",
                               text_color=self.colors["text_muted"],
                               hover_color=self.colors["sidebar_hover"],
                               command=lambda t=tag: self.select_category(t))
            btn.grid(row=i+1, column=0, padx=20, pady=6, sticky="ew")
            self.sidebar_buttons[tag] = btn

        # Info Box in Sidebar
        self.info_box = ctk.CTkFrame(self.sidebar_frame, fg_color=self.colors["sidebar_hover"], corner_radius=15)
        self.info_box.grid(row=7, column=0, padx=20, pady=40, sticky="ew")
        
        self.info_label = ctk.CTkLabel(self.info_box, text="Output Directory:", 
                                      font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_main"])
        self.info_label.pack(padx=20, pady=(15, 5), anchor="w")
        
        self.path_label = ctk.CTkLabel(self.info_box, text="/converted", 
                                      font=ctk.CTkFont(size=11), text_color=self.colors["text_muted"],
                                      wraplength=200, justify="left")
        self.path_label.pack(padx=20, pady=(0, 15), anchor="w")

        # --- MAIN AREA ---
        self.main_content = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Header Section
        self.top_header = ctk.CTkFrame(self.main_content, fg_color="transparent", height=100)
        self.top_header.grid(row=0, column=0, sticky="ew", padx=50, pady=(40, 0))
        
        self.content_title = ctk.CTkLabel(self.top_header, text="Bilder konvertieren", 
                                         font=ctk.CTkFont(size=32, weight="bold"),
                                         text_color=self.colors["text_main"])
        self.content_title.pack(side="left")

        # Work Area
        self.work_area = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.work_area.grid(row=1, column=0, sticky="nsew", padx=50, pady=30)
        self.work_area.grid_columnconfigure(0, weight=1)
        self.work_area.grid_rowconfigure(1, weight=1)

        # Upload Bar / Drag & Drop Visual
        self.upload_card = ctk.CTkFrame(self.work_area, fg_color=self.colors["card_bg"], corner_radius=15, height=120, border_width=1, border_color=self.colors["border"])
        self.upload_card.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        self.upload_card.grid_propagate(False)
        
        self.add_btn = ctk.CTkButton(self.upload_card, text="+ Neue Dateien hinzufügen", 
                                    font=ctk.CTkFont(size=15, weight="bold"),
                                    height=50, width=240, corner_radius=12,
                                    fg_color=self.colors["accent"], hover_color=self.colors["accent_hover"],
                                    command=self.select_files)
        self.add_btn.pack(side="left", padx=30, pady=35)
        
        self.clear_btn = ctk.CTkButton(self.upload_card, text="Alle leeren", 
                                      font=ctk.CTkFont(size=14),
                                      height=50, width=140, corner_radius=12,
                                      fg_color="transparent", text_color=self.colors["text_muted"],
                                      border_width=1, border_color=self.colors["border"],
                                      hover_color=self.colors["sidebar_hover"],
                                      command=self.clear_staged_files)
        self.clear_btn.pack(side="right", padx=30, pady=35)

        # File List Container
        self.list_container = ctk.CTkFrame(self.work_area, fg_color=self.colors["card_bg"], corner_radius=15, 
                                           border_width=1, border_color=self.colors["border"])
        self.list_container.grid(row=1, column=0, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(1, weight=1)
        
        # List Header
        self.list_header = ctk.CTkFrame(self.list_container, fg_color="transparent", height=50)
        self.list_header.grid(row=0, column=0, sticky="ew")
        self.list_header.grid_propagate(False)
        
        ctk.CTkLabel(self.list_header, text="DATEIINFORMATIONEN", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_muted"]).pack(side="left", padx=30)
        ctk.CTkLabel(self.list_header, text="STATUS", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_muted"]).pack(side="right", padx=120)

        # Scrollable Area
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

        # Bottom Action Bar
        self.action_bar = ctk.CTkFrame(self.main_content, fg_color=self.colors["sidebar"], height=120, corner_radius=0)
        self.action_bar.grid(row=2, column=0, sticky="ew")
        self.action_bar.grid_propagate(False)

        self.format_group = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.format_group.pack(side="left", padx=50, pady=20)

        self.format_label = ctk.CTkLabel(self.format_group, text="AUSGABEFORMAT", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.colors["text_muted"])
        self.format_label.pack(anchor="w", padx=2)

        self.format_dropdown = ctk.CTkOptionMenu(self.format_group, values=["PNG"], 
                                                fg_color=self.colors["bg"], text_color=self.colors["text_main"],
                                                button_color=self.colors["sidebar_hover"], button_hover_color=self.colors["border"],
                                                height=45, width=160, corner_radius=10)
        self.format_dropdown.pack(pady=(5, 0))

        self.convert_btn = ctk.CTkButton(self.action_bar, text="Konvertierung starten", 
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        height=60, width=280, corner_radius=12,
                                        fg_color=self.colors["success"], hover_color=self.colors["success_hover"],
                                        command=self.start_conversion)
        self.convert_btn.pack(side="right", padx=50, pady=30)

        # Footer Status
        self.footer = ctk.CTkFrame(self.main_content, fg_color="#0a0f1d", height=45, corner_radius=0)
        self.footer.grid(row=3, column=0, sticky="ew")
        self.footer.grid_propagate(False)

        self.progress_bar = ctk.CTkProgressBar(self.footer, height=6, fg_color=self.colors["sidebar"], progress_color=self.colors["success"])
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(50, 30))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(self.footer, text="System Bereit", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        self.status_label.pack(side="right", padx=50)

        # Initialize
        self.select_category("image")

    def select_category(self, category):
        self.current_category = category
        for cat, btn in self.sidebar_buttons.items():
            if cat == category:
                btn.configure(fg_color=self.colors["accent"], text_color="#ffffff", hover_color=self.colors["accent_hover"])
            else:
                btn.configure(fg_color="transparent", text_color=self.colors["text_muted"], hover_color=self.colors["sidebar_hover"])

        names = {"image": "Bilder", "video": "Videos", "text": "Text / Dokumente", "audio": "Audio"}
        self.content_title.configure(text=f"{names[category]} konvertieren")
        self.format_dropdown.configure(values=self.format_options[category])
        self.format_dropdown.set(self.format_options[category][0])

    def select_files(self):
        files = filedialog.askopenfilenames()
        if files:
            for f in files:
                if not any(item["path"] == f for item in self.staged_files):
                    self.add_file_to_list(f)

    def add_file_to_list(self, file_path):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=60)
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)
        
        # Hover effect simulation
        row.bind("<Enter>", lambda e: row.configure(fg_color=self.colors["sidebar_hover"]))
        row.bind("<Leave>", lambda e: row.configure(fg_color="transparent"))

        name = os.path.basename(file_path)
        ext = os.path.splitext(name)[1].upper()
        
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=25)
        
        lbl_name = ctk.CTkLabel(info_frame, text=name, font=ctk.CTkFont(size=14, weight="bold"), text_color=self.colors["text_main"])
        lbl_name.pack(anchor="w")
        
        lbl_ext = ctk.CTkLabel(info_frame, text=f"Typ: {ext}", font=ctk.CTkFont(size=11), text_color=self.colors["text_muted"])
        lbl_ext.pack(anchor="w")

        del_btn = ctk.CTkButton(row, text="Entfernen", width=90, height=32, 
                               fg_color="transparent", text_color=self.colors["danger"],
                               hover_color="#450a0a", font=ctk.CTkFont(size=12, weight="bold"),
                               border_width=1, border_color=self.colors["danger"],
                               command=lambda p=file_path: self.remove_file(p))
        del_btn.pack(side="right", padx=30)

        self.staged_files.append({"path": file_path, "ui_elements": [row]})

    def remove_file(self, file_path):
        for i, item in enumerate(self.staged_files):
            if item["path"] == file_path:
                for widget in item["ui_elements"]:
                    widget.destroy()
                self.staged_files.pop(i)
                break

    def clear_staged_files(self):
        for item in self.staged_files:
            for widget in item["ui_elements"]:
                widget.destroy()
        self.staged_files = []

    def start_conversion(self):
        if not self.staged_files:
            messagebox.showwarning("Fehlende Dateien", "Bitte füge zuerst Dateien hinzu.")
            return
        
        self.convert_btn.configure(state="disabled", text="Verarbeite...")
        self.add_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        
        target = self.format_dropdown.get().lower()
        threading.Thread(target=self.process_files, args=(target,), daemon=True).start()

    def process_files(self, target_format):
        try:
            total = len(self.staged_files)
            for i, item in enumerate(self.staged_files):
                file_path = item["path"]
                filename = os.path.basename(file_path)
                name_no_ext = os.path.splitext(filename)[0]
                
                final_folder = os.path.join(self.output_folder, self.current_category)
                os.makedirs(final_folder, exist_ok=True)
                
                output_path = os.path.join(final_folder, f"{name_no_ext}.{target_format}")

                self.after(0, lambda n=filename: self.status_label.configure(text=f"Konvertiere: {n}"))

                if self.current_category == "image":
                    self.convert_image(file_path, output_path, target_format)
                elif self.current_category == "video":
                    self.convert_video(file_path, output_path, target_format)
                elif self.current_category == "audio":
                    self.convert_audio(file_path, output_path, target_format)
                elif self.current_category == "text":
                    self.convert_text(file_path, output_path, target_format)

                self.after(0, lambda val=(i + 1) / total: self.progress_bar.set(val))

            self.after(0, lambda: messagebox.showinfo("Erfolg", f"Alle Dateien erfolgreich konvertiert!\n\nOrdner: {self.output_folder}"))
            os.startfile(self.output_folder)
        except Exception as e:
            self.after(0, lambda ex=str(e): messagebox.showerror("Konvertierungsfehler", f"Ein technischer Fehler ist aufgetreten:\n{ex}"))
        finally:
            self.after(0, self.reset_ui)

    def reset_ui(self):
        self.convert_btn.configure(state="normal", text="Konvertierung starten")
        self.add_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.status_label.configure(text="System Bereit")

    # --- Worker Methods (Optimized) ---
    def convert_image(self, input_path, output_path, target_format):
        with Image.open(input_path) as img:
            if target_format in ["jpg", "jpeg"]:
                img = img.convert("RGB")
            ext = target_format.upper() if target_format != "jpg" else "JPEG"
            img.save(output_path, ext, quality=95)

    def convert_video(self, input_path, output_path, target_format):
        clip = mp.VideoFileClip(input_path)
        if target_format == "gif":
            if clip.w > 640: clip = clip.resize(width=640)
            clip.write_gif(output_path, fps=12, logger=None)
        else:
            clip.write_videofile(output_path, codec="libx264" if target_format == "mp4" else None, 
                                audio_codec="aac" if target_format in ["mp4", "mov"] else None, logger=None)
        clip.close()

    def convert_audio(self, input_path, output_path, target_format):
        audio = mp.AudioFileClip(input_path)
        audio.write_audiofile(output_path, logger=None)
        audio.close()

    def convert_text(self, input_path, output_path, target_format):
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if target_format == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", size=12)
            for line in content.split('\n'):
                clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(0, 8, txt=clean_line, ln=True)
            pdf.output(output_path)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    app = FileTransformerApp()
    app.mainloop()
