import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
import pandas as pd

def ogrenci_listesi_yukle_pencere(parent):
    # Yeni bir pencere oluştur
    ogrenci_pencere = Toplevel(parent)
    ogrenci_pencere.title("Öğrenci Listesi Yükle")
    ogrenci_pencere.geometry("400x300")

    # Dosya yükleme butonu
    def dosya_yukle():
        file_path = filedialog.askopenfilename(
            title="Öğrenci Listesi Seç",
            filetypes=[("Excel Dosyaları", "*.xlsx")]
        )
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if "Ogrenci_No" in df.columns:
                    messagebox.showinfo("Başarılı", "Öğrenci listesi yüklendi!")
                    print(df["Ogrenci_No"].tolist())
                    ogrenci_pencere.destroy()
                else:
                    messagebox.showerror("Hata", "Dosyada 'Ogrenci_No' sütunu bulunamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya okunamadı: {e}")

    tk.Button(ogrenci_pencere, text="Öğrenci Listesi Yükle", command=dosya_yukle).pack(pady=20)
