import csv

nilai_list = []
ipk_list = []
jadwal_list = []
notif_list = []

# BACA CSV
def baca_csv(nama_file):
    hasil = []
    try:
        with open(nama_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            for data in reader:
                hasil.append(data)
    except FileNotFoundError:
        hasil = []
    return hasil

# TULIS CSV
def tulis_csv(nama_file, kolom, semua_data):
    with open(nama_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(semua_data)

# BONGKAR BARIS JADWAL
def bongkar_baris(baris):
    data_baris = ["", "", "", "", "", ""]
    kolom = 0
    for huruf in baris:
        if huruf == "|" or huruf == ",":
            kolom = kolom + 1
        elif huruf == "\n":
            pass
        else:
            if kolom < 6:
                data_baris[kolom] = data_baris[kolom] + huruf
    return data_baris

# BACA JADWAL.CSV
try:
    file_buka = open("jadwal.csv", "r")
    for baris in file_buka:
        if baris == "" or baris == "\n":
            continue
        pisah = bongkar_baris(baris)
        if pisah[0] == "Kelas":
            continue
        if pisah[2] != "":
            jadwal_list.append(pisah)
    file_buka.close()
except:
    jadwal_list = []

# SIMPAN JADWAL
def simpan_jadwal():
    file_tulis = open("jadwal.csv", "w")
    for nomor in range(len(jadwal_list)):
        file_tulis.write(jadwal_list[nomor][0] + "|" + jadwal_list[nomor][1] + "|" + jadwal_list[nomor][2] + "|" + jadwal_list[nomor][3] + "|" + jadwal_list[nomor][4] + "|" + jadwal_list[nomor][5] + "\n")
    file_tulis.close()

# TAMPILKAN JADWAL
def tampilkan_jadwal(kelas_pilih):
    print("\n===== JADWAL SAAT INI - KELAS " + kelas_pilih + " =====")
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    ada_jadwal = False
    for hari in hari_list:
        print("\n-- " + hari + " --")
        ada = False
        for nomor in range(len(jadwal_list)):
            if jadwal_list[nomor][0] == kelas_pilih and jadwal_list[nomor][1] == hari:
                print(str(nomor) + ". " + jadwal_list[nomor][2] + " | " + jadwal_list[nomor][3] + " | " + jadwal_list[nomor][4] + " | " + jadwal_list[nomor][5])
                ada = True
                ada_jadwal = True
        if not ada:
            print("(Libur / Kosong)")
    if not ada_jadwal:
        print("\nBelum ada jadwal! Tunggu admin input.")

# REGISTRASI MAHASISWA
def registrasi():
    print("\n===== REGISTRASI MAHASISWA =====")
    nama = input("Masukkan nama lengkap: ")
    nim = input("Masukkan NIM: ")
    username = input("Buat username: ")
    password = input("Buat password: ")
    prodi = input("Masukkan Prodi: ")
    fakultas = input("Masukkan Fakultas: ")
    kelas = ""
    while kelas != "A" and kelas != "B" and kelas != "C":
        kelas = input("Pilih Kelas (A/B/C): ")
        if kelas != "A" and kelas != "B" and kelas != "C":
            print("Pilih A, B, atau C aja!")
    semua = baca_csv("akun.csv")
    for data in semua:
        if data["Username"] == username:
            print("Username sudah digunakan!")
            return
        if data["NIM"] == nim:
            print("NIM sudah terdaftar! Kalau kamu dikeluarkan, hubungi admin.")
            return
    with open("akun.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Nama", "NIM", "Username", "Password", "Prodi", "Fakultas", "Kelas", "Status"])
        writer.writerow([nama, nim, username, password, prodi, fakultas, kelas, "Aktif"])
    print("\nRegistrasi berhasil!")
    print("Selamat, akun kamu sudah dibuat. Kelas kamu: " + kelas)

# LOGIN MAHASISWA
def login_mahasiswa():
    print("\n===== LOGIN MAHASISWA =====")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    semua = baca_csv("akun.csv")
    berhasil = False
    for data in semua:
        if data["Username"] == username and data["Password"] == password:
            if data["Status"] == "Dikeluarkan":
                print("\nAnda dikeluarkan dari UNIDAY, tidak bisa login lagi.")
                print("Hubungi admin untuk info lebih lanjut.")
                return
            berhasil = True
            print("\nLogin berhasil!")
            beranda_mahasiswa(data["Nama"], data["Kelas"])
            break
    if berhasil == False:
        print("\nUsername atau password salah!")

# JADWAL KULIAH MAHASISWA
def jadwal_kuliah_mahasiswa(kelas):
    if len(notif_list) > 0:
        print("=" * 40)
        print("PERHATIKAN!! ADA PERUBAHAN JADWAL")
        print("=" * 40)
        notif_list.pop(0)
    while True:
        print("\n--- JADWAL KULIAH - MAHASISWA KELAS " + kelas + " ---")
        print("1. Tampilkan Jadwal")
        print("2. Cari Jadwal")
        print("3. Kembali")
        pilih = input("Pilih: ")
        if pilih == "1":
            tampilkan_jadwal(kelas)
        elif pilih == "2":
            tampilkan_jadwal(kelas)
            cari = input("\nCari matkul / dosen / ruangan: ").title()
            ditemukan = False
            for nomor in range(len(jadwal_list)):
                if jadwal_list[nomor][0] == kelas and (cari in jadwal_list[nomor][2] or cari in jadwal_list[nomor][4] or cari in jadwal_list[nomor][5]):
                    print(jadwal_list[nomor][1] + " - " + jadwal_list[nomor][2] + " - " + jadwal_list[nomor][3] + " - " + jadwal_list[nomor][4] + " - " + jadwal_list[nomor][5])
                    ditemukan = True
            if not ditemukan:
                print("Gak ketemu!")
        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid!")

# TO-DO LIST
def todo_list(nama):
    while True:
        print("\n========================================")
        print("          UNIDAY - TO-DO LIST")
        print("       UNIVERSITY DAILY ACTIVITY")
        print("========================================")
        print("1. Add New Task")
        print("2. My Task List")
        print("3. Task Checklist")
        print("4. Delete Task")
        print("5. Kembali ke Beranda....")
        print("========================================")
        pilihan = input("Pilih menu (1-5): ")
        if pilihan == "1":
            print("\n========================================")
            print("        UNIDAY - ADD NEW TASK")
            print("          Track Your Daily Tasks")
            print("========================================")
            tugas = input("Nama Tugas       : ")
            matkul = input("Mata Kuliah      : ")
            deskripsi = input("Deskripsi Tugas  : ")
            deadline = input("Deadline         : ")
            prioritas = input("Prioritas (Tinggi/Sedang/Rendah): ")
            with open("todo.csv", "a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Nama", "Tugas", "Mata Kuliah", "Deskripsi", "Deadline", "Prioritas", "Status"])
                writer.writerow([nama, tugas, matkul, deskripsi, deadline, prioritas, "Belum Selesai"])
            print("\nTugas berhasil ditambahkan!")
        elif pilihan == "2":
            print("UNIDAY - MY TASK LIST")
            print("Track Your Daily Tasks")
            semua = baca_csv("todo.csv")
            daftar_tugas = []
            for data in semua:
                if data["Nama"] == nama:
                    daftar_tugas.append(data)
            if len(daftar_tugas) == 0:
                print("\nBelum ada tugas yang ditambahkan.")
            else:
                print("=" * 95)
                print("NO    NAMA TUGAS           MATA KULIAH            DEADLINE        PRIORITAS    STATUS")
                print("=" * 95)
                for nomor in range(len(daftar_tugas)):
                    data = daftar_tugas[nomor]
                    print(str(nomor + 1) + "     " + data["Tugas"] + "     " + data["Mata Kuliah"] + "     " + data["Deadline"] + "     " + data["Prioritas"] + "     " + data["Status"])
                print("=" * 95)
                print("Total Tugas: " + str(len(daftar_tugas)))
        elif pilihan == "3":
            print("\n========================================")
            print("        UNIDAY - TASK CHECKLIST")
            print("          Track Your Daily Tasks")
            print("========================================")
            semua = baca_csv("todo.csv")
            daftar_tugas = []
            for data in semua:
                if data["Nama"] == nama:
                    daftar_tugas.append(data)
            for nomor in range(len(daftar_tugas)):
                data = daftar_tugas[nomor]
                tanda = "[ ]"
                if data["Status"] == "Selesai":
                    tanda = "[V]"
                print("   " + str(nomor + 1) + " " + tanda + " " + data["Tugas"])
            print("\n========================================")
            pilih = input("Centang nomor tugas (0 untuk kembali): ")
            if pilih != "0":
                pilih = int(pilih)
                if pilih >= 1 and pilih <= len(daftar_tugas):
                    daftar_tugas[pilih - 1]["Status"] = "Selesai"
                    tulis_csv("todo.csv", ["Nama", "Tugas", "Mata Kuliah", "Deskripsi", "Deadline", "Prioritas", "Status"], semua)
                    print("\n[V] Tugas berhasil dicentang!")
        elif pilihan == "4":
            print("\n" + "=" * 95)
            print("                 UNIDAY - DELETE TASK")
            print("=" * 95)
            semua = baca_csv("todo.csv")
            daftar_tugas = []
            for data in semua:
                if data["Nama"] == nama:
                    daftar_tugas.append(data)
            if len(daftar_tugas) == 0:
                print("Belum ada tugas.")
            else:
                print("NO  | TUGAS           | MATKUL          | DESKRIPSI       | DEADLINE      | PRIORITAS  | STATUS")
                print("-" * 95)
                for nomor in range(len(daftar_tugas)):
                    data = daftar_tugas[nomor]
                    print(str(nomor + 1) + " | " + data["Tugas"] + " | " + data["Mata Kuliah"] + " | " + data["Deskripsi"] + " | " + data["Deadline"] + " | " + data["Prioritas"] + " | " + data["Status"])
                print("=" * 95)
                pilih = int(input("Pilih nomor tugas yang ingin dihapus: "))
                if pilih >= 1 and pilih <= len(daftar_tugas):
                    semua.remove(daftar_tugas[pilih - 1])
                    tulis_csv("todo.csv", ["Nama", "Tugas", "Mata Kuliah", "Deskripsi", "Deadline", "Prioritas", "Status"], semua)
                    print("\nTugas berhasil dihapus!")
                else:
                    print("Nomor tugas tidak ditemukan.")
        elif pilihan == "5":
            print("Kembali ke beranda...")
            break
        else:
            print("Pilihan tidak valid!")

