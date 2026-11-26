import csv
from datetime import datetime

jadwal_list = []
notif_list = []
nilai_list = []
ipk_list = []

def rata(teks, lebar):
    t = str(teks)
    if t == "" or t == "None":
        t = "-"
    while len(t) < lebar:
        t = t + " "
    return t[:lebar]

def tengah(teks, lebar):
    t = str(teks)
    if len(t) >= lebar:
        return t[:lebar]
    sisa = lebar - len(t)
    kiri = sisa // 2
    kanan = sisa - kiri
    return (" " * kiri) + t + (" " * kanan)

def tanggal_sekarang():
    # Jadi: 24 Nov 2026, 11:09
    return datetime.now().strftime("%d %b %Y, %H:%M")

def baca_csv(nama_file):
    hasil = []
    try:
        with open(nama_file, "r", newline="") as file:
            reader = csv.DictReader(file)
            for data in reader:
                data_bersih = {}
                for kunci, nilai in data.items():
                    if kunci is not None:
                        data_bersih[kunci.strip()] = nilai
                hasil.append(data_bersih)
    except FileNotFoundError:
        hasil = []
    return hasil

def tulis_csv(nama_file, kolom, semua_data):
    with open(nama_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(semua_data)

def input_angka(pesan, minimum, maksimum):
    while True:
        try:
            angka = float(input(pesan))
            if angka >= minimum and angka <= maksimum:
                return angka
            print("Input harus antara " + str(minimum) + " sampai " + str(maksimum))
        except ValueError:
            print("Masukkan angka yang valid!")

# JADWAL KULIAH
def urutan_hari(hari):
    if hari == "Senin":
        return 0
    if hari == "Selasa":
        return 1
    if hari == "Rabu":
        return 2
    if hari == "Kamis":
        return 3
    if hari == "Jumat":
        return 4
    return 5

def jadwal_urut_kelas(kelas_pilih):
    hasil = []
    for data in jadwal_list:
        if data[0] == kelas_pilih:
            hasil.append(data)
    for i in range(len(hasil)):
        for j in range(len(hasil) - 1):
            if urutan_hari(hasil[j][1]) > urutan_hari(hasil[j + 1][1]):
                temp = hasil[j]
                hasil[j] = hasil[j + 1]
                hasil[j + 1] = temp
    return hasil

def bongkar_baris(baris):
    data_baris = ["", "", "", "", "", ""]
    kolom = 0
    for predikat in baris:
        if predikat == "|" or predikat == ",":
            kolom = kolom + 1
        elif predikat == "\n":
            pass
        elif kolom < 6:
            data_baris[kolom] = data_baris[kolom] + predikat
    return data_baris

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

def simpan_jadwal():
    file_tulis = open("jadwal.csv", "w")
    file_tulis.write("Kelas,Hari,Mata Kuliah,Jam,Dosen,Ruangan\n")
    for nomor in range(len(jadwal_list)):
        d = jadwal_list[nomor]
        file_tulis.write(d[0] + "," + d[1] + "," + d[2] + "," + d[3] + "," + d[4] + "," + d[5] + "\n")
    file_tulis.close()

def tampilkan_jadwal(kelas_pilih):
    print("\nJADWAL KULIAH - KELAS " + kelas_pilih)
    urut = jadwal_urut_kelas(kelas_pilih)
    if len(urut) == 0:
        print("Belum ada jadwal! Tunggu admin input.")
        return urut
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    for hari in hari_list:
        ada = False
        for data in urut:
            if data[1] == hari:
                ada = True
                break
        if ada:
            print("\n-- " + hari + " --")
            print(rata("NO", 4) + " | " + rata("MATA KULIAH", 28) + " | " + rata("JAM", 14) + " | " + rata("DOSEN", 20) + " | " + rata("RUANGAN", 12))
            no_per_hari = 1
            for data in urut:
                if data[1] == hari:
                    print(rata(str(no_per_hari), 4) + " | " + rata(data[2], 28) + " | " + rata(data[3], 14) + " | " + rata(data[4], 20) + " | " + rata(data[5], 12))
                    no_per_hari = no_per_hari + 1
    return urut

def pilih_jadwal_per_hari(kelas_pilih):
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    for i in range(len(hari_list)):
        print(str(i + 1) + ". " + hari_list[i])
    nomor_hari = int(input("Pilih hari (1-5): ")) - 1
    if nomor_hari < 0 or nomor_hari >= len(hari_list):
        print("Nomor hari salah!")
        return None
    hari_pilih = hari_list[nomor_hari]
    urut = jadwal_urut_kelas(kelas_pilih)
    daftar_hari = []
    for data in urut:
        if data[1] == hari_pilih:
            daftar_hari.append(data)
    if len(daftar_hari) == 0:
        print("Tidak ada jadwal di hari " + hari_pilih)
        return None
    print("\nJadwal hari " + hari_pilih + ":")
    for i in range(len(daftar_hari)):
        print(str(i + 1) + ". " + daftar_hari[i][2] + " | " + daftar_hari[i][3] + " | " + daftar_hari[i][4] + " | " + daftar_hari[i][5])
    nomor = int(input("Nomor di hari " + hari_pilih + ": ")) - 1
    if nomor < 0 or nomor >= len(daftar_hari):
        print("Nomor salah!")
        return None
    return daftar_hari[nomor]

def cari_dan_tampilkan_jadwal(kelas_pilih, cari):
    cari_kecil = cari.lower()
    urut = jadwal_urut_kelas(kelas_pilih)
    ditemukan = False
    for data in urut:
        if cari_kecil in data[2].lower() or cari_kecil in data[4].lower() or cari_kecil in data[5].lower() or cari_kecil in data[1].lower():
            print(data[1] + " | " + data[2] + " | " + data[3] + " | " + data[4] + " | " + data[5])
            ditemukan = True
    if not ditemukan:
        print("Tidak ditemukan!")

def jadwal_kuliah_mahasiswa(kelas):
    if len(notif_list) > 0:
        print("\nPERHATIKAN!! ADA PERUBAHAN JADWAL")
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
            cari_dan_tampilkan_jadwal(kelas, cari)
        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid!")

# CATATAN MATA KULIAH - URUTAN: NO | MATA KULIAH | TOPIK | ISI | TANGGAL
def simpan_catatan(matkul, topik, isi):
    tanggal = tanggal_sekarang()
    with open("catatan_matkul.csv", "a", newline="") as file:
        tulis = csv.writer(file)
        if file.tell() == 0:
            tulis.writerow(["Matkul", "Topik", "Isi", "Tanggal"])
        tulis.writerow([matkul, topik, isi, tanggal])

def baca_catatan():
    list_catatan = []
    try:
        with open("catatan_matkul.csv", "r", newline="") as file:
            baca = csv.reader(file)
            header = next(baca, None)
            for row in baca:
                if len(row) == 3:
                    list_catatan.append([row[0], row[1], row[2], "-"])
                elif len(row) >= 4:
                    list_catatan.append([row[0], row[1], row[2], row[3]])
    except FileNotFoundError:
        list_catatan = []
    return list_catatan

def cari_materi(data, kata_kunci):
    kata_kecil = kata_kunci.lower()
    hasil = []
    for item in data:
        if kata_kecil in item[0].lower() or kata_kecil in item[1].lower() or kata_kecil in item[2].lower():
            hasil.append(item)
    return hasil

def tampilkan_catatan(data, judul_tabel):
    print("\n" + judul_tabel)
    print("-" * 40)
    print(rata("NO", 4) + " | " + rata("MATA KULIAH", 22) + " | " + rata("TOPIK", 28) + " | " + rata("ISI", 60) + " | " + rata("TANGGAL", 18))
    for nomor in range(len(data)):
        item = data[nomor]
        print(rata(str(nomor + 1), 4) + " | " + rata(item[0], 22) + " | " + rata(item[1], 28) + " | " + rata(item[2], 60) + " | " + rata(item[3], 18))

def catatan_matkul():
    pilih = ""
    while pilih != "0":
        print("\n===== CATATAN MATA KULIAH =====")
        print("1. Tambah Catatan Matkul")
        print("2. Lihat Semua Catatan")
        print("3. Cari Materi")
        print("0. Keluar")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            print("\n--- TAMBAH CATATAN ---")
            matkul = input("Nama mata kuliah : ")
            topik = input("Topik/materi      : ")
            isi = input("Isi catatan       : ")
            simpan_catatan(matkul, topik, isi)
            print("Catatan berhasil disimpan ke CSV.")
        elif pilih == "2":
            data = baca_catatan()
            if len(data) == 0:
                print("Belum ada catatan tersimpan.")
                continue
            tampilkan_catatan(data, "DAFTAR CATATAN MATA KULIAH")
            print("Total Catatan : " + str(len(data)))
        elif pilih == "3":
            kata = input("Masukkan kata kunci materi/matkul: ")
            data = baca_catatan()
            hasil_cari = cari_materi(data, kata)
            if len(hasil_cari) == 0:
                print("Materi tidak ketemu.")
                continue
            tampilkan_catatan(hasil_cari, "HASIL PENCARIAN '" + kata + "'")
        elif pilih == "0":
            print("Selesai, keluar program.")
            break
        else:
            print("Pilihan tidak ada.")

# TO-DO LIST - URUTAN SAMA: NO | MATA KULIAH | TUGAS | DESKRIPSI | DEADLINE | PRIORITAS | STATUS
def ambil_todo_saya(nama):
    semua = baca_csv("todo.csv")
    daftar = []
    for data in semua:
        if data.get("Nama") == nama:
            daftar.append(data)
    return semua, daftar

def tampilkan_todo(daftar, judul_tabel):
    print("\n" + judul_tabel)
    print(rata("NO", 4) + " | " + rata("MATA KULIAH", 20) + " | " + rata("TUGAS", 20) + " | " + rata("DESKRIPSI", 30) + " | " + rata("DEADLINE", 12) + " | " + rata("PRIORITAS", 10) + " | " + rata("STATUS", 14))
    for nomor in range(len(daftar)):
        d = daftar[nomor]
        print(rata(str(nomor + 1), 4) + " | " + rata(d.get("Mata Kuliah", "-"), 20) + " | " + rata(d.get("Tugas", "-"), 20) + " | " + rata(d.get("Deskripsi", "-"), 30) + " | " + rata(d.get("Deadline", "-"), 12) + " | " + rata(d.get("Prioritas", "-"), 10) + " | " + rata(d.get("Status", "-"), 14))

def todo_list(nama):
    while True:
        print("\n===== UNIDAY - TO-DO LIST =====")
        print("UNIVERSITY DAILY ACTIVITY")
        print("1. Add New Task")
        print("2. My Task List")
        print("3. Task Checklist")
        print("4. Delete Task")
        print("5. Kembali ke Beranda....")
        pilihan = input("Pilih menu (1-5): ")
        if pilihan == "1":
            print("\n--- UNIDAY - ADD NEW TASK ---")
            matkul = input("Mata Kuliah      : ")
            tugas = input("Nama Tugas       : ")
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
            semua, daftar = ambil_todo_saya(nama)
            if len(daftar) == 0:
                print("\nBelum ada tugas yang ditambahkan.")
            else:
                tampilkan_todo(daftar, "MY TASK LIST - " + nama)
                print("Total Tugas: " + str(len(daftar)))
        elif pilihan == "3":
            print("\n--- UNIDAY - TASK CHECKLIST ---")
            semua, daftar = ambil_todo_saya(nama)
            print(rata("NO", 4) + " | " + rata("STATUS", 8) + " | " + rata("MATA KULIAH", 20) + " | " + rata("TUGAS", 20) + " | " + rata("DESKRIPSI", 30) + " | " + rata("DEADLINE", 12) + " | " + rata("PRIORITAS", 10))
            for nomor in range(len(daftar)):
                d = daftar[nomor]
                tanda = "[V]" if d.get("Status") == "Selesai" else "[ ]"
                print(rata(str(nomor + 1), 4) + " | " + rata(tanda, 8) + " | " + rata(d.get("Mata Kuliah", "-"), 20) + " | " + rata(d.get("Tugas", "-"), 20) + " | " + rata(d.get("Deskripsi", "-"), 30) + " | " + rata(d.get("Deadline", "-"), 12) + " | " + rata(d.get("Prioritas", "-"), 10))
            pilih = input("Centang nomor tugas (0 untuk kembali): ")
            if pilih != "0":
                pilih = int(pilih) - 1
                if pilih >= 0 and pilih < len(daftar):
                    daftar[pilih]["Status"] = "Selesai"
                    tulis_csv("todo.csv", ["Nama", "Tugas", "Mata Kuliah", "Deskripsi", "Deadline", "Prioritas", "Status"], semua)
                    print("\n[V] Tugas berhasil dicentang!")
                    print("Tugas: " + str(daftar[pilih].get("Tugas")) + " | Status: Selesai")
        elif pilihan == "4":
            semua, daftar = ambil_todo_saya(nama)
            if len(daftar) == 0:
                print("Belum ada tugas.")
            else:
                tampilkan_todo(daftar, "UNIDAY - DELETE TASK")
                pilih = int(input("Pilih nomor tugas yang ingin dihapus: ")) - 1
                if pilih >= 0 and pilih < len(daftar):
                    semua.remove(daftar[pilih])
                    tulis_csv("todo.csv", ["Nama", "Tugas", "Mata Kuliah", "Deskripsi", "Deadline", "Prioritas", "Status"], semua)
                    print("\nTugas berhasil dihapus!")
                else:
                    print("Nomor tugas tidak ditemukan.")
        elif pilihan == "5":
            print("Kembali ke beranda...")
            break
        else:
            print("Pilihan tidak valid!")

# STUDY TRACKER
def baca_data_tracker():
    global nilai_list, ipk_list
    nilai_list = []
    ipk_list = []
    try:
        with open("Study Tracker.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for data in reader:
                if len(data) == 6:
                    if data[0] == "Nilai":
                        nilai_list.append([data[1], data[2], float(data[3]), float(data[4]), float(data[5])])
                    elif data[0] == "IPK":
                        ipk_list.append([data[1], data[2], float(data[5])])
                elif len(data) == 5:
                    if data[0] == "Nilai":
                        nilai_list.append(["", data[1], float(data[2]), float(data[3]), float(data[4])])
                    elif data[0] == "IPK":
                        ipk_list.append(["", data[1], float(data[4])])
    except:
        pass

def simpan_tracker():
    with open("Study Tracker.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Jenis Data", "Nama", "Mata Kuliah/Semester", "Kuis", "UTS", "UAS/IPK"])
        for data in nilai_list:
            writer.writerow(["Nilai"] + data)
        for data in ipk_list:
            writer.writerow(["IPK", data[0], data[1], "-", "-", data[2]])

def hitung_nilai(kuis, uts, uas):
    akhir = (kuis * 0.2) + (uts * 0.3) + (uas * 0.5)
    hitung_predikat = "E"
    if akhir >= 80:
        predikat = "A"
    elif akhir >= 70:
        predikat = "B"
    elif akhir >= 60:
        predikat = "C"
    elif akhir >= 50:
        predikat = "D"
    return akhir, predikat

def hitung_predikat(ipk):
    if ipk >= 3.5:
        return "Sangat Bagus / Cumlaude"
    if ipk >= 3.0:
        return "Bagus"
    if ipk >= 2.75:
        return "Normal / Cukup"
    if ipk >= 2.0:
        return "Kurang"
    return "Sangat Kurang, Semangat!"

def tampilkan_tracker_1_orang(nama_tampil):
    print("\nNAMA MAHASISWA : " + nama_tampil)
    print("\n-- NILAI --")
    print(rata("NO", 4) + " | " + rata("MATA KULIAH", 28) + " | " + rata("KUIS", 8) + " | " + rata("UTS", 8) + " | " + rata("UAS", 8) + " | " + rata("NILAI AKHIR", 12) + " | " + rata("PREDIKAT NILAI", 7))
    ada_nilai = False
    hitung = 1
    for nomor in range(len(nilai_list)):
        if nilai_list[nomor][0] == nama_tampil or nilai_list[nomor][0] == "":
            matkul = nilai_list[nomor][1]
            kuis = nilai_list[nomor][2]
            uts = nilai_list[nomor][3]
            uas = nilai_list[nomor][4]
            akhir, predikat = hitung_nilai(kuis, uts, uas)
            print(rata(str(hitung), 4) + " | " + rata(matkul, 28) + " | " + rata(str(kuis), 8) + " | " + rata(str(uts), 8) + " | " + rata(str(uas), 8) + " | " + rata(str(round(akhir, 2)), 12) + " | " + rata(predikat,14))
            ada_nilai = True
            hitung = hitung + 1
    if not ada_nilai:
        print("Belum ada nilai!")
    print("\n-- RIWAYAT IPK --")
    print(rata("NO", 4) + " | " + rata("SEMESTER", 12) + " | " + rata("IPK", 8) + " | " + rata("PREDIKAT", 30))
    ada_ipk = False
    hitung_ipk = 1
    for nomor in range(len(ipk_list)):
        if ipk_list[nomor][0] == nama_tampil or ipk_list[nomor][0] == "":
            semester = ipk_list[nomor][1]
            ipk = ipk_list[nomor][2]
            predikat = hitung_predikat(ipk)
            print(rata(str(hitung_ipk), 4) + " | " + rata(str(semester), 12) + " | " + rata(str(ipk), 8) + " | " + rata(predikat, 30))
            ada_ipk = True
            hitung_ipk = hitung_ipk + 1
    if not ada_ipk:
        print("Belum input IPK!")

def ambil_nilai_saya(nama):
    daftar = []
    for data in nilai_list:
        if data[0] == nama or data[0] == "":
            daftar.append(data)
    return daftar

def tampilkan_nilai_saya(daftar):
    print(rata("NO", 4) + " | " + rata("MATA KULIAH", 28) + " | " + rata("KUIS", 8) + " | " + rata("UTS", 8) + " | " + rata("UAS", 8))
    for nomor in range(len(daftar)):
        print(rata(str(nomor + 1), 4) + " | " + rata(daftar[nomor][1], 28) + " | " + rata(str(daftar[nomor][2]), 8) + " | " + rata(str(daftar[nomor][3]), 8) + " | " + rata(str(daftar[nomor][4]), 8))

def study_tracker(nama):
    baca_data_tracker()
    while True:
        print("\n========== STUDY TRACKER ==========")
        print("Nama Mahasiswa : " + nama)
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
            matkul = input("Nama Mata Kuliah: ")
            kuis = input_angka("Nilai Kuis: ", 0, 100)
            uts = input_angka("Nilai UTS: ", 0, 100)
            uas = input_angka("Nilai UAS: ", 0, 100)
            nilai_list.append([nama, matkul, kuis, uts, uas])
            simpan_tracker()
            print("Nilai berhasil disimpan!")
        elif pilih == "3":
            print("\n--- INPUT IPK ---")
            semester = input("Semester ke-berapa: ")
            ipk = input_angka("Masukkan IPK (0.00 - 4.00): ", 0, 4)
            ipk_list.append([nama, semester, ipk])
            simpan_tracker()
            print("IPK berhasil disimpan!")
        elif pilih == "4":
            daftar = ambil_nilai_saya(nama)
            if len(daftar) == 0:
                print("Belum ada nilai yang bisa diubah!")
            else:
                tampilkan_nilai_saya(daftar)
                try:
                    nomor_pilih = int(input("Nomor yang mau diubah: ")) - 1
                    if nomor_pilih >= 0 and nomor_pilih < len(daftar):
                        target = daftar[nomor_pilih]
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
            daftar = ambil_nilai_saya(nama)
            if len(daftar) == 0:
                print("Belum ada nilai yang bisa dihapus!")
            else:
                tampilkan_nilai_saya(daftar)
                try:
                    nomor_pilih = int(input("Nomor yang mau dihapus: ")) - 1
                    if nomor_pilih >= 0 and nomor_pilih < len(daftar):
                        nilai_list.remove(daftar[nomor_pilih])
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
        print("\n" + "=" * 44)
        print(tengah("UNIDAY", 44))
        print(tengah("UNIVERSITY DAILY ACTIVITY", 44))
        print("=" * 44)
        print(tengah("HELLO, " + nama, 44))
        print(tengah("KELAS " + kelas, 44))
        print(tengah("This is your academic journey", 44))
        print("=" * 44)
        print("   [01]  JADWAL KULIAH")
        print("   [02]  CATATAN MATA KULIAH")
        print("   [03]  TO-DO LIST")
        print("   [04]  STUDY TRACKER")
        print("   [05]  LOGOUT")
        print("=" * 44)
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

# REGISTRASI & LOGIN MAHASISWA
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
        if data.get("Username") == username:
            print("Username sudah digunakan!")
            return
        if data.get("NIM") == nim:
            print("NIM sudah terdaftar! Kalau kamu dikeluarkan, hubungi admin.")
            return
    with open("akun.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Nama", "NIM", "Username", "Password", "Prodi", "Fakultas", "Kelas", "Status"])
        writer.writerow([nama, nim, username, password, prodi, fakultas, kelas, "Aktif"])
    print("\nRegistrasi berhasil!")

