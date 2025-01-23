import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import pandas as pd

class DersSecimEkrani:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Ders Seçim Ekranı")
        self.window.geometry("900x600")
        
        # Stil ayarları
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Info.TLabel", font=("Arial", 10))
        style.configure("Action.TButton", padding=5)
        style.configure("List.Treeview", rowheight=30, font=("Arial", 10))
        style.configure("List.Treeview.Heading", font=("Arial", 10, "bold"))
        
        self.current_ders = None
        self.dersler = []
        
        self.load_dersler()
        self.create_widgets()
        
    def load_dersler(self):
        try:
            if os.path.exists("dersler.xlsx"):
                df = pd.read_excel("dersler.xlsx")
                self.dersler = []
                for _, row in df.iterrows():
                    self.dersler.append({
                        'kod': row['kod'],
                        'ad': row['ad']
                    })
        except Exception as e:
            messagebox.showerror("Hata", f"Ders listesi yüklenirken hata oluştu: {str(e)}")

    def create_widgets(self):
        # Ana container
        main_container = ttk.Frame(self.window, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Başlık
        ttk.Label(main_container, 
                 text="Ders Seçim Ekranı",
                 style="Title.TLabel").pack(pady=(0,20))
        
        # Sol panel - Ders listesi
        left_panel = ttk.LabelFrame(main_container, text="Mevcut Dersler", padding=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        # Ders listesi (Treeview olarak)
        self.ders_tree = ttk.Treeview(left_panel, columns=("kod", "ad"), 
                                     show="headings", 
                                     style="List.Treeview",
                                     height=10)
        
        self.ders_tree.heading("kod", text="Ders Kodu")
        self.ders_tree.heading("ad", text="Ders Adı")
        self.ders_tree.column("kod", width=100)
        self.ders_tree.column("ad", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", 
                                command=self.ders_tree.yview)
        self.ders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ders_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dersleri listeye ekle
        for ders in self.dersler:
            self.ders_tree.insert("", "end", values=(ders['kod'], ders['ad']))
        
        # Sağ panel - Bilgi ve işlemler
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Seçili ders bilgisi
        info_frame = ttk.LabelFrame(right_panel, text="Seçili Ders Bilgisi", padding=10)
        info_frame.pack(fill="x", pady=(0,20))
        
        self.selected_label = ttk.Label(info_frame, 
                                      text="Henüz ders seçilmedi",
                                      style="Info.TLabel")
        self.selected_label.pack(pady=10)
        
        # İşlem butonları
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, 
                  text="Dersi Seç",
                  style="Action.TButton",
                  command=self.select_ders).pack(fill="x", pady=2)
        
        ttk.Button(button_frame,
                  text="Dosyaları Görüntüle",
                  style="Action.TButton",
                  command=self.show_files).pack(fill="x", pady=2)
        
        ttk.Separator(button_frame, orient="horizontal").pack(fill="x", pady=10)
        
        ttk.Button(button_frame,
                  text="İptal",
                  style="Action.TButton",
                  command=self.window.destroy).pack(fill="x", pady=2)
        
        # Bilgi mesajı
        ttk.Label(right_panel, 
                 text="Not: Ders seçimi değiştiğinde önceki veriler silinecektir.",
                 style="Info.TLabel",
                 foreground="red").pack(pady=20)

    def show_files(self):
        """Seçili derse ait dosyaları göster"""
        if not self.current_ders:
            messagebox.showwarning("Uyarı", "Lütfen önce bir ders seçin!")
            return
            
        files = [f for f in os.listdir('.') if f.endswith(('.json', '.xlsx'))]
        if not files:
            messagebox.showinfo("Bilgi", "Bu ders için henüz dosya oluşturulmamış.")
        else:
            file_list = "\n".join(files)
            messagebox.showinfo("Ders Dosyaları", 
                              f"Mevcut dosyalar:\n\n{file_list}")

    def select_ders(self):
        selection = self.ders_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir ders seçin!")
            return
        
        selected_values = self.ders_tree.item(selection[0])['values']
        selected_ders = {
            'kod': selected_values[0],
            'ad': selected_values[1]
        }
        
        self.current_ders = selected_ders
        
        # Seçili dersi kaydet
        try:
            with open("current_ders.json", "w", encoding="utf-8") as f:
                json.dump(selected_ders, f, ensure_ascii=False, indent=4)
            
            self.selected_label.config(
                text=f"Seçili Ders: {selected_ders['kod']} - {selected_ders['ad']}")
            
            # Önceki verileri temizle
            response = messagebox.askokcancel("Onay", 
                "Ders değiştirilecek ve önceki veriler silinecek. Devam etmek istiyor musunuz?")
            
            if response:
                self.reset_ders_data()
                messagebox.showinfo("Başarılı", 
                    f"{selected_ders['kod']} - {selected_ders['ad']} dersi seçildi.\n" +
                    "Artık bu ders için işlem yapabilirsiniz.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ders seçimi kaydedilirken hata oluştu: {str(e)}")

    def reset_ders_data(self):
        """Seçilen ders değiştiğinde önceki verileri temizler"""
        files_to_remove = [
            "program_ciktilari.json",
            "ders_ciktilari.json",
            "degerlendirme_kriterleri.json",
            "tablo1.json",
            "tablo2.json",
            "ogrenci_notlari.json",
            "tablo4.xlsx",
            "tablo5.xlsx"
        ]
        
        for file in files_to_remove:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Hata: {file} silinirken hata oluştu - {str(e)}")

    def load_current_ders(self):
        try:
            if os.path.exists("secili_ders.xlsx"):
                df = pd.read_excel("secili_ders.xlsx")
                if not df.empty:
                    self.current_ders = {
                        'kod': df.iloc[0]['kod'],
                        'ad': df.iloc[0]['ad']
                    }
                    self.update_current_ders_label()
        except Exception as e:
            messagebox.showerror("Hata", f"Seçili ders yüklenirken hata oluştu: {str(e)}")

    def load_from_excel(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Excel Dosyası Seç",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not file_path:
                return
            
            df = pd.read_excel(file_path)
            
            if 'kod' not in df.columns or 'ad' not in df.columns:
                raise ValueError("Excel dosyası uygun formatta değil!")
            
            # Mevcut dersleri temizle
            self.dersler = []
            
            # Yeni dersleri ekle
            for _, row in df.iterrows():
                self.dersler.append({
                    'kod': row['kod'],
                    'ad': row['ad']
                })
            
            self.update_ders_listesi()
            messagebox.showinfo("Başarılı", "Dersler Excel'den yüklendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Excel yükleme hatası: {str(e)}")

    def export_to_excel(self):
        try:
            data = []
            for ders in self.dersler:
                data.append({
                    'kod': ders['kod'],
                    'ad': ders['ad']
                })
            
            df = pd.DataFrame(data)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Başarılı", "Dersler Excel'e aktarıldı!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Excel'e aktarma hatası: {str(e)}")

def ders_secim_ekrani():
    app = DersSecimEkrani()
    app.window.mainloop()

if __name__ == "__main__":
    ders_secim_ekrani()