# SIMPAN CATATAN
def simpan_catatan(matkul, topik, isi, sks, mode):
    with open("catatan_matkul.csv", mode, newline="") as f:
        tulis = csv.writer(f)
        if mode == "w":
            tulis.writerow(["Matkul", "Topik", "Isi", "SKS"])
        tulis.writerow([matkul, topik, isi, sks])

# BACA CATATAN
def baca_catatan():
    list_catatan = []
    try:
        with open("catatan_matkul.csv", "r", newline="") as f:
            baca = csv.reader(f)
            next(baca, None)
            for row in baca:
                if row:
                    list_catatan.append({"matkul": row[0], "topik": row[1], "isi": row[2], "sks": int(row[3])})
    except FileNotFoundError:
        simpan_catatan("Algoritma dan Pemrograman", "Perulangan dan Fungsi", "Pakai for, while, return", 3, "w")
        return baca_catatan()
    return list_catatan

# CARI MATERI
def cari_materi(data, kata_kunci):
    hasil = []
    for item in data:
        if kata_kunci in item["matkul"] or kata_kunci in item["topik"] or kata_kunci in item["isi"]:
            hasil.append(item)
    return hasil

# HITUNG TOTAL SKS
def hitung_total_sks(daftar_sks):
    total = 0
    for sks in daftar_sks:
        total = total + sks
    return total

