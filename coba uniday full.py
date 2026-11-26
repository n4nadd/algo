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
    file_tulis.write("Kelas,Hari,Mata Kuliah,Jam,Dosen,Ruangan\n")
    for nomor in range(len(jadwal_list)):
        file_tulis.write(jadwal_list[nomor][0] + "," + jadwal_list[nomor][1] + "," + jadwal_list[nomor][2] + "," + jadwal_list[nomor][3] + "," + jadwal_list[nomor][4] + "," + jadwal_list[nomor][5] + "\n")
    file_tulis.close()

# TAMPILKAN JADWAL

# TAMPILKAN JADWAL
def tampilkan_jadwal(kelas_pilih):
    print("\n===== JADWAL KULIAH - KELAS " + kelas_pilih + " =====")
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    ada_jadwal = False
    for hari in hari_list:
        data_hari = []
        for data in jadwal_list:
            if data[0] == kelas_pilih and data[1].lower() == hari.lower():
                data_hari.append(data)
        if len(data_hari) > 0:
            print("\n" + hari.upper())
            print("-" * 80)
            print(f"{'No':<4} {'Mata Kuliah':<30} {'Jam':<15} {'Dosen':<18} {'Ruangan'}")
            print("-" * 80)
            for nomor, data in enumerate(data_hari, start=1):
                print(f"{nomor:<4} {data[2]:<30} {data[3]:<15} {data[4]:<18} {data[5]}")
            ada_jadwal = True
    if not ada_jadwal:
        print("Belum ada jadwal! Tunggu admin input.")

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
            cari = input("\nCari matkul / dosen / ruangan: ")
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
            print("UNIDAY - MY TASK LIST - " + nama)
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
                print("NO | TUGAS | MATA KULIAH | DESKRIPSI | DEADLINE | PRIORITAS | STATUS")
                print("=" * 95)
                for nomor in range(len(daftar_tugas)):
                    data = daftar_tugas[nomor]
                    print(str(nomor + 1) + " | " + data["Tugas"] + " | " + data["Mata Kuliah"] + " | " + data["Deskripsi"] + " | " + data["Deadline"] + " | " + data["Prioritas"] + " | " + data["Status"])
                print("=" * 95)
                print("Total Tugas: " + str(len(daftar_tugas)) + " | Nama: " + nama)
        elif pilihan == "3":
            print("\n========================================")
            print("        UNIDAY - TASK CHECKLIST")
            print("          Track Your Daily Tasks")
            print("========================================")
            print("Keterangan: No | Status [ ] Belum / [V] Selesai | Tugas")
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
                print("   " + str(nomor + 1) + " " + tanda + " " + data["Tugas"] + " | " + data["Mata Kuliah"] + " | " + data["Deadline"])
            print("\n========================================")
            pilih = input("Centang nomor tugas (0 untuk kembali): ")
            if pilih != "0":
                pilih = int(pilih) - 1
                if pilih >= 0 and pilih < len(daftar_tugas):
                    daftar_tugas[pilih]["Status"] = "Selesai"
                    tulis_csv("todo.csv", ["Nama", "Tugas", "Mata Kuliah", "Deskripsi", "Deadline", "Prioritas", "Status"], semua)
                    print("\n[V] Tugas berhasil dicentang!")
        elif pilihan == "4":
            print("\n" + "=" * 95)
            print("                 UNIDAY - DELETE TASK")
            print("=" * 95)
            print("Keterangan: No | Tugas | Matkul | Deskripsi | Deadline | Prioritas | Status")
            semua = baca_csv("todo.csv")
            daftar_tugas = []
            for data in semua:
                if data["Nama"] == nama:
                    daftar_tugas.append(data)
            if len(daftar_tugas) == 0:
                print("Belum ada tugas.")
            else:
                print("NO  | TUGAS | MATKUL | DESKRIPSI | DEADLINE | PRIORITAS | STATUS")
                print("-" * 95)
                for nomor in range(len(daftar_tugas)):
                    data = daftar_tugas[nomor]
                    print(str(nomor + 1) + " | " + data["Tugas"] + " | " + data["Mata Kuliah"] + " | " + data["Deskripsi"] + " | " + data["Deadline"] + " | " + data["Prioritas"] + " | " + data["Status"])
                print("=" * 95)
                pilih = int(input("Pilih nomor tugas yang ingin dihapus: ")) - 1
                if pilih >= 0 and pilih < len(daftar_tugas):
                    semua.remove(daftar_tugas[pilih])
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
def simpan_catatan(matkul, topik, isi):
    with open("catatan_matkul.csv", "a", newline="") as file:
        tulis = csv.writer(file)
        if file.tell() == 0:
            tulis.writerow(["Matkul", "Topik", "Isi"])
        tulis.writerow([matkul, topik, isi])

