import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
import pandas as pd

def program_ciktilari_girisi_pencere(parent):
    # Yeni bir pencere oluştur
    program_pencere = Toplevel(parent)
    program_pencere.title("Program Çıktıları Girişi")
    program_pencere.geometry("400x300")

    # Giriş alanı ve butonlar
    tk.Label(program_pencere, text="Program Çıktısı Girin (Her biri yeni satırda):").pack(pady=10)
    cikti_text = tk.Text(program_pencere, height=10, width=40)
    cikti_text.pack(pady=5)

    def kaydet():
        ciktilar = cikti_text.get("1.0", tk.END).strip().split("\n")
        ciktilar = [c for c in ciktilar if c.strip()]
        if ciktilar:
            print("Program Çıktıları Kaydedildi:", ciktilar)
            messagebox.showinfo("Başarılı", "Program çıktıları kaydedildi!")
            program_pencere.destroy()
        else:
            messagebox.showerror("Hata", "Program çıktıları girilmelidir!")

    tk.Button(program_pencere, text="Kaydet", command=kaydet).pack(pady=20)

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
                    messagebox.showinfo("Başarılı", "Program çıktıları yüklendi!")
                else:
                    messagebox.showerror("Hata", "'Cikti' sütunu bulunamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya okunamadı: {e}")

    tk.Button(program_pencere, text="Dosya Yükle", command=dosya_yukle).pack(pady=10)
