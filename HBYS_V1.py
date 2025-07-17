import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

# Veritabanı işlemleri
def create_db():
    conn = sqlite3.connect('hbys.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS hastalar
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  isim TEXT NOT NULL,
                  soyisim TEXT NOT NULL,
                  tc_no TEXT UNIQUE NOT NULL,
                  dogum_tarihi TEXT,
                  telefon_no TEXT)''')
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('hbys.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, password):
    conn = sqlite3.connect('hbys.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def hasta_ekle(isim, soyisim, tc_no, dogum_tarihi, telefon_no):
    conn = sqlite3.connect('hbys.db')
    c = conn.cursor()
    c.execute("INSERT INTO hastalar (isim, soyisim, tc_no, dogum_tarihi, telefon_no) VALUES (?, ?, ?, ?, ?)",
              (isim, soyisim, tc_no, dogum_tarihi, telefon_no))
    conn.commit()
    conn.close()

def hastalari_listele():
    conn = sqlite3.connect('hbys.db')
    c = conn.cursor()
    c.execute("SELECT * FROM hastalar")
    hastalar = c.fetchall()
    conn.close()
    return hastalar

# GUI Arayüzü
class HBYSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HBYS Sistemi")
        self.root.geometry("800x600")
        self.root.config(bg="#f4f4f4")
        self.login_screen()

    def login_screen(self):
        # Login ekranı
        self.clear_screen()
        self.username_label = ttk.Label(self.root, text="Kullanıcı Adı:", font=("Arial", 14))
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self.root, text="Şifre:", font=("Arial", 14))
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.root, text="Giriş Yap", command=self.check_login, width=20)
        self.login_button.pack(pady=20)

        self.signup_button = ttk.Button(self.root, text="Hesap Oluştur", command=self.signup_screen, width=20)
        self.signup_button.pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login_user(username, password):
            self.main_screen(username)
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def signup_screen(self):
        # Kayıt ekranı
        self.clear_screen()
        self.signup_label = ttk.Label(self.root, text="Yeni Hesap Oluştur", font=("Arial", 16))
        self.signup_label.pack(pady=20)

        self.new_username_label = ttk.Label(self.root, text="Kullanıcı Adı:", font=("Arial", 14))
        self.new_username_label.pack(pady=10)
        self.new_username_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.new_username_entry.pack(pady=5)

        self.new_password_label = ttk.Label(self.root, text="Şifre:", font=("Arial", 14))
        self.new_password_label.pack(pady=10)
        self.new_password_entry = ttk.Entry(self.root, show="*", font=("Arial", 14))
        self.new_password_entry.pack(pady=5)

        self.signup_button = ttk.Button(self.root, text="Kaydol", command=self.register_user, width=20)
        self.signup_button.pack(pady=20)

        self.back_button = ttk.Button(self.root, text="Geri", command=self.login_screen, width=20)
        self.back_button.pack(pady=10)

    def register_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if username and password:
            add_user(username, password)
            messagebox.showinfo("Başarılı", "Hesap oluşturuldu! Giriş yapabilirsiniz.")
            self.login_screen()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz.")

    def main_screen(self, username):
        # Ana ekran
        self.clear_screen()
        self.welcome_label = ttk.Label(self.root, text=f"Hoş geldiniz, {username}!", font=("Arial", 16))
        self.welcome_label.pack(pady=20)

        self.patient_button = ttk.Button(self.root, text="Hasta Yönetimi", command=self.patients_screen, width=30)
        self.patient_button.pack(pady=10)

        self.logout_button = ttk.Button(self.root, text="Çıkış Yap", command=self.logout, width=30)
        self.logout_button.pack(pady=10)

    def patients_screen(self):
        # Hasta yönetimi ekranı
        self.clear_screen()
        self.patients_label = ttk.Label(self.root, text="Hasta Kayıtları", font=("Arial", 16))
        self.patients_label.pack(pady=20)

        self.add_patient_button = ttk.Button(self.root, text="Hasta Ekle", command=self.add_patient_screen, width=30)
        self.add_patient_button.pack(pady=10)

        self.patient_list_button = ttk.Button(self.root, text="Hasta Listesi", command=self.show_patients, width=30)
        self.patient_list_button.pack(pady=10)

        self.back_button = ttk.Button(self.root, text="Geri", command=self.main_screen, width=30)
        self.back_button.pack(pady=10)

    def add_patient_screen(self):
        # Hasta ekleme ekranı
        self.clear_screen()
        self.add_patient_label = ttk.Label(self.root, text="Yeni Hasta Ekle", font=("Arial", 16))
        self.add_patient_label.pack(pady=20)

        self.name_label = ttk.Label(self.root, text="İsim:", font=("Arial", 14))
        self.name_label.pack(pady=10)
        self.name_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        self.surname_label = ttk.Label(self.root, text="Soyisim:", font=("Arial", 14))
        self.surname_label.pack(pady=10)
        self.surname_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.surname_entry.pack(pady=5)

        self.tc_label = ttk.Label(self.root, text="TC Kimlik No:", font=("Arial", 14))
        self.tc_label.pack(pady=10)
        self.tc_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.tc_entry.pack(pady=5)

        self.birth_label =