# BACA CATATAN
def baca_catatan():
    list_catatan = []
    try:
        with open("catatan_matkul.csv", "r", newline="") as file:
            baca = csv.reader(file)
            next(baca, None)
            for row in baca:
                if len(row) == 3:
                    list_catatan.append([row[0], row[1], row[2]])
    except FileNotFoundError:
        list_catatan = []
    return list_catatan

# CARI MATERI
def cari_materi(data, kata_kunci):
    hasil = []
    for item in data:
        if kata_kunci in item[0] or kata_kunci in item[1] or kata_kunci in item[2]:
            hasil.append(item)
    return hasil

# CATATAN MATA KULIAH - KOTAK TABEL 1 KOLOM 1 BARIS
def catatan_matkul():
    pilih = ""
    while pilih != "0":
        print("\n===== CATATAN MATA KULIAH =====")
        print("Keterangan: Matkul | Topik | Isi Catatan")
        print("1. Tambah Catatan Matkul")
        print("2. Lihat Semua Catatan")
        print("3. Cari Materi")
        print("0. Keluar")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            print("\n--- TAMBAH CATATAN ---")
            print("Keterangan: Matkul | Topik | Isi")
            matkul = input("Nama mata kuliah : ")
            topik = input("Topik/materi      : ")
            isi = input("Isi catatan      : ")
            simpan_catatan(matkul, topik, isi)
            print("Catatan berhasil disimpan ke CSV.")
            print("Matkul: " + matkul + " | Topik: " + topik + " | Isi: " + isi)
        elif pilih == "2":
            data = baca_catatan()
            if len(data) == 0:
                print("Belum ada catatan tersimpan.")
                continue
            print("\n===== DAFTAR CATATAN MATA KULIAH =====")
            print("-" * 85)
            print(f"{'No':<4} {'Mata Kuliah':<20} {'Topik':<25} {'Isi Catatan'}")
            print("-" * 85)
            for nomor, item in enumerate(data, start=1):
                if item[0] == "Matkul":
                    continue

                print(
                    f"{nomor:<4} {item[0]:<20} "
                    f"{item[1]:<25} {item[2]}"
                )
            print("-" * 85)
            print("Total Catatan :", len(data))
        elif pilih == "3":
            kata = input("Masukkan kata kunci materi/matkul: ")
            data = baca_catatan()
            hasil_cari = cari_materi(data, kata)
            if len(hasil_cari) == 0:
                print("Materi tidak ditemukan.")
                continue
            print("\n===== HASIL PENCARIAN =====")
            print("-" * 85)
            print(f"{'No':<4} {'Mata Kuliah':<20} {'Topik':<25} {'Isi Catatan'}")
            print("-" * 85)
            for nomor, item in enumerate(hasil_cari, start=1):
                if item[0] == "Matkul":
                    continue
                print(
                    f"{nomor:<4} {item[0]:<20} "
                    f"{item[1]:<25} {item[2]}"
                )
            print("-" * 85)
            print("Total Hasil :", len(hasil_cari))
        elif pilih == "0":
            print("Selesai, keluar program.")
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

# =====================================
# STUDY TRACKER - PAKAI 1 FILE
# Study Tracker.csv
# =====================================

