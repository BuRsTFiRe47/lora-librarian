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
- **⚙️ Bağımsız Ayar Dosyası** — Ayarlar artık `LL-Settings.json` olarak saklanıyor (Preview Smith ile aynı klasörde çakışmasın diye); önceki `ayarlar.json` varsa ilk açılışta otomatik taşınır.
- **🏷️ İsim & Trigger Düzenleyici** — Anlamsız (hash/UUID/ULID/çok parçalı tarih-numara/numara/leetspeak gibi "3mb3ll1sh3d" tarzı obfuske edilmiş, Japonca/Çince) isimli LoRA dosyalarının gerçek adını Civitai'den çekip dosyayı ve tüm ilişkili dosyaları (`.civitai.info`, önizleme görselleri, `.json` vb.) yeniden adlandırır. Üç mod var: sadece anlamsız isimler, Civitai adından farklı olan her şey, ya da isimlere hiç dokunmadan sadece trigger word doldurma. Trigger word'ü eksik olanlar için sırasıyla: Civitai'nin resmi listesine, sonra örnek görsellerin komutlarına (jenerik kalite/vücut/saç tariflerini eleyip yalnızca kostüme özgü, tekrar eden kelimeleri — ayrıca modelin Civitai etiketleriyle örtüşenleri de — seçerek), sonra model açıklamasındaki "trigger words:" ifadesine, sonra "Clothing:"/"Accessories:" gibi başlıklı liste bölümlerine, son çare olarak da başlıksız ama virgüllü etiket listesi gibi görünen paragraflara bakar. NSFW modellerin örnek görsellerini de doğru şekilde çeker (Civitai API bunları varsayılan olarak filtreler) ve kapak görseli indirirken gerçek dosya imzasını kontrol ederek ağ engellemesinden kaynaklanan bozuk dosyaları tespit edip atlar. API hataları artık HTTP durum koduyla loglanır (tanılama kolaylığı için). Sonucu hem `.civitai.info`'ya hem de Forge/WebUI'nin LoRA kartında gösterdiği `.json` "activation text" alanına kaydeder — var olan bir bilgiyi asla ezmez.
- **🌐 4 Dil** — Türkçe / English / 日本語 / 中文 arayüz, açılır menü yerine kaydırmalı (segmented) düğmelerle anında değiştirilir.
- **🎨 Yeni Arayüz** — Mor/pembe degrade vurgulu koyu tema, sol kenar çubuğu navigasyonu, yuvarlak köşeli kart ve butonlar. Koyu/açık tema tam destekli.
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
- **⚙️ Standalone Settings File** — Settings are now stored as `LL-Settings.json` (so it doesn't collide with Preview Smith in the same folder); an existing `ayarlar.json` is migrated automatically on first launch.
- **🏷️ Rename & Trigger Editor** — Fetches the real title from Civitai for LoRA files with meaningless names (hashes, UUIDs, ULIDs, multi-part numeric IDs, leetspeak-obfuscated words like "3mb3ll1sh3d", or Japanese/Chinese titles) and renames the file plus every related file (`.civitai.info`, preview images, `.json`, etc.). Three modes: meaningless names only, everything that differs from the Civitai title, or a names-untouched mode that only fills in trigger words. For LoRAs missing a trigger word, it checks in order: Civitai's official trained-words list; sample-image prompts (filtering out generic quality/body/hair descriptors and keeping only repeated, costume-specific keywords — boosted by cross-checking the model's own Civitai tags); "trigger words:" in the model description; "Clothing:"/"Accessories:" style list sections in the description; and, as a last resort, any unlabeled comma-separated paragraph that looks like a tag list. Correctly fetches sample images for NSFW models too (Civitai's API hides them by default unless explicitly requested), and API failures are now logged with their HTTP status code for easier diagnosis. Saves the result to both `.civitai.info` and the `.json` "activation text" field that Forge/WebUI's LoRA card reads — never overwriting anything already there.
- **🌐 4 Languages** — Turkish / English / 日本語 / 中文 interface, switched instantly with segmented buttons instead of a dropdown menu.
- **🎨 Redesigned UI** — Dark theme with a violet-to-pink gradient accent, left sidebar navigation, rounded cards and buttons. Full dark/light theme support.
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