# CETAK REKAP
def cetak_rekap(total_catatan, total_sks, matkul_besar):
    print("\n=== Ringkasan Catatan ===")
    print("Total_Catatan : " + str(total_catatan))
    print("Total_SKS : " + str(total_sks))
    print("Matkul_3_Plus : " + matkul_besar)

# STATUS SKS
def status_sks(sks):
    if sks >= 4:
        return "Beban Berat"
    elif sks == 3:
        return "Beban Standar"
    elif sks >= 1:
        return "Beban Ringan"
    else:
        return "Tidak Valid"

# CATATAN MATA KULIAH
def catatan_matkul():
    pilih = ""
    while pilih != "0":
        print("\n1. Tambah Catatan Matkul")
        print("2. Lihat Semua Catatan")
        print("3. Cek Status SKS")
        print("4. Cari Materi")
        print("0. Keluar")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            matkul = input("Nama mata kuliah : ")
            topik = input("Topik/materi      : ")
            isi = input("Isi catatan      : ")
            while True:
                sks = int(input("Jumlah SKS       : "))
                if sks > 0:
                    break
                print("SKS harus lebih dari 0.")
            simpan_catatan(matkul, topik, isi, sks, "a")
            print("Catatan berhasil disimpan ke CSV.")
        elif pilih == "2":
            data = baca_catatan()
            if len(data) == 0:
                print("Belum ada catatan tersimpan.")
                continue
            print("\nDaftar Catatan Mata Kuliah:")
            for nomor in range(len(data)):
                item = data[nomor]
                ket_sks = status_sks(item["sks"])
                print(str(nomor + 1) + ". " + item["matkul"] + " - " + item["topik"] + " (" + str(item["sks"]) + " SKS) | " + ket_sks)
                print("   Catatan: " + item["isi"])
            kumpulan_sks = []
            matkul_besar = []
            for item in data:
                kumpulan_sks.append(item["sks"])
                if item["sks"] >= 3:
                    matkul_besar.append(item["matkul"])
            total_sks = hitung_total_sks(kumpulan_sks)
            teks_matkul_besar = "-"
            for nomor in range(len(matkul_besar)):
                if nomor == 0:
                    teks_matkul_besar = matkul_besar[nomor]
                else:
                    teks_matkul_besar = teks_matkul_besar + ", " + matkul_besar[nomor]
            cetak_rekap(len(data), total_sks, teks_matkul_besar)
            for i in range(2):
                for j in range(12):
                    print("=", end="")
                print()
        elif pilih == "3":
            cek_sks = int(input("Masukkan jumlah SKS: "))
            print("Status: " + status_sks(cek_sks))
        elif pilih == "4":
            kata = input("Masukkan kata kunci materi/matkul: ")
            data = baca_catatan()
            hasil_cari = cari_materi(data, kata)
            if len(hasil_cari) == 0:
                print("Materi tidak ketemu.")
                continue
            print("\nHasil pencarian '" + kata + "':")
            for nomor in range(len(hasil_cari)):
                item = hasil_cari[nomor]
                print(str(nomor + 1) + ". [" + item["matkul"] + "] " + item["topik"] + " (" + str(item["sks"]) + " SKS)")
                print("   Isi: " + item["isi"])
        elif pilih == "0":
            print("Selesai, keluar program.")
            break
        else:
            print("Pilihan tidak ada.")

