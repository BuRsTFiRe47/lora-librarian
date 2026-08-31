# 🎨 LoRA Librarian

**AI model (Checkpoint / LoRA) kütüphanenizi otomatik olarak düzenleyen, eksik verileri Civitai'den tamamlayan ve kütüphanenizi temiz tutan modern, çift dilli masaüstü uygulaması.**

**A modern, bilingual desktop app that automatically organizes your AI model (Checkpoint / LoRA) library, fills in missing data from Civitai, and keeps your library clean.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🇹🇷 Türkçe

### Özellikler

- **🏰 Checkpoint & 🎨 LoRA Düzenleme** — Modellerinizi taban model ailesine (SDXL, Flux, Flux Krea, Krea, Anima, Pony, Illustrious, NoobAI, Chroma, HiDream, Qwen Image, Wan Video ve daha fazlası), kategoriye (Konsept/Arkaplan) ve isterseniz yaratıcıya göre otomatik klasörler.
- **🆕 Yeni teknolojileri tanır** — `baseModel` etiketindeki küçük varyasyonları (ör. "Flux.1 D", "Flux.1 Krea Dev") tek bir temiz aile klasöründe toplayan akıllı bir normalize edici içerir; yeni/az bilinen teknolojiler geldikçe kolayca genişletilebilir (bkz. `base_models.py`).
- **🧹 Akıllı Temizlik** — Eski sürümleri ve düşük puanlı modelleri otomatik olarak ayrı bir çöp/arşiv klasörüne taşır.
- **🌐 4 Dil** — Türkçe / English / 日本語 / 中文 arayüz, açılır menü yerine kaydırmalı (segmented) düğmelerle anında değiştirilir.
- **🌗 Karanlık / Aydınlık Tema** — Varsayılan karanlık temayla açılır, tek tıkla aydınlığa geçer.
- **💾 Kalıcı Ayarlar** — Dil, tema, pencere boyutu, API anahtarı ve her sekmede en son kullanılan klasör otomatik hatırlanır.
- **⚡ Optimize Edilmiş** — Tekrarlanan taramalarda dosyaları yeniden hash'lememek için önbellekleme (`hash_cache.json`) ve paylaşılan bir HTTP oturumu (bağlantı havuzu) kullanır.

### Kurulum

```bash
git clone https://github.com/BuRsTFiRe47/lora-librarian.git
cd lora-librarian
pip install -r requirements.txt
python main.py
```

Hazır `.exe` dosyasını indirmek isterseniz, sağdaki **Releases** bölümüne bakabilirsiniz.

### Kullanım

1. Üstteki API anahtarı alanına (opsiyonel) Civitai API anahtarınızı girin.
2. İlgili sekmede (Checkpoint / LoRA / Temizlik) klasörünüzü seçin.
3. Düzenleme tercihlerinizi (taban modele göre, kategoriye göre, yaratıcıya göre vb.) ayarlayın.
4. İlgili "▶ Başlat" düğmesine basın ve canlı işlem kaydını takip edin.

---

## 🇬🇧 English

### Features

- **🏰 Checkpoint & 🎨 LoRA Organizing** — Automatically sorts your models into folders by base-model family (SDXL, Flux, Flux Krea, Krea, Anima, Pony, Illustrious, NoobAI, Chroma, HiDream, Qwen Image, Wan Video, and more), by category (Concept/Background), and optionally by creator.
- **🆕 Recognizes new technologies** — Includes a smart normalizer that groups small variations of the `baseModel` tag (e.g. "Flux.1 D", "Flux.1 Krea Dev") into one clean family folder, and can easily be extended as new/lesser-known technologies appear (see `base_models.py`).
- **🧹 Smart Cleanup** — Automatically moves outdated versions and low-rated models into a separate trash/archive folder.
- **🌐 4 Languages** — Turkish / English / 日本語 / 中文 interface, switched instantly with segmented buttons instead of a dropdown menu.
- **🌗 Dark / Light Theme** — Opens in dark mode by default, switches to light with a single click.
- **💾 Persistent Settings** — Language, theme, window size, API key, and the last-used folder on each tab are all remembered automatically.
- **⚡ Optimized** — Uses a hash cache (`hash_cache.json`) to avoid re-hashing unchanged files on repeat scans, plus a shared HTTP session (connection pooling) for API calls.

### Installation

```bash
git clone https://github.com/BuRsTFiRe47/lora-librarian.git
cd lora-librarian
pip install -r requirements.txt
python main.py
```

If you'd rather use a ready-made `.exe`, check the **Releases** section on the right.

### Usage

1. Optionally enter your Civitai API key in the field at the top.
2. Select your folder on the relevant tab (Checkpoint / LoRA / Cleanup).
3. Configure your organizing preferences (by base model, by category, by creator, etc.).
4. Click the corresponding "▶ Start" button and follow the live process log.

---

## 📄 License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).
