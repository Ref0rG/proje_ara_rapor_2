import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# GLOBAL DEĞİŞKENLER
dosya_adi = ""
sutunlar = []
veri_kutulari = {}
veri_seti_yolu = None

# === ORTAK KLASÖR KONTROL FONKSİYONU ===
def klasoru_olustur(yol="veri_setleri"):
    if not os.path.exists(yol):
        os.makedirs(yol)

# === MANUEL VERİ SETİ OLUŞTURMA FONKSİYONLARI ===
def veri_seti_adi_al():
    global dosya_adi
    dosya_adi = veri_seti_giris.get().strip()
    
    if not dosya_adi:
        messagebox.showwarning("Uyarı", "Lütfen veri seti adını girin!")
        return
    
    veri_seti_giris.config(state=tk.DISABLED)
    veri_seti_onay_butonu.config(state=tk.DISABLED)
    sutun_sayisi_cerceve.grid(row=3, column=0, columnspan=2, pady=10)

def sutun_sayisi_al():
    try:
        sutun_sayisi = int(sutun_sayisi_giris.get().strip())
        if sutun_sayisi <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Uyarı", "Lütfen geçerli bir sütun sayısı girin!")
        return
    
    sutun_sayisi_giris.config(state=tk.DISABLED)
    sutun_sayisi_onay_butonu.config(state=tk.DISABLED)
    sutunlari_al(sutun_sayisi)

def sutunlari_al(sutun_sayisi):
    global sutunlar, veri_kutulari
    sutunlar.clear()
    veri_kutulari.clear()
    sutun_sayisi_cerceve.grid_forget()

    for i in range(sutun_sayisi):
        label = tk.Label(sutun_cercevesi, text=f"Sütun {i+1} Adı:")
        label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
        sutun_giris = tk.Entry(sutun_cercevesi)
        sutun_giris.grid(row=i, column=1, padx=5, pady=2)
        veri_kutulari[f"sutun_{i+1}"] = sutun_giris

    sutunlari_onayla_buton.grid(row=sutun_sayisi, column=0, columnspan=2, pady=10)
    sutun_cercevesi.grid(row=4, column=0, columnspan=2, pady=10)

def sutunlari_onayla():
    global sutunlar
    for key in veri_kutulari:
        sutun_adi = veri_kutulari[key].get().strip()
        if not sutun_adi:
            messagebox.showwarning("Uyarı", "Sütun adı boş bırakılamaz!")
            return
        sutunlar.append(sutun_adi)
    
    sutun_cercevesi.grid_forget()
    sutunlari_onayla_buton.grid_forget()
    veri_giris_arayuzu_olustur()

def veri_giris_arayuzu_olustur():
    for i, sutun in enumerate(sutunlar):
        tk.Label(veri_cercevesi, text=sutun, font=('Arial', 10, 'bold')).grid(row=i, column=0, padx=5, pady=5, sticky="w")
        giris_kutusu = tk.Entry(veri_cercevesi)
        giris_kutusu.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        veri_kutulari[sutun] = giris_kutusu

    kaydet_buton.grid(row=len(sutunlar), column=0, columnspan=2, pady=10)
    veri_cercevesi.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

def veriyi_kaydet():
    if not dosya_adi or not sutunlar:
        messagebox.showwarning("Uyarı", "Lütfen önce veri seti adını ve sütunları girin!")
        return

    yeni_kayit = {sutun: veri_kutulari[sutun].get().strip() for sutun in sutunlar}
    klasoru_olustur()
    dosya_yolu = os.path.join("veri_setleri", f"{dosya_adi}.csv")
    dosya_var = os.path.exists(dosya_yolu)

    with open(dosya_yolu, mode='a', newline='', encoding='utf-8') as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=sutunlar)
        if not dosya_var:
            yazici.writeheader()
        yazici.writerow(yeni_kayit)

    messagebox.showinfo("Başarılı", "Veri başarıyla kaydedildi!")

    for kutu in veri_kutulari.values():
        kutu.delete(0, tk.END)

# === MEVCUT VERİ SETİNDEN DEVAM BUTONU ve FONKSİYONLARI ===
def mevcut_veri_setinden_devam_et():
    klasoru_olustur()
    dosyalar = [f for f in os.listdir("veri_setleri") if f.endswith(".csv")]

    if not dosyalar:
        messagebox.showwarning("Uyarı", "Klasör boş! Lütfen bir veri seti ekleyin ve tekrar deneyin.")
        return

    secim_pencere = tk.Toplevel(pencere)
    secim_pencere.title("Veri Seti Seçimi")
    secim_pencere.geometry("300x200")

    tk.Label(secim_pencere, text="Veri Setini Seçin:").pack(pady=10)
    combo = ttk.Combobox(secim_pencere, values=dosyalar, state="readonly")
    combo.pack(pady=10)

    def onayla():
        global veri_seti_yolu, sutunlar
        secilen = combo.get()
        if not secilen:
            messagebox.showwarning("Uyarı", "Lütfen bir veri seti seçin.")
            return

        veri_seti_yolu = os.path.join("veri_setleri", secilen)
        df = pd.read_csv(veri_seti_yolu)
        sutunlar.clear()
        sutunlar.extend(df.columns)
        secim_pencere.destroy()
        mevcut_veri_giris_ekrani(df)

    tk.Button(secim_pencere, text="Onayla", command=onayla).pack(pady=10)

