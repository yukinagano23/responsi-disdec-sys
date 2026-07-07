# Soal 3: Mekanisme Konsensus Blockchain L1: Ethereum (Proof of Stake)
### Pemilihan Blockchain
Blockchain L1 yang dipilih adalah **Ethereum**, dengan mekanisme konsensus **Proof of Stake (PoS)**, tepatnya implementasi bernama **Gasper**, gabungan dari dua protokol yaitu **Casper FFG (Friendly Finality Gadget)** dan **LMD-GHOST (Latest Message Driven Greediest Heaviest Observed SubTree)**. Mekanisme ini mulai digunakan penuh sejak peristiwa "The Merge" pada September 2022, menggantikan Proof of Work yang dipakai sebelumnya.

### Penjelasan Mekanisme Konsensus
#### 1. Konsep Dasar Proof of Stake
Berbeda dengan Proof of Work (dipakai Bitcoin) yang mengandalkan kekuatan komputasi (hashing power) untuk menentukan siapa berhak menambahkan blok baru, Proof of Stake mengandalkan **jumlah aset yang dikunci (staked)** oleh validator sebagai jaminan. Setiap validator di Ethereum wajib mengunci minimal **32 ETH** untuk bisa berpartisipasi. Semakin besar stake yang dikunci, semakin besar pula peluang validator terpilih untuk mengusulkan atau memvalidasi blok, namun stake ini juga menjadi jaminan yang bisa dipotong (slashing) jika validator terbukti berlaku curang.

#### 2. Pembagian Waktu: Slot dan Epoch
Ethereum PoS membagi waktu ke dalam satuan bernama **slot** (setiap slot berdurasi 12 detik) dan **epoch** (kumpulan dari 32 slot, sekitar 6,4 menit). Pada setiap slot, satu validator dipilih secara acak (namun berbobot sesuai stake) sebagai **block proposer** yang bertugas mengusulkan blok baru, sementara sekelompok validator lain bertindak sebagai attester yang bertugas memberi suara (vote) untuk mengonfirmasi validitas blok tersebut.

#### 3. Cara Kerja LMD-GHOST (Pemilihan Fork/Cabang)
Dalam kondisi jaringan yang terdesentralisasi, terkadang muncul lebih dari satu cabang (fork) blok pada waktu bersamaan. LMD-GHOST bertugas menentukan cabang mana yang dianggap sebagai **cabang utama (canonical chain)**, dengan cara memilih cabang yang memiliki **bobot suara terbanyak** dari validator, berdasarkan **pesan/vote terbaru (latest message)** dari tiap validator. Prinsip "greediest heaviest subtree" berarti algoritma ini selalu memilih cabang dengan akumulasi dukungan terbesar di setiap percabangan, bukan sekadar cabang terpanjang.

#### 4. Cara Kerja Casper FFG (Finalitas)
Casper FFG bertugas memberi status **"final"** pada blok-blok tertentu, sehingga blok yang sudah final tidak bisa lagi diubah atau di-revert, berbeda dengan mekanisme PoW yang secara teori masih bisa mengalami reorganisasi rantai meski probabilitasnya sangat kecil. Proses finalisasi bekerja per epoch: jika lebih dari **dua pertiga (66,7%) total stake** yang aktif memberi vote yang konsisten pada dua epoch berturut-turut (disebut proses **justification** lalu **finalization**), maka blok pada epoch tersebut dianggap final secara permanen.

#### 5. Mekanisme Slashing dan Insentif
Untuk menjaga kejujuran validator, Ethereum menerapkan sistem **reward dan penalti**. Validator yang aktif dan jujur dalam mengusulkan blok serta memberi vote akan mendapat imbalan berupa ETH baru. Sebaliknya, validator yang terbukti melakukan tindakan curang, seperti mengusulkan dua blok berbeda pada slot yang sama (equivocation) atau memberi vote yang saling bertentangan (double voting), akan dikenai **slashing**, yaitu sebagian stake-nya dipotong paksa dan validator tersebut dikeluarkan dari jaringan.

### Diagram Mekanisme Konsensus
<img width="4272" height="3040" alt="diagram_etherum" src="https://github.com/user-attachments/assets/ddd0af37-55dc-44f1-801a-d2f335c211ba" />

### Ringkasan Alur pada Diagram
Diagram di atas menggambarkan siklus lengkap mekanisme konsensus Gasper pada Ethereum, dimulai dari level **slot** (pemilihan proposer, pengusulan blok, proses attestation dengan LMD-GHOST), lalu naik ke level **epoch** (proses justification dan finalization oleh Casper FFG), hingga akhirnya blok mencapai status **final** dan tidak bisa direvert. Jalur slashing ditampilkan sebagai konsekuensi bagi validator yang melakukan tindakan curang selama proses ini berlangsung.

### Pembahasan Tambahan
* **Perbandingan singkat dengan Proof of Work**: PoS pada Ethereum jauh lebih hemat energi dibanding PoW (diperkirakan penurunan konsumsi energi lebih dari 99% setelah The Merge), karena tidak lagi bergantung pada komputasi hashing yang intensif, melainkan pada penguncian aset sebagai jaminan.
* **Trade-off**: PoS memberi finalitas yang lebih cepat dan pasti dibanding PoW yang hanya mengandalkan probabilitas (semakin banyak konfirmasi blok, semakin kecil kemungkinan di-revert), namun PoS memerlukan mekanisme tambahan seperti slashing untuk mencegah masalah "nothing at stake" (potensi validator memvalidasi banyak fork sekaligus tanpa risiko, karena tidak ada biaya komputasi seperti pada PoW).



