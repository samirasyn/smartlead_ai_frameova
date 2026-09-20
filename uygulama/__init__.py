"""
uygulama/__init__.py — Montaj Hattı
-------------------------------------
Tek tek parçaları (ayarlar, veritabanı, adresler, CORS) alır, hepsini bir araya
getirir ve çalışan bütün bir Flask programı üretir.
"""

from flask import Flask
from flask_cors import CORS

from ayarlar import ayar_secici
from uygulama.database import veritabani_baslat, baglantiyi_kapat


def uygulama_olustur(ayar_adi=None):
    uygulama = Flask(__name__, template_folder='sablonlar')

    # 1) Ayarları yükle (geliştirme mi, üretim mi?)
    secilen_ayar = ayar_secici.get(ayar_adi, ayar_secici['gelistirme'])
    uygulama.config.from_object(secilen_ayar)

    # 2) Dış sitelerin (Wix Studio dahil) bağlanmasına izin ver (CORS)
    cors_izinleri = uygulama.config.get('CORS_ALLOWED_ORIGINS', '*')
    CORS(
        uygulama,
        origins=cors_izinleri,
        methods=['GET', 'POST', 'OPTIONS'],
        supports_credentials=False,
    )

    # 3) Veritabanı tablosunu hazırla (yoksa oluştur)
    with uygulama.app_context():
        veritabani_baslat(uygulama)

    # Her istek bittiğinde veritabanı bağlantısını otomatik kapat
    uygulama.teardown_appcontext(baglantiyi_kapat)

    # 4) Adresleri (rotaları) sisteme tanıt
    from uygulama.rotalar import api_arayuzu, sayfa_arayuzu
    uygulama.register_blueprint(api_arayuzu, url_prefix='/api')
    uygulama.register_blueprint(sayfa_arayuzu)

    return uygulama
