// =====================================================================
// Wix Studio / Velo — Karşılama Sayfası Kodu
// Bu kodu, sohbet ve formun bulunduğu SAYFANIN kod panosuna yapıştırın.
// (Sayfayı seçin > alt kısımdaki "Bu sayfa için kod ekle" / kod ikonu)
// =====================================================================

import { fetch } from 'wix-fetch';

// ÖNEMLİ: Render'da yayınladığınız gerçek adresle değiştirin.
const API = 'https://SIZIN-APP.onrender.com';

let gecmis = []; // konuşma hafızası (tarayıcı sekmesi kapanınca sıfırlanır)

$w.onReady(function () {
    $w('#btnSor').onClick(sohbetGonder);
    $w('#btnKaydet').onClick(musteriKaydet);

    // Enter tuşuyla da gönderilsin isterseniz:
    $w('#inputMesaj').onKeyPress((event) => {
        if (event.key === 'Enter') sohbetGonder();
    });
});

// ---------------------------------------------------------------------
// 1) SOHBET — /api/sohbet adresine mesaj gönderir
// ---------------------------------------------------------------------
async function sohbetGonder() {
    const mesaj = $w('#inputMesaj').value;
    if (!mesaj) return;

    $w('#txtCevap').text = 'Yanıt yazılıyor...';
    $w('#btnSor').disable();

    try {
        const cevap = await fetch(`${API}/api/sohbet`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mesaj, gecmis })
        });
        const veri = await cevap.json();

        if (veri.basari) {
            $w('#txtCevap').text = veri.cevap;
            gecmis.push({ role: 'user', content: mesaj });
            gecmis.push({ role: 'assistant', content: veri.cevap });
        } else {
            $w('#txtCevap').text = 'Üzgünüm, şu an yanıt veremiyorum: ' + veri.hata;
        }
    } catch (hata) {
        $w('#txtCevap').text = 'Sunucuya bağlanılamadı. Lütfen daha sonra tekrar deneyin.';
        console.error(hata);
    } finally {
        $w('#inputMesaj').value = '';
        $w('#btnSor').enable();
    }
}

// ---------------------------------------------------------------------
// 2) İLETİŞİM FORMU — /api/adaylar adresine kayıt gönderir
// ---------------------------------------------------------------------
async function musteriKaydet() {
    const isim = $w('#inputIsim').value;
    const telefon = $w('#inputTelefon').value;
    const not = $w('#inputNot').value || '';

    if (!isim || !telefon) {
        $w('#txtFormDurum').text = 'Lütfen isim ve telefon alanlarını doldurun.';
        return;
    }

    try {
        const cevap = await fetch(`${API}/api/adaylar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ isim, telefon, mesaj: not })
        });
        const veri = await cevap.json();
        $w('#txtFormDurum').text = veri.mesaj;

        if (veri.basari) {
            $w('#inputIsim').value = '';
            $w('#inputTelefon').value = '';
            $w('#inputNot').value = '';
        }
    } catch (hata) {
        $w('#txtFormDurum').text = 'Bir hata oluştu, lütfen tekrar deneyin.';
        console.error(hata);
    }
}
