import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import islem

class PlakaTanimlamaUygulamasi:
    def __init__(self, master):
        self.master = master
        self.master.title("Plaka Tanıma Uygulaması")

        self.label_resim_adresi = tk.Label(master, text="Resim adı ve uzantısı giriniz.:")
        self.label_resim_adresi.pack(pady=10)

        self.entry_resim_adresi = tk.Entry(master)
        self.entry_resim_adresi.pack(pady=10)

        self.buton_onayla = tk.Button(master, text="Onayla", command=self.onayla)
        self.buton_onayla.pack(pady=10)

        self.label_durum = tk.Label(master, text="")
        self.label_durum.pack(pady=10)

        self.buton_plaka_tespit = tk.Button(master, text="Plakayı Tespit Et", command=self.plaka_tespit_et)
        self.buton_plaka_tespit.pack(pady=10)

    def onayla(self):
        resim_adresi = self.entry_resim_adresi.get()
        resim_klasoru = "Resim"

        if os.path.exists(os.path.join(resim_klasoru, resim_adresi)):
            image = Image.open(os.path.join(resim_klasoru, resim_adresi))
            image.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.label_durum.config(image=photo, text="Resim Onaylandı", compound="right", fg="green")
            self.label_durum.photo = photo
        else:
            self.label_durum.config(text="Geçersiz Resim Adresi", image=None, fg="red")

    def plaka_tespit_et(self):
        resim_adresi = self.entry_resim_adresi.get()
        if resim_adresi:
            try:
                sonuc = islem.goruntu(resim_adresi)
                self.label_durum.config(text=sonuc)
                self.master.destroy()  # Arayüzü kapat
            except Exception as e:
                self.label_durum.config(text=f"Hata: {str(e)}", fg="red")
        else:
            self.label_durum.config(text="Lütfen bir resim adresi girin.")

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = PlakaTanimlamaUygulamasi(root)
    root.mainloop()
