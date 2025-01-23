import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json
import os
from constants import FILE_NAMES

class Tablo1Girisi:
    def __init__(self, parent):
        print(f"DEBUG: Tablo1Girisi başlatılıyor... Parent: {parent}")
        self.parent = parent  # Ana pencereyi sakla
        self.window = parent
        print(f"DEBUG: Window atandı: {self.window}")
        
        # Pencere kapatma olayını yakala
        def on_closing():
            print("DEBUG: Pencere kapatılıyor...")
            self.window.grab_release()
            self.window.destroy()
            
        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        print("DEBUG: Pencere kapatma protokolü ayarlandı")
        
        # Widget'ları oluşturmadan önce pencereyi hazırla
        self.window.update_idletasks()
        
        try:
            print("DEBUG: Stil ayarları başlıyor...")
            style = ttk.Style()
            style.configure("Title.TLabel", font=("Arial", 16, "bold"))
            style.configure("Header.TLabel", font=("Arial", 12, "bold"))
            style.configure("Info.TLabel", font=("Arial", 10))
            style.configure("Action.TButton", padding=5)
            style.configure("Matrix.TEntry", font=("Arial", 10))
            print("DEBUG: Stil ayarları tamamlandı")
        except Exception as e:
            print(f"DEBUG: Stil ayarlama hatası: {str(e)}")
        
        print("DEBUG: Widget oluşturma başlıyor...")
        self.program_ciktilari = []
        self.ders_ciktilari = []
        self.matrix_entries = []
        
        self.load_ciktilar()
        self.create_widgets()
        self.load_existing_data()
        print("DEBUG: Widget oluşturma tamamlandı")

    def load_ciktilar(self):
        try:
            print("DEBUG: Program çıktıları yükleniyor...")
            if os.path.exists("program_ciktilari.json"):
                with open("program_ciktilari.json", "r", encoding="utf-8") as f:
                    self.program_ciktilari = json.load(f)
                    print(f"DEBUG: {len(self.program_ciktilari)} program çıktısı yüklendi")
            else:
                print("DEBUG: Varsayılan program çıktıları oluşturuluyor...")
                self.program_ciktilari = ["Program çıktısı 1", "Program çıktısı 2", "Program çıktısı 3"]
                with open("program_ciktilari.json", "w", encoding="utf-8") as f:
                    json.dump(self.program_ciktilari, f, ensure_ascii=False, indent=4)
                print("DEBUG: Varsayılan program çıktıları kaydedildi")

            print("DEBUG: Ders çıktıları yükleniyor...")
            if os.path.exists("ders_ciktilari.json"):
                with open("ders_ciktilari.json", "r", encoding="utf-8") as f:
                    self.ders_ciktilari = json.load(f)
                    print(f"DEBUG: {len(self.ders_ciktilari)} ders çıktısı yüklendi")
            else:
                print("DEBUG: Varsayılan ders çıktıları oluşturuluyor...")
                self.ders_ciktilari = ["Ders çıktısı 1", "Ders çıktısı 2", "Ders çıktısı 3"]
                with open("ders_ciktilari.json", "w", encoding="utf-8") as f:
                    json.dump(self.ders_ciktilari, f, ensure_ascii=False, indent=4)
                print("DEBUG: Varsayılan ders çıktıları kaydedildi")

        except Exception as e:
            print(f"DEBUG: Çıktı yükleme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Çıktılar yüklenirken hata oluştu: {str(e)}")
            self.window.destroy()
            return

    def create_widgets(self):
        try:
            print(f"DEBUG: Ana container oluşturuluyor... Window: {self.window}")
            main_container = ttk.Frame(self.window, padding="20")
            print("DEBUG: Ana container oluşturuldu")
            main_container.pack(fill="both", expand=True)
            print("DEBUG: Ana container pack edildi")
            
            # Başlık
            ttk.Label(main_container, 
                     text="Program/Ders Çıktıları İlişki Matrisi",
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
            
            # Matris frame
            matrix_frame = ttk.LabelFrame(main_container, text="İlişki Matrisi", padding=10)
            matrix_frame.pack(fill="both", expand=True)
            
            # Scroll canvas
            canvas = tk.Canvas(matrix_frame)
            scrollbar_y = ttk.Scrollbar(matrix_frame, orient="vertical", command=canvas.yview)
            scrollbar_x = ttk.Scrollbar(matrix_frame, orient="horizontal", command=canvas.xview)
            
            self.scrollable_frame = ttk.Frame(canvas)
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            # Başlık hücresi
            ttk.Label(self.scrollable_frame, text="Ders Çıktıları/\nProgram Çıktıları",
                     style="Header.TLabel").grid(row=0, column=0, padx=5, pady=5)
            
            # Program çıktıları başlıkları
            for j, program_ciktisi in enumerate(self.program_ciktilari, 1):
                ttk.Label(self.scrollable_frame, 
                         text=f"P{j}\n{program_ciktisi[:30]}...",
                         wraplength=100).grid(row=0, column=j, padx=2, pady=2)
            
            # Matris oluştur
            self.matrix_entries = []
            for i, ders_ciktisi in enumerate(self.ders_ciktilari, 1):
                row_entries = []
                ttk.Label(self.scrollable_frame, 
                         text=f"D{i}\n{ders_ciktisi[:30]}...",
                         wraplength=100).grid(row=i, column=0, padx=2, pady=2)
                
                for j in range(len(self.program_ciktilari)):
                    entry = ttk.Entry(self.scrollable_frame, width=8, 
                                    style="Matrix.TEntry")
                    entry.grid(row=i, column=j+1, padx=2, pady=2)
                    entry.insert(0, "0")
                    entry.bind('<FocusOut>', self.validate_entry)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
            
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
        except Exception as e:
            print(f"DEBUG: Widget oluşturma hatası: {str(e)}")

    def validate_entry(self, event):
        try:
            value = float(event.widget.get())
            if not (0 <= value <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen 0-1 arasında bir değer girin!")
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
                
            df = pd.read_excel(file_path, index_col=0)
            
            if df.shape != (len(self.ders_ciktilari), len(self.program_ciktilari)):
                raise ValueError("Excel dosyası boyutları uyumsuz!")
            
            for i in range(len(self.ders_ciktilari)):
                for j in range(len(self.program_ciktilari)):
                    value = float(df.iloc[i, j])
                    if not (0 <= value <= 1):
                        raise ValueError(f"Geçersiz değer: {value}")
                    self.matrix_entries[i][j].delete(0, tk.END)
                    self.matrix_entries[i][j].insert(0, str(value))
                    
            messagebox.showinfo("Başarılı", "Veriler Excel'den yüklendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Excel yükleme hatası: {str(e)}")

    def export_to_excel(self):
        try:
            data = []
            for i in range(len(self.ders_ciktilari)):
                row = []
                for j in range(len(self.program_ciktilari)):
                    value = float(self.matrix_entries[i][j].get())
                    if not (0 <= value <= 1):
                        raise ValueError(f"Geçersiz değer: {value}")
                    row.append(value)
                data.append(row)
            
            headers = [f'P{i+1}' for i in range(len(self.program_ciktilari))]
            df = pd.DataFrame(data, columns=headers)
            df.index = [f'D{i+1}' for i in range(len(self.ders_ciktilari))]
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if file_path:
                df.to_excel(file_path)
                messagebox.showinfo("Başarılı", "Veriler Excel'e aktarıldı!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Excel'e aktarma hatası: {str(e)}")

    def save_data(self):
        try:
            data = []
            # DataFrame için başlıkları hazırla
            headers = [f'P{i+1}' for i in range(len(self.program_ciktilari))]
            
            # Verileri topla
            for i in range(len(self.ders_ciktilari)):
                row = []
                for j in range(len(self.program_ciktilari)):
                    value = float(self.matrix_entries[i][j].get())
                    if not (0 <= value <= 1):
                        raise ValueError(f"Geçersiz değer: {value}")
                    row.append(value)
                data.append(row)
            
            # DataFrame oluştur ve Excel'e kaydet
            df = pd.DataFrame(data, columns=headers)
            df.index = [f'D{i+1}' for i in range(len(self.ders_ciktilari))]
            df.to_excel(FILE_NAMES['tablo1'])
            
            messagebox.showinfo("Başarılı", "Veriler kaydedildi!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

    def load_existing_data(self):
        try:
            if os.path.exists(FILE_NAMES['tablo1']):
                df = pd.read_excel(FILE_NAMES['tablo1'], index_col=0)
                
                for i in range(len(self.ders_ciktilari)):
                    for j in range(len(self.program_ciktilari)):
                        self.matrix_entries[i][j].delete(0, tk.END)
                        self.matrix_entries[i][j].insert(0, str(df.iloc[i, j]))
                        
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yükleme hatası: {str(e)}")

    def on_closing(self):
        """Pencere kapatıldığında çağrılır"""
        self.window.destroy()

def tablo1_girisi_pencere(parent):
    Tablo1Girisi(parent)
