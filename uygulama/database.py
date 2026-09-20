"""
uygulama/database.py — Arşiv Memuru
-------------------------------------
Veritabanıyla ilgili HER işlem yalnızca bu dosyada yapılır (Repository Pattern).
İki temel iş: yeni müşteri kaydetmek ve tüm kayıtları geri getirmek.
"""

import sqlite3
from flask import current_app, g


def baglanti_al():
    """Veritabanı dosyasına bağlanır. Aynı istek içinde tekrar tekrar açmaz (g nesnesi)."""
    if 'db' not in g:
        veritabani_yolu = current_app.config.get('DATABASE_URL', 'akilli_satis.db')
        g.db = sqlite3.connect(veritabani_yolu)
        g.db.row_factory = sqlite3.Row
    return g.db


def veritabani_baslat(uygulama):
    """Tablo yoksa oluşturur (ilk açılışta çalışır)."""
    with uygulama.app_context():
        baglanti = sqlite3.connect(uygulama.config.get('DATABASE_URL', 'akilli_satis.db'))
        imlec = baglanti.cursor()
        imlec.execute('''
            CREATE TABLE IF NOT EXISTS musteri_adaylari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                olusturulma_tarihi TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        baglanti.commit()
        baglanti.close()


def musteri_adayi_ekle(isim, telefon, mesaj):
    """Yeni bir müşteri adayını arşive ekler. Form gönderildiğinde çalışır."""
    baglanti = baglanti_al()
    imlec = baglanti.cursor()
    # '?' yer tutucuları: bilgiler doğrudan metne yapıştırılmaz, SQL Injection önlenir.
    imlec.execute(
        'INSERT INTO musteri_adaylari (isim, telefon, mesaj) VALUES (?, ?, ?)',
        (isim, telefon, mesaj)
    )
    baglanti.commit()
    return imlec.lastrowid


def tum_adaylari_getir():
    """Tüm müşteri adaylarını en yeniden eskiye sıralı şekilde getirir."""
    baglanti = baglanti_al()
    imlec = baglanti.cursor()
    imlec.execute('SELECT * FROM musteri_adaylari ORDER BY olusturulma_tarihi DESC')
    satirlar = imlec.fetchall()
    return [dict(satir) for satir in satirlar]


def baglantiyi_kapat(e=None):
    """Her istek bittiğinde veritabanı bağlantısını temizler."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
