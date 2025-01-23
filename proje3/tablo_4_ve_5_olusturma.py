import pandas as pd
import numpy as np
from tkinter import messagebox
import os
from constants import FILE_NAMES

def tablo_4_ve_5_olustur():
    try:
        print("DEBUG: Tablo 4 ve 5 oluşturma başlatılıyor...")
        
        # Dosyaları yükle
        tablo1_df = pd.read_excel(FILE_NAMES['tablo1'], index_col=0)
        tablo2_df = pd.read_excel(FILE_NAMES['tablo2'], index_col=0)
        notlar_df = pd.read_excel(FILE_NAMES['ogrenci_notlari'])
        
        # Sütun isimlerini kontrol et
        print("DEBUG: Öğrenci notları sütunları:", list(notlar_df.columns))

        # Doğru sütun adını kullan
        ogrenci_no_column = 'Ogrenci_No'

        print("DEBUG: Tablo 4 hesaplanıyor...")
        # Tablo 4 hesaplama
        tablo4_data = []
        for _, ogrenci in notlar_df.iterrows():
            ogrenci_no = ogrenci[ogrenci_no_column]  # Doğru sütun adı kullanıldı
            ders_ciktilari_notlari = []
            for i, ders_ciktisi in enumerate(tablo2_df.index):
                toplam_puan = sum(
                    ogrenci[kriter] * tablo2_df.loc[ders_ciktisi, kriter]
                    for kriter in tablo2_df.columns
                )
                ders_ciktilari_notlari.append(toplam_puan)
            tablo4_data.append({'Öğrenci No': ogrenci_no, **{f'D{i+1}': puan for i, puan in enumerate(ders_ciktilari_notlari)}})

        tablo4_df = pd.DataFrame(tablo4_data)
        tablo4_df.to_excel(FILE_NAMES['tablo4'], index=False)
        print("DEBUG: Tablo 4 başarıyla kaydedildi.")

        print("DEBUG: Tablo 5 hesaplanıyor...")
        # Tablo 5 hesaplama
        tablo5_data = []
        for _, ogrenci in notlar_df.iterrows():
            ogrenci_no = ogrenci[ogrenci_no_column]  # Doğru sütun adı kullanıldı
            program_ciktilari_notlari = []
            for j, program_ciktisi in enumerate(tablo1_df.columns):
                toplam_puan = sum(
                    tablo1_df.loc[ders_ciktisi, program_ciktisi] * tablo4_df.loc[_, f'D{i+1}']
                    for i, ders_ciktisi in enumerate(tablo2_df.index)
                )
                program_ciktilari_notlari.append(toplam_puan)
            tablo5_data.append({'Öğrenci No': ogrenci_no, **{f'P{i+1}': puan for i, puan in enumerate(program_ciktilari_notlari)}})

        tablo5_df = pd.DataFrame(tablo5_data)
        tablo5_df.to_excel(FILE_NAMES['tablo5'], index=False)
        print("DEBUG: Tablo 5 başarıyla kaydedildi.")

        print("DEBUG: İstatistiksel analizler hesaplanıyor...")
        # Tablo 4 ve Tablo 5 için istatistiksel analiz
        tablo4_stats = tablo4_df.describe()
        tablo5_stats = tablo5_df.describe()

        tablo4_stats.to_excel(FILE_NAMES['tablo4_stats'])
        tablo5_stats.to_excel(FILE_NAMES['tablo5_stats'])
        print("DEBUG: İstatistiksel analizler başarıyla kaydedildi.")

        messagebox.showinfo("Başarılı", "Tablo 4 ve Tablo 5 başarıyla oluşturuldu!")
    except Exception as e:
        print(f"DEBUG: Hata oluştu: {str(e)}")
        messagebox.showerror("Hata", f"Tablolar oluşturulurken hata oluştu:\n{str(e)}")
