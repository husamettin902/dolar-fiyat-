import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import datetime
import os

def get_dolar_fiyat():
    # BigPara'nın döviz kuru sayfasının URL'si
    url = "https://bigpara.hurriyet.com.tr/doviz/dolar/"
    
    try:
        # Sayfayı al
        response = requests.get(url)
        response.raise_for_status()  # HTTP hata kodları varsa bir istisna fırlatır.
    except requests.exceptions.RequestException as e:
        # Bağlantı hatası durumunda kullanıcıyı bilgilendir
        messagebox.showerror("Hata", f"Sayfaya erişilemedi: {e}")
        return None
    
    # Sayfa içeriğini parse et
    soup = BeautifulSoup(response.content, "html.parser")
    
    try:
        # Dolar fiyatını çekme (BigPara'nın sayfasındaki elemente göre)
        dolar_fiyat = soup.find("span", class_="value")
        if dolar_fiyat:
            fiyat = dolar_fiyat.get_text(strip=True)
            return fiyat
        else:
            return "Dolar fiyatı bulunamadı."
    except Exception as e:
        # Parse hatası durumunda kullanıcıyı bilgilendir
        messagebox.showerror("Hata", f"Veri çekilirken hata oluştu: {e}")
        return None

def save_to_file(fiyat):
    # Şu anki tarihi alalım (dosya adı için)
    current_time = datetime.datetime.now()
    tarih = current_time.strftime("%Y-%m-%d_%H-%M-%S")  # Tarih formatı (2024-12-26_15-30-00)
    
    # Masaüstü yolunu almak için farklı yöntemler kullanacağız:
    if os.name == 'nt':  # Windows
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    else:  # Mac/Linux
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Masaüstü yolunu kontrol et
    if not os.path.exists(desktop_path):
        messagebox.showerror("Hata", f"Masaüstü yolu bulunamadı: {desktop_path}")
        return
    
    # Dosya adı (her kayıtta yeni dosya)
    file_name = f"dolar_fiyat_{tarih}.txt"
    
    # Dosya yolunu oluştur
    file_path = os.path.join(desktop_path, file_name)
    
    try:
        # Dosyayı kaydet
        with open(file_path, "w") as file:
            file.write(f"Dolar Fiyatı: {fiyat}\n")
            file.write(f"Alındığı Tarih: {tarih}\n")
        
        # Dosyanın başarıyla kaydedildiğini kullanıcıya bildirelim
        messagebox.showinfo("Başarılı", f"Dolar fiyatı ve tarih {file_path} dosyasına kaydedildi.")
    except Exception as e:
        # Dosya yazılırken bir hata oluşursa kullanıcıyı bilgilendirelim
        messagebox.showerror("Hata", f"Dosya kaydedilirken hata oluştu: {e}")

def show_dolar_fiyat():
    # Dolar fiyatını al
    fiyat = get_dolar_fiyat()
    
    if fiyat:
        # Dolar fiyatını göster
        messagebox.showinfo("Bugünkü Dolar Fiyatı", f"Dolar Fiyatı: {fiyat}")
        # Dosyaya kaydet
        save_to_file(fiyat)
    else:
        messagebox.showerror("Hata", "Dolar fiyatı alınamadı.")

# Tkinter penceresi oluşturma
root = tk.Tk()
root.title("Dolar Fiyatı Gösterici")
root.geometry("300x150")  # Pencere boyutu

# Buton ekleyelim
button = tk.Button(root, text="Dolar Fiyatını Göster ve Kaydet", command=show_dolar_fiyat)
button.pack(pady=30)  # Butonun pencere içinde ortalanması için padding ekledik

# Tkinter pencereyi çalıştır
root.mainloop()