# BACA DATA TRACKER - ADA NAMA, BISA BACA CSV LAMA JUGA
def baca_data_tracker():
    global nilai_list, ipk_list
    nilai_list = []
    ipk_list = []
    try:
        with open("Study Tracker.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for data in reader:
                # FORMAT BARU - 6 kolom : Jenis Data,Nama,Matkul/Semester,Kuis,UTS,UAS/IPK
                if len(data) == 6:
                    if data[0] == "Nilai":
                        nilai_list.append([data[1], data[2], float(data[3]), float(data[4]), float(data[5])])
                    elif data[0] == "IPK":
                        ipk_list.append([data[1], data[2], float(data[5])])
                # FORMAT LAMA - 5 kolom : Jenis Data,Matkul/Semester,Kuis,UTS,UAS/IPK (gak ada Nama)
                elif len(data) == 5:
                    if data[0] == "Nilai":
                        nilai_list.append(["", data[1], float(data[2]), float(data[3]), float(data[4])])
                    elif data[0] == "IPK":
                        ipk_list.append(["", data[1], float(data[4])])
    except:
        pass

# SIMPAN TRACKER - ADA NAMA
def simpan_tracker():
    with open("Study Tracker.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Jenis Data", "Nama", "Mata Kuliah/Semester", "Kuis", "UTS", "UAS/IPK"])
        for data in nilai_list:
            writer.writerow(["Nilai"] + data)
        for data in ipk_list:
            writer.writerow(["IPK", data[0], data[1], "-", "-", data[2]])

# HITUNG NILAI AKHIR + HURUF
def hitung_nilai(kuis, uts, uas):
    akhir = (kuis * 0.2) + (uts * 0.3) + (uas * 0.5)
    huruf = "E"
    if akhir >= 80:
        huruf = "A"
    elif akhir >= 70:
        huruf = "B"
    elif akhir >= 60:
        huruf = "C"
    elif akhir >= 50:
        huruf = "D"
    return akhir, huruf

# HITUNG PREDIKAT IPK
def hitung_predikat(ipk):
    predikat = "Sangat Kurang, Semangat!"
    if ipk >= 3.5:
        predikat = "Sangat Bagus / Cumlaude"
    elif ipk >= 3.0:
        predikat = "Bagus"
    elif ipk >= 2.75:
        predikat = "Normal / Cukup"
    elif ipk >= 2.0:
        predikat = "Kurang"
    return predikat

# TAMPILKAN STUDY TRACKER 1 MAHASISWA
def tampilkan_tracker_1_orang(nama_tampil):
    print("\n========================================")
    print("NAMA MAHASISWA : " + nama_tampil)
    print("========================================")
    print("--- NILAI ---")
    print("Keterangan: No | Mata Kuliah | Kuis | UTS | UAS | Nilai Akhir | Huruf")
    ada_nilai = False
    hitung = 1
    for nomor in range(len(nilai_list)):
        # Nama kosong = data lama, tetep ditampilin biar gak ilang
        if nilai_list[nomor][0] == nama_tampil or nilai_list[nomor][0] == "":
            matkul = nilai_list[nomor][1]
            kuis = nilai_list[nomor][2]
            uts = nilai_list[nomor][3]
            uas = nilai_list[nomor][4]
            akhir, huruf = hitung_nilai(kuis, uts, uas)
            bulat = akhir // 1
            sisa = round(akhir % 1, 2)
            print(str(hitung) + ". " + matkul + " | Kuis: " + str(kuis) + " | UTS: " + str(uts) + " | UAS: " + str(uas) + " | Nilai Akhir: " + str(round(akhir, 2)) + " (bulat " + str(bulat) + " sisa " + str(sisa) + ")" + " | Huruf: " + huruf)
            ada_nilai = True
            hitung = hitung + 1
    if not ada_nilai:
        print("Belum ada nilai!")
    print("--- RIWAYAT IPK ---")
    print("Keterangan: No | Semester | IPK | Predikat")
    ada_ipk = False
    hitung_ipk = 1
    for nomor in range(len(ipk_list)):
        if ipk_list[nomor][0] == nama_tampil or ipk_list[nomor][0] == "":
            semester = ipk_list[nomor][1]
            ipk = ipk_list[nomor][2]
            predikat = hitung_predikat(ipk)
            print(str(hitung_ipk) + ". Semester " + semester + " | IPK: " + str(ipk) + " | Predikat: " + predikat)
            ada_ipk = True
            hitung_ipk = hitung_ipk + 1
    if not ada_ipk:
        print("Belum input IPK!")

