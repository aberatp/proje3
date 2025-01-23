import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json
import os
from datetime import datetime

class TabloYuklemeArayuzu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tablo Yükleme Arayüzü")
        self.window.geometry("800x600")
        
        # Stil ayarları
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Status.TLabel", font=("Arial", 10))
        style.configure("Action.TButton", padding=5)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ana container
        main_container = ttk.Frame(self.window, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Başlık
        ttk.Label(main_container, 
                 text="Excel Dosyası Yükleme Arayüzü",
                 style="Title.TLabel").pack(pady=(0,20))
        
        # Sol panel - Yükleme seçenekleri
        left_panel = ttk.LabelFrame(main_container, text="Yükleme İşlemleri", padding=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        # Tablo seçenekleri
        self.tablo_options = [
            ("Program Çıktıları", "program_ciktilari.json"),
            ("Ders Çıktıları", "ders_ciktilari.json"),
            ("Öğrenci Listesi", "ogrenci_listesi.json"),
            ("Tablo 1", "tablo1.json"),
            ("Tablo 2", "tablo2.json"),
            ("Öğrenci Notları", "ogrenci_notlari.json")
        ]
        
        # Her tablo için yükleme butonu ve durum etiketi oluştur
        self.status_labels = {}
        
        for i, (tablo_adi, dosya_adi) in enumerate(self.tablo_options):
            frame = ttk.Frame(left_panel)
            frame.pack(fill="x", pady=5)
            
            ttk.Label(frame, text=f"{tablo_adi}:", 
                     style="Header.TLabel", width=20).pack(side="left")
            
            btn = ttk.Button(frame, 
                           text="Excel'den Yükle",
                           style="Action.TButton",
                           command=lambda d=dosya_adi, t=tablo_adi: self.yukle_excel(d, t))
            btn.pack(side="left", padx=5)
            
            status_label = ttk.Label(frame, text="Yüklenmedi ✗", 
                                   style="Status.TLabel", foreground="red")
            status_label.pack(side="left", padx=5)
            self.status_labels[dosya_adi] = status_label
            
            self.check_file_status(dosya_adi)
        
        # Sağ panel - Dosya önizleme
        right_panel = ttk.LabelFrame(main_container, text="Dosya Önizleme", padding=10)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Dosya listesi
        self.file_tree = ttk.Treeview(right_panel, columns=("size", "status"), 
                                     show="headings", height=10)
        self.file_tree.heading("size", text="Boyut")
        self.file_tree.heading("status", text="Durum")
        self.file_tree.pack(fill="both", expand=True, pady=5)
        
        # Alt butonlar
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame,
                  text="Tümünü Kontrol Et",
                  style="Action.TButton",
                  command=self.check_all_files).pack(side="left", padx=5)
        
        ttk.Button(button_frame,
                  text="Dosyaları Yenile",
                  style="Action.TButton",
                  command=self.refresh_file_list).pack(side="left", padx=5)
        
        ttk.Button(button_frame,
                  text="Kapat",
                  style="Action.TButton",
                  command=self.window.destroy).pack(side="right", padx=5)
        
        self.refresh_file_list()

    def refresh_file_list(self):
        # Dosya listesini temizle
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Dosyaları listele
        for tablo_adi, dosya_adi in self.tablo_options:
            if os.path.exists(dosya_adi):
                size = os.path.getsize(dosya_adi)
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024**2:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/1024**2:.1f} MB"
                    
                self.file_tree.insert("", "end", text=dosya_adi,
                                    values=(size_str, "Yüklendi ✓"))
            else:
                self.file_tree.insert("", "end", text=dosya_adi,
                                    values=("--", "Yüklenmedi ✗"))

    def yukle_excel(self, dosya_adi, tablo_adi):
        try:
            file_path = filedialog.askopenfilename(
                title=f"{tablo_adi} Excel Dosyası Seç",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not file_path:
                return
                
            df = pd.read_excel(file_path)
            
            # Excel verilerini JSON formatına dönüştür
            if dosya_adi == "program_ciktilari.json":
                data = df['Program Çıktısı'].tolist()
            elif dosya_adi == "ders_ciktilari.json":
                data = df['Ders Çıktısı'].tolist()
            elif dosya_adi == "ogrenci_listesi.json":
                data = df['Öğrenci No'].tolist()
            else:
                data = df.to_dict('records')
            
            # JSON dosyasına kaydet
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            self.status_labels[dosya_adi].config(
                text="Yüklendi ✓", 
                foreground="green"
            )
            
            messagebox.showinfo("Başarılı", f"{tablo_adi} başarıyla yüklendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"{tablo_adi} yüklenirken hata oluştu:\n{str(e)}")

    def check_file_status(self, dosya_adi):
        if os.path.exists(dosya_adi):
            self.status_labels[dosya_adi].config(
                text="Yüklendi ✓",
                foreground="green"
            )
        else:
            self.status_labels[dosya_adi].config(
                text="Yüklenmedi",
                foreground="red"
            )

    def check_all_files(self):
        try:
            missing_files = []
            for name, info in self.file_status.items():
                if not info["status"]:
                    missing_files.append(name)
            
            if missing_files:
                message = "Aşağıdaki dosyalar eksik:\n\n"
                message += "\n".join(f"- {file}" for file in missing_files)
                messagebox.showwarning("Eksik Dosyalar", message)
            else:
                messagebox.showinfo("Başarılı", "Tüm tablolar yüklenmiş durumda!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kontrolü sırasında hata oluştu: {str(e)}")

    def load_file_info(self):
        try:
            # Excel dosyalarını kontrol et
            files_to_check = {
                "Öğrenci Listesi": "ogrenci_listesi.xlsx",
                "Program Çıktıları": "program_ciktilari.xlsx",
                "Ders Çıktıları": "ders_ciktilari.xlsx",
                "Değerlendirme Kriterleri": "degerlendirme_kriterleri.xlsx",
                "Tablo 1": "tablo1.xlsx",
                "Tablo 2": "tablo2.xlsx",
                "Öğrenci Notları": "ogrenci_notlari.xlsx"
            }
            
            self.file_status = {}
            
            for name, filename in files_to_check.items():
                if os.path.exists(filename):
                    df = pd.read_excel(filename)
                    if not df.empty:
                        self.file_status[name] = {
                            "status": True,
                            "message": "Yüklendi",
                            "size": os.path.getsize(filename),
                            "date": datetime.fromtimestamp(os.path.getmtime(filename))
                        }
                    else:
                        self.file_status[name] = {
                            "status": False,
                            "message": "Boş dosya"
                        }
                else:
                    self.file_status[name] = {
                        "status": False,
                        "message": "Dosya bulunamadı"
                    }
            
            self.update_file_list()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya bilgileri yüklenirken hata oluştu: {str(e)}")

    def update_file_list(self):
        # Mevcut öğeleri temizle
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Dosya durumlarını listele
        for name, info in self.file_status.items():
            if info["status"]:
                size = info["size"]
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024**2:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/1024**2:.1f} MB"
                    
                date_str = info["date"].strftime("%Y-%m-%d %H:%M")
                
                self.file_tree.insert("", "end", values=(
                    name,
                    info["message"],
                    size_str,
                    date_str
                ))
            else:
                self.file_tree.insert("", "end", values=(
                    name,
                    info["message"],
                    "-",
                    "-"
                ))

    def refresh_files(self):
        self.load_file_info()
        messagebox.showinfo("Bilgi", "Dosya listesi yenilendi!")

def tablo_yukleme_arayuzu():
    app = TabloYuklemeArayuzu()
    app.window.mainloop()

if __name__ == "__main__":
    tablo_yukleme_arayuzu()