def login_mahasiswa():
    print("\n===== LOGIN MAHASISWA =====")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    semua = baca_csv("akun.csv")
    for data in semua:
        if data.get("Username") == username and data.get("Password") == password:
            if data.get("Status") == "Dikeluarkan":
                print("\nAnda dikeluarkan dari UNIDAY, tidak bisa login lagi.")
                print("Hubungi admin untuk info lebih lanjut.")
                return
            print("\nLogin berhasil!")
            beranda_mahasiswa(data.get("Nama"), data.get("Kelas"))
            return
    print("\nUsername atau password salah!")

# ADMIN
def urutkan_mahasiswa(semua):
    urut = []
    for data in semua:
        urut.append(data)
    for i in range(len(urut)):
        for j in range(len(urut) - 1):
            if urut[j].get("Kelas", "") > urut[j + 1].get("Kelas", ""):
                temp = urut[j]
                urut[j] = urut[j + 1]
                urut[j + 1] = temp
    return urut

def tampilkan_mahasiswa(urut, dengan_username=True):
    if dengan_username:
        print(rata("NO", 4) + " | " + rata("NAMA", 35) + " | " + rata("NIM", 15) + " | " + rata("USERNAME", 14) + " | " + rata("KELAS", 6) + " | " + rata("PRODI", 20) + " | " + rata("FAKULTAS", 26) + " | " + rata("STATUS", 12))
        for nomor in range(len(urut)):
            d = urut[nomor]
            print(rata(str(nomor + 1), 4) + " | " + rata(d.get("Nama", "-"), 35) + " | " + rata(d.get("NIM", "-"), 15) + " | " + rata(d.get("Username", "-"), 14) + " | " + rata(d.get("Kelas", "-"), 6) + " | " + rata(d.get("Prodi", "-"), 20) + " | " + rata(d.get("Fakultas", "-"), 26) + " | " + rata(d.get("Status", "-"), 12))
    else:
        print(rata("NO", 4) + " | " + rata("NAMA", 35) + " | " + rata("NIM", 15) + " | " + rata("KELAS", 6) + " | " + rata("STATUS", 12))
        for nomor in range(len(urut)):
            d = urut[nomor]
            print(rata(str(nomor + 1), 4) + " | " + rata(d.get("Nama", "-"), 35) + " | " + rata(d.get("NIM", "-"), 15) + " | " + rata(d.get("Kelas", "-"), 6) + " | " + rata(d.get("Status", "-"), 12))