# STUDY TRACKER MAHASISWA - CUMA PUNYA DIA SENDIRI
def study_tracker(nama):
    baca_data_tracker()
    while True:
        print("\n========== STUDY TRACKER ==========")
        print("Nama Mahasiswa : " + nama)
        print("Keterangan Nilai: Nama | Mata Kuliah | Kuis | UTS | UAS | Nilai Akhir | Huruf")
        print("Keterangan IPK: Nama | Semester | IPK | Predikat")
        print("====================================")
        print("1. Lihat Nilai dan IPK Saya")
        print("2. Input Nilai (Kuis, UTS, UAS)")
        print("3. Input IPK (Input Sendiri)")
        print("4. Ubah Nilai")
        print("5. Hapus Nilai")
        print("6. Kembali")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_tracker_1_orang(nama)
        elif pilih == "2":
            print("\n--- INPUT NILAI ---")
            print("Keterangan: Mata Kuliah | Kuis (0-100) | UTS (0-100) | UAS (0-100)")
            matkul = input("Nama Mata Kuliah: ")
            kuis = input_angka("Nilai Kuis: ", 0, 100)
            uts = input_angka("Nilai UTS: ", 0, 100)
            uas = input_angka("Nilai UAS: ", 0, 100)
            nilai_list.append([nama, matkul, kuis, uts, uas])
            simpan_tracker()
            print("Nilai berhasil disimpan!")
            print("Nama: " + nama + " | Matkul: " + matkul + " | Kuis: " + str(kuis) + " | UTS: " + str(uts) + " | UAS: " + str(uas))
        elif pilih == "3":
            print("\n--- INPUT IPK ---")
            print("Keterangan: Semester | IPK (0.00 - 4.00)")
            semester = input("Semester ke-berapa: ")
            ipk = input_angka("Masukkan IPK (0.00 - 4.00): ", 0, 4)
            ipk_list.append([nama, semester, ipk])
            simpan_tracker()
            print("IPK berhasil disimpan!")
            print("Nama: " + nama + " | Semester: " + semester + " | IPK: " + str(ipk))
        elif pilih == "4":
            daftar_saya = []
            for data in nilai_list:
                if data[0] == nama or data[0] == "":
                    daftar_saya.append(data)
            if len(daftar_saya) == 0:
                print("Belum ada nilai yang bisa diubah!")
            else:
                print("\nDaftar Mata Kuliah - " + nama + ":")
                print("NO | MATA KULIAH | KUIS | UTS | UAS")
                for nomor in range(len(daftar_saya)):
                    print(str(nomor + 1) + " . " + daftar_saya[nomor][1] + " | Kuis: " + str(daftar_saya[nomor][2]) + " | UTS: " + str(daftar_saya[nomor][3]) + " | UAS: " + str(daftar_saya[nomor][4]))
                try:
                    nomor_pilih = int(input("Nomor yang mau diubah: ")) - 1
                    if nomor_pilih >= 0 and nomor_pilih < len(daftar_saya):
                        target = daftar_saya[nomor_pilih]
                        for data in nilai_list:
                            if data == target:
                                data[0] = nama
                                data[2] = input_angka("Kuis baru: ", 0, 100)
                                data[3] = input_angka("UTS baru: ", 0, 100)
                                data[4] = input_angka("UAS baru: ", 0, 100)
                                break
                        simpan_tracker()
                        print("Nilai berhasil diubah!")
                    else:
                        print("Nomor tidak ditemukan!")
                except ValueError:
                    print("Masukkan nomor yang valid!")
        elif pilih == "5":
            daftar_saya = []
            for data in nilai_list:
                if data[0] == nama or data[0] == "":
                    daftar_saya.append(data)
            if len(daftar_saya) == 0:
                print("Belum ada nilai yang bisa dihapus!")
            else:
                print("\nDaftar Mata Kuliah - " + nama + ":")
                print("NO | MATA KULIAH | KUIS | UTS | UAS")
                for nomor in range(len(daftar_saya)):
                    print(str(nomor + 1) + " . " + daftar_saya[nomor][1] + " | Kuis: " + str(daftar_saya[nomor][2]) + " | UTS: " + str(daftar_saya[nomor][3]) + " | UAS: " + str(daftar_saya[nomor][4]))
                try:
                    nomor_pilih = int(input("Nomor yang mau dihapus: ")) - 1
                    if nomor_pilih >= 0 and nomor_pilih < len(daftar_saya):
                        nilai_list.remove(daftar_saya[nomor_pilih])
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
            study_tracker(nama)
        elif pilihan == "5":
            print("\nBerhasil logout!")
            break
        else:
            print("\nPilihan tidak valid!")

