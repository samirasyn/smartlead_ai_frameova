"""
baslat.py — "Aç" Düğmesi
-------------------------
Bu dosyanın tek görevi programı fabrikadan (uygulama_olustur) almak ve çalıştırmak.
Karmaşık mantık burada YOKTUR; sadece programı uyandırır.
Çalıştırmak için: python baslat.py
"""

import os
from uygulama import uygulama_olustur

# Hazır programı fabrikadan al.
# FLASK_ORTAMI .env dosyasında 'uretim' ise UretimAyarlari, aksi halde GelistirmeAyarlari kullanılır.
uygulama = uygulama_olustur(os.environ.get('FLASK_ORTAMI', 'gelistirme'))

if __name__ == '__main__':
    # Sadece 'python baslat.py' yazınca çalışır.
    # host='0.0.0.0' -> aynı ağdaki telefon/tabletten de erişilebilsin diye
    # port=5000      -> program bilgisayarın 5000 numaralı kapısında dinler
    # debug=True     -> hata olunca detay göster (SADECE geliştirmede kullanın)
    debug_modu = os.environ.get('FLASK_ORTAMI', 'gelistirme') != 'uretim'
    uygulama.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_modu)