def lihat_data_mahasiswa_admin():
    semua = baca_csv("akun.csv")
    urut = urutkan_mahasiswa(semua)
    print("\nDATA MAHASISWA UNIDAY - SEMUA KELAS")
    tampilkan_mahasiswa(urut, True)
    print("Jumlah Mahasiswa: " + str(len(urut)))

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

def tandai_ada_perubahan():
    if len(notif_list) == 0:
        notif_list.append("ada")

def atur_jadwal_admin():
    while True:
        print("\n--- JADWAL KULIAH - ADMIN ---")
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
                print("\n-- " + hari.upper() + " --")
                while True:
                    matkul = input("Matkul (ketik 'skip' kalau libur): ")
                    if matkul == "skip" or matkul == "":
                        break
                    jam = input("Jam: ")
                    dosen = input("Dosen: ")
                    ruangan = input("Ruangan: ")
                    jadwal_list.append([kelas_admin, hari, matkul, jam, dosen, ruangan])
                    lagi = input("Ada jadwal lagi di " + hari + "? (y/n): ")
                    if lagi != "y":
                        break
            simpan_jadwal()
            tandai_ada_perubahan()
            print("Jadwal tersimpan!")
        elif pilih == "3":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            print("\n--- TAMBAH JADWAL BARU - KELAS " + kelas_admin + " ---")
            hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
            for nomor_hari in range(len(hari_list)):
                print(str(nomor_hari + 1) + ". " + hari_list[nomor_hari])
            nomor_hari = int(input("Nomor hari: ")) - 1
            if nomor_hari >= 0 and nomor_hari < len(hari_list):
                hari_pilih = hari_list[nomor_hari]
                matkul = input("Matkul baru: ")
                jam = input("Jam: ")
                dosen = input("Dosen: ")
                ruangan = input("Ruangan: ")
                if matkul != "" and jam != "":
                    jadwal_list.append([kelas_admin, hari_pilih, matkul, jam, dosen, ruangan])
                    simpan_jadwal()
                    tandai_ada_perubahan()
                    print("Berhasil ditambah! Jadwal lama tetap ada.")
                else:
                    print("Matkul dan jam jangan sampai kosong!")
            else:
                print("Nomor hari salah!")
        elif pilih == "4":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            cari = input("Cari matkul / dosen / ruangan: ")
            cari_dan_tampilkan_jadwal(kelas_admin, cari)
        elif pilih == "5":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            print("\n--- GANTI JADWAL - KELAS " + kelas_admin + " ---")
            target = pilih_jadwal_per_hari(kelas_admin)
            if target != None:
                print("Isi baru (kosongin / enter aja kalau gak mau diubah):")
                matkul_baru = input("Matkul baru [" + target[2] + "]: ")
                jam_baru = input("Jam baru [" + target[3] + "]: ")
                dosen_baru = input("Dosen baru [" + target[4] + "]: ")
                ruangan_baru = input("Ruangan baru [" + target[5] + "]: ")
                if matkul_baru != "":
                    target[2] = matkul_baru
                if jam_baru != "":
                    target[3] = jam_baru
                if dosen_baru != "":
                    target[4] = dosen_baru
                if ruangan_baru != "":
                    target[5] = ruangan_baru
                simpan_jadwal()
                tandai_ada_perubahan()
                print("Berhasil diganti!")
        elif pilih == "6":
            kelas_admin = pilih_kelas_jadwal()
            tampilkan_jadwal(kelas_admin)
            print("\n--- HAPUS JADWAL - KELAS " + kelas_admin + " ---")
            target = pilih_jadwal_per_hari(kelas_admin)
            if target != None:
                jadwal_list.remove(target)
                simpan_jadwal()
                tandai_ada_perubahan()
                print("Berhasil dihapus!")
        elif pilih == "7":
            break
        else:
            print("Pilihan tidak tersedia!")

