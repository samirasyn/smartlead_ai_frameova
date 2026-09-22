"""
yapay_zeka_servisi.py — Tercüman
------------------------------------
Ziyaretçinin sorusunu alır, dış yapay zekâ servisine (Groq / Gemini / OpenAI)
gönderir, gelen yanıtı geri getirir. Strateji Deseni: hangi servisin kullanılacağı
ayarlar.py'deki AI_PROVIDER değerine göre çalışma anında seçilir.
"""

import requests
from flask import current_app


class YapayZekaServisHatasi(Exception):
    """Yapay zekâ servisine ulaşılamadığında veya hata döndüğünde fırlatılır."""
    pass


class YapayZekaServisi:

    # ------------------------------------------------------------------
    # 1) AKILLI SEÇİM
    # ------------------------------------------------------------------
    def yanit_uret(self, kullanici_mesaji, sohbet_gecmisi=None):
        sohbet_gecmisi = sohbet_gecmisi or []
        saglayici = current_app.config.get('AI_PROVIDER', 'groq').lower()

        # Anahtar tanımlı değilse, hangi sağlayıcı seçilmiş olursa olsun demoya düş.
        anahtar_haritasi = {
            'openai': current_app.config.get('OPENAI_API_KEY'),
            'groq': current_app.config.get('GROQ_API_KEY'),
            'gemini': current_app.config.get('GEMINI_API_KEY'),
        }
        if not anahtar_haritasi.get(saglayici):
            return self._demo_yaniti_ver()

        try:
            if saglayici == 'openai':
                return self._openai_cagir(kullanici_mesaji, sohbet_gecmisi)
            elif saglayici == 'gemini':
                return self._gemini_cagir(kullanici_mesaji, sohbet_gecmisi)
            else:
                return self._groq_cagir(kullanici_mesaji, sohbet_gecmisi)
        except requests.RequestException as hata:
            raise YapayZekaServisHatasi(
                f"Yapay zekâ servisine ulaşılamadı: {hata}"
            )

    # ------------------------------------------------------------------
    # 2) SİSTEM TALİMATI — Yapay zekânın kişiliği
    # ------------------------------------------------------------------
    def _sistem_talimati_olustur(self):
        return current_app.config.get(
            'BUSINESS_CONTEXT',
            "Sen kibar ve profesyonel bir satış asistanısın. Türkçe konuş."
        )

    # ------------------------------------------------------------------
    # 3) GROQ (varsayılan, ücretsiz, hızlı)
    # ------------------------------------------------------------------
    def _groq_cagir(self, mesaj, gecmis):
        anahtar = current_app.config.get('GROQ_API_KEY')
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {anahtar}",
            "Content-Type": "application/json",
        }
        mesajlar = [{"role": "system", "content": self._sistem_talimati_olustur()}]
        mesajlar.extend(gecmis)
        mesajlar.append({"role": "user", "content": mesaj})

        payload = {
            "model": "openai/gpt-oss-120b",
            "messages": mesajlar,
            "temperature": 0.7,
            "max_tokens": 500,
        }
        yanit = requests.post(url, headers=headers, json=payload, timeout=20)
        yanit.raise_for_status()
        veri = yanit.json()
        return veri["choices"][0]["message"]["content"].strip()

    # ------------------------------------------------------------------
    # 4) GOOGLE GEMİNİ
    # ------------------------------------------------------------------
    def _gemini_cagir(self, mesaj, gecmis):
        anahtar = current_app.config.get('GEMINI_API_KEY')
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={anahtar}"
        )
        icerikler = []
        for gecmis_mesaj in gecmis:
            rol = "model" if gecmis_mesaj.get("role") == "assistant" else "user"
            icerikler.append({"role": rol, "parts": [{"text": gecmis_mesaj.get("content", "")}]})
        icerikler.append({"role": "user", "parts": [{"text": mesaj}]})

        payload = {
            "system_instruction": {"parts": [{"text": self._sistem_talimati_olustur()}]},
            "contents": icerikler,
        }
        yanit = requests.post(url, json=payload, timeout=20)
        yanit.raise_for_status()
        veri = yanit.json()
        return veri["candidates"][0]["content"]["parts"][0]["text"].strip()

    # ------------------------------------------------------------------
    # 5) OPENAI
    # ------------------------------------------------------------------
    def _openai_cagir(self, mesaj, gecmis):
        anahtar = current_app.config.get('OPENAI_API_KEY')
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {anahtar}",
            "Content-Type": "application/json",
        }
        mesajlar = [{"role": "system", "content": self._sistem_talimati_olustur()}]
        mesajlar.extend(gecmis)
        mesajlar.append({"role": "user", "content": mesaj})

        payload = {
            "model": "gpt-4o-mini",
            "messages": mesajlar,
            "temperature": 0.7,
            "max_tokens": 500,
        }
        yanit = requests.post(url, headers=headers, json=payload, timeout=20)
        yanit.raise_for_status()
        veri = yanit.json()
        return veri["choices"][0]["message"]["content"].strip()

    # ------------------------------------------------------------------
    # 6) DEMO MODU — API anahtarı yokken
    # ------------------------------------------------------------------
    def _demo_yaniti_ver(self):
        return (
            "Sistem demo modunda çalışıyor, lütfen .env dosyanızı kontrol edin. "
            "(AI_PROVIDER için geçerli bir API anahtarı tanımlı değil.)"
        )


# Rota dosyasının (rotalar.py) doğrudan import edip kullanabileceği tek örnek (instance)
yapay_zeka_servisi = YapayZekaServisi()
