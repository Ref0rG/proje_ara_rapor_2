import tkinter as tk
from tkinter import Toplevel, StringVar
import subprocess

class Secim_Yap:
    def __init__(self, pencere):
        # Ana pencere ayarları
        self.pencere = pencere
        self.pencere.title("VERİ KÜPÜ")
        self.pencere.geometry("700x500")
        self.pencere.configure(bg="lightblue")
        
        # Ana çerçeve oluşturuluyor
        self.cerceve = tk.Frame(pencere, bg="lightblue")
        self.cerceve.pack(expand=True)
        
        # Başlık etiketi ekleniyor
        self.etiket = tk.Label(self.cerceve, text="Yapmak İstediğiniz İşlemi Seçin", font=("Arial", 16), fg="blue", bg="orange", width=30)
        self.etiket.pack(pady=20)
        
        # Buton isimleri ve çalıştırılacak komutlar tanımlanıyor
        self.butonlar = {
            "Modülleri Kontrol Et": "kutuphane_pip.py",  # menu.py ile aynı klasörde bulunan kutuphane_pip.py çalıştırılacak
            "Veri Seti Oluştur": self.veri_seti_olustur,    # yeni pencere açılarak seçim yapılacak
            "Veri Seti Test Et": "veri_seti_test.py",        # veri_seti_test.py çalıştırılacak
            "Geçmiş Kayıtları Görüntüle": "test_kayit.py"     # test_kayit.py çalıştırılacak
        }
        
        # Tanımlanan her işlem için buton oluşturuluyor
        # lambda ile basit bir döngü içerisinde butonlar oluşturuldu.
        for yazi, komut in self.butonlar.items():
            buton = tk.Button(self.cerceve, text=yazi, font=("Arial", 14), command=lambda t=komut: self.islem_yap(t), bg="green", width=30)
            buton.pack(pady=5)
    
    def islem_yap(self, komut):
        # Eğer komut fonksiyon ise (örn. Veri Seti Oluştur) onu çağırır, değilse subprocess ile .py dosyasını çalıştırır
        if callable(komut):
            komut()
        else:
            subprocess.run(["python", komut])
    
    def veri_seti_olustur(self):
        # "Veri Seti Oluştur" için yeni pencere oluşturuluyor
        yeni_pencere = Toplevel(self.pencere)
        yeni_pencere.title("Veri Seti Oluştur")
        yeni_pencere.geometry("400x300")
        yeni_pencere.configure(bg="lightblue")
        
        # Seçim yapılacağına dair başlık etiketi ekleniyor
        tk.Label(yeni_pencere, text="Seçim Yapın", font=("Arial", 14), fg="blue", bg="orange").pack(pady=10)
        
        # Seçenekler sözlüğü: her seçenek için çalıştırılacak dosya belirleniyor
        secenekler = {
            "Excel Dosyasını CSV'ye Dönüştür": "veri_seti_excel.py",
            "Manuel Olarak Veri Seti Oluştur (.csv)": "veri_seti_manuel.py",
            "Resimler ile Veri Seti Oluştur (.csv)": "veri_seti_resim.py"
        }
        
        # Seçilen değeri tutmak için StringVar oluşturuluyor ve varsayılan değer atanıyor
        secim_var = StringVar()
        secim_var.set(next(iter(secenekler)))
        
        # Radio buttonlar ile seçim seçenekleri ekleniyor
        for text, komut in secenekler.items():
            tk.Radiobutton(yeni_pencere, text=text, variable=secim_var, value=komut, bg="lightblue").pack(anchor="w", padx=20)
        
        def secimi_onayla():
            # Onay butonuna basıldığında seçime göre ilgili .py dosyası çalıştırılıyor
            subprocess.run(["python", secim_var.get()])
            yeni_pencere.destroy()
        
        # Onay butonu ekleniyor
        tk.Button(yeni_pencere, text="Onayla", command=secimi_onayla, bg="green", fg="white").pack(pady=10)
        
# Uygulamayı başlat: Ana pencere oluşturulup, uygulama çalıştırılıyor
pencere = tk.Tk()
uygulama = Secim_Yap(pencere)
pencere.mainloop()