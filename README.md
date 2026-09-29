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
- **🏷️ İsim & Trigger Düzenleyici** — Anlamsız (hash/UUID/ULID/çok parçalı tarih-numara/numara/leetspeak gibi "3mb3ll1sh3d" tarzı obfuske edilmiş, Japonca/Çince) isimli LoRA dosyalarının gerçek adını Civitai'den çekip dosyayı ve tüm ilişkili dosyaları (`.civitai.info`, önizleme görselleri, `.json` vb.) yeniden adlandırır. Üç mod var: sadece anlamsız isimler, Civitai adından farklı olan her şey, ya da isimlere hiç dokunmadan sadece trigger word doldurma. Trigger word'ü eksik olanlar için sırasıyla: Civitai'nin resmi listesine, sonra örnek görsellerin komutlarına (jenerik kalite/vücut/saç tariflerini eleyip yalnızca kostüme özgü, tekrar eden kelimeleri — ayrıca modelin Civitai etiketleriyle örtüşenleri de — seçerek), sonra model açıklamasındaki "trigger words:" ifadesine, sonra "Clothing:"/"Accessories:" gibi başlıklı liste bölümlerine, son çare olarak da başlıksız ama virgüllü etiket listesi gibi görünen paragraflara bakar. Trigger word'ü tek bir birleşik kelimeyse (ör. `pinkcamisoledress`), örnek görsellerin komutlarında ya da model etiketlerinde bunun boşluklu hâlini (`pink camisole dress`) arayıp yanına ekler; zaten 2+ kelimelik bir trigger word'ü olan LoRA'lara ise hiç dokunmaz. İsim tespiti; UUID, ULID, çok parçalı tarih/numara kombinasyonları, leetspeak (`3mb3ll1sh3d`), ürün/parti kodları (`HMS2025SPK01`) ve sadece taban-model/sürüm etiketi içerip gerçek kelime barındırmayan isimleri (`Ilus_v10` gibi) de kapsar. NSFW modellerin örnek görsellerini de doğru şekilde çeker (Civitai API bunları varsayılan olarak filtreler) ve kapak görseli indirirken gerçek dosya imzasını kontrol ederek ağ engellemesinden kaynaklanan bozuk dosyaları tespit edip atlar. API hataları artık HTTP durum koduyla loglanır (tanılama kolaylığı için). Sonucu hem `.civitai.info`'ya hem de Forge/WebUI'nin LoRA kartında gösterdiği `.json` "activation text" alanına kaydeder — var olan bir bilgiyi asla ezmez.
- **🧬 Kopya Bulucu** — Dosya içeriğine (hash) göre birebir aynı LoRA'ları bulur; her grupta Civitai bilgisi olan/ismi anlamlı olan/en sığ klasördeki kopyayı tutar, diğerlerini **ilişkili tüm dosyalarıyla birlikte** (`.civitai.info`, önizleme görselleri, `.json` vb. — sıradan kopya bulucuların atladığı eşlikçi dosyalar dahil) çöp klasörüne taşır. Kalıcı silme yapmaz.
- **🌐 4 Dil** — Türkçe / English / 日本語 / 中文 arayüz, açılır menü yerine kaydırmalı (segmented) düğmelerle anında değiştirilir.
- **🎨 Yeni Arayüz** — Siyah/mavi degrade vurgulu koyu tema, sol kenar çubuğu navigasyonu, hafif kabarık/gölgeli yuvarlak köşeli kart ve butonlar. Koyu/açık tema tam destekli.
- **📁 Klasör Geçmişi** — Her klasör alanının yanındaki 🕘 simgesiyle son kullanılan klasörler listelenir, her birinin yanında kaldırma (✕) seçeneği vardır — özellikle birden fazla Stable Diffusion kurulumu olanlar için her seferinde baştan klasör seçmeyi gereksiz kılar.
- **💾 Log Kaydı** — Canlı işlem kaydı, işlem bitiminde ekranda kalır ve "Logu Kaydet" butonuyla `.txt` dosyası olarak diske kaydedilebilir.
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