def mevcut_veri_giris_ekrani(df):
    for widget in ana_cerceve.winfo_children():
        widget.grid_forget()

    bilgi = tk.Label(ana_cerceve, text=f"{os.path.basename(veri_seti_yolu)} dosyasına veri ekleyin", font=("Arial", 10, "bold"))
    bilgi.grid(row=0, column=0, columnspan=2, pady=10)

    veri_kutulari.clear()
    for i, sutun in enumerate(df.columns):
        tk.Label(ana_cerceve, text=sutun).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(ana_cerceve)
        entry.grid(row=i+1, column=1, padx=5, pady=5)
        veri_kutulari[sutun] = entry

    def kaydet():
        yeni_veri = [veri_kutulari[s].get() for s in df.columns]
        if not all(yeni_veri):
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return
        yeni_kayit = pd.DataFrame([yeni_veri], columns=df.columns)
        df2 = pd.concat([df, yeni_kayit], ignore_index=True)
        df2.to_csv(veri_seti_yolu, index=False)

        for e in veri_kutulari.values():
            e.delete(0, tk.END)
        messagebox.showinfo("Başarılı", "Veri başarıyla eklendi.")

    tk.Button(ana_cerceve, text="Veriyi Kaydet", command=kaydet).grid(row=len(df.columns)+2, column=0, columnspan=2, pady=10)

# === TKINTER ARAYÜZ BAŞLAT ===
pencere = tk.Tk()
pencere.title("Veri Seti Oluşturucu ve Düzenleyici")
pencere.geometry("900x650")

ana_cerceve = tk.Frame(pencere)
ana_cerceve.grid(row=0, column=0, padx=10, pady=10)

# Bilgilendirme metni
bilgi_metni = tk.Label(ana_cerceve, text="Oluşturacağınız bu veri setinde her kayıt için kaydet butonuna bastıktan sonra tekrar yeni gözlemlerinizi girerek işleminize devam edebilirsiniz.",
                      fg="blue", font=("Arial", 10, "italic"), wraplength=900, justify="center")
bilgi_metni.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Mevcut veri setinden devam butonu (EKLENEN YER)
tk.Button(ana_cerceve, text="Mevcut Veri Setinden Devam Et", command=mevcut_veri_setinden_devam_et).grid(row=1, column=0, columnspan=2, pady=(0, 20))

# Veri seti adı girişi
veri_seti_cerceve = tk.Frame(ana_cerceve)
veri_seti_cerceve.grid(row=2, column=0, columnspan=2, pady=(0, 10))

tk.Label(veri_seti_cerceve, text="Veri Seti Adı:").grid(row=0, column=0, padx=5)
veri_seti_giris = tk.Entry(veri_seti_cerceve, width=30)
veri_seti_giris.grid(row=0, column=1, padx=5)
veri_seti_onay_butonu = tk.Button(veri_seti_cerceve, text="Onayla", command=veri_seti_adi_al)
veri_seti_onay_butonu.grid(row=0, column=2, padx=5)

# Geri kalan giriş alanları (başlangıçta gizli)
sutun_sayisi_cerceve = tk.Frame(ana_cerceve)
sutun_sayisi_giris = tk.Entry(sutun_sayisi_cerceve, width=10)
tk.Label(sutun_sayisi_cerceve, text="Sütun Sayısı:").grid(row=0, column=0, padx=5)
sutun_sayisi_giris.grid(row=0, column=1, padx=5)
sutun_sayisi_onay_butonu = tk.Button(sutun_sayisi_cerceve, text="Tamam", command=sutun_sayisi_al)
sutun_sayisi_onay_butonu.grid(row=0, column=2, padx=5)

sutun_cercevesi = tk.Frame(ana_cerceve)
sutunlari_onayla_buton = tk.Button(ana_cerceve, text="Sütunları Onayla", command=sutunlari_onayla)
veri_cercevesi = tk.Frame(ana_cerceve)
kaydet_buton = tk.Button(ana_cerceve, text="Verileri Kaydet", command=veriyi_kaydet)

# Uygulama döngüsü
pencere.mainloop()
