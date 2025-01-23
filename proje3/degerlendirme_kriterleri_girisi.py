import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import pandas as pd

class DegerlendirmeKriterleriGirisi:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Değerlendirme Kriterleri Girişi")
        self.window.geometry("900x600")
        
        # Stil ayarları
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Info.TLabel", font=("Arial", 10))
        style.configure("Action.TButton", padding=5)
        style.configure("List.Treeview", rowheight=30, font=("Arial", 10))
        style.configure("List.Treeview.Heading", font=("Arial", 10, "bold"))
        
        self.kriterler = []
        self.create_widgets()
        self.load_existing_data()

    def create_widgets(self):
        # Ana container
        main_container = ttk.Frame(self.window, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Başlık
        ttk.Label(main_container, 
                 text="Değerlendirme Kriterleri Girişi",
                 style="Title.TLabel").pack(pady=(0,20))
        
        # Sol panel - Kriter ekleme
        left_panel = ttk.LabelFrame(main_container, text="Yeni Kriter Ekle", padding=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        # Kriter seçimi
        kriter_frame = ttk.Frame(left_panel)
        kriter_frame.pack(fill="x", pady=5)
        
        ttk.Label(kriter_frame, text="Kriter:", 
                 style="Header.TLabel").pack(side="left", padx=5)
        
        self.kriter_combo = ttk.Combobox(kriter_frame, values=[
            "Ödev", "Proje", "Sunum", "Rapor", "KPL",
            "Derse Katılım", "Vize", "Final"
        ], width=20)
        self.kriter_combo.pack(side="left", padx=5)
        
        # Ağırlık girişi
        agirlik_frame = ttk.Frame(left_panel)
        agirlik_frame.pack(fill="x", pady=5)
        
        ttk.Label(agirlik_frame, text="Ağırlık (%):", 
                 style="Header.TLabel").pack(side="left", padx=5)
        
        self.agirlik_entry = ttk.Entry(agirlik_frame, width=10)
        self.agirlik_entry.pack(side="left", padx=5)
        
        # Ekle butonu
        ttk.Button(left_panel, text="Kriter Ekle", 
                  style="Action.TButton",
                  command=self.add_kriter).pack(pady=10)
        
        # Toplam ağırlık göstergesi
        self.toplam_label = ttk.Label(left_panel, 
                                    text="Toplam Ağırlık: %0",
                                    style="Info.TLabel")
        self.toplam_label.pack(pady=10)
        
        # Sağ panel - Kriter listesi
        right_panel = ttk.LabelFrame(main_container, text="Mevcut Kriterler", padding=10)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Kriter listesi (Treeview)
        self.kriter_tree = ttk.Treeview(right_panel, 
                                      columns=("kriter", "agirlik"),
                                      show="headings",
                                      style="List.Treeview")
        
        self.kriter_tree.heading("kriter", text="Kriter")
        self.kriter_tree.heading("agirlik", text="Ağırlık (%)")
        
        self.kriter_tree.column("kriter", width=150)
        self.kriter_tree.column("agirlik", width=100)
        
        self.kriter_tree.pack(fill="both", expand=True, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="Seçili Kriteri Düzenle",
                  style="Action.TButton",
                  command=self.edit_kriter).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Seçili Kriteri Sil",
                  style="Action.TButton",
                  command=self.delete_kriter).pack(side="left", padx=5)
        
        # Alt butonlar
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill="x", pady=20)
        
        ttk.Button(bottom_frame, text="Kaydet",
                  style="Action.TButton",
                  command=self.save_data).pack(side="left", padx=5)
        
        ttk.Button(bottom_frame, text="İptal",
                  style="Action.TButton",
                  command=self.window.destroy).pack(side="right", padx=5)

    def add_kriter(self):
        kriter = self.kriter_combo.get()
        try:
            agirlik = float(self.agirlik_entry.get())
            if not (0 <= agirlik <= 100):
                raise ValueError("Ağırlık 0-100 arasında olmalıdır")
                
            # Toplam ağırlık kontrolü
            toplam = sum(float(self.kriter_tree.item(item)["values"][1]) 
                        for item in self.kriter_tree.get_children())
            if toplam + agirlik > 100:
                raise ValueError("Toplam ağırlık 100'ü geçemez")
            
            self.kriter_tree.insert("", "end", values=(kriter, agirlik))
            self.update_toplam()
            
            # Formu temizle
            self.kriter_combo.set("")
            self.agirlik_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def edit_kriter(self):
        selected = self.kriter_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen düzenlenecek kriteri seçin!")
            return
            
        item = selected[0]
        values = self.kriter_tree.item(item)["values"]
        
        # Düzenleme penceresi
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Kriter Düzenle")
        edit_window.geometry("300x200")
        
        ttk.Label(edit_window, text="Kriter:").pack(pady=5)
        kriter_entry = ttk.Entry(edit_window)
        kriter_entry.insert(0, values[0])
        kriter_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Ağırlık (%):").pack(pady=5)
        agirlik_entry = ttk.Entry(edit_window)
        agirlik_entry.insert(0, values[1])
        agirlik_entry.pack(pady=5)
        
        def save_edit():
            try:
                yeni_agirlik = float(agirlik_entry.get())
                if not (0 <= yeni_agirlik <= 100):
                    raise ValueError("Ağırlık 0-100 arasında olmalıdır")
                
                # Toplam ağırlık kontrolü
                toplam = sum(float(self.kriter_tree.item(i)["values"][1]) 
                           for i in self.kriter_tree.get_children() if i != item)
                if toplam + yeni_agirlik > 100:
                    raise ValueError("Toplam ağırlık 100'ü geçemez")
                
                self.kriter_tree.item(item, values=(kriter_entry.get(), yeni_agirlik))
                self.update_toplam()
                edit_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Hata", str(e))
        
        ttk.Button(edit_window, text="Kaydet", 
                  command=save_edit).pack(pady=10)

    def delete_kriter(self):
        selected = self.kriter_tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silinecek kriteri seçin!")
            return
            
        if messagebox.askyesno("Onay", "Seçili kriteri silmek istediğinize emin misiniz?"):
            self.kriter_tree.delete(selected[0])
            self.update_toplam()

    def update_toplam(self):
        toplam = sum(float(self.kriter_tree.item(item)["values"][1]) 
                    for item in self.kriter_tree.get_children())
        self.toplam_label.config(text=f"Toplam Ağırlık: %{toplam:.1f}")

    def save_data(self):
        try:
            data = []
            toplam = 0
            
            # Verileri topla
            for item in self.kriter_tree.get_children():
                values = self.kriter_tree.item(item)["values"]
                kriter = values[0]
                agirlik = float(values[1])
                toplam += agirlik
                data.append({
                    'kriter': kriter,
                    'agirlik': agirlik
                })
            
            if toplam != 100:
                messagebox.showerror("Hata", 
                    f"Toplam ağırlık 100 olmalıdır! (Şu an: {toplam:.1f})")
                return
            
            # DataFrame oluştur ve Excel'e kaydet
            df = pd.DataFrame(data)
            df.to_excel("degerlendirme_kriterleri.xlsx", index=False)
            
            messagebox.showinfo("Başarılı", "Değerlendirme kriterleri kaydedildi!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

    def load_existing_data(self):
        try:
            if os.path.exists("degerlendirme_kriterleri.xlsx"):
                df = pd.read_excel("degerlendirme_kriterleri.xlsx")
                
                for _, row in df.iterrows():
                    self.kriter_tree.insert("", "end", 
                        values=(row['kriter'], row['agirlik']))
                self.update_toplam()
                    
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yükleme hatası: {str(e)}")

    def load_from_excel(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Excel Dosyası Seç",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not file_path:
                return
            
            df = pd.read_excel(file_path)
            
            if 'kriter' not in df.columns or 'agirlik' not in df.columns:
                raise ValueError("Excel dosyası uygun formatta değil!")
            
            # Mevcut kriterleri temizle
            for item in self.kriter_tree.get_children():
                self.kriter_tree.delete(item)
            
            # Yeni kriterleri ekle
            for _, row in df.iterrows():
                kriter = row['kriter']
                agirlik = float(row['agirlik'])
                
                if not (0 <= agirlik <= 100):
                    raise ValueError(f"Geçersiz ağırlık değeri: {agirlik}")
                    
                self.kriter_tree.insert("", "end", values=(kriter, agirlik))
            
            self.update_toplam()
            messagebox.showinfo("Başarılı", "Kriterler Excel'den yüklendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Excel yükleme hatası: {str(e)}")

    def export_to_excel(self):
        try:
            data = []
            for item in self.kriter_tree.get_children():
                values = self.kriter_tree.item(item)["values"]
                data.append({
                    'kriter': values[0],
                    'agirlik': float(values[1])
                })
            
            df = pd.DataFrame(data)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Başarılı", "Kriterler Excel'e aktarıldı!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Excel'e aktarma hatası: {str(e)}")

def degerlendirme_kriterleri_girisi_pencere(parent):
    DegerlendirmeKriterleriGirisi(parent)