# LOGIN ADMIN
def login_admin():
    print("\n===== LOGIN ADMIN =====")
    print("Keterangan: Username | Password")
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
        print("Keterangan: Kelas A | Kelas B | Kelas C")
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
        print("\n--- JADWAL KULIAH - ADMIN ---")
        print("Keterangan: Kelas | Hari | Mata Kuliah | Jam | Dosen | Ruangan")
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
                print("Keterangan: Mata Kuliah | Jam | Dosen | Ruangan")
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
            print("Keterangan: Hari | Mata Kuliah | Jam | Dosen | Ruangan")
            hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
            for nomor_hari in range(len(hari_list)):
                print(str(nomor_hari + 1) + ". " + hari_list[nomor_hari])
            nomor_hari = int(input("Nomor hari: ")) - 1
            if nomor_hari >= 0 and nomor_hari < len(hari_list):
                hari_pilih = hari_list[nomor_hari]
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
                    print("Kelas: " + kelas_admin + " | Hari: " + hari_pilih + " | Matkul: " + matkul + " | Jam: " + jam + " | Dosen: " + dosen + " | Ruangan: " + ruangan)
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
            print("Keterangan: No | Hari | Mata Kuliah | Jam | Dosen | Ruangan")
            nomor = int(input("Nomor yang mau diganti: ")) - 1
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
            print("\n--- HAPUS JADWAL - KELAS " + kelas_admin + " ---")
            print("Keterangan: No | Hari | Mata Kuliah | Jam | Dosen | Ruangan")
            nomor = int(input("Nomor yang mau dihapus: ")) - 1
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
            print("No | Nama | NIM | Username | Kelas | Prodi | Fakultas | Status")
            print("-" * 90)
            for nomor in range(len(urut)):
                data = urut[nomor]
                nama_rata = data["Nama"]
                while len(nama_rata) < 20:
                    nama_rata = nama_rata + " "
                nim_rata = data["NIM"]
                while len(nim_rata) < 12:
                    nim_rata = nim_rata + " "
                user_rata = data["Username"]
                while len(user_rata) < 12:
                    user_rata = user_rata + " "
                prodi_rata = data["Prodi"]
                while len(prodi_rata) < 15:
                    prodi_rata = prodi_rata + " "
                print(str(nomor + 1) + " | " + nama_rata + " | " + nim_rata + " | " + user_rata + " | " + data["Kelas"] + " | " + prodi_rata + " | " + data["Fakultas"] + " | " + data["Status"])
            print("-" * 90)
            print("Jumlah Mahasiswa: " + str(len(urut)))
        elif pilihan == "2":
            atur_jadwal_admin()
        elif pilihan == "3":
            print("\n===== STUDY TRACKER MAHASISWA (ADMIN LIHAT SAJA) =====")
            print("Keterangan: Per Mahasiswa - Nama | Nilai | IPK")
            baca_data_tracker()
            semua_mhs = baca_csv("akun.csv")
            if len(semua_mhs) == 0:
                print("Belum ada mahasiswa.")
            else:
                for data_mhs in semua_mhs:
                    tampilkan_tracker_1_orang(data_mhs["Nama"])
        elif pilihan == "4":
            semua = baca_csv("akun.csv")
            urut = urutkan_mahasiswa(semua)
            if len(urut) == 0:
                print("Belum ada mahasiswa.")
            else:
                print("\n===== KELUARKAN MAHASISWA =====")
                for nomor in range(len(urut)):
                    data = urut[nomor]
                    print(str(nomor + 1) + ". " + data["Nama"] + " - NIM: " + data["NIM"] + " - Kelas " + data["Kelas"] + " - " + data["Status"])
                pilih = int(input("Pilih nomor mahasiswa yang dikeluarkan: ")) - 1
                if pilih >= 0 and pilih < len(urut):
                    nama_keluar = urut[pilih]["Nama"]
                    urut[pilih]["Status"] = "Dikeluarkan"
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