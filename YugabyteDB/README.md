# Pengerjaan Soal 1: Setup Docker + YugabyteDB di WSL Debian
## Bagian A: Persiapan WSL
### 1. Update sistem Debian
<img width="1037" height="662" alt="gambar" src="https://github.com/user-attachments/assets/3e63b5d1-0fcd-4d37-9c64-765345b0bffe" />

**Penjelasan**: Perintah ini memastikan seluruh paket di sistem WSL Debian dalam kondisi terbaru sebelum instalasi Docker dimulai. Langkah ini penting supaya tidak terjadi konflik dependency saat instalasi Docker berlangsung.

### 2. Install paket pendukung
<img width="1034" height="665" alt="gambar" src="https://github.com/user-attachments/assets/6eb13743-e49a-46d8-81dd-c40fb60df382" />

**Penjelasan**: Paket-paket ini dibutuhkan agar sistem bisa mengunduh dan memverifikasi paket Docker secara aman melalui HTTPS dan repository resmi Docker.

---

## Bagian B: Instalasi Docker Engine
### 3. Tambahkan GPG key resmi Docker
<img width="1038" height="192" alt="gambar" src="https://github.com/user-attachments/assets/0921859f-be3b-4912-bfe5-82f32e36a799" />

**Penjelasan**: GPG key ini digunakan sistem untuk memverifikasi bahwa paket Docker yang diunduh benar-benar berasal dari sumber resmi, bukan paket yang dimodifikasi pihak ketiga.

### 4. Tambahkan repository Docker
<img width="1037" height="123" alt="gambar" src="https://github.com/user-attachments/assets/50a920dd-8601-4f76-8ef9-c3dd947f23e5" />

**Penjelasan**: Baris ini mendaftarkan repository resmi Docker ke daftar sumber paket sistem, sehingga apt bisa menemukan dan mengunduh paket Docker.

### 5. Install Docker Engine
<img width="1035" height="679" alt="gambar" src="https://github.com/user-attachments/assets/9154b82b-9806-4746-a8a4-b2f03c758831" />

**Penjelasan**: Perintah ini menginstal Docker Engine beserta plugin pendukung seperti Docker Compose, yang nantinya berguna jika ingin menjalankan multi-container.

### 6. Jalankan Docker service
<img width="1034" height="162" alt="gambar" src="https://github.com/user-attachments/assets/2ffc484e-0394-44a5-bcda-31f4f81a0ccd" />

**Penjelasan**: WSL tidak menggunakan systemd secara default, sehingga Docker daemon perlu dijalankan manual dengan service alih-alih systemctl.

### 7. Verifikasi instalasi Docker
<img width="1037" height="487" alt="gambar" src="https://github.com/user-attachments/assets/0187e5ad-9483-4093-974a-51c4424ea8b8" />

**Penjelasan**: Perintah ini menjadi bukti bahwa Docker Engine sudah berjalan dengan benar. Jika berhasil, akan muncul pesan konfirmasi dari image hello-world yang diunduh dan dijalankan.

---

## Bagian C: Menjalankan YugabyteDB via Docker
### 9. Tarik image YugabyteDB
<img width="1035" height="398" alt="gambar" src="https://github.com/user-attachments/assets/7db92a35-00e9-455e-8db1-391f9291f89d" />

**Penjelasan**: Perintah ini mengunduh image resmi YugabyteDB dari Docker Hub ke lokal, sebagai dasar untuk membuat container.

### 10. Jalankan container YugabyteDB
<img width="1037" height="224" alt="gambar" src="https://github.com/user-attachments/assets/89a0bc20-ab50-495d-b70e-316449d73ebf" />

**Penjelasan**:
* Port 7000 digunakan untuk YugabyteDB Master UI.
* Port 9000 digunakan untuk TServer UI.
* Port 5433 merupakan port YSQL (kompatibel PostgreSQL), yang akan dipakai untuk koneksi ysqlsh maupun REST API di Soal 2.
* Port 9042 digunakan untuk YCQL (opsional, tidak wajib dipakai di tugas ini).
* Flag -d menjalankan container di background (detached mode), sehingga terminal tetap bisa dipakai untuk perintah lain.

