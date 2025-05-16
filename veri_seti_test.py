import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class YapayZekaTestEkrani:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Veri Seti Testi")
        self.pencere.geometry("700x450")

        self.veri_seti_adi = ""
        self.veri_seti_yolu = ""
        self.model_yolu = ""
        self.test_orani = 0.0
        self.veri_seti_turu = ""

        self.baslik_olustur()
        self.adim_butonlarini_olustur()
        self.test_et_butonu_olustur()

    def baslik_olustur(self):
        baslik = tk.Label(self.pencere, text="Test İşlemine Başlamak İçin Sırasıyla Aşağıdaki İşlemleri Uygulayınız.",
                          font=("Arial", 12), wraplength=600, justify="center", fg="blue")
        baslik.pack(pady=10)

    def adim_butonlarini_olustur(self):
        self.adim_frame = tk.Frame(self.pencere)
        self.adim_frame.pack(pady=10)

        # 1. adım - veri seti
        self.btn1 = tk.Button(self.adim_frame, text="1- Veri Setini Seçin", command=self.veri_seti_ekle)
        self.btn1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.label1 = tk.Label(self.adim_frame, text="")
        self.label1.grid(row=0, column=1, padx=10)

        # 2. adım - model seçimi
        self.btn2 = tk.Button(self.adim_frame, text="2- Modeli Seçin", command=self.model_sec, state="disabled")
        self.btn2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.label2 = tk.Label(self.adim_frame, text="")
        self.label2.grid(row=1, column=1, padx=10)

        # 3. adım - test oranı belirleme
        self.oran_label = tk.Label(self.adim_frame, text="3- Test Oranını Belirleyin:")
        self.oran_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.oran_olcegi = tk.Scale(self.adim_frame, from_=1, to=20, orient="horizontal", length=200)
        self.oran_olcegi.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")
        self.oran_goster = tk.Label(self.adim_frame, text="Seçilen Test Oranı: %0")
        self.oran_goster.grid(row=4, column=0, padx=3)

        self.oran_olcegi.bind("<B1-Motion>", self.oran_guncelle)
        self.btn_oran_onayla = tk.Button(self.adim_frame, text="Oranı Onayla", command=self.orani_onayla, state="disabled")
        self.btn_oran_onayla.grid(row=4, column=1, pady=3)

    def test_et_butonu_olustur(self):
        self.test_butonu = tk.Button(self.pencere, text="Veri Setini Test Et", command=self.test_et, state="disabled")
        self.test_butonu.pack(pady=10)

    def oran_guncelle(self,event=None):
        oran = self.oran_olcegi.get()
        self.oran_goster.config(text=f"Oran: %{oran}")
        self.btn_oran_onayla.config(state="normal")

    def orani_onayla(self):
        self.test_orani = self.oran_olcegi.get()
        self.oran_olcegi.config(state="disabled")
        self.btn_oran_onayla.config(state="disabled")
        self.test_butonu.config(state="normal")

    def veri_seti_ekle(self):
         pencere = tk.Toplevel(self.pencere)
         pencere.title("Veri Seti Türü Seçimi")
         pencere.geometry("400x300")
         pencere.attributes("-topmost", True)
         tur = tk.StringVar()
         tur.set(None)

         tk.Label(pencere, text="Veri Setinizin Çıktı Türünü Seçin:").pack(pady=(10, 5))
         tk.Radiobutton(pencere, text="Sayısal Veri Seti", variable=tur, value="Sayısal", takefocus=0).pack(padx=20)
         tk.Radiobutton(pencere, text="Metinsel Veri Seti", variable=tur, value="Metinsel", takefocus=0).pack(padx=20)
         tk.Radiobutton(pencere, text="Görsel Veri Seti", variable=tur, value="Görsel", takefocus=0).pack(padx=20)

         sec_onay_btn = tk.Button(pencere, text="Tür Seçimini Onayla")
         sec_onay_btn.pack(pady=10)
        #  radio buttonlar tıklanmadan seçildiği için çözüm olarak yeni pencere ekleidk
         file_frame = tk.Frame(pencere)
         file_frame.pack(pady=5)
         lbl_dosya = tk.Label(file_frame, text="Veri Seti Dosyasını Seçin:")
         lbl_dosya.grid(row=0, column=0, padx=5, sticky="e")
         combo = ttk.Combobox(file_frame, state="disabled", width=25)
         combo.grid(row=0, column=1, padx=5)

         def secimi_onayla():
            secim = tur.get()
            if secim == None:
                  messagebox.showwarning("Uyarı", "Lütfen veri setinizin çıktı türünü seçin.")
                  return

            self.veri_seti_turu = secim
            messagebox.showinfo(
                  "Bilgi",
                  "Seçtiğiniz Veri Seti Türü Kaydedildi.\nKullanacağınız Veri Setinizi Kullanıma Açılacak Listeden Seçin.\nEğer Veri Setiniz Listede Yoksa veri_setleri Klasörüne Ekleyin.\nArdından Mevcut İşleminizi Tekrar Başlatın."
            )

            klasor = "veri_setleri"
            if not os.path.exists(klasor):
                os.makedirs(klasor)

            dosyalar = [f for f in os.listdir(klasor) if f.endswith(".csv")]
            if not dosyalar:
                  messagebox.showwarning("Uyarı", "Klasörde .csv dosyası yok.")
                  return
      
            combo.configure(values=dosyalar, state="readonly")
            sec_onay_btn.pack_forget()  # Buton gizleniyor
         sec_onay_btn.config(command=secimi_onayla)        
         def dosya_sec():
            secilen = combo.get()
            if not secilen:
                messagebox.showwarning("Uyarı", "Veri seti seçilmedi.")
                return
            self.veri_seti_adi = secilen
            self.veri_seti_yolu = os.path.join("veri_setleri", secilen)
            self.label1.config(text=f"{secilen} ({self.veri_seti_turu})")
            self.btn1.config(state="disabled")
            self.btn2.config(state="normal")
            pencere.destroy()

         tk.Button(pencere, text="Dosyayı Onayla", command=dosya_sec).pack(pady=10)

    def model_sec(self):
        pencere = tk.Toplevel(self.pencere)
        pencere.title("Model Seçimi")
        pencere.geometry("900x500")
        pencere.attributes("-topmost", True)

        tk.Label(pencere, text="Programdaki Tüm Modeller Listeleniyor..", font=("Arial", 12, "bold")).pack(pady=10)

        frame = tk.Frame(pencere)
        frame.pack()

        # Listeler
        regresyon_list = tk.Listbox(frame, height=15, width=45, exportselection=False)
        siniflandirma_list = tk.Listbox(frame, height=15, width=45, exportselection=False)
        regresyon_list.grid(row=1, column=0, padx=20)
        siniflandirma_list.grid(row=1, column=1, padx=20)

        tk.Label(frame, text="Regresyon Modelleri").grid(row=0, column=0)
        tk.Label(frame, text="Sınıflandırma Modelleri").grid(row=0, column=1)

        # Dosyaları yükle
        reg_path = os.path.join("modeller", "regresyon")
        clf_path = os.path.join("modeller", "siniflandirma")
        regresyon_modelleri = [f for f in os.listdir(reg_path) if f.endswith(".py")]
        siniflandirma_modelleri = [f for f in os.listdir(clf_path) if f.endswith(".py")]

        for model in regresyon_modelleri:
            regresyon_list.insert(tk.END, model)
        for model in siniflandirma_modelleri:
            siniflandirma_list.insert(tk.END, model)

        # Seçim kutusu ve onay
        secim_frame = tk.Frame(pencere)
        secim_frame.pack(pady=20)

        secilen_model = tk.StringVar()
        tk.Label(secim_frame, text="Model Seçiminizi Yapınız", font=("Arial", 12, "bold")).pack()

        model_combo = ttk.Combobox(secim_frame, state="readonly", width=60)
        if self.veri_seti_turu == "Sayısal":
            model_combo['values'] = regresyon_modelleri
        else:
            model_combo['values'] = siniflandirma_modelleri
        model_combo.pack(pady=10)

        def modeli_onayla():
            secim = model_combo.get()
            if not secim:
                messagebox.showwarning("Uyarı", "Model seçilmedi.")
                return
            # Yolu belirle
            model_klasoru = "regresyon" if self.veri_seti_turu == "Sayısal" else "siniflandirma"
            self.model_yolu = os.path.join("modeller", model_klasoru, secim)
            self.label2.config(text=secim)
            self.btn2.config(state="disabled")
            self.btn_oran_onayla.config(state="normal")
            pencere.destroy()

        tk.Button(secim_frame, text="Modeli Onayla", command=modeli_onayla).pack(pady=10)

    def test_et(self):
      if not self.veri_seti_yolu or not self.model_yolu or self.test_orani == 0.0:
         messagebox.showwarning("Eksik Bilgi", "Lütfen veri seti, model ve test oranını seçtiğinizden emin olun.")
         return

      test_pencere = tk.Toplevel(self.pencere)
      test_pencere.title("Veri Seti Testi")
      test_pencere.geometry("700x600")

# Uygulamayı başlat
pencere = tk.Tk()
app = YapayZekaTestEkrani(pencere)
pencere.mainloop()