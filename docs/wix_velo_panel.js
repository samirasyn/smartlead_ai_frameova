// =====================================================================
// Wix Studio / Velo — Yönetim Paneli Sayfası Kodu
// Bu kodu, müşteri listesinin gösterileceği SAYFANIN kod panosuna yapıştırın.
// Sayfaya önceden bir "Repeater" (#repeaterLeads) eklemiş olmanız gerekir.
// =====================================================================

import { fetch } from 'wix-fetch';

const API = 'https://SIZIN-APP.onrender.com';

$w.onReady(async function () {
    await listeyiYukle();
    $w('#btnYenile').onClick(listeyiYukle); // isteğe bağlı bir "Yenile" butonu
});

async function listeyiYukle() {
    try {
        const cevap = await fetch(`${API}/api/adaylar`, { method: 'GET' });
        const veri = await cevap.json();

        if (!veri.basari) {
            console.error('Liste alınamadı:', veri);
            return;
        }

        // Repeater'a veriyi bağla — her objede _id ZORUNLU
        $w('#repeaterLeads').data = veri.adaylar.map(aday => ({
            _id: String(aday.id),
            isim: aday.isim,
            telefon: aday.telefon,
            mesaj: aday.mesaj,
            tarih: aday.olusturulma_tarihi
        }));

        $w('#txtToplam').text = `Toplam müşteri adayı: ${veri.toplam}`;

        // Her satır oluşturulurken içini doldur.
        // ÖNEMLİ: Satır içinde $item('#...') kullanın, ASLA $w('#...') değil!
        $w('#repeaterLeads').onItemReady(($item, satir) => {
            $item('#txtIsim').text = satir.isim;
            $item('#txtTelefon').text = satir.telefon;
            $item('#txtMesaj').text = satir.mesaj || '-';
            $item('#txtTarih').text = satir.tarih;
        });
    } catch (hata) {
        console.error('Sunucuya bağlanılamadı:', hata);
    }
}
