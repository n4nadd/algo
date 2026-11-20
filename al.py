
#Rules pertama buat file akun.csv (untuk menyimpan data mahasiswa)
import csv #Mengimpor library csv untuk membaca dan menyimpan data CSV
import os #Mengimpor library os untuk mengelola file
# Fitur registrasi mahasiswa
def registrasi():
    print("\n===== REGISTRASI MAHASISWA =====")
    nama = input("Masukkan nama lengkap: ")
    nim = input("Masukkan NIM: ")
    username = input("Buat username: ")
    password = input("Buat password: ")
    prodi = input("Masukkan Prodi: ")
    fakultas = input("Masukkan Fakultas: ")
    # Memeriksa apakah username atau NIM sudah digunakan
    with open("akun.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for data in reader:
            if data["Username"] == username:
                print("Username sudah digunakan!")
                return
            if data["NIM"] == nim:
                print("NIM sudah terdaftar!")
                return
    # Menyimpan data mahasiswa
    # Membuka file akun.csv untuk menambahkan data
    with open("akun.csv", "a", newline="") as file:
        writer = csv.writer(file)
    # Membuat perintah untuk menulis data CSV
        writer.writerow([nama, nim, username, password, prodi, fakultas])
    print("\nRegistrasi berhasil!")
    print("Selamat, akun kamu sudah dibuat.")
def login_mahasiswa():
    print("\n===== LOGIN MAHASISWA ======")
    username = input("Masukkan username: ")
    # Meminta pengguna memasukkan password
    password = input("Masukkan password: ")
    with open("akun.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        berhasil = False

        for data in reader:
            if data["Username"] == username and data["Password"] == password:
                print("\nLogin berhasil!")
                # berhasil = True
                # Masuk ke beranda mahasiswa
                beranda_mahasiswa(
                data["Nama"],
                data["Prodi"],
                data["Fakultas"])
                break
            # Menghentikan perulangan
            if berhasil == False:
                print("\nUsername atau password salah!")

def beranda_mahasiswa(nama, prodi, fakultas):
    # Perulangan agar menu terus ditampilkan
    while True:
        # Header UNIDAY
        print("\n")
        print("============================================")
        print("                   UNIDAY                   ")
        print("          UNIVERSITY DAILY ACTIVITY         ")
        print("============================================")
        print("   HELLO, " + nama.upper())
        print("   Ready to organize your academic journey? ")
        # Pilihan menu mahasiswa
        print("============================================")
        print("   [01]  JADWAL KULIAH                      ")
        print("   [02]  CATATAN MATA KULIAH                ")
        print("   [03]  TO-DO LIST                         ")
        print("   [04]  STUDY TRACKER                      ")
        print("   [05]  LOGOUT                             ")
        print("============================================")
        # Meminta pilihan dari mahasiswa
        pilihan = input("  Pilih menu (1-5): ")
        # Jika memilih menu jadwal kuliah
        if pilihan == "1":
            print("\n===== JADWAL KULIAH =====")
        # Jika memilih menu catatan mata kuliah
        elif pilihan == "2":
            print("\n===== CATATAN MATA KULIAH =====")
        # Jika memilih menu To-Do List
        elif pilihan == "3":
            todo_list(nama)
        # Jika memilih menu Study Tracker
        elif pilihan == "4":
            print("\n===== STUDY TRACKER =====")
        # Jika memilih logout
        elif pilihan == "5":
            print("\nBerhasil logout!")
            break
        # Jika pilihan tidak tersedia
        else:
            print("\nPilihan tidak valid!")

def todo_list(nama):
    # Perulangan agar menu terus muncul
    while True:
        # Menampilkan judul To-Do List
        print("\n========================================")
        print("          UNIDAY - TO-DO LIST")
        print("       UNIVERSITY DAILY ACTIVITY")
        print("========================================")
        # Menampilkan pilihan menu
        print("1. Add New Task")
        print("2. My Task List")
        print("3. Task Cheklist")
        print("4. Delete Task")
        print("5. Kembali ke Beranda....")
        print("========================================")
        # Meminta pengguna memilih menu
        pilihan = input("Pilih menu (1-5): ")
        # Jika memilih menu 1
        if pilihan == "1":
            print("\n========================================")
            print("        UNIDAY - ADD NEW TASK")
            print("          Track Your Daily Tasks")
            print("========================================")
            # Meminta data tugas dari mahasiswa
            tugas = input("Nama Tugas       : ")
            matkul = input("Mata Kuliah      : ")
            deskripsi = input("Deskripsi Tugas  : ")
            deadline = input("Deadline         : ")
            prioritas = input("Prioritas (Tinggi/Sedang/Rendah): ")
            # Membuka file untuk menyimpan data
            with open("todo.csv", "a", newline="") as file:
                writer = csv.writer(file)
                # Membuat header jika file masih kosong
                if file.tell() == 0:
                    writer.writerow([
                        "Nama",
                        "Tugas",
                        "Mata Kuliah",
                        "Deskripsi",
                        "Deadline",
                        "Prioritas",
                        "Status"
                    ])
                # Menyimpan data tugas ke file CSV
                writer.writerow([
                    nama,
                    tugas,
                    matkul,
                    deskripsi,
                    deadline,
                    prioritas,
                    "Belum Selesai"
                ])
            # Menampilkan pesan jika tugas berhasil disimpan
            print("\nTugas berhasil ditambahkan!")
        # Jika memilih menu 2
        elif pilihan == "2":
            print("UNIDAY - MY TASK LIST")
            print("Track Your Daily Tasks")
            # Membaca data tugas dari file CSV
            try:
                with open("todo.csv", "r", newline="") as file:
                    reader = csv.DictReader(file)
                    # Mengambil tugas milik mahasiswa yang sedang login
                    daftar_tugas = [
                        data for data in reader
                        if data["Nama"] == nama
                    ]
                # Memeriksa apakah ada tugas
                if len(daftar_tugas) == 0:
                    print("\nBelum ada tugas yang ditambahkan.")
                else:
                    # Menampilkan daftar tugas dalam bentuk tabel
                    print("=" * 95)
                    print(f"{'NO':<5} {'NAMA TUGAS':<20} {'MATA KULIAH':<22} {'DEADLINE':<15} {'PRIORITAS':<12} {'STATUS':<15}")
                    print("=" * 95)
                    for nomor, data in enumerate(daftar_tugas, start=1):
                        print(
                            f"{nomor:<5} "
                            f"{data['Tugas']:<20} "
                            f"{data['Mata Kuliah']:<22} "
                            f"{data['Deadline']:<15} "
                            f"{data['Prioritas']:<12} "
                            f"{data['Status']:<15}"
                        )
                    print("=" * 95)
                    print("Total Tugas:", len(daftar_tugas))
            except FileNotFoundError:
                print("\nBelum ada data tugas.")
        # Jika memilih menu 3
        elif pilihan == "3":
            print("\n========================================")
            print("        UNIDAY - TASK CHECKLIST")
            print("          Track Your Daily Tasks")
            print("========================================")
            with open("todo.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                semua_tugas = list(reader)
            daftar_tugas = []
            for data in semua_tugas:
                if data["Nama"] == nama:
                    daftar_tugas.append(data)
            for nomor, data in enumerate(daftar_tugas, start=1):
                if data["Status"] == "Selesai":
                    tanda = "[✓]"
                else:
                    tanda = "[ ]"
                print("   ", nomor, tanda, data["Tugas"])
            print("\n========================================")
            pilih = input("Centang nomor tugas (0 untuk kembali): ")
            if pilih != "0":
                pilih = int(pilih)
                if 1 <= pilih <= len(daftar_tugas):
                    daftar_tugas[pilih - 1]["Status"] = "Selesai"
                    with open("todo.csv", "w", newline="") as file:
                        kolom = [
                            "Nama", "Tugas", "Mata Kuliah",
                            "Deskripsi", "Deadline", "Prioritas", "Status"
                        ]
                        writer = csv.DictWriter(file, fieldnames=kolom)
                        writer.writeheader()
                        writer.writerows(semua_tugas)
                    print("\n[✓] Tugas berhasil dicentang!")
        # Jika memilih menu 4
        elif pilihan == "4":
                    # Jika memilih menu 4
            print("\n" + "=" * 95)
            print("                 UNIDAY - DELETE TASK")
            print("=" * 95)
            # Membaca data tugas
            with open("todo.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                semua_tugas = list(reader)
            # Mengambil tugas mahasiswa yang login
            daftar_tugas = []
            for data in semua_tugas:
                if data["Nama"] == nama:
                    daftar_tugas.append(data)
            # Memeriksa daftar tugas
            if len(daftar_tugas) == 0:
                print("Belum ada tugas.")
            else:
                print(f"{'NO':<3} | {'TUGAS':<15} | {'MATKUL':<10} | {'DESKRIPSI':<15} | {'DEADLINE':<12} | {'PRIORITAS':<9} | {'STATUS':<12}")
                print("-" * 95)

                for nomor, data in enumerate(daftar_tugas, start=1):
                    print(
                        f"{nomor:<3} | "
                        f"{data['Tugas']:<15} | "
                        f"{data['Mata Kuliah']:<10} | "
                        f"{data['Deskripsi']:<15} | "
                        f"{data['Deadline']:<12} | "
                        f"{data['Prioritas']:<9} | "
                        f"{data['Status']:<12}"
                    )
                print("=" * 95)
                pilih = int(input("Pilih nomor tugas yang ingin dihapus: "))
                if 1 <= pilih <= len(daftar_tugas):
                    tugas = daftar_tugas[pilih - 1]
                    semua_tugas.remove(tugas)
                    # Menyimpan perubahan
                    with open("todo.csv", "w", newline="") as file:
                        kolom = [
                            "Nama", "Tugas", "Mata Kuliah",
                            "Deskripsi", "Deadline", "Prioritas", "Status"
                        ]

                        writer = csv.DictWriter(file, fieldnames=kolom)
                        writer.writeheader()
                        writer.writerows(semua_tugas)

                    print("\nTugas berhasil dihapus!")

                else:
                    print("Nomor tugas tidak ditemukan.")
        # Jika memilih menu 5
        elif pilihan == "5":
            print("Kembali ke beranda...")
            break
        # Jika pilihan tidak sesuai
        else:
            print("Pilihan tidak valid!")

# Membuat fungsi login admin
def login_admin():
    # Menampilkan judul login admin
    print("\n===== LOGIN ADMIN =====")
    # Meminta username admin
    username = input("Masukkan username admin: ")
    # Meminta password admin
    password = input("Masukkan password admin: ")
    # Memeriksa username dan password admin
    if username == "admin" and password == "admin123":
        # Menampilkan pesan login berhasil
        print("\nLogin admin berhasil!")
        # Memanggil menu admin
        menu_admin()
    else:
        # Menampilkan pesan jika login gagal
        print("\nUsername atau password admin salah!")
# Membuat fungsi menu admin
def menu_admin():
    while True:
        print("\n===== MENU ADMIN =====")
        print("1. Lihat data mahasiswa")
        print("2. Logout")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            # Membuka file akun.csv
            with open("akun.csv", "r", newline="", encoding="utf-8-sig") as file:
                # Membaca file CSV
                reader = csv.DictReader(file)
                # Mengambil seluruh data mahasiswa
                daftar_mahasiswa = list(reader)
                # Menampilkan tabel
                print("\n" + "=" * 92)
                print("DATA MAHASISWA UNIDAY".center(92))
                print("=" * 92)
                print(f"{'No':<4}{'Nama':<25}{'NIM':<16}{'Prodi':<20}{'Fakultas':<25}")
                print("-" * 90)
                for nomor, data in enumerate(daftar_mahasiswa, start=1):
                    print(f"{nomor:<4}{data['Nama']:<25}{data['NIM']:<16}{data['Prodi']:<20}{data['Fakultas']:<25}")
                print("-" * 90)
                print("Jumlah Mahasiswa:", len(daftar_mahasiswa))
        elif pilihan == "2":
            print("Admin berhasil logout!")
            break
        else:
            print("Pilihan tidak tersedia!")
def menu_utama():
    while True:
          # Menampilkan judul aplikasi
        print("\n====================================")
        print("               UNIDAY                ")
        print("      UNIVERSITY DAILY ACTIVITY")
        print("=====================================")
        # Menampilkan pilihan menu
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
        # Jika pilihan tidak tersedia
        else:
            print("\nPilihan tidak valid! Silakan coba lagi.")
# Menjalankan menu utama
menu_utama()
