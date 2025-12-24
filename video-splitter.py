import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
import threading
import os
import math
import subprocess
import shutil
import time
from datetime import datetime

# ==================== KURUMSAL TASARIM AYARLARI ====================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Kurumsal renk paleti - primary_dark eklendi
CORPORATE_COLORS = {
    "primary": "#0A84FF",       # Ana mavi (Apple Blue)
    "primary_dark": "#0066CC",   # Koyu mavi (Apple Blue Dark) - EKLENDİ
    "secondary": "#5E5CE6",     # Mor (Apple Purple)
    "success": "#30D158",       # Yeşil (Apple Green)
    "warning": "#FF9F0A",       # Turuncu (Apple Orange)
    "danger": "#FF453A",        # Kırmızı (Apple Red)
    "background": "#F8F9FA",    # Açık gri arkaplan
    "card": "#FFFFFF",          # Beyaz kartlar
    "text": "#1D1D1F",          # Ana metin rengi
    "text_secondary": "#8E8E93", # İkincil metin
    "border": "#C7C7CC",        # Border rengi
    "hover": "#E5E5EA"          # Hover efekti
}

class CorporateVideoSplitter(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Pencere ayarları
        self.title("HK Solutions - Video Splitter Pro")
        self.geometry("1100x850")
        self.minsize(1000, 750)
        
        # Değişkenler
        self.video_path = ""
        self.output_folder = ""
        self.is_processing = False
        self.total_segments = 0
        self.ffmpeg_path = "ffmpeg"
        
        # Kurumsal fontlar
        self.title_font = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        self.subtitle_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        self.body_font = ctk.CTkFont(family="Segoe UI", size=14)
        self.small_font = ctk.CTkFont(family="Segoe UI", size=12)
        self.button_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        
        # Arka plan rengi
        self.configure(fg_color=CORPORATE_COLORS["background"])
        
        # GUI'yi oluştur
        self.setup_ui()
        self.center_window()
        self.check_ffmpeg()

    def setup_ui(self):
        # Ana container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # ========== HEADER ==========
        self.create_corporate_header()
        
        # ========== MAIN CONTENT ==========
        main_content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        main_content.pack(fill="both", expand=True, pady=(20, 0))
        
        # Grid yapısı
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)
        main_content.grid_rowconfigure(0, weight=1)
        
        # SOL KOLON - Video ve Ayarlar
        left_column = ctk.CTkFrame(main_content, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # SAĞ KOLON - Bilgi ve İstatistik
        right_column = ctk.CTkFrame(main_content, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        # Sol kolon içeriği
        self.create_left_column(left_column)
        
        # Sağ kolon içeriği
        self.create_right_column(right_column)
        
        # ========== FOOTER ==========
        self.create_footer()

    def create_corporate_header(self):
        """Kurumsal header tasarımı"""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Logo ve marka bölümü
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.pack(side="left", fill="y")
        
        # HK Solutions logosu (kurumsal badge)
        self.create_logo_badge(logo_frame)
        
        # Başlık ve açıklama
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="right", fill="y")
        
        ctk.CTkLabel(
            title_frame,
            text="Video Splitter Pro",
            font=self.title_font,
            text_color=CORPORATE_COLORS["text"]
        ).pack(anchor="e")
        
        ctk.CTkLabel(
            title_frame,
            text="Profesyonel Video İşleme Çözümü",
            font=self.small_font,
            text_color=CORPORATE_COLORS["text_secondary"]
        ).pack(anchor="e", pady=(5, 0))

    def create_logo_badge(self, parent):
        """HK Solutions kurumsal logosu"""
        badge = ctk.CTkFrame(
            parent,
            fg_color=CORPORATE_COLORS["primary"],
            corner_radius=12,
            width=200,
            height=50
        )
        badge.pack_propagate(False)
        badge.pack()
        
        badge_content = ctk.CTkFrame(badge, fg_color="transparent")
        badge_content.pack(expand=True, fill="both", padx=20)
        
        ctk.CTkLabel(
            badge_content,
            text="HK",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).pack(side="left")
        
        ctk.CTkLabel(
            badge_content,
            text="SOLUTIONS",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="normal"),
            text_color="white"
        ).pack(side="left", padx=(8, 0))

    def create_left_column(self, parent):
        """Sol kolon - Video ve ayarlar"""
        # 1. Video Yükleme Kartı
        video_card = self.create_card(parent, "📁 Video Yükleme", height=200)
        
        # Modern upload butonu
        self.upload_btn = self.create_modern_button(
            video_card,
            text="Video Dosyası Seç",
            command=self.select_video,
            color="primary",
            height=55,
            icon="📂"
        )
        self.upload_btn.pack(padx=25, pady=(25, 15), fill="x")
        
        # Seçilen video bilgisi
        self.video_info_frame = ctk.CTkFrame(
            video_card,
            fg_color=CORPORATE_COLORS["hover"],
            corner_radius=10,
            height=70
        )
        self.video_info_frame.pack_propagate(False)
        self.video_info_frame.pack(padx=25, pady=(0, 20), fill="x")
        
        self.video_label = ctk.CTkLabel(
            self.video_info_frame,
            text="Henüz video seçilmedi",
            font=self.small_font,
            text_color=CORPORATE_COLORS["text_secondary"]
        )
        self.video_label.pack(expand=True)
        
        # 2. Bölme Ayarları Kartı
        settings_card = self.create_card(parent, "⚙️ Bölme Ayarları", height=250)
        
        settings_content = ctk.CTkFrame(settings_card, fg_color="transparent")
        settings_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Süre seçimi
        ctk.CTkLabel(
            settings_content,
            text="Bölüm Süresi (saniye):",
            font=self.body_font,
            text_color=CORPORATE_COLORS["text"]
        ).pack(anchor="w", pady=(0, 15))
        
        # Modern slider
        self.create_duration_slider(settings_content)
        
        # Format seçimi
        ctk.CTkLabel(
            settings_content,
            text="Çıktı Formatı:",
            font=self.body_font,
            text_color=CORPORATE_COLORS["text"]
        ).pack(anchor="w", pady=(20, 10))
        
        self.create_format_selector(settings_content)

    def create_right_column(self, parent):
        """Sağ kolon - Çıktı ve istatistik"""
        # 1. Çıktı Ayarları Kartı
        output_card = self.create_card(parent, "📤 Çıktı Ayarları", height=200)
        
        # Modern klasör seçim butonu
        self.folder_btn = self.create_modern_button(
            output_card,
            text="Kayıt Klasörü Seç",
            command=self.select_output_folder,
            color="secondary",
            height=55,
            icon="📁"
        )
        self.folder_btn.pack(padx=25, pady=(25, 15), fill="x")
        
        # Seçilen klasör bilgisi
        self.folder_info_frame = ctk.CTkFrame(
            output_card,
            fg_color=CORPORATE_COLORS["hover"],
            corner_radius=10,
            height=70
        )
        self.folder_info_frame.pack_propagate(False)
        self.folder_info_frame.pack(padx=25, pady=(0, 20), fill="x")
        
        self.folder_label = ctk.CTkLabel(
            self.folder_info_frame,
            text="Henüz klasör seçilmedi",
            font=self.small_font,
            text_color=CORPORATE_COLORS["text_secondary"]
        )
        self.folder_label.pack(expand=True)
        
        # 2. Video Bilgileri Kartı
        info_card = self.create_card(parent, "📊 Video Bilgileri", height=250)
        
        info_content = ctk.CTkFrame(info_card, fg_color="transparent")
        info_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Bilgi grid'i
        self.info_grid = ctk.CTkFrame(info_content, fg_color="transparent")
        self.info_grid.pack(fill="both", expand=True)
        
        # Bilgi satırları
        self.create_info_rows()

    def create_footer(self):
        """Footer - İlerleme ve butonlar"""
        footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 0))
        
        # İlerleme kartı
        progress_card = ctk.CTkFrame(
            footer_frame,
            fg_color=CORPORATE_COLORS["card"],
            corner_radius=14,
            border_width=1,
            border_color=CORPORATE_COLORS["border"]
        )
        progress_card.pack(fill="x", pady=(0, 20))
        
        progress_content = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_content.pack(fill="both", padx=25, pady=25)
        
        # İlerleme başlığı
        progress_header = ctk.CTkFrame(progress_content, fg_color="transparent")
        progress_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            progress_header,
            text="İşlem Durumu",
            font=self.subtitle_font,
            text_color=CORPORATE_COLORS["text"]
        ).pack(side="left")
        
        self.status_label = ctk.CTkLabel(
            progress_header,
            text="Hazır",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=CORPORATE_COLORS["success"]
        )
        self.status_label.pack(side="right")
        
        # İlerleme çubuğu
        self.progress_bar = ctk.CTkProgressBar(
            progress_content,
            height=10,
            corner_radius=5,
            progress_color=CORPORATE_COLORS["primary"],
            fg_color=CORPORATE_COLORS["hover"],
            border_width=0
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        # Detaylar
        details_frame = ctk.CTkFrame(progress_content, fg_color="transparent")
        details_frame.pack(fill="x")
        
        self.details_label = ctk.CTkLabel(
            details_frame,
            text="Video ve klasör seçerek başlayın",
            font=self.small_font,
            text_color=CORPORATE_COLORS["text_secondary"]
        )
        self.details_label.pack(side="left")
        
        self.time_label = ctk.CTkLabel(
            details_frame,
            text="",
            font=self.small_font,
            text_color=CORPORATE_COLORS["text_secondary"]
        )
        self.time_label.pack(side="right")
        
        # AKSİYON BUTONLARI
        action_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        action_frame.pack(fill="x")
        
        # Sol: Yardım butonları
        help_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        help_frame.pack(side="left")
        
        # Temizle butonu
        ctk.CTkButton(
            help_frame,
            text="Temizle",
            command=self.reset_all,
            font=self.body_font,
            height=45,
            width=120,
            corner_radius=10,
            fg_color=CORPORATE_COLORS["hover"],
            hover_color=CORPORATE_COLORS["border"],
            text_color=CORPORATE_COLORS["text"],
            border_width=1,
            border_color=CORPORATE_COLORS["border"]
        ).pack(side="left", padx=(0, 10))
        
        # Sağ: Ana başlat butonu
        self.start_button = ctk.CTkButton(
            action_frame,
            text="🚀 VİDEOYU BÖLMEYE BAŞLA",
            command=self.start_splitting,
            font=self.button_font,
            height=60,
            corner_radius=12,
            fg_color=CORPORATE_COLORS["primary"],
            hover_color=CORPORATE_COLORS["primary_dark"],  # DÜZELTİLDİ
            border_width=0,
            state="disabled"
        )
        self.start_button.pack(side="right")
        
        # Copyright
        copyright_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        copyright_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            copyright_frame,
            text="© 2024 HK Solutions - Tüm Hakları Saklıdır",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=CORPORATE_COLORS["text_secondary"]
        ).pack(anchor="center")

    def create_card(self, parent, title, height=None):
        """Kurumsal kart tasarımı"""
        card = ctk.CTkFrame(
            parent,
            fg_color=CORPORATE_COLORS["card"],
            corner_radius=14,
            border_width=1,
            border_color=CORPORATE_COLORS["border"]
        )
        card.pack(fill="both", expand=True, pady=(0, 15))
        
        if height:
            card.configure(height=height)
        
        # Kart başlığı
        header = ctk.CTkFrame(card, fg_color="transparent", height=50)
        header.pack(fill="x", padx=20, pady=(20, 0))
        
        ctk.CTkLabel(
            header,
            text=title,
            font=self.subtitle_font,
            text_color=CORPORATE_COLORS["text"]
        ).pack(anchor="w")
        
        # İçerik alanı
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(10, 0))
        
        return content

    def create_modern_button(self, parent, text, command, color="primary", height=50, icon=""):
        """Modern buton tasarımı"""
        if color == "primary":
            fg_color = CORPORATE_COLORS["primary"]
            hover_color = CORPORATE_COLORS["primary_dark"]  # DÜZELTİLDİ
        else:
            fg_color = CORPORATE_COLORS["secondary"]
            hover_color = "#4A4ACD"
        
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}  {text}" if icon else text,
            command=command,
            font=self.body_font,
            height=height,
            corner_radius=10,
            fg_color=fg_color,
            hover_color=hover_color,
            border_width=0
        )
        return btn

    def create_duration_slider(self, parent):
        """Modern süre slider'ı"""
        slider_frame = ctk.CTkFrame(parent, fg_color="transparent")
        slider_frame.pack(fill="x", pady=(0, 20))
        
        self.duration_var = ctk.IntVar(value=20)
        
        self.duration_slider = ctk.CTkSlider(
            slider_frame,
            from_=5,
            to=300,
            number_of_steps=59,
            variable=self.duration_var,
            command=self.update_duration_display,
            progress_color=CORPORATE_COLORS["primary"],
            button_color=CORPORATE_COLORS["primary"],
            button_hover_color=CORPORATE_COLORS["primary"],
            height=8
        )
        self.duration_slider.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        self.duration_display = ctk.CTkLabel(
            slider_frame,
            text="20 s",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=CORPORATE_COLORS["primary"],
            width=60
        )
        self.duration_display.pack(side="right")
        
        # Hızlı seçim butonları
        quick_frame = ctk.CTkFrame(parent, fg_color="transparent")
        quick_frame.pack(fill="x")
        
        durations = [15, 30, 60, 120, 180]
        for i, duration in enumerate(durations):
            btn = ctk.CTkButton(
                quick_frame,
                text=f"{duration}s",
                command=lambda d=duration: self.set_duration(d),
                font=self.small_font,
                height=30,
                width=60,
                corner_radius=6,
                fg_color=CORPORATE_COLORS["hover"] if duration != 20 else CORPORATE_COLORS["primary"],
                hover_color=CORPORATE_COLORS["border"],
                text_color=CORPORATE_COLORS["text"] if duration != 20 else "white"
            )
            btn.grid(row=0, column=i, padx=(0, 8) if i < len(durations)-1 else 0)

    def create_format_selector(self, parent):
        """Modern format seçici"""
        self.format_var = ctk.StringVar(value="mp4")
        
        format_frame = ctk.CTkFrame(parent, fg_color="transparent")
        format_frame.pack(fill="x")
        
        formats = [("MP4", "mp4"), ("MOV", "mov"), ("AVI", "avi")]
        for i, (text, value) in enumerate(formats):
            btn = ctk.CTkButton(
                format_frame,
                text=text,
                command=lambda v=value: self.set_format(v),
                font=self.body_font,
                height=45,
                corner_radius=10,
                fg_color=CORPORATE_COLORS["primary"] if value == "mp4" else CORPORATE_COLORS["hover"],
                hover_color=CORPORATE_COLORS["primary_dark"] if value == "mp4" else CORPORATE_COLORS["border"],  # DÜZELTİLDİ
                border_width=2 if value == "mp4" else 1,
                border_color=CORPORATE_COLORS["primary"] if value == "mp4" else CORPORATE_COLORS["border"]
            )
            btn.grid(row=0, column=i, padx=(0, 15) if i < len(formats)-1 else 0, sticky="ew")
            format_frame.grid_columnconfigure(i, weight=1)

    def create_info_rows(self):
        """Video bilgileri grid'i"""
        info_items = [
            ("Süre", "--:--:--"),
            ("Çözünürlük", "-- x --"),
            ("FPS", "--"),
            ("Boyut", "-- MB"),
            ("Ses", "--"),
            ("Format", "--")
        ]
        
        for i, (label, value) in enumerate(info_items):
            item_frame = ctk.CTkFrame(self.info_grid, fg_color="transparent")
            row = i // 2
            col = i % 2
            item_frame.grid(row=row, column=col, sticky="nsew", padx=(0, 20) if col == 0 else 0, pady=(0, 15))
            
            # Etiket
            ctk.CTkLabel(
                item_frame,
                text=label,
                font=self.small_font,
                text_color=CORPORATE_COLORS["text_secondary"]
            ).pack(anchor="w")
            
            # Değer
            value_label = ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=CORPORATE_COLORS["text"]
            )
            value_label.pack(anchor="w", pady=(3, 0))
            
            # Referans için sakla
            setattr(self, f"info_{label.lower()}", value_label)

    def center_window(self):
        """Pencereyi ortala"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def check_ffmpeg(self):
        """FFmpeg kontrolü"""
        try:
            if not shutil.which(self.ffmpeg_path):
                self.status_label.configure(
                    text="⚠️ FFmpeg Bulunamadı",
                    text_color=CORPORATE_COLORS["warning"]
                )
                return False
            self.status_label.configure(text="✓ FFmpeg Hazır", text_color=CORPORATE_COLORS["success"])
            return True
        except:
            self.status_label.configure(text="✗ FFmpeg Hatası", text_color=CORPORATE_COLORS["danger"])
            return False

    def get_video_duration(self, video_path):
        """Video süresini al"""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                raise RuntimeError("Video süresi alınamadı")
            
            return float(result.stdout.strip())
        except Exception as e:
            print(f"Video süresi hatası: {e}")
            return 0

    def set_duration(self, seconds):
        """Süreyi ayarla"""
        self.duration_slider.set(seconds)
        self.update_duration_display(seconds)

    def set_format(self, format_value):
        """Formatı ayarla"""
        self.format_var.set(format_value)

    def update_duration_display(self, value):
        """Süre ekranını güncelle"""
        self.duration_display.configure(text=f"{int(float(value))} s")
        if self.video_path:
            self.update_video_info()

    def select_video(self):
        """Video seç"""
        filetypes = [
            ("Video Dosyaları", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm *.m4v"),
            ("Tüm Dosyalar", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Video dosyası seçin",
            filetypes=filetypes
        )
        
        if filename:
            self.video_path = filename
            display_name = os.path.basename(filename)
            if len(display_name) > 30:
                display_name = display_name[:27] + "..."
            
            self.video_label.configure(
                text=f"✓ {display_name}",
                text_color=CORPORATE_COLORS["success"]
            )
            self.update_video_info()
            self.check_ready_state()

    def select_output_folder(self):
        """Klasör seç"""
        folder = filedialog.askdirectory(title="Kayıt klasörünü seçin")
        if folder:
            self.output_folder = folder
            display_path = folder
            if len(folder) > 40:
                display_path = "..." + folder[-37:]
            
            self.folder_label.configure(
                text=f"✓ {display_path}",
                text_color=CORPORATE_COLORS["success"]
            )
            self.check_ready_state()

    def update_video_info(self):
        """Video bilgilerini güncelle"""
        if not self.video_path or not os.path.exists(self.video_path):
            return
        
        try:
            # OpenCV'yi import et
            import cv2
            
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if fps > 0:
                duration = total_frames / fps
                hours = int(duration // 3600)
                minutes = int((duration % 3600) // 60)
                seconds = int(duration % 60)
                
                # Ses kontrolü
                has_audio = False
                try:
                    cmd = ['ffprobe', '-i', self.video_path, '-show_streams', 
                          '-select_streams', 'a', '-loglevel', 'error']
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    has_audio = result.returncode == 0 and 'codec_type=audio' in result.stdout
                except:
                    try:
                        has_audio = cap.get(cv2.CAP_PROP_AUDIO_TOTAL_CHANNELS) > 0
                    except:
                        has_audio = False
                
                # Bilgileri güncelle
                self.info_süre.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                self.info_çözünürlük.configure(text=f"{width} × {height}")
                self.info_fps.configure(text=f"{fps:.1f}")
                
                file_size = os.path.getsize(self.video_path) / (1024 * 1024)
                self.info_boyut.configure(text=f"{file_size:.1f} MB")
                self.info_ses.configure(text=f"{'Var ✓' if has_audio else 'Yok'}")
                
                file_ext = os.path.splitext(self.video_path)[1][1:].upper()
                self.info_format.configure(text=file_ext)
                
                # Tahmini bölüm sayısı
                segment_duration = self.duration_var.get()
                total_segments = math.ceil(duration / segment_duration)
                
                self.status_label.configure(
                    text=f"✓ {total_segments} Bölüm Hazır",
                    text_color=CORPORATE_COLORS["success"]
                )
                
                self.video_info = {
                    'fps': fps,
                    'total_frames': total_frames,
                    'duration': duration,
                    'width': width,
                    'height': height,
                    'has_audio': has_audio,
                    'total_segments': total_segments
                }
            
            cap.release()
            
        except Exception as e:
            print(f"Video bilgi hatası: {e}")

    def check_ready_state(self):
        """Başlat butonunu kontrol et"""
        if self.video_path and self.output_folder and self.check_ffmpeg():
            self.start_button.configure(state="normal", fg_color=CORPORATE_COLORS["primary"])
        else:
            self.start_button.configure(state="disabled", fg_color=CORPORATE_COLORS["hover"])

    def reset_all(self):
        """Tüm ayarları sıfırla"""
        if self.is_processing:
            if not messagebox.askyesno("Onay", "İşlem devam ediyor. Sıfırlamak istediğinize emin misiniz?"):
                return
            self.is_processing = False
        
        self.video_path = ""
        self.output_folder = ""
        
        self.video_label.configure(
            text="Henüz video seçilmedi",
            text_color=CORPORATE_COLORS["text_secondary"]
        )
        
        self.folder_label.configure(
            text="Henüz klasör seçilmedi",
            text_color=CORPORATE_COLORS["text_secondary"]
        )
        
        # Video bilgilerini sıfırla
        self.info_süre.configure(text="--:--:--")
        self.info_çözünürlük.configure(text="-- x --")
        self.info_fps.configure(text="--")
        self.info_boyut.configure(text="-- MB")
        self.info_ses.configure(text="--")
        self.info_format.configure(text="--")
        
        # İlerleme bilgilerini sıfırla
        self.progress_bar.set(0)
        self.status_label.configure(text="Hazır", text_color=CORPORATE_COLORS["success"])
        self.details_label.configure(text="Video ve klasör seçerek başlayın")
        self.time_label.configure(text="")
        
        self.start_button.configure(
            state="disabled",
            text="🚀 VİDEOYU BÖLMEYE BAŞLA",
            fg_color=CORPORATE_COLORS["hover"]
        )

    def start_splitting(self):
        """Bölme işlemini başlat"""
        if self.is_processing:
            messagebox.showwarning("Uyarı", "İşlem zaten devam ediyor.")
            return
        
        if not self.video_path:
            messagebox.showwarning("Eksik", "Lütfen video seçin.")
            return
        
        if not self.output_folder:
            messagebox.showwarning("Eksik", "Lütfen klasör seçin.")
            return
        
        try:
            segment_duration = int(self.duration_var.get())
            if segment_duration <= 0:
                messagebox.showerror("Hata", "Geçerli bir süre girin (0'dan büyük)")
                return
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir sayı girin")
            return
        
        # Onay
        total_segments = self.video_info.get('total_segments', 0)
        has_audio = self.video_info.get('has_audio', False)
        
        confirm_msg = (
            f"Video bölme işlemini başlatmak üzeresiniz:\n\n"
            f"📹 Video: {os.path.basename(self.video_path)}\n"
            f"⏱️ Her bölüm: {segment_duration} saniye\n"
            f"🔢 Toplam bölüm: {total_segments}\n"
            f"🔊 Ses durumu: {'Sesli ✓' if has_audio else 'Sessiz'}\n"
            f"📁 Kayıt yeri: {self.output_folder}\n\n"
            f"Devam etmek istiyor musunuz?"
        )
        
        if not messagebox.askyesno("Onay", confirm_msg):
            return
        
        # İşlemi başlat
        self.is_processing = True
        
        # Thread'de işlemi başlat
        thread = threading.Thread(
            target=self.split_video_ffmpeg,
            args=(segment_duration,)
        )
        thread.daemon = True
        thread.start()

    def split_video_ffmpeg(self, segment_duration):
        """FFmpeg ile video bölme"""
        start_time = time.time()
        
        # UI güncelle
        self.start_button.configure(
            state="disabled",
            text="⏳ İŞLENİYOR...",
            fg_color=CORPORATE_COLORS["secondary"]
        )
        
        self.status_label.configure(
            text="⏳ Video bölünüyor...",
            text_color=CORPORATE_COLORS["warning"]
        )
        
        self.progress_bar.set(0.1)
        
        try:
            # Çıktı klasörünü oluştur
            os.makedirs(self.output_folder, exist_ok=True)
            
            # Çıktı dosya pattern'i
            output_pattern = os.path.join(
                self.output_folder,
                "video_part_%03d.mp4"
            )
            
            # FFmpeg komutu
            cmd = [
                self.ffmpeg_path,
                "-i", self.video_path,
                "-map", "0",
                "-c", "copy",
                "-f", "segment",
                "-segment_time", str(segment_duration),
                "-reset_timestamps", "1",
                "-y",  # Overwrite
                output_pattern
            ]
            
            # FFmpeg'i çalıştır
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Progress takibi
            self.monitor_ffmpeg_process(process, start_time)
            
            # Process sonucunu bekle
            process.wait()
            
            if process.returncode != 0:
                raise RuntimeError(f"FFmpeg hatası (code: {process.returncode})")
            
            # Başarılı
            elapsed = time.time() - start_time
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            
            # ========== BİLDİRİM GÖSTER ==========
            self.after(0, self.show_completion_notification, elapsed, segment_duration)
            
        except Exception as e:
            self.after(0, self.show_error, str(e))
        
        finally:
            self.is_processing = False
            self.after(0, self.reset_ui)

    def monitor_ffmpeg_process(self, process, start_time):
        """FFmpeg sürecini takip et"""
        # Basit progress güncellemesi
        # FFmpeg segment modunda gerçek zamanlı progress çıktısı sınırlıdır
        
        def update():
            if not self.is_processing:
                return
            
            elapsed = time.time() - start_time
            total_segments = self.video_info.get('total_segments', 1)
            
            # Segment başına ortalama süre (hızlı kopyalama için)
            avg_time_per_segment = 0.3  # saniye
            
            estimated_total = total_segments * avg_time_per_segment
            
            if estimated_total > 0:
                progress = min(elapsed / estimated_total, 0.95)  # %95'e kadar
                self.progress_bar.set(progress)
                
                if progress < 0.95:
                    remaining = max(0, estimated_total - elapsed)
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    
                    self.time_label.configure(text=f"Kalan: {mins:02d}:{secs:02d}")
                    self.details_label.configure(text=f"Bölümler işleniyor...")
            
            # Her 100ms'de bir kontrol et
            self.after(100, update)
        
        update()

    def show_completion_notification(self, elapsed_time, segment_duration):
        """Tamamlama bildirimi göster"""
        total_segments = self.video_info.get('total_segments', 0)
        mins = int(elapsed_time // 60)
        secs = int(elapsed_time % 60)
        
        # Progress bar tamamlandı
        self.progress_bar.set(1)
        
        # UI güncelle
        self.status_label.configure(
            text=f"✓ {total_segments} Bölüm Tamamlandı",
            text_color=CORPORATE_COLORS["success"]
        )
        
        self.details_label.configure(
            text=f"İşlem süresi: {mins:02d}:{secs:02d}"
        )
        
        self.time_label.configure(text="")
        
        # ========== MODERN BİLDİRİM PENCERESİ ==========
        self.show_completion_popup(total_segments, elapsed_time, segment_duration)

    def show_completion_popup(self, total_segments, elapsed_time, segment_duration):
        """Modern tamamlama bildirimi penceresi"""
        popup = Toplevel(self)
        popup.title("🎉 İşlem Tamamlandı!")
        popup.geometry("500x450")
        popup.configure(bg="white")
        popup.resizable(False, False)
        
        # Pencereyi ortala
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Başlık
        header_frame = ctk.CTkFrame(popup, fg_color="transparent", height=100)
        header_frame.pack(fill="x", pady=(30, 20), padx=30)
        
        ctk.CTkLabel(
            header_frame,
            text="✅ VIDEO BÖLME İŞLEMİ TAMAMLANDI",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=CORPORATE_COLORS["success"]
        ).pack()
        
        # Başarı ikonu
        ctk.CTkLabel(
            header_frame,
            text="🎬",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(10, 0))
        
        # Bilgi kartı
        info_frame = ctk.CTkFrame(
            popup,
            fg_color=CORPORATE_COLORS["card"],
            corner_radius=12,
            border_width=1,
            border_color=CORPORATE_COLORS["border"]
        )
        info_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # İstatistikler
        stats = [
            ("📹 Video", os.path.basename(self.video_path)),
            ("📁 Kayıt Klasörü", self.output_folder),
            ("⏱️ Bölüm Süresi", f"{segment_duration} saniye"),
            ("🔢 Toplam Bölüm", f"{total_segments} adet"),
            ("⏰ İşlem Süresi", f"{int(elapsed_time // 60)}:{int(elapsed_time % 60):02d}"),
            ("📅 Tarih", datetime.now().strftime("%d.%m.%Y %H:%M"))
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = ctk.CTkFrame(info_content, fg_color="transparent")
            stat_frame.pack(fill="x", pady=(0, 12))
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=CORPORATE_COLORS["text_secondary"]
            ).pack(side="left")
            
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=CORPORATE_COLORS["text"]
            ).pack(side="right")
        
        # Butonlar
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        # Klasörü aç butonu
        ctk.CTkButton(
            button_frame,
            text="📂 KLASÖRÜ AÇ",
            command=lambda: os.startfile(self.output_folder),
            height=45,
            corner_radius=10,
            fg_color=CORPORATE_COLORS["primary"],
            hover_color=CORPORATE_COLORS["primary_dark"],  # DÜZELTİLDİ
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Tamam butonu
        ctk.CTkButton(
            button_frame,
            text="TAMAM",
            command=popup.destroy,
            height=45,
            corner_radius=10,
            fg_color=CORPORATE_COLORS["hover"],
            hover_color=CORPORATE_COLORS["border"],
            font=ctk.CTkFont(family="Segoe UI", size=14)
        ).pack(side="right", fill="x", expand=True)

    def show_error(self, error_msg):
        """Hata göster"""
        self.start_button.configure(
            state="normal",
            text="🔁 TEKRAR DENE",
            fg_color=CORPORATE_COLORS["danger"]
        )
        
        self.status_label.configure(
            text=f"✗ İşlem Başarısız",
            text_color=CORPORATE_COLORS["danger"]
        )
        
        # Hata mesajını göster
        messagebox.showerror(
            "Hata",
            f"Video bölme işlemi başarısız oldu:\n\n{error_msg}\n\n"
            "Lütfen FFmpeg'in doğru kurulu olduğundan emin olun."
        )
        
        # Butonu orijinal haline döndür
        self.after(3000, lambda: self.start_button.configure(
            text="🚀 VİDEOYU BÖLMEYE BAŞLA",
            fg_color=CORPORATE_COLORS["primary"]
        ))

    def reset_ui(self):
        """UI'yı sıfırla"""
        self.start_button.configure(
            state="normal",
            text="🚀 VİDEOYU BÖLMEYE BAŞLA",
            fg_color=CORPORATE_COLORS["primary"]
        )

def main():
    app = CorporateVideoSplitter()
    app.mainloop()

if __name__ == "__main__":
    main()