# INPUT ANGKA
def input_angka(pesan, minimum, maksimum):
    while True:
        try:
            angka = float(input(pesan))
            if angka >= minimum and angka <= maksimum:
                return angka
            else:
                print("Input harus antara " + str(minimum) + " sampai " + str(maksimum))
        except ValueError:
            print("Masukkan angka yang valid!")

# BACA DATA TRACKER
def baca_data_tracker():
    global nilai_list, ipk_list
    nilai_list = []
    ipk_list = []
    try:
        with open("nilai.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for data in reader:
                if len(data) == 4:
                    nilai_list.append([data[0], float(data[1]), float(data[2]), float(data[3])])
    except:
        pass
    try:
        with open("ipk.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for data in reader:
                if len(data) == 2:
                    ipk_list.append([data[0], float(data[1])])
    except:
        pass

# SIMPAN TRACKER
def simpan_tracker():
    with open("nilai.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Mata Kuliah", "Kuis", "UTS", "UAS"])
        writer.writerows(nilai_list)
    with open("ipk.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Semester", "IPK"])
        writer.writerows(ipk_list)

# STUDY TRACKER
def study_tracker():
    baca_data_tracker()
    while True:
        print("\n========== STUDY TRACKER ==========")
        print("1. Lihat Nilai dan IPK")
        print("2. Input Nilai (Kuis, UTS, UAS)")
        print("3. Input IPK (Input Sendiri)")
        print("4. Ubah Nilai")
        print("5. Hapus Nilai")
        print("6. Kembali")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            print("\n========== NILAI MAHASISWA ==========")
            if len(nilai_list) == 0:
                print("Belum ada nilai!")
            else:
                for nomor in range(len(nilai_list)):
                    matkul = nilai_list[nomor][0]
                    kuis = nilai_list[nomor][1]
                    uts = nilai_list[nomor][2]
                    uas = nilai_list[nomor][3]
                    akhir = (kuis * 0.2) + (uts * 0.3) + (uas * 0.5)
                    bulat = akhir // 1
                    sisa = round(akhir % 1, 2)
                    huruf = "E"
                    if akhir >= 80:
                        huruf = "A"
                    elif akhir >= 70:
                        huruf = "B"
                    elif akhir >= 60:
                        huruf = "C"
                    elif akhir >= 50:
                        huruf = "D"
                    print(matkul + " | Kuis: " + str(kuis) + " | UTS: " + str(uts) + " | UAS: " + str(uas) + " | Nilai Akhir: " + str(round(akhir, 2)) + " (bulat " + str(bulat) + " sisa " + str(sisa) + ")" + " | Huruf: " + huruf)
            print("\n========== RIWAYAT IPK ==========")
            if len(ipk_list) == 0:
                print("Belum input IPK!")
            else:
                for nomor in range(len(ipk_list)):
                    semester = ipk_list[nomor][0]
                    ipk = ipk_list[nomor][1]
                    predikat = "Sangat Kurang, Semangat!"
                    if ipk >= 3.5:
                        predikat = "Sangat Bagus / Cumlaude"
                    elif ipk >= 3.0:
                        predikat = "Bagus"
                    elif ipk >= 2.75:
                        predikat = "Normal / Cukup"
                    elif ipk >= 2.0:
                        predikat = "Kurang"
                    print("Semester " + semester + " | IPK: " + str(ipk) + " | " + predikat)
        elif pilih == "2":
            matkul = input("Nama Mata Kuliah: ")
            kuis = input_angka("Nilai Kuis: ", 0, 100)
            uts = input_angka("Nilai UTS: ", 0, 100)
            uas = input_angka("Nilai UAS: ", 0, 100)
            nilai_list.append([matkul, kuis, uts, uas])
            simpan_tracker()
            print("Nilai berhasil disimpan!")
        elif pilih == "3":
            semester = input("Semester ke-berapa: ")
            ipk = input_angka("Masukkan IPK (0.00 - 4.00): ", 0, 4)
            ipk_list.append([semester, ipk])
            simpan_tracker()
            print("IPK berhasil disimpan!")
        elif pilih == "4":
            if len(nilai_list) == 0:
                print("Belum ada nilai yang bisa diubah!")
            else:
                print("\nDaftar Mata Kuliah:")
                for nomor in range(len(nilai_list)):
                    print(str(nomor) + " . " + nilai_list[nomor][0])
                try:
                    nomor = int(input("Nomor yang mau diubah: "))
                    if nomor >= 0 and nomor < len(nilai_list):
                        nilai_list[nomor][1] = input_angka("Kuis baru: ", 0, 100)
                        nilai_list[nomor][2] = input_angka("UTS baru: ", 0, 100)
                        nilai_list[nomor][3] = input_angka("UAS baru: ", 0, 100)
                        simpan_tracker()
                        print("Nilai berhasil diubah!")
                    else:
                        print("Nomor tidak ditemukan!")
                except ValueError:
                    print("Masukkan nomor yang valid!")
        elif pilih == "5":
            if len(nilai_list) == 0:
                print("Belum ada nilai yang bisa dihapus!")
            else:
                print("\nDaftar Mata Kuliah:")
                for nomor in range(len(nilai_list)):
                    print(str(nomor) + " . " + nilai_list[nomor][0])
                try:
                    nomor = int(input("Nomor yang mau dihapus: "))
                    if nomor >= 0 and nomor < len(nilai_list):
                        nilai_list.pop(nomor)
                        simpan_tracker()
                        print("Nilai berhasil dihapus!")
                    else:
                        print("Nomor tidak ditemukan!")
                except ValueError:
                    print("Masukkan nomor yang valid!")
        elif pilih == "6":
            print("Kembali ke menu utama...")
            break
        else:
            print("Pilihan tidak tersedia!")

