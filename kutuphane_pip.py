import subprocess

# pip.txt dosyasını oku ve komutları çalıştır
with open("pip.txt", "r", encoding="utf-8") as dosya:
    for satır in dosya:
        komut = satır.strip()
        if komut:  # Boş satırları atla
            try:
                subprocess.run(komut, shell=True, check=True)
                print(f"Başarıyla çalıştırıldı: {komut}")
            except subprocess.CalledProcessError as hata:
                print(f"Hata oluştu: {komut}\n{hata}")