> ⚠️ **Windows Defender uyarısı hakkında:** PyInstaller ile derlenen Python programları, kendini geçici klasöre açma davranışı yüzünden bazen Defender tarafından yanlışlıkla "Trojan:Win32/Wacatac.B!ml" olarak işaretlenir — bu, PyInstaller tabanlı binlerce açık kaynak projede görülen bilinen bir yanlış pozitiftir, gerçek bir virüs değildir. Kaynak kodun tamamı bu depoda açık; isterseniz kendiniz derleyebilir ya da [dosyayı VirusTotal'da tarayabilirsiniz](https://www.virustotal.com/).

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
- **🏷️ Rename & Trigger Editor** — Fetches the real title from Civitai for LoRA files with meaningless names (hashes, UUIDs, ULIDs, multi-part numeric IDs, leetspeak-obfuscated words like "3mb3ll1sh3d", or Japanese/Chinese titles) and renames the file plus every related file (`.civitai.info`, preview images, `.json`, etc.). Three modes: meaningless names only, everything that differs from the Civitai title, or a names-untouched mode that only fills in trigger words. For LoRAs missing a trigger word, it checks in order: Civitai's official trained-words list; sample-image prompts (filtering out generic quality/body/hair descriptors and keeping only repeated, costume-specific keywords — boosted by cross-checking the model's own Civitai tags); "trigger words:" in the model description; "Clothing:"/"Accessories:" style list sections in the description; and, as a last resort, any unlabeled comma-separated paragraph that looks like a tag list. When the trigger word is a single run-together word (e.g. `pinkcamisoledress`), it searches sample prompts and the model's tags for the spaced-out form (`pink camisole dress`) and adds it alongside - LoRAs that already have a 2+ word trigger are left completely untouched. Name detection also covers UUIDs, ULIDs, multi-part date/number IDs, leetspeak (`3mb3ll1sh3d`), product/batch codes (`HMS2025SPK01`), and names that carry only a base-model/version tag with no real word (e.g. `Ilus_v10`). Correctly fetches sample images for NSFW models too (Civitai's API hides them by default unless explicitly requested), and API failures are now logged with their HTTP status code for easier diagnosis. Saves the result to both `.civitai.info` and the `.json` "activation text" field that Forge/WebUI's LoRA card reads — never overwriting anything already there.
- **🧬 Duplicate Finder** — Finds byte-identical LoRAs by content hash; in each group it keeps the copy with Civitai metadata / a meaningful name / the shallowest folder, and moves the rest — **along with all their related files** (`.civitai.info`, preview images, `.json`, etc. - the companion files ordinary duplicate finders leave behind) — to the trash folder. Never permanently deletes.
- **🌐 4 Languages** — Turkish / English / 日本語 / 中文 interface, switched instantly with segmented buttons instead of a dropdown menu.
- **🎨 Redesigned UI** — Dark theme with a black/blue gradient accent, left sidebar navigation, subtly raised/shadowed rounded cards and buttons. Full dark/light theme support.
- **📁 Folder History** — A 🕘 icon next to every folder field lists recently used folders, each with a remove (✕) option - handy if you juggle more than one Stable Diffusion install and don't want to browse from scratch every time.
- **💾 Log Saving** — The live process log stays on screen after a run finishes, and a "Save Log" button exports it as a `.txt` file.
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

> ⚠️ **About the Windows Defender warning:** Python programs built with PyInstaller are sometimes flagged by Defender as "Trojan:Win32/Wacatac.B!ml" because of how they self-extract to a temp folder at startup - this is a well-known false positive seen across thousands of PyInstaller-based open-source projects, not an actual virus. The full source is right here in this repo; you're welcome to build it yourself, or [scan the file on VirusTotal](https://www.virustotal.com/).

### Usage

1. Optionally enter your Civitai API key in the field at the top.
2. Select your folder on the relevant tab (Checkpoint / LoRA / Cleanup).
3. Configure your organizing preferences (by base model, by category, by creator, etc.).
4. Click the corresponding "▶ Start" button and follow the live process log.

---

## 📄 License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).
