# SmartLead AI — Kurulum Rehberi (Sıfırdan Başlayanlar İçin)

Bu proje, rehberdeki mimariye birebir uyar. Amaç: Wix Studio ile kurduğunuz
web sitesine bağlanacak bir **AI sohbet backend'i** çalıştırmak.

## 1) Bilgisayarınıza kurun

```bash
cd smartlead_ai
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r gereksinimler.txt
```

## 2) API anahtarınızı alın (ücretsiz, önerilen: Groq)

1. https://console.groq.com adresine gidin, Google hesabınızla giriş yapın.
2. Sol menüden **API Keys** > **Create API Key**.
3. `gsk_...` ile başlayan anahtarı kopyalayın (bir daha gösterilmez).

## 3) .env dosyasını oluşturun

`.env.example` dosyasını kopyalayıp `.env` olarak kaydedin, içine anahtarınızı yapıştırın:

```bash
cp .env.example .env   # Windows'ta: copy .env.example .env
```

`.env` içinde `GROQ_API_KEY=gsk_...` satırını doldurun.

## 4) Yerel olarak çalıştırıp test edin

```bash
python baslat.py
```

Tarayıcıda açın:
- http://localhost:5000 → basit test sayfası (sohbet kutusu)
- http://localhost:5000/panel → yönetim paneli
- http://localhost:5000/saglik-durumu → `{"durum":"calisiyor"}` görmelisiniz

## 5) İnternete yayınlayın (Render — ücretsiz)

1. Kodu GitHub'a yükleyin (`.env` dosyası `.gitignore` sayesinde yüklenmez).
2. https://render.com üzerinde "New Web Service" oluşturun, GitHub reponuzu bağlayın.
3. Ayarlar:
   - **Build Command:** `pip install -r gereksinimler.txt`
   - **Start Command:** `gunicorn baslat:uygulama`
   - **Environment Variables:** `.env` içindeki tüm satırları buraya tek tek girin
     (özellikle `GROQ_API_KEY`, `AI_PROVIDER`, `FLASK_ORTAMI=uretim`)
4. Yayınlandıktan sonra size bir adres verilir: `https://sizin-app.onrender.com`

## 6) Wix Studio'ya bağlayın

`docs/` klasöründeki iki dosyayı kullanın:

- **`wix_velo_sohbet.js`** → Karşılama sayfanızın koduna yapıştırın (sohbet + form).
- **`wix_velo_panel.js`** → Yönetim paneli sayfanızın koduna yapıştırın (müşteri listesi).

Her iki dosyada da `const API = 'https://SIZIN-APP.onrender.com';` satırını,
Render'ın size verdiği gerçek adresle değiştirin.

Wix Editor'da gereken bileşen ID'leri (Ayarlar > ID) için rehberin
**13.6.1 Bileşenlere ID Verme** bölümüne bakın:

| Bileşen         | ID               |
|-----------------|------------------|
| Metin kutusu    | `#inputMesaj`    |
| Buton           | `#btnSor`        |
| Metin           | `#txtCevap`      |
| Metin kutusu    | `#inputIsim`     |
| Metin kutusu    | `#inputTelefon`  |
| Metin kutusu    | `#inputNot`      |
| Buton           | `#btnKaydet`     |
| Metin           | `#txtFormDurum`  |
| Repeater        | `#repeaterLeads` |

## 7) CORS'u daraltın (canlıya alınca)

`.env` içinde (veya Render ortam değişkenlerinde):

```
CORS_ALLOWED_ORIGINS=https://siteniz.wixsite.com
```

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| "No module named flask" | Sanal ortamı aktive edin |
| AI "demo modunda" diyor | `.env`'e doğru `GROQ_API_KEY` girin |
| Wix'ten istek gitmiyor | CORS_ALLOWED_ORIGINS ve API adresini kontrol edin |
| "TemplateNotFound" | `uygulama/sablonlar/` klasörünün yerini kontrol edin |
