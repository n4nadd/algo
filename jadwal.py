jadwal_list = []
notif_list = []

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

# TAMPILKAN JADWAL
def tampilkan_jadwal(kelas_pilih):
    print("\n===== JADWAL KULIAH - KELAS " + kelas_pilih + " =====")
    print("NO | HARI | MATA KULIAH | JAM | DOSEN | RUANGAN")
    print("-" * 70)
    ada_jadwal = False
    for nomor in range(len(jadwal_list)):
        if jadwal_list[nomor][0] == kelas_pilih:
            print(str(nomor + 1) + ". " + jadwal_list[nomor][1] + " | " + jadwal_list[nomor][2] + " | " + jadwal_list[nomor][3] + " | " + jadwal_list[nomor][4] + " | " + jadwal_list[nomor][5])
            ada_jadwal = True
    if not ada_jadwal:
        print("Belum ada jadwal! Tunggu admin input.")

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

# JALANKAN - TANYA KELAS DULU
print("===== JADWAL KULIAH MAHASISWA =====")
kelas = ""
while kelas != "A" and kelas != "B" and kelas != "C":
    kelas = input("Masukkan Kelas kamu (A/B/C): ")
    if kelas != "A" and kelas != "B" and kelas != "C":
        print("Pilih A, B, atau C aja!")

jadwal_kuliah_mahasiswa(kelas)
print("Terima kasih!")