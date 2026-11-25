
import csv
import os

# =====================================
# STUDY TRACKER - UNIDAY
# =====================================

nilai_list = []
ipk_list = []

FILE_CSV = "Study Tracker.csv"

# =====================================
# MEMBACA DATA CSV
# =====================================

def baca_data():
    global nilai_list, ipk_list

    if os.path.exists(FILE_CSV):
        with open(FILE_CSV, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for data in reader:
                if len(data) == 5:

                    if data[0] == "Nilai":
                        nilai_list.append([
                            data[1],
                            float(data[2]),
                            float(data[3]),
                            float(data[4])
                        ])

                    elif data[0] == "IPK":
                        ipk_list.append([
                            data[1],
                            float(data[4])
                        ])

# =====================================
# MENYIMPAN DATA CSV
# =====================================

def simpan_semua():
    with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Jenis Data",
            "Mata Kuliah/Semester",
            "Kuis",
            "UTS",
            "UAS/IPK"
        ])

        for data in nilai_list:
            writer.writerow(["Nilai"] + data)

        for data in ipk_list:
            writer.writerow([
                "IPK",
                data[0],
                "-",
                "-",
                data[1]
            ])

# =====================================
# FUNGSI INPUT ANGKA
# =====================================

def input_angka(pesan, minimum, maksimum):
    while True:
        try:
            angka = float(input(pesan))

            if minimum <= angka <= maksimum:
                return angka
            else:
                print("Input harus antara", minimum, "sampai", maksimum)

        except ValueError:
            print("Masukkan angka yang valid!")

# =====================================
# STUDY TRACKER
# =====================================

def study_tracker():
    while True:
        print("\n========== STUDY TRACKER ==========")
        print("1. Lihat Nilai & IPK")
        print("2. Input Nilai (Kuis, UTS, UAS)")
        print("3. Input IPK (Input Sendiri)")
        print("4. Ubah Nilai")
        print("5. Hapus Nilai")
        print("6. Kembali")

        pilih = input("Pilih menu: ")

        # 1. LIHAT NILAI DAN IPK
        if pilih == "1":
            print("\n========== NILAI MAHASISWA ==========")

            if len(nilai_list) == 0:
                print("Belum ada nilai!")
            else:
                for n in range(len(nilai_list)):
                    matkul = nilai_list[n][0]
                    kuis = nilai_list[n][1]
                    uts = nilai_list[n][2]
                    uas = nilai_list[n][3]

                    akhir = (kuis * 0.2) + (uts * 0.3) + (uas * 0.5)

                    if akhir >= 80:
                        huruf = "A"
                    elif akhir >= 70:
                        huruf = "B"
                    elif akhir >= 60:
                        huruf = "C"
                    elif akhir >= 50:
                        huruf = "D"
                    else:
                        huruf = "E"

                    print(
                        matkul,
                        "| Kuis:", kuis,
                        "| UTS:", uts,
                        "| UAS:", uas,
                        "| Nilai Akhir:", round(akhir, 2),
                        "| Huruf:", huruf
                    )

            print("\n========== RIWAYAT IPK ==========")

            if len(ipk_list) == 0:
                print("Belum input IPK!")
            else:
                for i in range(len(ipk_list)):
                    semester = ipk_list[i][0]
                    ipk = ipk_list[i][1]

                    if ipk >= 3.5:
                        predikat = "Sangat Bagus / Cumlaude"
                    elif ipk >= 3.0:
                        predikat = "Bagus"
                    elif ipk >= 2.75:
                        predikat = "Normal / Cukup"
                    elif ipk >= 2.0:
                        predikat = "Kurang"
                    else:
                        predikat = "Sangat Kurang, Semangat!"

                    print(
                        "Semester", semester,
                        "| IPK:", ipk,
                        "|", predikat
                    )

        # 2. INPUT NILAI
        elif pilih == "2":
            matkul = input("Nama Mata Kuliah: ")

            kuis = input_angka("Nilai Kuis: ", 0, 100)
            uts = input_angka("Nilai UTS: ", 0, 100)
            uas = input_angka("Nilai UAS: ", 0, 100)

            nilai_list.append([matkul, kuis, uts, uas])

            simpan_semua()
            print("Nilai berhasil disimpan!")

        # 3. INPUT IPK
        elif pilih == "3":
            semester = input("Semester ke-berapa: ")
            ipk = input_angka("Masukkan IPK (0.00 - 4.00): ", 0, 4)

            ipk_list.append([semester, ipk])

            simpan_semua()
            print("IPK berhasil disimpan!")

        # 4. UBAH NILAI
        elif pilih == "4":
            if len(nilai_list) == 0:
                print("Belum ada nilai yang bisa diubah!")
            else:
                print("\nDaftar Mata Kuliah:")

                for n in range(len(nilai_list)):
                    print(n, ".", nilai_list[n][0])

                try:
                    nomor = int(input("Nomor yang mau diubah: "))

                    if 0 <= nomor < len(nilai_list):
                        nilai_list[nomor][1] = input_angka("Kuis baru: ", 0, 100)
                        nilai_list[nomor][2] = input_angka("UTS baru: ", 0, 100)
                        nilai_list[nomor][3] = input_angka("UAS baru: ", 0, 100)

                        simpan_semua()
                        print("Nilai berhasil diubah!")
                    else:
                        print("Nomor tidak ditemukan!")

                except ValueError:
                    print("Masukkan nomor yang valid!")

        # 5. HAPUS NILAI
        elif pilih == "5":
            if len(nilai_list) == 0:
                print("Belum ada nilai yang bisa dihapus!")
            else:
                print("\nDaftar Mata Kuliah:")

                for n in range(len(nilai_list)):
                    print(n, ".", nilai_list[n][0])

                try:
                    nomor = int(input("Nomor yang mau dihapus: "))

                    if 0 <= nomor < len(nilai_list):
                        nilai_list.pop(nomor)

                        simpan_semua()
                        print("Nilai berhasil dihapus!")
                    else:
                        print("Nomor tidak ditemukan!")

                except ValueError:
                    print("Masukkan nomor yang valid!")

        # 6. KEMBALI
        elif pilih == "6":
            print("Kembali ke menu utama...")
            break

        else:
            print("Pilihan tidak tersedia!")

# =====================================
# PROGRAM UTAMA
# =====================================

baca_data()
study_tracker()