### 11. Cek status container
<img width="1031" height="172" alt="gambar" src="https://github.com/user-attachments/assets/2febeb13-0317-4485-a761-63306ee4014a" />

**Penjelasan**: Perintah ini menampilkan daftar container yang sedang berjalan, sebagai konfirmasi awal bahwa container YugabyteDB aktif dan port sudah ter-mapping dengan benar.

### 12. Cek log startup YugabyteDB (opsional, untuk troubleshooting)
<img width="1032" height="148" alt="gambar" src="https://github.com/user-attachments/assets/84ce0494-90b2-40ff-b1e4-eeeafded51b3" />

**Penjelasan**: Log ini berguna untuk memastikan proses yugabyted benar-benar sudah selesai inisialisasi sebelum mencoba koneksi ke database.

---

## Bagian D: Membuat Tabel dan Mengisi Data via ysqlsh
### 13. Masuk ke ysqlsh dari dalam container
<img width="1036" height="145" alt="gambar" src="https://github.com/user-attachments/assets/e9a7c92a-0828-48c5-a575-d43f7a023e4f" />

**Penjelasan**: Perintah bash -c 'bin/ysqlsh -h $(hostname) -U yugabyte -d yugabyte' berhasil karena $(hostname) dijalankan di dalam container saat itu juga, sehingga otomatis mengambil hostname container yang sedang aktif (sama seperti ID container yang muncul di docker ps atau yugabyted status) — tanpa perlu diketik manual. Karena YSQL server di image ini memang bind ke hostname container (bukan ke localhost), maka koneksi berhasil dan langsung masuk ke prompt yugabyte=#

### 14. Buat tabel pertama (contoh: mahasiswa)
<img width="1032" height="189" alt="gambar" src="https://github.com/user-attachments/assets/d833a3bf-4990-4c48-811f-2f3a7659b43f" />

**Penjelasan**: Query ini membentuk struktur tabel dengan 4 kolom, di mana id sebagai primary key yang otomatis bertambah nilainya (SERIAL).

### 15. Isi 5 data ke tabel mahasiswa
<img width="1033" height="196" alt="gambar" src="https://github.com/user-attachments/assets/e979111c-12c4-415c-ab34-0e53501a766e" />

**Penjelasan**: Query ini memasukkan 5 baris data ke tabel mahasiswa sekaligus dalam satu perintah INSERT.

### 16. Buat tabel kedua (contoh: matakuliah)
<img width="1029" height="166" alt="gambar" src="https://github.com/user-attachments/assets/1b9b9e52-a684-4480-95f1-558d73981912" />

**Penjelasan**: Tabel kedua ini independen dari tabel pertama, sesuai instruksi soal yang meminta 2 tabel dengan nama dan kolom bebas.

### 17. Isi 5 data ke tabel matakuliah
<img width="1037" height="169" alt="gambar" src="https://github.com/user-attachments/assets/f0db48d7-1a9e-4e0c-a99c-36f6c4336a4a" />

### 18. Bukti pembuatan tabel dan data
<img width="1032" height="298" alt="gambar" src="https://github.com/user-attachments/assets/3721d5db-30e0-4769-91f7-36e364d257a8" />

**Penjelasan**:
* \dt menampilkan daftar seluruh tabel yang ada di database sebagai bukti kedua tabel berhasil dibuat.
* SELECT * FROM ... menampilkan seluruh isi data di masing-masing tabel sebagai bukti data berhasil diisikan.

### 19. Keluar dari ysqlsh
<img width="1030" height="211" alt="gambar" src="https://github.com/user-attachments/assets/32fb6824-156f-43b1-ae22-6486b9ba69e7" />

---

## Bagian E: Verifikasi Alternatif via YugabyteDB UI
### 20. Buka browser dan akses UI
<img width="1366" height="684" alt="gambar" src="https://github.com/user-attachments/assets/6cfbc09e-825d-49f1-97ee-fd9c244cdf72" />
<img width="1217" height="644" alt="gambar" src="https://github.com/user-attachments/assets/7c26627b-1bbb-4201-bb10-a97ad6b19f51" />

**Penjelasan**: Alamat ini membuka YugabyteDB Master UI, tempat status cluster, node, dan tablet bisa dipantau secara visual sebagai bukti tambahan bahwa instance YugabyteDB berjalan normal.











