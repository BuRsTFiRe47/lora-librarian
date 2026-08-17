# -*- coding: utf-8 -*-
"""
LoRA Librarian - Language / Dil Module
Merkezi çift dilli (TR/EN) metin sözlüğü.
Central bilingual (TR/EN) text dictionary.
"""

TRANSLATIONS = {
    "app_title": {"tr": "LoRA Librarian - AI Model Kütüphane Yöneticisi", "en": "LoRA Librarian - AI Model Library Manager"},

    # Top bar
    "api_key_label": {"tr": "🔑 Civitai API Anahtarı (Opsiyonel):", "en": "🔑 Civitai API Key (Optional):"},
    "lang_tr": {"tr": "Türkçe", "en": "Turkish"},
    "lang_en": {"tr": "İngilizce", "en": "English"},
    "theme_dark": {"tr": "Koyu", "en": "Dark"},
    "theme_light": {"tr": "Açık", "en": "Light"},

    # Tabs
    "tab_checkpoint": {"tr": "🏰 Checkpoint Düzenle", "en": "🏰 Edit Checkpoints"},
    "tab_lora": {"tr": "🎨 LoRA Düzenle", "en": "🎨 Edit LoRAs"},
    "tab_clean": {"tr": "🧹 Akıllı Temizlik", "en": "🧹 Smart Cleanup"},

    # Path pickers
    "folder_checkpoint": {"tr": "Düzenlenecek Checkpoint Klasörü:", "en": "Checkpoint Folder to Organize:"},
    "folder_lora": {"tr": "Düzenlenecek LoRA Klasörü:", "en": "LoRA Folder to Organize:"},
    "folder_scan": {"tr": "Taranacak Ana Klasör:", "en": "Main Folder to Scan:"},
    "folder_trash": {"tr": "Ayıklananların Gideceği Klasör (Çöp/Arşiv):", "en": "Destination for Removed Items (Trash/Archive):"},
    "browse": {"tr": "Gözat", "en": "Browse"},

    # Organize settings
    "switch_base_model": {"tr": "Tabana Göre (SDXL, Flux, Krea, Anima vb.)", "en": "By Base Model (SDXL, Flux, Krea, Anima etc.)"},
    "switch_fetch_meta": {"tr": "Eksik Kapakları/JSON'ları İndir", "en": "Download Missing Covers/JSON"},
    "switch_category": {"tr": "Kategoriye Göre (Sadece Konsept & Arkaplan)", "en": "By Category (Concept & Background Only)"},
    "creator_folder_label": {"tr": "Yaratıcıya (Creator) Göre Klasörle:", "en": "Organize by Creator:"},
    "creator_hint": {"tr": "↳ 'Sadece Listeyi' seçerseniz aranacak isimleri buraya alt alta yazın:", "en": "↳ If you choose 'List Only', type the usernames below, one per line:"},
    "creator_mode_off": {"tr": "Kapalı", "en": "Off"},
    "creator_mode_all": {"tr": "Tüm Kullanıcıları Ayır", "en": "Separate All Creators"},
    "creator_mode_list": {"tr": "Sadece Listedekileri Ayır", "en": "Only Separate Listed Ones"},
    "conflict_label": {"tr": "Aynı İsimde Dosya Çakışırsa:", "en": "If a Filename Conflict Occurs:"},
    "conflict_rename": {"tr": "Yeniden Adlandır", "en": "Rename"},
    "conflict_skip": {"tr": "Es Geç (Dokunma)", "en": "Skip (Leave As Is)"},
    "conflict_overwrite": {"tr": "Üzerine Yaz (Eskisini Sil)", "en": "Overwrite (Delete Old)"},

    "btn_organize_checkpoint": {"tr": "▶ Checkpointleri Düzenle", "en": "▶ Organize Checkpoints"},
    "btn_organize_lora": {"tr": "▶ LoRA'ları Düzenle", "en": "▶ Organize LoRAs"},
    "btn_start_clean": {"tr": "▶ Temizliği Başlat", "en": "▶ Start Cleanup"},

    # Cleanup tab
    "switch_old_versions": {"tr": "Eski Sürümleri Çöpe Taşı (Yenisi varsa eskisini ayıklar)", "en": "Move Old Versions to Trash (removes old ones if a newer version exists)"},
    "switch_low_rating": {"tr": "Düşük Puanlıları Çöpe Taşı", "en": "Move Low-Rated Models to Trash"},
    "min_rating_label": {"tr": "Min Puan:", "en": "Min Rating:"},
    "conflict_trash_label": {"tr": "Çöp Klasöründe Çakışma Olursa:", "en": "If a Conflict Occurs in the Trash Folder:"},

    # Log / status
    "status_label_prefix": {"tr": "Canlı İşlem Kaydı - Durum:", "en": "Live Process Log - Status:"},
    "status_waiting": {"tr": "Bekliyor", "en": "Waiting"},
    "status_running": {"tr": "İşlem Yapılıyor...", "en": "Processing..."},
    "status_done": {"tr": "Tamamlandı!", "en": "Completed!"},
    "log_ready": {"tr": "Sistem Hazır. Ayarlarınız otomatik olarak hatırlanır.\nSadece Konsept ve Arkaplan ayırma modülü devrede.", "en": "System Ready. Your settings are remembered automatically.\nOnly the Concept and Background separation module is active."},
    "log_system_started": {"tr": "=== SİSTEM BAŞLADI ({mode}) ===", "en": "=== SYSTEM STARTED ({mode}) ==="},
    "log_total_models": {"tr": "[Bilgi] Toplam {count} model tespit edildi.", "en": "[Info] {count} models detected in total."},
    "log_model": {"tr": "[Model] {file}", "en": "[Model] {file}"},
    "log_hash_reading": {"tr": "   [Hash] Okunuyor...", "en": "   [Hash] Reading..."},
    "log_api_saved": {"tr": "   [+] Veriler JSON olarak kaydedildi.", "en": "   [+] Data saved as JSON."},
    "log_api_failed": {"tr": "   [!] API bağlantısı kurulamadı.", "en": "   [!] Could not connect to the API."},
    "log_cover_downloaded": {"tr": "   [+] Kapak indirildi.", "en": "   [+] Cover image downloaded."},
    "log_cover_failed": {"tr": "   [!] Kapak indirilemedi (bağlantı hatası ya da geçersiz görsel).", "en": "   [!] Could not download cover image (connection error or invalid image)."},
    "log_extracting_rating": {"tr": "   [Ayıklanıyor] Puan: {rating}/5", "en": "   [Extracting] Rating: {rating}/5"},
    "log_folder_error": {"tr": "   [HATA] Klasör oluşturulamadı!", "en": "   [ERROR] Could not create folder!"},
    "log_skipped_exists": {"tr": "   [Atlandı] Hedefte '{file}' zaten var.", "en": "   [Skipped] '{file}' already exists at destination."},
    "log_renamed": {"tr": "   [Yeniden Adlandırıldı] -> {file}", "en": "   [Renamed] -> {file}"},
    "log_moved": {"tr": "   [->] Taşındı: {folder}", "en": "   [->] Moved to: {folder}"},
    "log_move_failed": {"tr": "   [HATA] Taşınamadı!", "en": "   [ERROR] Could not move!"},
    "log_empty_folders": {"tr": "[Süpürge] {count} adet boş klasör silindi.", "en": "[Sweep] {count} empty folder(s) deleted."},
    "log_summary_title": {"tr": "=== ÖZET RAPOR ===", "en": "=== SUMMARY REPORT ==="},

    "summary_text": {
        "tr": "✅ İşlem Başarıyla Tamamlandı!\n\n📦 Düzenlenen/Taşınan Model: {moved}\n🗑️ Ayıklanan (Çöpe Giden) Model: {extracted}\n🧹 Silinen Boş Klasör Sayısı: {empty}\n\nHatalı kategoriler temizlendi, kütüphaneniz aslına döndü!",
        "en": "✅ Operation Completed Successfully!\n\n📦 Organized/Moved Models: {moved}\n🗑️ Extracted (Trashed) Models: {extracted}\n🧹 Empty Folders Deleted: {empty}\n\nMisplaced categories were cleaned up, your library is back in order!",
    },

    "dialog_warning_title": {"tr": "Hata", "en": "Warning"},
    "dialog_warning_no_folder": {"tr": "Lütfen düzenlenecek klasörü seçin!", "en": "Please select the folder to organize!"},
    "dialog_warning_no_scan_trash": {"tr": "Lütfen taranacak ve çöp klasörünü seçin!", "en": "Please select the scan folder and the trash folder!"},
    "dialog_report_title": {"tr": "İşlem Raporu", "en": "Operation Report"},

    "unknown_base": {"tr": "BilinmeyenTaban", "en": "UnknownBase"},
    "unknown_creator": {"tr": "BilinmeyenYaratici", "en": "UnknownCreator"},
    "category_concept": {"tr": "Konsept", "en": "Concept"},
    "category_background": {"tr": "Arkaplan", "en": "Background"},
    "folder_old_versions": {"tr": "Eski_Surumler", "en": "Old_Versions"},
    "folder_low_rated": {"tr": "Dusuk_Puanlilar", "en": "Low_Rated"},

    "mode_checkpoint": {"tr": "checkpoint", "en": "checkpoint"},
    "mode_lora": {"tr": "lora", "en": "lora"},
    "mode_clean": {"tr": "temizle", "en": "clean"},
}


def t(key: str, lang: str = "tr", **kwargs) -> str:
    """Return the translated string for `key` in `lang`, formatted with kwargs."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("tr", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
