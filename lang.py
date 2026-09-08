# -*- coding: utf-8 -*-
"""
LoRA Librarian - Language / Dil / 言語 / 语言 Module
Merkezi çok dilli (TR/EN/JA/ZH) metin sözlüğü.
Central multilingual (TR/EN/JA/ZH) text dictionary.
中央集約された多言語（TR/EN/JA/ZH）テキスト辞書。
中央多语言（TR/EN/JA/ZH）文本字典。
"""

TRANSLATIONS = {
    "app_title": {
        "tr": "LoRA Librarian - AI Model Kütüphane Yöneticisi",
        "en": "LoRA Librarian - AI Model Library Manager",
        "ja": "LoRA Librarian - AIモデルライブラリ管理ツール",
        "zh": "LoRA Librarian - AI模型库管理工具",
    },

    # Top bar
    "api_key_label": {
        "tr": "🔑 Civitai API Anahtarı (Opsiyonel):",
        "en": "🔑 Civitai API Key (Optional):",
        "ja": "🔑 Civitai APIキー（任意）：",
        "zh": "🔑 Civitai API 密钥（可选）：",
    },
    "lang_tr": {"tr": "Türkçe", "en": "Turkish", "ja": "トルコ語", "zh": "土耳其语"},
    "lang_en": {"tr": "İngilizce", "en": "English", "ja": "英語", "zh": "英语"},
    "lang_ja": {"tr": "Japonca", "en": "Japanese", "ja": "日本語", "zh": "日语"},
    "lang_zh": {"tr": "Çince", "en": "Chinese", "ja": "中国語", "zh": "中文"},
    "theme_dark": {"tr": "Koyu", "en": "Dark", "ja": "ダーク", "zh": "深色"},
    "theme_light": {"tr": "Açık", "en": "Light", "ja": "ライト", "zh": "浅色"},

    # Tabs
    "tab_checkpoint": {"tr": "🏰 Checkpoint Düzenle", "en": "🏰 Edit Checkpoints", "ja": "🏰 チェックポイント整理", "zh": "🏰 整理 Checkpoint"},
    "tab_lora": {"tr": "🎨 LoRA Düzenle", "en": "🎨 Edit LoRAs", "ja": "🎨 LoRA整理", "zh": "🎨 整理 LoRA"},
    "tab_clean": {"tr": "🧹 Akıllı Temizlik", "en": "🧹 Smart Cleanup", "ja": "🧹 スマートクリーンアップ", "zh": "🧹 智能清理"},
    "tab_rename": {"tr": "🏷️ İsim & Trigger", "en": "🏷️ Rename & Triggers", "ja": "🏷️ 名前とトリガー", "zh": "🏷️ 重命名与触发词"},

    # Path pickers
    "folder_checkpoint": {"tr": "Düzenlenecek Checkpoint Klasörü:", "en": "Checkpoint Folder to Organize:", "ja": "整理するチェックポイントフォルダ：", "zh": "要整理的 Checkpoint 文件夹："},
    "folder_lora": {"tr": "Düzenlenecek LoRA Klasörü:", "en": "LoRA Folder to Organize:", "ja": "整理するLoRAフォルダ：", "zh": "要整理的 LoRA 文件夹："},
    "folder_scan": {"tr": "Taranacak Ana Klasör:", "en": "Main Folder to Scan:", "ja": "スキャンするメインフォルダ：", "zh": "要扫描的主文件夹："},
    "folder_trash": {"tr": "Ayıklananların Gideceği Klasör (Çöp/Arşiv):", "en": "Destination for Removed Items (Trash/Archive):", "ja": "除外されたファイルの移動先（ゴミ箱/アーカイブ）：", "zh": "移除项目的目标文件夹（回收站/存档）："},
    "browse": {"tr": "Gözat", "en": "Browse", "ja": "参照", "zh": "浏览"},

    # Organize settings
    "switch_base_model": {"tr": "Tabana Göre (SDXL, Flux, Krea, Anima vb.)", "en": "By Base Model (SDXL, Flux, Krea, Anima etc.)", "ja": "ベースモデル別（SDXL、Flux、Krea、Animaなど）", "zh": "按基础模型分类（SDXL、Flux、Krea、Anima 等）"},
    "switch_fetch_meta": {"tr": "Eksik Kapakları/JSON'ları İndir", "en": "Download Missing Covers/JSON", "ja": "不足しているカバー画像/JSONをダウンロード", "zh": "下载缺失的封面/JSON"},
    "switch_category": {"tr": "Kategoriye Göre (Sadece Konsept & Arkaplan)", "en": "By Category (Concept & Background Only)", "ja": "カテゴリー別（コンセプト＆背景のみ）", "zh": "按类别分类（仅概念与背景）"},
    "creator_folder_label": {"tr": "Yaratıcıya (Creator) Göre Klasörle:", "en": "Organize by Creator:", "ja": "作成者別にフォルダ分け：", "zh": "按创作者整理："},
    "creator_hint": {"tr": "↳ 'Sadece Listeyi' seçerseniz aranacak isimleri buraya alt alta yazın:", "en": "↳ If you choose 'List Only', type the usernames below, one per line:", "ja": "↳「リストのみ」を選択した場合、検索するユーザー名を1行ずつ入力してください：", "zh": "↳ 如果选择“仅列表”，请在下方逐行输入要匹配的用户名："},
    "creator_mode_off": {"tr": "Kapalı", "en": "Off", "ja": "オフ", "zh": "关闭"},
    "creator_mode_all": {"tr": "Tüm Kullanıcıları Ayır", "en": "Separate All Creators", "ja": "すべての作成者を分ける", "zh": "分离所有创作者"},
    "creator_mode_list": {"tr": "Sadece Listedekileri Ayır", "en": "Only Separate Listed Ones", "ja": "リストにある作成者のみ分ける", "zh": "仅分离列表中的创作者"},
    "conflict_label": {"tr": "Aynı İsimde Dosya Çakışırsa:", "en": "If a Filename Conflict Occurs:", "ja": "同名ファイルが競合した場合：", "zh": "如果文件名发生冲突："},
    "conflict_rename": {"tr": "Yeniden Adlandır", "en": "Rename", "ja": "名前を変更", "zh": "重命名"},
    "conflict_skip": {"tr": "Es Geç (Dokunma)", "en": "Skip (Leave As Is)", "ja": "スキップ（そのままにする）", "zh": "跳过（保持不变）"},
    "conflict_overwrite": {"tr": "Üzerine Yaz (Eskisini Sil)", "en": "Overwrite (Delete Old)", "ja": "上書き（古いファイルを削除）", "zh": "覆盖（删除旧文件）"},

    "btn_organize_checkpoint": {"tr": "▶ Checkpointleri Düzenle", "en": "▶ Organize Checkpoints", "ja": "▶ チェックポイントを整理", "zh": "▶ 整理 Checkpoint"},
    "btn_organize_lora": {"tr": "▶ LoRA'ları Düzenle", "en": "▶ Organize LoRAs", "ja": "▶ LoRAを整理", "zh": "▶ 整理 LoRA"},
    "btn_start_clean": {"tr": "▶ Temizliği Başlat", "en": "▶ Start Cleanup", "ja": "▶ クリーンアップを開始", "zh": "▶ 开始清理"},

    # Cleanup tab
    "switch_old_versions": {"tr": "Eski Sürümleri Çöpe Taşı (Yenisi varsa eskisini ayıklar)", "en": "Move Old Versions to Trash (removes old ones if a newer version exists)", "ja": "古いバージョンをゴミ箱へ移動（新しいバージョンがある場合、古い方を除外）", "zh": "将旧版本移至回收站（如存在更新版本则移除旧版本）"},
    "switch_low_rating": {"tr": "Düşük Puanlıları Çöpe Taşı", "en": "Move Low-Rated Models to Trash", "ja": "低評価のモデルをゴミ箱へ移動", "zh": "将低评分模型移至回收站"},
    "min_rating_label": {"tr": "Min Puan:", "en": "Min Rating:", "ja": "最低評価：", "zh": "最低评分："},
    "conflict_trash_label": {"tr": "Çöp Klasöründe Çakışma Olursa:", "en": "If a Conflict Occurs in the Trash Folder:", "ja": "ゴミ箱フォルダで競合が発生した場合：", "zh": "如果回收站文件夹中发生冲突："},

    # Rename & Trigger tab
    "rename_info_text": {
        "tr": "Civitai'den model adını çekip LoRA dosyasını ve aynı isimdeki tüm ilişkili dosyaları (.civitai.info, önizleme görselleri, .json vb.) yeni isme çevirir. Eksik trigger word'leri de Civitai verisinden ya da örnek görsellerin komutlarından (sadece ilgili kelimeleri, tüm komutu değil) çıkarıp kaydeder.",
        "en": "Fetches the model's title from Civitai and renames the LoRA file plus every related file sharing its name (.civitai.info, preview images, .json, etc.). Also fills in missing trigger words from Civitai's data or from sample-image prompts (only the relevant keywords, not the full prompt).",
        "ja": "Civitaiからモデル名を取得し、LoRAファイルと同名のすべての関連ファイル（.civitai.info、プレビュー画像、.jsonなど）の名前を変更します。トリガーワードが不足している場合は、Civitaiのデータまたはサンプル画像のプロンプト（プロンプト全体ではなく関連するキーワードのみ）から抽出して保存します。",
        "zh": "从 Civitai 获取模型名称，并重命名 LoRA 文件及所有同名的相关文件（.civitai.info、预览图片、.json 等）。同时会从 Civitai 数据或示例图片的提示词中（仅提取相关关键词，而非完整提示词）补全缺失的触发词。",
    },
    "rename_mode_label": {"tr": "Yeniden Adlandırma Modu:", "en": "Rename Mode:", "ja": "リネームモード：", "zh": "重命名模式："},
    "rename_mode_meaningless": {"tr": "Sadece Anlamsız İsimler", "en": "Meaningless Names Only", "ja": "意味のない名前のみ", "zh": "仅无意义的文件名"},
    "rename_mode_all": {"tr": "Civitai Adından Farklı Olan Tümü", "en": "All That Differ From Civitai Title", "ja": "Civitaiのタイトルと異なるすべて", "zh": "所有与 Civitai 标题不同的文件"},
    "switch_fill_trigger": {"tr": "Eksik Trigger Word'leri Doldur (Civitai/örnek görsellerden)", "en": "Fill Missing Trigger Words (from Civitai / sample images)", "ja": "不足しているトリガーワードを補完（Civitai／サンプル画像から）", "zh": "补全缺失的触发词（来自 Civitai／示例图片）"},
    "btn_start_rename": {"tr": "▶ Yeniden Adlandır & Trigger Doldur", "en": "▶ Rename & Fill Triggers", "ja": "▶ リネーム＆トリガー補完を開始", "zh": "▶ 开始重命名并填充触发词"},

    "log_rename_meaningless_skip": {"tr": "   [Atlandı] İsim zaten anlamlı görünüyor.", "en": "   [Skipped] Name already looks meaningful.", "ja": "   [スキップ] 名前は既に意味があるようです。", "zh": "   [已跳过] 文件名看起来已经有意义。"},
    "log_renamed_files": {"tr": "   [🏷️] Yeniden adlandırıldı: {old} -> {new}", "en": "   [🏷️] Renamed: {old} -> {new}", "ja": "   [🏷️] 名前変更：{old} -> {new}", "zh": "   [🏷️] 已重命名：{old} -> {new}"},
    "log_trigger_from_api": {"tr": "   [🔑] Trigger word(ler) Civitai'den alındı: {words}", "en": "   [🔑] Trigger word(s) fetched from Civitai: {words}", "ja": "   [🔑] Civitaiからトリガーワードを取得：{words}", "zh": "   [🔑] 已从 Civitai 获取触发词：{words}"},
    "log_trigger_from_description": {"tr": "   [🔑] Model açıklamasından bulundu: {words}", "en": "   [🔑] Found in the model description: {words}", "ja": "   [🔑] モデルの説明文から検出：{words}", "zh": "   [🔑] 在模型描述中找到：{words}"},
    "log_trigger_extracted": {"tr": "   [🔑] Örnek görsellerden çıkarıldı: {words}", "en": "   [🔑] Extracted from sample images: {words}", "ja": "   [🔑] サンプル画像から抽出：{words}", "zh": "   [🔑] 已从示例图片中提取：{words}"},
    "log_trigger_none_found": {"tr": "   [–] Trigger word bulunamadı (örnek görsel/veri yetersiz).", "en": "   [–] No trigger word could be found (insufficient sample data).", "ja": "   [–] トリガーワードが見つかりませんでした（サンプルデータ不足）。", "zh": "   [–] 未能找到触发词（示例数据不足）。"},
    "log_trigger_already": {"tr": "   [–] Trigger word zaten mevcut, atlandı.", "en": "   [–] Trigger word already present, skipped.", "ja": "   [–] トリガーワードは既に存在するためスキップしました。", "zh": "   [–] 触发词已存在，已跳过。"},
    "log_no_metadata": {"tr": "   [!] Civitai verisi bulunamadı, atlandı.", "en": "   [!] No Civitai data found, skipped.", "ja": "   [!] Civitaiのデータが見つからないためスキップしました。", "zh": "   [!] 未找到 Civitai 数据，已跳过。"},

    "summary_text_rename": {
        "tr": "✅ İşlem Başarıyla Tamamlandı!\n\n🏷️ Yeniden Adlandırılan Model: {renamed}\n🔑 Trigger Word Dolduruldu: {triggers}",
        "en": "✅ Operation Completed Successfully!\n\n🏷️ Models Renamed: {renamed}\n🔑 Trigger Words Filled: {triggers}",
        "ja": "✅ 処理が正常に完了しました！\n\n🏷️ 名前変更されたモデル数：{renamed}\n🔑 トリガーワードを補完した数：{triggers}",
        "zh": "✅ 操作已成功完成！\n\n🏷️ 已重命名的模型数：{renamed}\n🔑 已补全触发词的数量：{triggers}",
    },

    # Log / status
    "status_label_prefix": {"tr": "Canlı İşlem Kaydı - Durum:", "en": "Live Process Log - Status:", "ja": "リアルタイム処理ログ - 状態：", "zh": "实时处理日志 - 状态："},
    "status_waiting": {"tr": "Bekliyor", "en": "Waiting", "ja": "待機中", "zh": "等待中"},
    "status_running": {"tr": "İşlem Yapılıyor...", "en": "Processing...", "ja": "処理中...", "zh": "处理中..."},
    "status_done": {"tr": "Tamamlandı!", "en": "Completed!", "ja": "完了しました！", "zh": "已完成！"},
    "log_ready": {
        "tr": "Sistem Hazır. Ayarlarınız otomatik olarak hatırlanır.\nSadece Konsept ve Arkaplan ayırma modülü devrede.",
        "en": "System Ready. Your settings are remembered automatically.\nOnly the Concept and Background separation module is active.",
        "ja": "システム準備完了。設定は自動的に保存されます。\nコンセプトと背景の分類モジュールのみが有効です。",
        "zh": "系统就绪。您的设置将自动保存。\n目前仅启用了概念与背景分类模块。",
    },
    "log_system_started": {"tr": "=== SİSTEM BAŞLADI ({mode}) ===", "en": "=== SYSTEM STARTED ({mode}) ===", "ja": "=== システム開始（{mode}）===", "zh": "=== 系统已启动（{mode}）==="},
    "log_total_models": {"tr": "[Bilgi] Toplam {count} model tespit edildi.", "en": "[Info] {count} models detected in total.", "ja": "[情報] 合計{count}個のモデルが検出されました。", "zh": "[信息] 共检测到 {count} 个模型。"},
    "log_model": {"tr": "[Model] {file}", "en": "[Model] {file}", "ja": "[モデル] {file}", "zh": "[模型] {file}"},
    "log_hash_reading": {"tr": "   [Hash] Okunuyor...", "en": "   [Hash] Reading...", "ja": "   [ハッシュ] 読み込み中...", "zh": "   [哈希] 正在读取..."},
    "log_api_saved": {"tr": "   [+] Veriler JSON olarak kaydedildi.", "en": "   [+] Data saved as JSON.", "ja": "   [+] データをJSONとして保存しました。", "zh": "   [+] 数据已保存为 JSON。"},
    "log_api_failed": {"tr": "   [!] API bağlantısı kurulamadı.", "en": "   [!] Could not connect to the API.", "ja": "   [!] APIに接続できませんでした。", "zh": "   [!] 无法连接到 API。"},
    "log_cover_downloaded": {"tr": "   [+] Kapak indirildi.", "en": "   [+] Cover image downloaded.", "ja": "   [+] カバー画像をダウンロードしました。", "zh": "   [+] 封面图片已下载。"},
    "log_cover_failed": {"tr": "   [!] Kapak indirilemedi (bağlantı hatası ya da geçersiz görsel).", "en": "   [!] Could not download cover image (connection error or invalid image).", "ja": "   [!] カバー画像をダウンロードできませんでした（接続エラーまたは無効な画像）。", "zh": "   [!] 无法下载封面图片（连接错误或图片无效）。"},
    "log_extracting_rating": {"tr": "   [Ayıklanıyor] Puan: {rating}/5", "en": "   [Extracting] Rating: {rating}/5", "ja": "   [除外中] 評価：{rating}/5", "zh": "   [正在移除] 评分：{rating}/5"},
    "log_folder_error": {"tr": "   [HATA] Klasör oluşturulamadı!", "en": "   [ERROR] Could not create folder!", "ja": "   [エラー] フォルダを作成できませんでした！", "zh": "   [错误] 无法创建文件夹！"},
    "log_skipped_exists": {"tr": "   [Atlandı] Hedefte '{file}' zaten var.", "en": "   [Skipped] '{file}' already exists at destination.", "ja": "   [スキップ] '{file}' は既に移動先に存在します。", "zh": "   [已跳过] 目标位置已存在 '{file}'。"},
    "log_renamed": {"tr": "   [Yeniden Adlandırıldı] -> {file}", "en": "   [Renamed] -> {file}", "ja": "   [名前変更済み] -> {file}", "zh": "   [已重命名] -> {file}"},
    "log_moved": {"tr": "   [->] Taşındı: {folder}", "en": "   [->] Moved to: {folder}", "ja": "   [->] 移動先：{folder}", "zh": "   [->] 已移动至：{folder}"},
    "log_move_failed": {"tr": "   [HATA] Taşınamadı!", "en": "   [ERROR] Could not move!", "ja": "   [エラー] 移動できませんでした！", "zh": "   [错误] 移动失败！"},
    "log_empty_folders": {"tr": "[Süpürge] {count} adet boş klasör silindi.", "en": "[Sweep] {count} empty folder(s) deleted.", "ja": "[お掃除] {count}個の空フォルダを削除しました。", "zh": "[清理] 已删除 {count} 个空文件夹。"},
    "log_summary_title": {"tr": "=== ÖZET RAPOR ===", "en": "=== SUMMARY REPORT ===", "ja": "=== 概要レポート ===", "zh": "=== 汇总报告 ==="},

    "summary_text": {
        "tr": "✅ İşlem Başarıyla Tamamlandı!\n\n📦 Düzenlenen/Taşınan Model: {moved}\n🗑️ Ayıklanan (Çöpe Giden) Model: {extracted}\n🧹 Silinen Boş Klasör Sayısı: {empty}\n\nHatalı kategoriler temizlendi, kütüphaneniz aslına döndü!",
        "en": "✅ Operation Completed Successfully!\n\n📦 Organized/Moved Models: {moved}\n🗑️ Extracted (Trashed) Models: {extracted}\n🧹 Empty Folders Deleted: {empty}\n\nMisplaced categories were cleaned up, your library is back in order!",
        "ja": "✅ 処理が正常に完了しました！\n\n📦 整理・移動されたモデル数：{moved}\n🗑️ 除外（ゴミ箱行き）されたモデル数：{extracted}\n🧹 削除された空フォルダ数：{empty}\n\n誤ったカテゴリーが整理され、ライブラリが元通りになりました！",
        "zh": "✅ 操作已成功完成！\n\n📦 已整理/移动的模型数：{moved}\n🗑️ 已移除（移至回收站）的模型数：{extracted}\n🧹 已删除的空文件夹数：{empty}\n\n错误分类已清理，您的模型库已恢复整洁！",
    },

    "dialog_warning_title": {"tr": "Hata", "en": "Warning", "ja": "警告", "zh": "警告"},
    "dialog_warning_no_folder": {"tr": "Lütfen düzenlenecek klasörü seçin!", "en": "Please select the folder to organize!", "ja": "整理するフォルダを選択してください！", "zh": "请选择要整理的文件夹！"},
    "dialog_warning_no_scan_trash": {"tr": "Lütfen taranacak ve çöp klasörünü seçin!", "en": "Please select the scan folder and the trash folder!", "ja": "スキャンフォルダとゴミ箱フォルダの両方を選択してください！", "zh": "请选择扫描文件夹和回收站文件夹！"},
    "dialog_report_title": {"tr": "İşlem Raporu", "en": "Operation Report", "ja": "処理レポート", "zh": "操作报告"},

    "unknown_base": {"tr": "BilinmeyenTaban", "en": "UnknownBase", "ja": "不明なベース", "zh": "未知基础模型"},
    "unknown_creator": {"tr": "BilinmeyenYaratici", "en": "UnknownCreator", "ja": "不明な作成者", "zh": "未知创作者"},
    "category_concept": {"tr": "Konsept", "en": "Concept", "ja": "コンセプト", "zh": "概念"},
    "category_background": {"tr": "Arkaplan", "en": "Background", "ja": "背景", "zh": "背景"},
    "folder_old_versions": {"tr": "Eski_Surumler", "en": "Old_Versions", "ja": "古いバージョン", "zh": "旧版本"},
    "folder_low_rated": {"tr": "Dusuk_Puanlilar", "en": "Low_Rated", "ja": "低評価", "zh": "低评分"},

    "mode_checkpoint": {"tr": "checkpoint", "en": "checkpoint", "ja": "checkpoint", "zh": "checkpoint"},
    "mode_lora": {"tr": "lora", "en": "lora", "ja": "lora", "zh": "lora"},
    "mode_clean": {"tr": "temizle", "en": "clean", "ja": "clean", "zh": "clean"},
}


def t(key: str, lang: str = "tr", **kwargs) -> str:
    """Return the translated string for `key` in `lang`, formatted with kwargs."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", entry.get("tr", key)))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
