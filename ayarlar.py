"""
ayarlar.py — Kontrol Paneli
----------------------------
Şifreler, hangi yapay zekânın kullanılacağı, veritabanı dosyasının adı gibi
TÜM ayarlar tek bir yerde toplanır. Kodun içinde kaybolmadan buradan ayarlarsınız.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki gizli ayarları oku


class Ayarlar:
    """Ortak (hem geliştirme hem üretimde geçerli) ayarlar."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan-sifre-DEGISTIRIN')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'akilli_satis.db')

    # --- Yapay Zekâ Ayarları ---
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')  # groq / gemini / openai
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

    # Yapay zekânın kişiliği / rolü. Bunu firmanıza göre özgürce değiştirin.
    BUSINESS_CONTEXT = os.environ.get(
        'BUSINESS_CONTEXT',
        "Sen TechDrone Systems firmasının satış asistanısın. Kibar, profesyonel ve "
        "kısa cevaplar ver. Ziyaretçiyi ürünler hakkında bilgilendir ve mümkünse "
        "demo talebi bırakmaya yönlendir. Sadece Türkçe konuş."
    )

    # Wix gibi dış sitelerin sunucuya bağlanabilmesi için izin verilen adresler.
    # Geliştirmede '*' (herkese açık) kullanılabilir; üretimde kendi Wix adresinizle
    # değiştirin, örn: "https://siteniz.wixsite.com"
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '*')


class GelistirmeAyarlari(Ayarlar):
    """Kendi bilgisayarınızda test ederken kullanılır. Hatalar detaylı gösterilir."""
    DEBUG = True


class UretimAyarlari(Ayarlar):
    """Site internette (Render vb.) yayındayken kullanılır. Hatalar gizlenir."""
    DEBUG = False


# uygulama/__init__.py bu sözlükten doğru ayar sınıfını seçer.
ayar_secici = {
    'gelistirme': GelistirmeAyarlari,
    'uretim': UretimAyarlari,
}