def lihat_study_tracker_admin():
    print("\n===== STUDY TRACKER MAHASISWA (ADMIN LIHAT SAJA) =====")
    baca_data_tracker()
    semua_mhs = baca_csv("akun.csv")
    if len(semua_mhs) == 0:
        print("Belum ada mahasiswa.")
    else:
        for data_mhs in semua_mhs:
            tampilkan_tracker_1_orang(data_mhs.get("Nama", "-"))

def keluarkan_mahasiswa_admin():
    semua = baca_csv("akun.csv")
    urut = urutkan_mahasiswa(semua)
    if len(urut) == 0:
        print("Belum ada mahasiswa.")
        return
    print("\nKELUARKAN MAHASISWA")
    tampilkan_mahasiswa(urut, False)
    pilih = int(input("Pilih nomor mahasiswa yang dikeluarkan: ")) - 1
    if pilih >= 0 and pilih < len(urut):
        nama_keluar = urut[pilih].get("Nama")
        urut[pilih]["Status"] = "Dikeluarkan"
        tulis_csv("akun.csv", ["Nama", "NIM", "Username", "Password", "Prodi", "Fakultas", "Kelas", "Status"], semua)
        print("\n" + str(nama_keluar) + " berhasil dikeluarkan! Dia tidak bisa login lagi.")
    else:
        print("Nomor tidak ditemukan.")

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
            lihat_data_mahasiswa_admin()
        elif pilihan == "2":
            atur_jadwal_admin()
        elif pilihan == "3":
            lihat_study_tracker_admin()
        elif pilihan == "4":
            keluarkan_mahasiswa_admin()
        elif pilihan == "5":
            print("Admin berhasil logout!")
            break
        else:
            print("Pilihan tidak tersedia!")

def login_admin():
    print("\n===== LOGIN ADMIN =====")
    username = input("Masukkan username admin: ")
    password = input("Masukkan password admin: ")
    semua = baca_csv("admin.csv")
    if len(semua) == 0:
        print("Data admin tidak ditemukan. Cek file admin.csv!")
        return
    for data in semua:
        if data.get("Username") == username and data.get("Password") == password:
            print("\nLogin admin berhasil!")
            menu_admin()
            return
    print("\nUsername atau password admin salah!")

# 8. MENU UTAMA
def menu_utama():
    while True:
        print("\n" + "=" * 36)
        print(tengah("UNIDAY", 36))
        print(tengah("UNIVERSITY DAILY ACTIVITY", 36))
        print("=" * 36)
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