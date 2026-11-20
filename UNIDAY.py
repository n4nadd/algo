# =================================================
# UNIDAY - JADWAL KULIAH
# Aplikasi penjadwal kuliah Senin sampai Jumat
# Data disimpan di jadwal.txt
# Format data: Hari|Matkul|Jam|Dosen|Ruangan
# =================================================

is_jalan = True

# ===== LIST =====
# [Hari, Matkul, Jam, Dosen, Ruangan]
jadwal_list = []

# ===== FUNGSI MEMBACA SATU BARIS DATA =====
# Memisahkan data berdasarkan karakter "|"
def bongkar_baris(baris):
    hasil = ["", "", "", "", ""]
    pos = 0
    for i in range(len(baris)):
        h = baris[i]
        if h == "|":
            pos = pos + 1
        elif h == "\n":
            pass
        else:
            if pos < 5:
                hasil[pos] = hasil[pos] + h
    return hasil

# ===== FUNGSI INPUT NOMOR =====
# Memastikan input hanya angka dan dalam rentang yang ada
def input_nomor(pesan, maksimal):
    while True:
        teks = input(pesan)
        if teks == "":
            print("Harus input angka ya! Coba lagi.")
            continue
        ok = True
        for i in range(len(teks)):
            if teks[i] < "0" or teks[i] > "9":
                ok = False
        if ok == False:
            print("Harus input angka ya! Coba lagi.")
            continue
        angka = int(teks)
        if angka < 0 or angka >= maksimal:
            print("Nomor gak ada! Coba lagi.")
            continue
        return angka

# ===== FILE HANDLING: BACA jadwal.txt =====
try:
    file_buka = open("jadwal.txt", "r")
    for baris in file_buka:
        if baris == "" or baris == "\n":
            continue
        pisah = bongkar_baris(baris)
        if pisah[1] != "":
            jadwal_list.append(pisah)
    file_buka.close()
except:
    jadwal_list = []

# ===== FILE HANDLING: SIMPAN jadwal.txt =====
def simpan_semua():
    file_tulis = open("jadwal.txt", "w")
    for j in range(len(jadwal_list)):
        file_tulis.write(jadwal_list[j][0] + "|" + jadwal_list[j][1] + "|" + jadwal_list[j][2] + "|" + jadwal_list[j][3] + "|" + jadwal_list[j][4] + "\n")
    file_tulis.close()

print("===== JADWAL KULIAH KAMU =====")
if len(jadwal_list) == 0:
    print("Belum ada jadwal! Input dulu di menu 1.")
else:
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    for hari in hari_list:
        print("\n-- " + hari + " --")
        ada = False
        for j in range(len(jadwal_list)):
            if jadwal_list[j][0] == hari:
                print(jadwal_list[j][1] + " | " + jadwal_list[j][2] + " | " + jadwal_list[j][3] + " | " + jadwal_list[j][4])
                ada = True
        if not ada:
            print("(Libur / Kosong)")

