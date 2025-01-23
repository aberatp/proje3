import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
import pandas as pd

def ders_ciktilari_girisi_pencere(parent):
    # Yeni bir pencere oluştur
    ders_pencere = Toplevel(parent)
    ders_pencere.title("Ders Çıktıları Girişi")
    ders_pencere.geometry("400x300")

    # Giriş alanı ve butonlar
    tk.Label(ders_pencere, text="Ders Çıktısı Girin (Her biri yeni satırda):").pack(pady=10)
    cikti_text = tk.Text(ders_pencere, height=10, width=40)
    cikti_text.pack(pady=5)

    def kaydet():
        ciktilar = cikti_text.get("1.0", tk.END).strip().split("\n")
        ciktilar = [c for c in ciktilar if c.strip()]
        if ciktilar:
            print("Ders Çıktıları Kaydedildi:", ciktilar)
            messagebox.showinfo("Başarılı", "Ders çıktıları kaydedildi!")
            ders_pencere.destroy()
        else:
            messagebox.showerror("Hata", "Ders çıktıları girilmelidir!")

    tk.Button(ders_pencere, text="Kaydet", command=kaydet).pack(pady=20)

    def dosya_yukle():
        file_path = filedialog.askopenfilename(
            title="Dosya Seç",
            filetypes=[("Excel Dosyaları", "*.xlsx")]
        )
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if "Cikti" in df.columns:
                    cikti_text.delete("1.0", tk.END)
                    cikti_text.insert(tk.END, "\n".join(df["Cikti"].astype(str).tolist()))
                    messagebox.showinfo("Başarılı", "Ders çıktıları yüklendi!")
                else:
                    messagebox.showerror("Hata", "'Cikti' sütunu bulunamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya okunamadı: {e}")

    tk.Button(ders_pencere, text="Dosya Yükle", command=dosya_yukle).pack(pady=10)
