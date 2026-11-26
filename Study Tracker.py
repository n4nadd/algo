import csv

nilai_list = []
ipk_list = []

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

def tampilkan_tracker_1_orang(nama_tampil):
    print("\n========================================")
    print("NAMA MAHASISWA : " + nama_tampil)
    print("========================================")
    print("--- NILAI ---")
    ada_nilai = False
    hitung = 1
    for nomor in range(len(nilai_list)):
        if nilai_list[nomor][0] == nama_tampil or nilai_list[nomor][0] == "":
            matkul = nilai_list[nomor][1]
            kuis = nilai_list[nomor][2]
            uts = nilai_list[nomor][3]
            uas = nilai_list[nomor][4]
            akhir, huruf = hitung_nilai(kuis, uts, uas)
            print(str(hitung) + ". " + matkul + " | Kuis: " + str(kuis) + " | UTS: " + str(uts) + " | UAS: " + str(uas) + " | Nilai Akhir: " + str(round(akhir, 2)) + " | Huruf: " + huruf)
            ada_nilai = True
            hitung = hitung + 1
    if not ada_nilai:
        print("Belum ada nilai!")
    print("--- RIWAYAT IPK ---")
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

def study_tracker(nama):
    baca_data_tracker()
    while True:
        print("\n========== STUDY TRACKER - MAHASISWA ==========")
        print("Nama : " + nama)
        print("1. Lihat Nilai dan IPK Saya")
        print("2. Input Nilai")
        print("3. Input IPK")
        print("4. Ubah Nilai")
        print("5. Hapus Nilai")
        print("6. Keluar")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_tracker_1_orang(nama)
        elif pilih == "2":
            matkul = input("Nama Mata Kuliah: ")
            kuis = input_angka("Nilai Kuis: ", 0, 100)
            uts = input_angka("Nilai UTS: ", 0, 100)
            uas = input_angka("Nilai UAS: ", 0, 100)
            nilai_list.append([nama, matkul, kuis, uts, uas])
            simpan_tracker()
            print("Nilai berhasil disimpan!")
        elif pilih == "3":
            semester = input("Semester ke-berapa: ")
            ipk = input_angka("Masukkan IPK (0.00 - 4.00): ", 0, 4)
            ipk_list.append([nama, semester, ipk])
            simpan_tracker()
            print("IPK berhasil disimpan!")
        elif pilih == "4":
            daftar_saya = []
            for data in nilai_list:
                if data[0] == nama or data[0] == "":
                    daftar_saya.append(data)
            if len(daftar_saya) == 0:
                print("Belum ada nilai!")
            else:
                for nomor in range(len(daftar_saya)):
                    print(str(nomor + 1) + ". " + daftar_saya[nomor][1])
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
                except ValueError:
                    print("Masukkan nomor yang valid!")
        elif pilih == "5":
            daftar_saya = []
            for data in nilai_list:
                if data[0] == nama or data[0] == "":
                    daftar_saya.append(data)
            if len(daftar_saya) == 0:
                print("Belum ada nilai!")
            else:
                for nomor in range(len(daftar_saya)):
                    print(str(nomor + 1) + ". " + daftar_saya[nomor][1])
                try:
                    nomor_pilih = int(input("Nomor yang mau dihapus: ")) - 1
                    if nomor_pilih >= 0 and nomor_pilih < len(daftar_saya):
                        nilai_list.remove(daftar_saya[nomor_pilih])
                        simpan_tracker()
                        print("Nilai berhasil dihapus!")
                except ValueError:
                    print("Masukkan nomor yang valid!")
        elif pilih == "6":
            break
        else:
            print("Pilihan tidak tersedia!")

nama = input("Masukkan Nama: ")
study_tracker(nama)