# BERANDA MAHASISWA
def beranda_mahasiswa(nama, kelas):
    while True:
        print("\n")
        print("============================================")
        print("                   UNIDAY                   ")
        print("          UNIVERSITY DAILY ACTIVITY         ")
        print("============================================")
        print("HELLO, " + nama)
        print("KELAS " + kelas)
        print("        This is your academic journey       ")
        print("============================================")
        print("   [01]  JADWAL KULIAH                      ")
        print("   [02]  CATATAN MATA KULIAH                ")
        print("   [03]  TO-DO LIST                         ")
        print("   [04]  STUDY TRACKER                      ")
        print("   [05]  LOGOUT                             ")
        print("============================================")
        pilihan = input("  Pilih menu (1-5): ")
        if pilihan == "1":
            jadwal_kuliah_mahasiswa(kelas)
        elif pilihan == "2":
            catatan_matkul()
        elif pilihan == "3":
            todo_list(nama)
        elif pilihan == "4":
            study_tracker()
        elif pilihan == "5":
            print("\nBerhasil logout!")
            break
        else:
            print("\nPilihan tidak valid!")

# LOGIN ADMIN
def login_admin():
    print("\n===== LOGIN ADMIN =====")
    username = input("Masukkan username admin: ")
    password = input("Masukkan password admin: ")
    semua = baca_csv("admin.csv")
    if len(semua) == 0:
        print("Data admin tidak ditemukan. Cek file admin.csv!")
        return
    for data in semua:
        if data["Username"] == username and data["Password"] == password:
            print("\nLogin admin berhasil!")
            menu_admin()
            return
    print("\nUsername atau password admin salah!")

