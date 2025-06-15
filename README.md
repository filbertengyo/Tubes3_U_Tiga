# Deskripsi Singkat Program

Pemanfaatan Pattern Matching untuk Membangun Sistem ATS (Applicant Tracking System) Berbasis CV Digital. Aplikasi sistem ATS yang dapat melakukan deteksi informasi pelamar berbasis dokumen CV digital. Metode yang akan digunakan untuk melakukan deteksi pola dalam CV adalah Boyer-Moore dan Knuth-Morris-Pratt. Selain itu, sistem ini dihubungkan dengan identitas kandidat melalui basis data sehingga terbentuk sebuah sistem yang dapat mengenali profil pelamar secara lengkap hanya dengan menggunakan CV digital.

## Requirement Program

Untuk menjalankan program, diperlukan hal-hal berikut:

`Python 3.8`

`Terminal atau Bash`

`UV`


## Cara Menjalankan Program



Clone repository github

```bash
  git clone https://github.com/filbertengyo/Tubes3_U_Tiga
```

Pindah Direktori

```bash
  cd src
```
Setup uv virtual enviroment

```bash
  uv python install
```

Jalankan docker untuk MySql

```bash
  docker compose up
```
Jalankan Program

```bash
  uv run main.py
```
## Identitas Pembuat

1. Kenneth Ricardo Chandra    | 13523022
2. Muhammad Kinan Arkansyadd  | 13523152
3. Filbert Engyo              | 13523163