# ===== MENU UTAMA =====
while is_jalan:
    print("\n===== MENU UTAMA =====")
    print("1. Jadwal Kuliah")
    print("2. Catatan Matkul")
    print("3. To Do List")
    print("4. Study Tracker")
    print("5. Keluar")
    print("6. Hapus Akun / Reset Dari Nol")
    pilih = input("Pilih: ")

    # ---------- 1. JADWAL KULIAH ----------
    if pilih == "1":
        while True:
            print("\n--- JADWAL KULIAH ---")
            print("1. Tampilkan Jadwal")
            print("2. Masukkan Jadwal (Senin-Jumat)")
            print("3. Tambah Jadwal (Baru/Pindahan)")
            print("4. Cari Jadwal")
            print("5. Ubah Jadwal")
            print("6. Hapus Jadwal")
            print("7. Kembali")
            p = input("Pilih: ")

            if p == "1":
                hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
                for hari in hari_list:
                    print("\n-- " + hari + " --")
                    ada = False
                    for j in range(len(jadwal_list)):
                        if jadwal_list[j][0] == hari:
                            print(str(j) + ". " + jadwal_list[j][1] + " | " + jadwal_list[j][2] + " | " + jadwal_list[j][3] + " | " + jadwal_list[j][4])
                            ada = True
                    if not ada:
                        print("(Kosong)")

            elif p == "2":
                hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
                for hari in hari_list:
                    print("\n== " + hari + " ==")
                    while True:
                        matkul = input("Matkul (ketik 'skip' kalau libur): ")
                        if matkul.lower() == "skip" or matkul == "":
                            break
                        jam = input("Jam: ")
                        dosen = input("Dosen: ")
                        ruangan = input("Ruangan: ")
                        jadwal_list.append([hari, matkul, jam, dosen, ruangan])
                        lagi = input("Ada jadwal lagi di " + hari + "? (y/n): ")
                        if not (lagi.lower() == "y"):
                            break
                simpan_semua()
                print("Jadwal tersimpan!")

            elif p == "3":
                print("\n--- TAMBAH JADWAL BARU ---")
                hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
                for h in range(len(hari_list)):
                    print(str(h) + ". " + hari_list[h])
                nomor_hari = int(input("Nomor hari: "))
                if nomor_hari >= 0 and nomor_hari < len(hari_list):
                    hari_pilih = hari_list[nomor_hari]
                    print("\nJadwal yang udah ada di " + hari_pilih + ":")
                    ada = False
                    for j in range(len(jadwal_list)):
                        if jadwal_list[j][0] == hari_pilih:
                            print("- " + jadwal_list[j][1] + " | " + jadwal_list[j][2] + " | " + jadwal_list[j][3] + " | " + jadwal_list[j][4])
                            ada = True
                    if not ada:
                        print("(Masih kosong)")
                    print("\nIsi jadwal baru:")
                    matkul = input("Matkul baru: ")
                    jam = input("Jam: ")
                    dosen = input("Dosen: ")
                    ruangan = input("Ruangan: ")
                    if matkul != "" and jam != "":
                        jadwal_list.append([hari_pilih, matkul, jam, dosen, ruangan])
                        simpan_semua()
                        print("Berhasil ditambah! Jadwal lama tetap ada.")
                    else:
                        print("Matkul dan jam jangan sampai kosong!")
                else:
                    print("Nomor hari salah!")

            elif p == "4":
                cari = input("Cari matkul / dosen / ruangan: ")
                cari_kecil = cari.lower()
                ketemu = False
                for j in range(len(jadwal_list)):
                    matkul_kecil = jadwal_list[j][1].lower()
                    dosen_kecil = jadwal_list[j][3].lower()
                    ruangan_kecil = jadwal_list[j][4].lower()
                    if cari_kecil in matkul_kecil or cari_kecil in dosen_kecil or cari_kecil in ruangan_kecil:
                        print(jadwal_list[j][0] + " - " + jadwal_list[j][1] + " - " + jadwal_list[j][2] + " - " + jadwal_list[j][3] + " - " + jadwal_list[j][4])
                        ditemukan = True
                if not ditemukan:
                    print("Gak ketemu!")

            elif p == "5":
                for j in range(len(jadwal_list)):
                    print(str(j) + ". " + jadwal_list[j][0] + " - " + jadwal_list[j][1] + " | " + jadwal_list[j][2] + " | " + jadwal_list[j][3] + " | " + jadwal_list[j][4])
                nomor = int(input("Nomor yang mau diubah: "))
                if nomor >= 0 and nomor < len(jadwal_list):
                    print("Isi baru (kosongin / enter aja kalau gak mau diubah):")
                    matkul_baru = input("Matkul baru [" + jadwal_list[nomor][1] + "]: ")
                    jam_baru = input("Jam baru [" + jadwal_list[nomor][2] + "]: ")
                    dosen_baru = input("Dosen baru [" + jadwal_list[nomor][3] + "]: ")
                    ruangan_baru = input("Ruangan baru [" + jadwal_list[nomor][4] + "]: ")
                    if matkul_baru != "":
                        jadwal_list[nomor][1] = matkul_baru
                    if jam_baru != "":
                        jadwal_list[nomor][2] = jam_baru
                    if dosen_baru != "":
                        jadwal_list[nomor][3] = dosen_baru
                    if ruangan_baru != "":
                        jadwal_list[nomor][4] = ruangan_baru
                    simpan_semua()
                    print("Berhasil diubah!")
                else:
                    print("Nomor salah!")

            elif p == "6":
                for j in range(len(jadwal_list)):
                    print(str(j) + ". " + jadwal_list[j][0] + " - " + jadwal_list[j][1])
                nomor = int(input("Nomor yang mau dihapus: "))
                if nomor >= 0 and nomor < len(jadwal_list):
                    jadwal_list.pop(nomor)
                    simpan_semua()
                    print("Berhasil dihapus!")
            elif p == "7":
                break