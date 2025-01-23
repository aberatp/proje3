import tkinter as tk
from tkinter import Toplevel

def ders_ekle_pencere(parent):
    # Yeni bir pencere oluştur
    ders_pencere = Toplevel(parent)
    ders_pencere.title("Ders Ekle")
    ders_pencere.geometry("400x300")

    # Etiket ve giriş alanları
    tk.Label(ders_pencere, text="Ders Kodu:").pack(pady=5)
    ders_kodu = tk.Entry(ders_pencere)
    ders_kodu.pack(pady=5)

    tk.Label(ders_pencere, text="Ders Adı:").pack(pady=5)
    ders_adi = tk.Entry(ders_pencere)
    ders_adi.pack(pady=5)

    # Kaydet butonu
    def kaydet():
        kod = ders_kodu.get()
        ad = ders_adi.get()
        if kod and ad:
            print(f"Ders Eklendi: {kod} - {ad}")
            ders_pencere.destroy()
        else:
            tk.messagebox.showerror("Hata", "Ders kodu ve adı girilmelidir!")

    tk.Button(ders_pencere, text="Kaydet", command=kaydet).pack(pady=20)