# PILIH KELAS JADWAL
def pilih_kelas_jadwal():
    kelas_admin = ""
    while kelas_admin != "A" and kelas_admin != "B" and kelas_admin != "C":
        print("\n===== PILIH KELAS JADWAL =====")
        print("1. Kelas A")
        print("2. Kelas B")
        print("3. Kelas C")
        pilih_kelas = input("Pilih kelas (1-3): ")
        if pilih_kelas == "1":
            kelas_admin = "A"
        elif pilih_kelas == "2":
            kelas_admin = "B"
        elif pilih_kelas == "3":
            kelas_admin = "C"
        else:
            print("Pilih 1, 2, atau 3 aja!")
    print("\nJadwal yang diatur: Kelas " + kelas_admin)
    return kelas_admin

# ATUR JADWAL ADMIN
def atur_jadwal_admin():
    while True:
        print("\n--- JADWAL KULIAH ---")
        print("1. Tampilkan Jadwal")
        print("2. Masukkan Jadwal (Senin-Jumat)")
        print("3. Tambah Jadwal (Baru/Pindahan)")
        print("4. Cari Jadwal")
        print("5. Ganti Jadwal")
        print("6. Hapus Jadwal")
        print("7. Kembali")
        pilih = input("Pilih: ")
        if pilih == "1":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
        elif pilih == "2":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
            for hari in hari_list:
                print("\n== " + hari + " ==")
                while True:
                    matkul = input("Matkul (ketik 'skip' kalau libur): ")
                    if matkul == "skip" or matkul == "":
                        break
                    jam = input("Jam: ")
                    dosen = input("Dosen: ")
                    ruangan = input("Ruangan: ")
                    jadwal_list.append([kelas_admin, hari, matkul, jam, dosen, ruangan])
                    lagi = input("Ada jadwal lagi di " + hari + "? (y/n): ")
                    if not (lagi == "y"):
                        break
            simpan_jadwal()
            if len(notif_list) == 0:
                notif_list.append("ada")
            print("Jadwal tersimpan!")
        elif pilih == "3":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            print("\n--- TAMBAH JADWAL BARU - KELAS " + kelas_admin + " ---")
            hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
            for nomor_hari in range(len(hari_list)):
                print(str(nomor_hari) + ". " + hari_list[nomor_hari])
            nomor_hari = int(input("Nomor hari: "))
            if nomor_hari >= 0 and nomor_hari < len(hari_list):
                hari_pilih = hari_list[nomor_hari]
                print("\nJadwal yang udah ada di " + hari_pilih + ":")
                ada = False
                for nomor in range(len(jadwal_list)):
                    if jadwal_list[nomor][0] == kelas_admin and jadwal_list[nomor][1] == hari_pilih:
                        print("- " + jadwal_list[nomor][2] + " | " + jadwal_list[nomor][3] + " | " + jadwal_list[nomor][4] + " | " + jadwal_list[nomor][5])
                        ada = True
                if not ada:
                    print("(Masih kosong)")
                print("\nIsi jadwal baru:")
                matkul = input("Matkul baru: ")
                jam = input("Jam: ")
                dosen = input("Dosen: ")
                ruangan = input("Ruangan: ")
                if matkul != "" and jam != "":
                    jadwal_list.append([kelas_admin, hari_pilih, matkul, jam, dosen, ruangan])
                    simpan_jadwal()
                    if len(notif_list) == 0:
                        notif_list.append("ada")
                    print("Berhasil ditambah! Jadwal lama tetap ada.")
                else:
                    print("Matkul dan jam jangan sampai kosong!")
            else:
                print("Nomor hari salah!")
        elif pilih == "4":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            cari = input("Cari matkul / dosen / ruangan: ")
            ditemukan = False
            for nomor in range(len(jadwal_list)):
                if jadwal_list[nomor][0] == kelas_admin and (cari in jadwal_list[nomor][2] or cari in jadwal_list[nomor][4] or cari in jadwal_list[nomor][5]):
                    print(jadwal_list[nomor][1] + " - " + jadwal_list[nomor][2] + " - " + jadwal_list[nomor][3] + " - " + jadwal_list[nomor][4] + " - " + jadwal_list[nomor][5])
                    ditemukan = True
            if not ditemukan:
                print("Gak ketemu!")
        elif pilih == "5":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            print("\n--- GANTI JADWAL - KELAS " + kelas_admin + " ---")
            nomor = int(input("Nomor yang mau diganti: "))
            if nomor >= 0 and nomor < len(jadwal_list) and jadwal_list[nomor][0] == kelas_admin:
                print("Isi baru (kosongin / enter aja kalau gak mau diubah):")
                matkul_baru = input("Matkul baru [" + jadwal_list[nomor][2] + "]: ")
                jam_baru = input("Jam baru [" + jadwal_list[nomor][3] + "]: ")
                dosen_baru = input("Dosen baru [" + jadwal_list[nomor][4] + "]: ")
                ruangan_baru = input("Ruangan baru [" + jadwal_list[nomor][5] + "]: ")
                if matkul_baru != "":
                    jadwal_list[nomor][2] = matkul_baru
                if jam_baru != "":
                    jadwal_list[nomor][3] = jam_baru
                if dosen_baru != "":
                    jadwal_list[nomor][4] = dosen_baru
                if ruangan_baru != "":
                    jadwal_list[nomor][5] = ruangan_baru
                simpan_jadwal()
                if len(notif_list) == 0:
                    notif_list.append("ada")
                print("Berhasil diganti!")
            else:
                print("Nomor salah! Itu bukan jadwal kelas " + kelas_admin)
        elif pilih == "6":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            nomor = int(input("Nomor yang mau dihapus: "))
            if nomor >= 0 and nomor < len(jadwal_list) and jadwal_list[nomor][0] == kelas_admin:
                jadwal_list.pop(nomor)
                simpan_jadwal()
                if len(notif_list) == 0:
                    notif_list.append("ada")
                print("Berhasil dihapus!")
            else:
                print("Nomor salah! Itu bukan jadwal kelas " + kelas_admin)
        elif pilih == "7":
            break
        else:
            print("Pilihan tidak tersedia!")

