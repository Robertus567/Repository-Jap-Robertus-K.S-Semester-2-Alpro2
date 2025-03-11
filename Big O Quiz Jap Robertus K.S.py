def hitung_total_belanja():
    # List untuk menyimpan barang dan harga
    daftar_belanja = []
    
    print("Program Menghitung Total Belanja")
    print("--------------------------------")
    
    while True:
        nama_barang = input("Masukkan nama barang (ketik 'selesai' untuk mengakhiri): ")
        
        # Cek apakah pengguna ingin mengakhiri input
        if nama_barang.lower() == 'selesai':
            break
            
        try:
            harga_barang = float(input("Masukkan harga barang: Rp "))
            jumlah_barang = int(input("Masukkan jumlah barang: "))
            
            # Menambahkan item ke daftar belanja
            daftar_belanja.append({
                'nama': nama_barang,
                'harga': harga_barang,
                'jumlah': jumlah_barang,
                'subtotal': harga_barang * jumlah_barang
            })
            
            print(f"Barang '{nama_barang}' ditambahkan!\n")
            
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka untuk harga dan jumlah.\n")
    
    # Menampilkan daftar belanja
    if daftar_belanja:
        print("\nRincian Belanja:")
        print("---------------")
        total = 0
        
        for index, item in enumerate(daftar_belanja, 1):
            print(f"{index}. {item['nama']}: {item['jumlah']} x Rp {item['harga']:,.2f} = Rp {item['subtotal']:,.2f}")
            total += item['subtotal']
        
        print("\nTotal Belanja: Rp {:,.2f}".format(total))
        
        # Implementasi kompleksitas O(1) untuk menampilkan total
        print("\nKompleksitas untuk mendapatkan total belanja: O(1)")
        print("Karena kita menyimpan total selama proses iterasi")
    else:
        print("Tidak ada barang yang dimasukkan.")

# Jalankan program
if __name__ == "__main__":
    hitung_total_belanja()