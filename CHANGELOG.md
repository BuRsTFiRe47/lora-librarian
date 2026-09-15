# Changelog

Bu dosya, v1.4'ten bu yana yapılan tüm değişiklikleri tek bir yerde özetler.
This file summarizes every change made since v1.4 in one place.

---

## 🇹🇷 Türkçe

### 📦 Derleme / Yanlış virüs uyarısı düzeltmesi
- GitHub Actions derleme ayarı `--onefile`'dan `--onedir` + `--noupx`'e çevrildi — Windows Defender'ın PyInstaller `.exe` dosyalarını yanlışlıkla "Trojan:Win32/Wacatac.B!ml" olarak işaretlemesine (bilinen, çok yaygın bir yanlış pozitif) neden olan iki ana etken buydu. Artık release'ler tek `.exe` yerine bir `.zip` klasörü olarak yayınlanıyor.

### 🖼️ Kapak görseli ve NSFW modeller
- Civitai API'ye artık `nsfw`/`browsingLevel` parametreleri gönderiliyor — daha önce NSFW işaretli modellerin örnek görselleri Civitai tarafından varsayılan olarak filtreleniyordu, bu yüzden trigger word/kapak çıkarımı bu modellerde sessizce başarısız oluyordu.
- Kapak görseli indirirken artık dosyanın gerçek imzası (PNG/JPEG/WEBP başlığı) kontrol ediliyor; ağ engellemesi "200 başarılı" ama sahte içerik döndürürse artık bozuk dosya diske yazılmıyor.
- Görsel indirme önce `civitai.red` üzerinden deneniyor (görsel CDN'i ayrı bir alan adında olduğu için), başarısız olursa orijinal adrese düşüyor.

### 🏷️ "Anlamsız isim" tespiti önemli ölçüde genişletildi
- UUID (`000f06d1-...TA_trained` gibi eklentili olsa bile)
- ULID / rastgele uzun ID'ler (`030FY8RE0VGZ181DJSS8QX93R0` gibi)
- Çok parçalı tarih/numara kombinasyonları (`20260605-1780688763120-000006` gibi)
- Leetspeak ile gizlenmiş kelimeler (`3mb3ll1sh3d`, `4d41`, `M1n1` gibi — harflerin rakamla değiştirildiği isimler)
- Rakam oranı çok yüksek isimler (`2434_6_soci24` gibi)
- Sadece Japonca/Çince karakterlerden oluşan isimler
- **Yeni mod:** "Hiçbiri" seçeneği eklendi — isimlere hiç dokunmadan sadece trigger word doldurma.
- **Yeni:** Yeniden adlandırılan dosyaların sonuna taban model adı ekleniyor (ör. `Lingerie V1 - Illustrious`, `White Garter - Krea`).

### 🔑 Trigger word çıkarımı daha isabetli
- Jenerik kalite/vücut tipi/saç/çerçeveleme kelimeleri (full body, petite, çekim açısı vb.) artık filtreleniyor, yalnızca kostüme özgü kelimeler kalıyor.
- Modelin kendi Civitai etiketleriyle örtüşen kelimeler, az tekrarlansa da güçlü sinyal sayılıp korunuyor.
- Model açıklamasındaki "Trigger words:" gibi açık ifadeler artık okunuyor.
- "Clothing:" / "Accessories:" gibi başlıklı liste bölümleri (numaralı ya da virgüllü) artık ayrıştırılıyor.
- Hiçbir başlık yoksa bile, açıklamadaki en "etiket listesi gibi" görünen virgüllü paragraf son çare olarak kullanılıyor (teşekkür/Patreon gibi düzyazı metinlerle karıştırılmadan).
- Bir önceki çalıştırmadan etiketler zaten yerel dosyada kayıtlıysa açıklama metninin hiç çekilmediği bir hata düzeltildi.

### 🩺 Tanılama
- API istekleri başarısız olduğunda artık HTTP durum kodu (404, bağlantı hatası vb.) log'a yazılıyor.

### 📁 Klasör ve ayar yönetimi
- Ayar dosyası `LL-Settings.json` olarak yeniden adlandırıldı (Preview Smith ile aynı klasörde çakışmasın diye); eski `ayarlar.json` varsa ilk açılışta otomatik taşınıyor.
- Her klasör alanı artık bir **geçmiş listesi** tutuyor; klasör simgesine tıklayınca son kullanılan klasörler listeleniyor, her birinin yanında kaldırma (🗑) seçeneği var.

### 🧬 Yeni: Kopya Bulucu sekmesi
- Dosya içeriğine (hash) göre birebir aynı LoRA'ları buluyor — isimler farklı olsa bile.
- Her kopya grubunda hangi dosyanın tutulacağına şu sırayla karar veriyor: yanında Civitai bilgisi (`.civitai.info`) olan, ismi anlamlı olan, en sığ klasördeki.
- Diğer kopyalar **ilişkili tüm dosyalarıyla birlikte** (`.civitai.info`, önizleme görselleri, `.json` vb.) çöp klasörüne taşınıyor — sıradan kopya bulucuların atladığı "yancı dosya" sorununu çözüyor. Kalıcı silme yapmıyor.

### 🖥️ Arayüz
- Sekmeler arası geçişte önceki sekmenin butonlarının "ghosting" gibi ekranda kalması hatası düzeltildi.
- Log paneli inceltildi (daha küçük font, daha ince ilerleme çubuğu, daha az boşluk) ve varsayılan pencere yüksekliği küçültüldü — daha küçük ekranlara sığması için.
- **Yeni:** "💾 Logu Kaydet" butonu eklendi — işlem kaydını `.txt` dosyası olarak diske kaydedebilirsiniz. (Not: log zaten işlem bitiminde ekranda kalıyor; kaybolmuyor.)

---

## 🇬🇧 English

### 📦 Build / False-positive virus warning fix
- GitHub Actions build switched from `--onefile` to `--onedir` + `--noupx` - the two biggest contributors to Windows Defender falsely flagging PyInstaller `.exe` files as "Trojan:Win32/Wacatac.B!ml" (a well-known, very common false positive). Releases now ship as a `.zip` folder instead of a single `.exe`.

### 🖼️ Cover images and NSFW models
- Civitai API calls now include `nsfw`/`browsingLevel` parameters — previously, NSFW-flagged models' sample images were filtered out by Civitai by default, so trigger-word/cover extraction silently failed for them.
- Cover image downloads now verify the actual file signature (PNG/JPEG/WEBP header); if network filtering returns a fake "200 OK" with bogus content, a broken file is no longer written to disk.
- Image downloads now try the `civitai.red` mirror first (since the image CDN is a separate domain from the main API), falling back to the original host if that fails.

### 🏷️ "Meaningless name" detection significantly expanded
- UUIDs (even with a suffix like `000f06d1-...TA_trained`)
- ULIDs / long random IDs (e.g. `030FY8RE0VGZ181DJSS8QX93R0`)
- Multi-segment date/number combinations (e.g. `20260605-1780688763120-000006`)
- Leetspeak-obfuscated words (`3mb3ll1sh3d`, `4d41`, `M1n1` - letters swapped for digits)
- Names that are mostly digits by ratio (e.g. `2434_6_soci24`)
- Names made up entirely of Japanese/Chinese characters
- **New mode:** "None" - don't touch filenames at all, only fill in trigger words.
- **New:** Renamed files now get the base model name appended (e.g. `Lingerie V1 - Illustrious`, `White Garter - Krea`).

### 🔑 More accurate trigger-word extraction
- Generic quality/body-type/hair/framing terms (full body, petite, camera angle, etc.) are now filtered out, leaving only costume-specific keywords.
- Candidates that also match the model's own Civitai tags are kept even if they don't repeat often - a strong extra signal.
- Explicit "Trigger words:" declarations in the model description are now read.
- "Clothing:" / "Accessories:" style itemized sections (numbered or comma-separated) in the description are now parsed.
- Even with no header at all, the most "tag-list-like" comma-separated paragraph in the description is used as a last resort (without being confused by prose like thank-you/Patreon notes).
- Fixed a bug where the description text was never fetched at all if tags happened to already be cached locally from a previous run.

### 🩺 Diagnostics
- Failed API requests now log the HTTP status code (404, connection error, etc.) instead of a generic message.

### 📁 Folder and settings management
- The settings file was renamed to `LL-Settings.json` (so it doesn't collide with Preview Smith in the same folder); an existing `ayarlar.json` is migrated automatically on first launch.
- Every folder field now keeps a **history list**; clicking the folder icon shows recently used folders, each with a remove (🗑) option.

### 🧬 New: Duplicate Finder tab
- Finds byte-identical LoRAs by file content hash - even when the filenames are completely different.
- In each duplicate group, decides which file to keep in this order: the one with Civitai metadata (`.civitai.info`) next to it, the one with a meaningful name, the one in the shallowest folder.
- The other copies are moved to the trash folder **along with all their related files** (`.civitai.info`, preview images, `.json`, etc.) - solving the "orphaned companion file" problem that ordinary duplicate finders leave behind. Never permanently deletes.

### 🖥️ Interface
- Fixed a "ghosting" bug where the previous tab's buttons remained visible on screen after switching tabs.
- Slimmed down the log panel (smaller font, thinner progress bar, tighter spacing) and reduced the default window height to better fit smaller screens.
- **New:** Added a "💾 Save Log" button to export the process log as a `.txt` file. (Note: the log already stays on screen after a run completes - it isn't cleared.)
