"""
uygulama/rotalar.py — Trafik Polisi
--------------------------------------
Gelen her isteğe bakar ve doğru yere yönlendirir. Kendisi yemek pişirmez
(yapay zekâ çalıştırmaz) veya arşivlemez (veritabanı işlemez); sadece yönlendirir.
"""

from flask import Blueprint, request, jsonify, render_template

from uygulama.database import musteri_adayi_ekle, tum_adaylari_getir
from uygulama.servisler.yapay_zeka_servisi import yapay_zeka_servisi, YapayZekaServisHatasi

# İki ayrı blueprint: biri API (JSON) adresleri için, biri sayfa (HTML) adresleri için.
api_arayuzu = Blueprint('api_arayuzu', __name__)
sayfa_arayuzu = Blueprint('sayfa_arayuzu', __name__)


# =====================================================================
# SAYFA ADRESLERİ (Flask kendi arayüzünüzü de sunabilir; Wix kullanıyorsanız
# bu iki adres sadece yerel test/demo amaçlıdır, Wix bunları kullanmaz.)
# =====================================================================

@sayfa_arayuzu.route('/')
def karsilama_sayfasi():
    """Karşılama sayfasını gösterir."""
    return render_template('index.html')


@sayfa_arayuzu.route('/panel')
def yonetim_paneli():
    """Yönetim panelini gösterir (yalnızca firma yetkilisi için)."""
    adaylar = tum_adaylari_getir()
    return render_template('dashboard.html', adaylar=adaylar)


# =====================================================================
# API ADRESLERİ — Wix Studio (Velo) buradan besleniyor
# =====================================================================

@api_arayuzu.route('/sohbet', methods=['POST'])
def sohbet_et():
    """
    Ziyaretçi soru sorduğunda çalışır.
    Beklenen gövde (JSON): { "mesaj": "...", "gecmis": [...] }
    Dönen gövde (JSON):    { "basari": true, "cevap": "..." }
    """
    veri = request.json or {}
    mesaj = veri.get('mesaj')
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj boş olamaz.'}), 400

    try:
        yanit = yapay_zeka_servisi.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'cevap': yanit})
    except YapayZekaServisHatasi as e:
        # Bir sorun olursa program çökmez, kibar bir hata döner.
        return jsonify({'basari': False, 'hata': str(e)}), 503


@api_arayuzu.route('/adaylar', methods=['POST'])
def musteri_kaydet():
    """
    Ziyaretçi iletişim formunu gönderdiğinde çalışır.
    Beklenen gövde (JSON): { "isim": "...", "telefon": "...", "mesaj": "..." }
    Dönen gövde (JSON):    { "basari": true, "mesaj": "..." }
    """
    veri = request.json or {}
    isim = (veri.get('isim') or '').strip()
    telefon = (veri.get('telefon') or '').strip()
    mesaj = (veri.get('mesaj') or '').strip()

    if not isim or not telefon:
        return jsonify({'basari': False, 'mesaj': 'İsim ve telefon zorunludur.'}), 400

    musteri_adayi_ekle(isim, telefon, mesaj)
    return jsonify({'basari': True, 'mesaj': 'Kaydınız alındı, teşekkürler!'})


@api_arayuzu.route('/adaylar', methods=['GET'])
def musteri_listele():
    """
    Yönetim panelindeki tabloyu (veya Wix Repeater'ı) besler.
    Dönen gövde (JSON): { "basari": true, "toplam": N, "adaylar": [...] }
    """
    adaylar = tum_adaylari_getir()
    return jsonify({'basari': True, 'toplam': len(adaylar), 'adaylar': adaylar})


@sayfa_arayuzu.route('/saglik-durumu', methods=['GET'])
def saglik_durumu():
    """Sunucu ayakta mı diye kontrol etmek için basit bir uç nokta."""
    return jsonify({'durum': 'calisiyor'})
