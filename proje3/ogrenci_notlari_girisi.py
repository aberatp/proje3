import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json
import os

class OgrenciNotlariGirisi:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Öğrenci Notları Girişi")
        self.window.geometry("1200x700")
        
        # Stil ayarları
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Info.TLabel", font=("Arial", 10))
        style.configure("Action.TButton", padding=5)
        style.configure("Grade.TEntry", font=("Arial", 10))
        style.configure("Student.Treeview", rowheight=30, font=("Arial", 10))
        style.configure("Student.Treeview.Heading", font=("Arial", 10, "bold"))
        
        self.ogrenciler = []
        self.degerlendirme_kriterleri = []
        self.not_entries = {}
        
        self.load_data()
        self.create_widgets()
        self.load_existing_data()

    def load_data(self):
        try:
            with open("ogrenci_listesi.json", "r", encoding="utf-8") as f:
                self.ogrenciler = json.load(f)
        except:
            messagebox.showerror("Hata", "Öğrenci listesi bulunamadı!")
            self.window.destroy()
            return

        try:
            with open("degerlendirme_kriterleri.json", "r", encoding="utf-8") as f:
                self.degerlendirme_kriterleri = json.load(f)
        except:
            messagebox.showerror("Hata", "Değerlendirme kriterleri bulunamadı!")
            self.window.destroy()
            return

    def create_widgets(self):
        # Ana container
        main_container = ttk.Frame(self.window, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Başlık
        ttk.Label(main_container, 
                 text="Öğrenci Notları Girişi",
                 style="Title.TLabel").pack(pady=(0,20))
        
        # Üst butonlar
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill="x", pady=(0,10))
        
        ttk.Button(button_frame, text="Excel'den Yükle",
                  style="Action.TButton",
                  command=self.load_from_excel).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Excel'e Aktar",
                  style="Action.TButton",
                  command=self.export_to_excel).pack(side="left", padx=5)
        
        # Not girişi frame
        grades_frame = ttk.LabelFrame(main_container, text="Not Girişi", padding=10)
        grades_frame.pack(fill="both", expand=True)
        
        # Scroll canvas
        canvas = tk.Canvas(grades_frame)
        scrollbar_y = ttk.Scrollbar(grades_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(grades_frame, orient="horizontal", command=canvas.xview)
        
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Başlıklar
        ttk.Label(self.scrollable_frame, text="Öğrenci No",
                 style="Header.TLabel").grid(row=0, column=0, padx=5, pady=5)
        
        for j, kriter in enumerate(self.degerlendirme_kriterleri, 1):
            ttk.Label(self.scrollable_frame, 
                     text=f"{kriter['kriter']}\n(Ağırlık: %{kriter['agirlik']})",
                     wraplength=100).grid(row=0, column=j, padx=2, pady=2)
        
        # Not giriş alanları
        self.not_entries = {}
        for i, ogrenci in enumerate(self.ogrenciler, 1):
            ttk.Label(self.scrollable_frame, 
                     text=ogrenci,
                     style="Info.TLabel").grid(row=i, column=0, padx=5, pady=2)
            
            self.not_entries[ogrenci] = {}
            for j, kriter in enumerate(self.degerlendirme_kriterleri, 1):
                entry = ttk.Entry(self.scrollable_frame, width=8,
                                style="Grade.TEntry")
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                entry.bind('<FocusOut>', self.validate_entry)
                self.not_entries[ogrenci][kriter['kriter']] = entry
        
        # Pack the canvas and scrollbars
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Alt butonlar
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill="x", pady=20)
        
        ttk.Button(bottom_frame, text="Kaydet",
                  style="Action.TButton",
                  command=self.save_data).pack(side="left", padx=5)
        
        ttk.Button(bottom_frame, text="İptal",
                  style="Action.TButton",
                  command=self.window.destroy).pack(side="right", padx=5)

    def validate_entry(self, event):
        try:
            value = float(event.widget.get())
            if not (0 <= value <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen 0-100 arasında bir değer girin!")
            event.widget.delete(0, tk.END)
            event.widget.insert(0, "0")

    def load_from_excel(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Excel Dosyası Seç",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not file_path:
                return
                
            df = pd.read_excel(file_path)
            
            for ogrenci in self.ogrenciler:
                if ogrenci not in df['Öğrenci No'].values:
                    raise ValueError(f"Öğrenci bulunamadı: {ogrenci}")
                
                for kriter in self.degerlendirme_kriterleri:
                    if kriter['kriter'] not in df.columns:
                        raise ValueError(f"Kriter bulunamadı: {kriter['kriter']}")
                    
                    value = float(df[df['Öğrenci No'] == ogrenci][kriter['kriter']].values[0])
                    if not (0 <= value <= 100):
                        raise ValueError(f"Geçersiz not: {value}")
                        
                    self.not_entries[ogrenci][kriter['kriter']].delete(0, tk.END)
                    self.not_entries[ogrenci][kriter['kriter']].insert(0, str(value))
            
            messagebox.showinfo("Başarılı", "Notlar Excel'den yüklendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Excel yükleme hatası: {str(e)}")

    def export_to_excel(self):
        try:
            data = []
            for ogrenci in self.ogrenciler:
                row = {'Öğrenci No': ogrenci}
                for kriter in self.degerlendirme_kriterleri:
                    value = float(self.not_entries[ogrenci][kriter['kriter']].get())
                    if not (0 <= value <= 100):
                        raise ValueError(f"Geçersiz not: {value}")
                    row[kriter['kriter']] = value
                data.append(row)
            
            df = pd.DataFrame(data)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Başarılı", "Notlar Excel'e aktarıldı!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Excel'e aktarma hatası: {str(e)}")

    def save_data(self):
        try:
            data = []
            # DataFrame için başlıkları hazırla
            headers = ['Öğrenci No'] + [k['kriter'] for k in self.degerlendirme_kriterleri]
            
            # Verileri topla
            for ogrenci in self.ogrenciler:
                row = [ogrenci]  # İlk sütun öğrenci no
                for kriter in self.degerlendirme_kriterleri:
                    value = float(self.not_entries[ogrenci][kriter['kriter']].get())
                    if not (0 <= value <= 100):
                        raise ValueError(f"Geçersiz not: {value}")
                    row.append(value)
                data.append(row)
            
            # DataFrame oluştur ve Excel'e kaydet
            df = pd.DataFrame(data, columns=headers)
            df.to_excel("ogrenci_notlari.xlsx", index=False)
            
            messagebox.showinfo("Başarılı", "Notlar kaydedildi!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

    def load_existing_data(self):
        try:
            if os.path.exists("ogrenci_notlari.xlsx"):
                df = pd.read_excel("ogrenci_notlari.xlsx")
                
                for _, row in df.iterrows():
                    ogrenci = str(row['Öğrenci No'])
                    if ogrenci in self.not_entries:
                        for kriter in self.degerlendirme_kriterleri:
                            if kriter['kriter'] in df.columns:
                                self.not_entries[ogrenci][kriter['kriter']].delete(0, tk.END)
                                self.not_entries[ogrenci][kriter['kriter']].insert(0, 
                                    str(row[kriter['kriter']]))
                    
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yükleme hatası: {str(e)}")

def ogrenci_notlari_girisi_pencere(parent):
    OgrenciNotlariGirisi(parent)
