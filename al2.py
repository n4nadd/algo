# UNIDAY - Registrasi dan Login Mahasiswa

import csv
import os

FILE_AKUN = "akun.csv"
FIELDNAMES = ["Nama", "NIM", "Username", "Password", "Prodi", "Fakultas"]


# Fungsi untuk menyiapkan file akun.csv
def siapkan_file_akun():
    if not os.path.exists(FILE_AKUN) or os.path.getsize(FILE_AKUN) == 0:
        with open(FILE_AKUN, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDNAMES)


# Fitur registrasi mahasiswa
def registrasi():
    print("\n===== REGISTRASI MAHASISWA =====")

    nama = input("Masukkan nama lengkap: ").strip()
    nim = input("Masukkan NIM: ").strip()
    username = input("Buat username: ").strip()
    password = input("Buat password: ").strip()
    prodi = input("Masukkan Prodi: ").strip()
    fakultas = input("Masukkan Fakultas: ").strip()

    # Memeriksa apakah username atau NIM sudah digunakan
    with open(FILE_AKUN, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for data in reader:
            if data["Username"] == username:
                print("Username sudah digunakan!")
                return

            if data["NIM"] == nim:
                print("NIM sudah terdaftar!")
                return

    # Menyimpan data mahasiswa
    with open(FILE_AKUN, "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([nama, nim, username, password, prodi, fakultas])

    print("\nRegistrasi berhasil!")
    print("Selamat, akun kamu sudah dibuat.")


# Fitur login mahasiswa
def login_mahasiswa():
    print("\n===== LOGIN MAHASISWA =====")

    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    with open(FILE_AKUN, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        berhasil = False

        for data in reader:
            if data["Username"] == username and data["Password"] == password:
                berhasil = True
                print("\nLogin berhasil!")
                print("Selamat datang,", data["Nama"])
                break

        if berhasil == False:
            print("\nUsername atau password salah!")


# Fitur login admin
def login_admin():
    print("\n===== LOGIN ADMIN =====")

    username = input("Masukkan username admin: ")
    password = input("Masukkan password admin: ")

    if username == "admin" and password == "admin123":
        print("\nLogin admin berhasil!")
        menu_admin()
    else:
        print("\nUsername atau password admin salah!")


# Menu admin
def menu_admin():
    while True:
        print("\n===== MENU ADMIN =====")
        print("1. Lihat data mahasiswa")
        print("2. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":

            # Membuka dan membaca file CSV
            with open(FILE_AKUN, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                daftar_mahasiswa = list(reader)

            # Menampilkan tabel data mahasiswa
            print("\n" + "=" * 92)
            print("DATA MAHASISWA UNIDAY".center(92))
            print("=" * 92)

            print(f"{'No':<4}{'Nama':<25}{'NIM':<16}{'Prodi':<20}{'Fakultas':<25}")
            print("-" * 90)

            for nomor, data in enumerate(daftar_mahasiswa, start=1):
                print(
                    f"{nomor:<4}{data['Nama']:<25}{data['NIM']:<16}"
                    f"{data['Prodi']:<20}{data['Fakultas']:<25}"
                )

            print("-" * 90)
            print("Jumlah Mahasiswa:", len(daftar_mahasiswa))

        elif pilihan == "2":
            print("Admin berhasil logout!")
            break

        else:
            print("Pilihan tidak tersedia!")


# Menu utama UNIDAY
def menu_utama():
    while True:
        print("\n===================================")
        print("               UNIDAY")
        print("      UNIVERSITY DAILY ACTIVITY")
        print("===================================")

        print("1. Registrasi Mahasiswa")
        print("2. Login Mahasiswa")
        print("3. Login Admin")
        print("4. Keluar")

        pilihan = input("Pilihan menu (1/4): ")

        if pilihan == "1":
            registrasi()

        elif pilihan == "2":
            login_mahasiswa()

        elif pilihan == "3":
            login_admin()

        elif pilihan == "4":
            print("\nTerima kasih telah menggunakan aplikasi!")
            break

        else:
            print("\nPilihan tidak valid! Silakan coba lagi.")


# Menjalankan program
siapkan_file_akun()
menu_utama()2
