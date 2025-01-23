import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

# Modül importları
from tablo1_girisi import tablo1_girisi_pencere
from tablo2_girisi import tablo2_girisi_pencere
from tablo_4_ve_5_olusturma import tablo_4_ve_5_olustur
from tablo_yukleme_arayuzu import tablo_yukleme_arayuzu
from ders_seçim_ekranı import ders_secim_ekrani
from degerlendirme_kriterleri_girisi import degerlendirme_kriterleri_girisi_pencere
from ogrenci_notlari_girisi import ogrenci_notlari_girisi_pencere

class BasariHesaplamaArayuzu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Başarı Hesaplama Arayüzü")
        self.root.geometry("1000x700")
        
        # Açık olan pencereyi takip etmek için
        self.current_window = None
        
        # Stil ayarları
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 12))
        style.configure("Menu.TButton", padding=10)
        
        self.create_widgets()
        self.create_file_viewer()
        
    def create_widgets(self):
        # Ana başlık
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(header_frame, 
                 text="Başarı Hesaplama Arayüzü",
                 style="Title.TLabel").pack()
        
        # Menü ve dosya görüntüleyici için container
        main_container = ttk.PanedWindow(self.root, orient="horizontal")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sol menü frame
        menu_frame = ttk.LabelFrame(main_container, text="İşlemler", padding=10)
        main_container.add(menu_frame, weight=1)
        
        # Menü butonları
        buttons = [
            ("Değerlendirme Kriterleri", self.degerlendirme_kriterleri_girisi),
            ("Tablo 1 Girişi", self.tablo1_girisi),
            ("Tablo 2 Girişi", self.tablo2_girisi),
            ("Öğrenci Notları Girişi", self.ogrenci_notlari_girisi),
            ("Tablo 4 ve 5 Oluştur", self.tablo_4_ve_5),
            ("Ders Seç", self.ders_sec),
            ("Tablo Yükle", self.tablo_yukle)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(menu_frame, text=text, command=command, style="Menu.TButton")
            btn.pack(fill="x", pady=2)
        
        ttk.Separator(menu_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(menu_frame, text="Sıfırla", command=self.reset_application, 
                  style="Menu.TButton").pack(fill="x", pady=2)
        ttk.Button(menu_frame, text="Çıkış", command=self.root.quit, 
                  style="Menu.TButton").pack(fill="x", pady=2)

    def create_file_viewer(self):
        # Sağ frame - Dosya görüntüleyici
        file_frame = ttk.LabelFrame(self.root, text="Dosya Görüntüleyici", padding=10)
        file_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)
        
        # Dosya listesi
        self.file_list = ttk.Treeview(file_frame, columns=("size", "date"), 
                                     show="headings")
        self.file_list.heading("size", text="Boyut")
        self.file_list.heading("date", text="Tarih")
        self.file_list.pack(fill="both", expand=True)
        
        # Yenile butonu
        ttk.Button(file_frame, text="Dosyaları Yenile", 
                  command=self.refresh_files).pack(pady=5)
        
        self.refresh_files()

    def refresh_files(self):
        # Dosya listesini temizle
        for item in self.file_list.get_children():
            self.file_list.delete(item)
        
        # İzlenecek dosya uzantıları
        extensions = ('.json', '.xlsx', '.xls')
        
        # Dosyaları listele
        for file in os.listdir('.'):
            if file.endswith(extensions):
                size = os.path.getsize(file)
                date = datetime.fromtimestamp(os.path.getmtime(file))
                
                # Boyutu formatla
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024**2:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/1024**2:.1f} MB"
                
                self.file_list.insert("", "end", text=file, 
                                    values=(size_str, date.strftime("%Y-%m-%d %H:%M")))

    def close_current_window(self):
        """Açık olan pencereyi kapatır"""
        if self.current_window and self.current_window.winfo_exists():
            self.current_window.destroy()
            self.current_window = None

    def degerlendirme_kriterleri_girisi(self):
        self.close_current_window()
        self.current_window = tk.Toplevel(self.root)
        degerlendirme_kriterleri_girisi_pencere(self.current_window)

    def tablo1_girisi(self):
        try:
            print("DEBUG: Tablo1 penceresi açılıyor...")
            if self.current_window:
                print(f"DEBUG: Mevcut pencere durumu: {self.current_window.winfo_exists()}")
                self.current_window.destroy()
                print("DEBUG: Mevcut pencere kapatıldı")
        except Exception as e:
            print(f"DEBUG: Pencere kapatma hatası: {str(e)}")
        
        try:
            print("DEBUG: Yeni pencere oluşturuluyor...")
            self.current_window = tk.Toplevel(self.root)
            print(f"DEBUG: Yeni pencere ID: {self.current_window}")
            self.current_window.title("Tablo 1 Girişi")
            self.current_window.geometry("1000x700")
            
            # Pencereyi modal yap
            self.current_window.transient(self.root)
            self.current_window.grab_set()
            
            # Pencere kapatıldığında temizlik yap
            def on_closing():
                self.current_window.grab_release()
                self.current_window.destroy()
                self.current_window = None
                
            self.current_window.protocol("WM_DELETE_WINDOW", on_closing)
            print("DEBUG: Pencere özellikleri ayarlandı")
            
            print("DEBUG: tablo1_girisi_pencere çağrılıyor...")
            tablo1_girisi_pencere(self.current_window)
            print("DEBUG: tablo1_girisi_pencere tamamlandı")
            
            # Pencereyi ana pencereye bağla
            self.current_window.wait_window()
            
        except Exception as e:
            print(f"DEBUG: Pencere oluşturma hatası: {str(e)}")

    def tablo2_girisi(self):
        try:
            if self.current_window:
                self.current_window.destroy()
        except:
            pass
        self.current_window = tk.Toplevel(self.root)
        self.current_window.title("Tablo 2 Girişi")
        self.current_window.geometry("1000x700")
        self.current_window.grab_set()
        self.current_window.focus_set()
        tablo2_girisi_pencere(self.current_window)

    def ogrenci_notlari_girisi(self):
        try:
            if self.current_window:
                self.current_window.destroy()
        except:
            pass
        self.current_window = tk.Toplevel(self.root)
        self.current_window.title("Öğrenci Notları Girişi")
        self.current_window.geometry("1000x700")
        self.current_window.grab_set()
        self.current_window.focus_set()
        ogrenci_notlari_girisi_pencere(self.current_window)

    def tablo_4_ve_5(self):
        self.close_current_window()
        tablo_4_ve_5_olustur()

    def ders_sec(self):
        self.close_current_window()
        ders_secim_ekrani()

    def tablo_yukle(self):
        self.close_current_window()
        tablo_yukleme_arayuzu()

    def reset_application(self):
        """Uygulamayı sıfırlar ve ders seçim ekranına döner"""
        response = messagebox.askokcancel(
            "Sıfırla", 
            "Tüm veriler silinecek ve ders seçim ekranına dönülecek. Emin misiniz?"
        )
        if response:
            self.close_current_window()
            self.ders_sec()

def main():
    app = BasariHesaplamaArayuzu()
    app.root.mainloop()

if __name__ == "__main__":
    main()