# URUTKAN MAHASISWA PER KELAS
def urutkan_mahasiswa(semua):
    urut = []
    for data in semua:
        urut.append(data)
    for i in range(len(urut)):
        for j in range(len(urut) - 1):
            if urut[j]["Kelas"] > urut[j + 1]["Kelas"]:
                temp = urut[j]
                urut[j] = urut[j + 1]
                urut[j + 1] = temp
    return urut

# MENU ADMIN
def menu_admin():
    while True:
        print("\n===== MENU ADMIN =====")
        print("1. Lihat data mahasiswa")
        print("2. Atur jadwal kuliah mahasiswa")
        print("3. Lihat Study Tracker mahasiswa")
        print("4. Keluarkan mahasiswa")
        print("5. Logout")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            semua = baca_csv("akun.csv")
            urut = urutkan_mahasiswa(semua)
            print("\n" + "=" * 92)
            print("DATA MAHASISWA UNIDAY - SEMUA KELAS")
            print("=" * 92)
            print("No  Nama                               NIM            Kelas  Prodi               Fakultas")
            print("-" * 90)
            for nomor in range(len(urut)):
                data = urut[nomor]
                nama_rata = data["Nama"]
                while len(nama_rata) < 35:
                    nama_rata = nama_rata + " "
                nim_rata = data["NIM"]
                while len(nim_rata) < 15:
                    nim_rata = nim_rata + " "
                prodi_rata = data["Prodi"]
                while len(prodi_rata) < 20:
                    prodi_rata = prodi_rata + " "
                print(str(nomor + 1) + "   " + nama_rata + nim_rata + data["Kelas"] + "      " + prodi_rata + data["Fakultas"])
            print("-" * 90)
            print("Jumlah Mahasiswa: " + str(len(urut)))
        elif pilihan == "2":
            atur_jadwal_admin()
        elif pilihan == "3":
            print("\n===== STUDY TRACKER MAHASISWA (ADMIN LIHAT SAJA) =====")
            baca_data_tracker()
            if len(nilai_list) == 0:
                print("Belum ada nilai.")
            else:
                for nomor in range(len(nilai_list)):
                    print(nilai_list[nomor][0] + " | Kuis: " + str(nilai_list[nomor][1]) + " | UTS: " + str(nilai_list[nomor][2]) + " | UAS: " + str(nilai_list[nomor][3]))
            if len(ipk_list) == 0:
                print("Belum ada IPK.")
            else:
                for nomor in range(len(ipk_list)):
                    print("Semester " + ipk_list[nomor][0] + " | IPK: " + str(ipk_list[nomor][1]))
        elif pilihan == "4":
            semua = baca_csv("akun.csv")
            urut = urutkan_mahasiswa(semua)
            if len(urut) == 0:
                print("Belum ada mahasiswa.")
            else:
                for nomor in range(len(urut)):
                    data = urut[nomor]
                    print(str(nomor + 1) + ". " + data["Nama"] + " - " + data["NIM"] + " - Kelas " + data["Kelas"] + " - " + data["Status"])
                pilih = int(input("Pilih nomor mahasiswa yang dikeluarkan: "))
                if pilih >= 1 and pilih <= len(urut):
                    nama_keluar = urut[pilih - 1]["Nama"]
                    urut[pilih - 1]["Status"] = "Dikeluarkan"
                    tulis_csv("akun.csv", ["Nama", "NIM", "Username", "Password", "Prodi", "Fakultas", "Kelas", "Status"], semua)
                    print("\n" + nama_keluar + " berhasil dikeluarkan! Dia tidak bisa login lagi.")
                else:
                    print("Nomor tidak ditemukan.")
        elif pilihan == "5":
            print("Admin berhasil logout!")
            break
        else:
            print("Pilihan tidak tersedia!")

# MENU UTAMA
def menu_utama():
    while True:
        print("\n====================================")
        print("               UNIDAY                ")
        print("      UNIVERSITY DAILY ACTIVITY")
        print("=====================================")
        print("1. Registrasi Mahasiswa")
        print("2. Login Mahasiswa")
        print("3. Login Admin")
        print("4. Keluar")
        pilihan = input("Pilihan menu (1-4): ")
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

menu_utama()