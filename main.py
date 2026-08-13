# -*- coding: utf-8 -*-
"""
LoRA Librarian
==============
AI model (Checkpoint / LoRA) kütüphanenizi otomatik olarak düzenleyen,
eksik kapak/etiket verisini Civitai'den tamamlayan ve düşük puanlı ya
da eski sürümleri ayıklayan modern, çift dilli masaüstü uygulaması.

A modern, bilingual desktop app that automatically organizes your AI
model (Checkpoint / LoRA) library, fills in missing cover/tag data
from Civitai, and separates out low-rated or outdated versions.

License: MIT
"""

import os
import sys
import hashlib
import shutil
import time
import json
import threading

import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox

from lang import t
from base_models import normalize_base_model

APP_VERSION = "2.0.0"
API_DOMAIN = "civitai.red"

CONFLICT_CODES = ["rename", "skip", "overwrite"]
CONFLICT_KEYS = {"rename": "conflict_rename", "skip": "conflict_skip", "overwrite": "conflict_overwrite"}

CREATOR_CODES = ["off", "all", "list"]
CREATOR_KEYS = {"off": "creator_mode_off", "all": "creator_mode_all", "list": "creator_mode_list"}

# Theme-aware color tuples: (light_mode, dark_mode)
ACCENT = ("#0a7d63", "#00ffcc")
LOG_BG = ("#f2f2f2", "#121212")
CARD_BG = ("#e8e8e8", "#2b2b2b")


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


SETTINGS_PATH = os.path.join(app_dir(), "ayarlar.json")
HASH_CACHE_PATH = os.path.join(app_dir(), "hash_cache.json")


class LoraLibrarianApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "tr"
        self.islem_devam_ediyor = False
        self.hash_cache = self._hash_cache_yukle()
        self.session = requests.Session()

        self.api_key = ctk.StringVar()

        # --- CHECKPOINT ---
        self.cp_kaynak = ctk.StringVar()
        self.cp_chk_taban = ctk.BooleanVar(value=True)
        self.cp_chk_kategori = ctk.BooleanVar(value=False)
        self.cp_chk_resim = ctk.BooleanVar(value=True)
        self.cp_yaratici_mod = ctk.StringVar(value="off")
        self.cp_cakisma_mod = ctk.StringVar(value="rename")

        # --- LORA ---
        self.lr_kaynak = ctk.StringVar()
        self.lr_chk_taban = ctk.BooleanVar(value=True)
        self.lr_chk_kategori = ctk.BooleanVar(value=True)
        self.lr_chk_resim = ctk.BooleanVar(value=True)
        self.lr_yaratici_mod = ctk.StringVar(value="off")
        self.lr_cakisma_mod = ctk.StringVar(value="rename")

        # --- TEMİZLİK ---
        self.tm_kaynak = ctk.StringVar()
        self.tm_hedef = ctk.StringVar()
        self.tm_chk_puan = ctk.BooleanVar(value=True)
        self.tm_chk_eski = ctk.BooleanVar(value=True)
        self.tm_min_puan = ctk.DoubleVar(value=4.0)
        self.tm_cakisma_mod = ctk.StringVar(value="rename")

        self.istatistik_tasinan = 0
        self.istatistik_ayiklanan = 0
        self.istatistik_bos_klasor = 0

        self._creator_text_cp = ""
        self._creator_text_lr = ""

        self.ayarlari_yukle()

        ctk.set_appearance_mode("dark")
        self.geometry("1000x920")

        self.arayuz_ciz()
        self.ayarlari_uygula_widget()
        self.protocol("WM_DELETE_WINDOW", self.kapatirken_kaydet)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def arayuz_ciz(self):
        for w in self.winfo_children():
            w.destroy()

        self.title(t("app_title", self.lang))

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 0))

        api_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        api_frame.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(api_frame, text=t("api_key_label", self.lang), font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10))
        ctk.CTkEntry(api_frame, textvariable=self.api_key, width=380, show="*").pack(side="left")

        controls_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        controls_frame.pack(side="right")

        theme_values = [t("theme_dark", self.lang), t("theme_light", self.lang)]
        self.theme_seg = ctk.CTkSegmentedButton(controls_frame, values=theme_values, command=self._on_theme_change)
        current_theme_display = t("theme_dark", self.lang) if self.theme == "dark" else t("theme_light", self.lang)
        self.theme_seg.set(current_theme_display)
        self.theme_seg.pack(side="right", padx=(10, 0))

        lang_values = [t("lang_tr", self.lang), t("lang_en", self.lang)]
        self.lang_seg = ctk.CTkSegmentedButton(controls_frame, values=lang_values, command=self._on_lang_change)
        self.lang_seg.set(t("lang_tr", self.lang) if self.lang == "tr" else t("lang_en", self.lang))
        self.lang_seg.pack(side="right")

        self.sekme = ctk.CTkTabview(self)
        self.sekme.pack(fill="x", padx=20, pady=10)

        self.tab_cp = self.sekme.add(t("tab_checkpoint", self.lang))
        self.tab_lr = self.sekme.add(t("tab_lora", self.lang))
        self.tab_tm = self.sekme.add(t("tab_clean", self.lang))

        self.sekme_checkpoint_doldur()
        self.sekme_lora_doldur()
        self.sekme_temizle_doldur()

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        baslik_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        baslik_frame.pack(fill="x", padx=10, pady=(5, 0))

        self.lbl_durum = ctk.CTkLabel(baslik_frame, text=f'{t("status_label_prefix", self.lang)} {t("status_waiting", self.lang)}', font=("Segoe UI", 12, "bold"))
        self.lbl_durum.pack(side="left")

        self.lbl_yuzde = ctk.CTkLabel(baslik_frame, text="%0", font=("Segoe UI", 14, "bold"), text_color=ACCENT)
        self.lbl_yuzde.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(log_frame, progress_color=ACCENT)
        self.progress_bar.pack(fill="x", padx=10, pady=(5, 5))
        self.progress_bar.set(0)

        self.log_kutusu = ctk.CTkTextbox(log_frame, state="disabled", font=("Consolas", 12), text_color=ACCENT, fg_color=LOG_BG)
        self.log_kutusu.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_yaz(t("log_ready", self.lang))

    def _on_lang_change(self, value):
        self.lang = "tr" if value == t("lang_tr", self.lang) else "en"
        self._creator_text_cp = self.metin_kutusunu_oku(self.cp_yaratici_kutu) if hasattr(self, "cp_yaratici_kutu") else self._creator_text_cp
        self._creator_text_lr = self.metin_kutusunu_oku(self.lr_yaratici_kutu) if hasattr(self, "lr_yaratici_kutu") else self._creator_text_lr
        self.arayuz_ciz()
        self.ayarlari_uygula_widget()

    def _on_theme_change(self, value):
        self.theme = "dark" if value == t("theme_dark", self.lang) else "light"
        ctk.set_appearance_mode(self.theme)

    def yol_secici_ciz(self, parent, kaynak_var, hedef_var=None, metin=None):
        frame = ctk.CTkFrame(parent, fg_color=CARD_BG)
        frame.pack(fill="x", pady=10)

        ctk.CTkLabel(frame, text=metin, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(frame, textvariable=kaynak_var, width=550).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkButton(frame, text=t("browse", self.lang), width=80, command=lambda: self.klasor_sec(kaynak_var)).grid(row=1, column=1, pady=5)

        if hedef_var is not None:
            ctk.CTkLabel(frame, text=t("folder_trash", self.lang), font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
            ctk.CTkEntry(frame, textvariable=hedef_var, width=550).grid(row=3, column=0, padx=10, pady=(5, 10), sticky="w")
            ctk.CTkButton(frame, text=t("browse", self.lang), width=80, command=lambda: self.klasor_sec(hedef_var)).grid(row=3, column=1, pady=(5, 10))

    def yaratici_menu_guncelle(self, kod, kutu):
        kutu.configure(state="normal" if kod == "list" else "disabled")

    def _conflict_display_values(self):
        return [t(CONFLICT_KEYS[c], self.lang) for c in CONFLICT_CODES]

    def _conflict_display_from_code(self, code):
        return t(CONFLICT_KEYS.get(code, "conflict_rename"), self.lang)

    def _conflict_code_from_display(self, display):
        for c in CONFLICT_CODES:
            if t(CONFLICT_KEYS[c], self.lang) == display:
                return c
        return "rename"

    def _creator_display_values(self):
        return [t(CREATOR_KEYS[c], self.lang) for c in CREATOR_CODES]

    def _creator_display_from_code(self, code):
        return t(CREATOR_KEYS.get(code, "creator_mode_off"), self.lang)

    def _creator_code_from_display(self, display):
        for c in CREATOR_CODES:
            if t(CREATOR_KEYS[c], self.lang) == display:
                return c
        return "off"

    def ayarlar_ciz(self, parent, mod_tipi):
        chk_taban = self.cp_chk_taban if mod_tipi == "cp" else self.lr_chk_taban
        chk_resim = self.cp_chk_resim if mod_tipi == "cp" else self.lr_chk_resim
        chk_kategori = self.cp_chk_kategori if mod_tipi == "cp" else self.lr_chk_kategori
        yaratici_mod = self.cp_yaratici_mod if mod_tipi == "cp" else self.lr_yaratici_mod
        cakisma_mod = self.cp_cakisma_mod if mod_tipi == "cp" else self.lr_cakisma_mod

        ust_frame = ctk.CTkFrame(parent, fg_color="transparent")
        ust_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkSwitch(ust_frame, text=t("switch_base_model", self.lang), variable=chk_taban).grid(row=0, column=0, sticky="w", pady=5)
        ctk.CTkSwitch(ust_frame, text=t("switch_fetch_meta", self.lang), variable=chk_resim).grid(row=0, column=1, sticky="w", padx=30, pady=5)
        ctk.CTkSwitch(ust_frame, text=t("switch_category", self.lang), variable=chk_kategori).grid(row=1, column=0, columnspan=2, sticky="w", pady=10)

        yaratici_frame = ctk.CTkFrame(parent, fg_color=CARD_BG)
        yaratici_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(yaratici_frame, text=t("creator_folder_label", self.lang), font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        yaratici_kutu = ctk.CTkTextbox(yaratici_frame, height=80, width=420)

        opt = ctk.CTkOptionMenu(
            yaratici_frame,
            values=self._creator_display_values(),
            command=lambda disp, kutu=yaratici_kutu, var=yaratici_mod: (
                var.set(self._creator_code_from_display(disp)),
                self.yaratici_menu_guncelle(var.get(), kutu),
            ),
        )
        opt.set(self._creator_display_from_code(yaratici_mod.get()))
        opt.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        ctk.CTkLabel(yaratici_frame, text=t("creator_hint", self.lang), font=("Segoe UI", 10, "italic"), text_color="gray").grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 5))

        yaratici_kutu.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10))
        yaratici_kutu.configure(state="normal" if yaratici_mod.get() == "list" else "disabled")

        if mod_tipi == "cp":
            self.cp_yaratici_kutu = yaratici_kutu
            self.metin_kutusunu_doldur(yaratici_kutu, self._creator_text_cp)
        else:
            self.lr_yaratici_kutu = yaratici_kutu
            self.metin_kutusunu_doldur(yaratici_kutu, self._creator_text_lr)
        if yaratici_mod.get() != "list":
            yaratici_kutu.configure(state="disabled")

        cakisma_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cakisma_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(cakisma_frame, text=t("conflict_label", self.lang), font=("Segoe UI", 12, "bold")).pack(side="left", padx=10)
        opt2 = ctk.CTkOptionMenu(
            cakisma_frame,
            values=self._conflict_display_values(),
            command=lambda disp, var=cakisma_mod: var.set(self._conflict_code_from_display(disp)),
        )
        opt2.set(self._conflict_display_from_code(cakisma_mod.get()))
        opt2.pack(side="left", padx=10)

    def sekme_checkpoint_doldur(self):
        self.yol_secici_ciz(self.tab_cp, self.cp_kaynak, metin=t("folder_checkpoint", self.lang))
        self.ayarlar_ciz(self.tab_cp, "cp")
        self.btn_cp = ctk.CTkButton(self.tab_cp, text=t("btn_organize_checkpoint", self.lang), fg_color="#2b7a0b", hover_color="#3e9915", command=lambda: self.baslat_thread("checkpoint"))
        self.btn_cp.pack(pady=10)

    def sekme_lora_doldur(self):
        self.yol_secici_ciz(self.tab_lr, self.lr_kaynak, metin=t("folder_lora", self.lang))
        self.ayarlar_ciz(self.tab_lr, "lr")
        self.btn_lr = ctk.CTkButton(self.tab_lr, text=t("btn_organize_lora", self.lang), fg_color="#0b5b7a", hover_color="#157199", command=lambda: self.baslat_thread("lora"))
        self.btn_lr.pack(pady=10)

    def sekme_temizle_doldur(self):
        self.yol_secici_ciz(self.tab_tm, self.tm_kaynak, self.tm_hedef, metin=t("folder_scan", self.lang))

        c_frame = ctk.CTkFrame(self.tab_tm, fg_color="transparent")
        c_frame.pack(anchor="w", padx=20, pady=10)

        ctk.CTkSwitch(c_frame, text=t("switch_old_versions", self.lang), variable=self.tm_chk_eski).grid(row=0, column=0, sticky="w", pady=10)
        ctk.CTkSwitch(c_frame, text=t("switch_low_rating", self.lang), variable=self.tm_chk_puan).grid(row=1, column=0, sticky="w", pady=(10, 0))

        slider_frame = ctk.CTkFrame(c_frame, fg_color="transparent")
        slider_frame.grid(row=2, column=0, sticky="w", pady=5, padx=30)
        ctk.CTkLabel(slider_frame, text=t("min_rating_label", self.lang)).pack(side="left")
        puan_lbl = ctk.CTkLabel(slider_frame, text=f"{self.tm_min_puan.get():.1f}", width=30)
        slider = ctk.CTkSlider(slider_frame, from_=0.0, to=5.0, number_of_steps=50, variable=self.tm_min_puan, command=lambda v: puan_lbl.configure(text=f"{v:.1f}"))
        slider.pack(side="left", padx=10)
        puan_lbl.pack(side="left")

        cakisma_frame = ctk.CTkFrame(self.tab_tm, fg_color="transparent")
        cakisma_frame.pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(cakisma_frame, text=t("conflict_trash_label", self.lang), font=("Segoe UI", 12, "bold")).pack(side="left")
        opt3 = ctk.CTkOptionMenu(
            cakisma_frame,
            values=self._conflict_display_values(),
            command=lambda disp: self.tm_cakisma_mod.set(self._conflict_code_from_display(disp)),
        )
        opt3.set(self._conflict_display_from_code(self.tm_cakisma_mod.get()))
        opt3.pack(side="left", padx=10)

        self.btn_tm = ctk.CTkButton(self.tab_tm, text=t("btn_start_clean", self.lang), fg_color="#b5261a", hover_color="#d63424", command=lambda: self.baslat_thread("temizle"))
        self.btn_tm.pack(pady=20)

    # ------------------------------------------------------------------
    # Settings persistence (Ayarlar / Settings)
    # ------------------------------------------------------------------
    def metin_kutusunu_doldur(self, kutu, metin):
        kutu.configure(state="normal")
        kutu.delete("1.0", "end")
        if metin:
            kutu.insert("1.0", metin)

    def metin_kutusunu_oku(self, kutu):
        return kutu.get("1.0", "end-1c").strip()

    def ayarlari_yukle(self):
        self.theme = "dark"
        if not os.path.exists(SETTINGS_PATH):
            return
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                ayarlar = json.load(f)
            self.lang = ayarlar.get("lang", "tr")
            self.theme = ayarlar.get("theme", "dark")
            self._pending_geometry = ayarlar.get("geometry", "1000x920")
            self.api_key.set(ayarlar.get("api_key", ""))

            if "cp" in ayarlar:
                d = ayarlar["cp"]
                self.cp_kaynak.set(d.get("kaynak", ""))
                self.cp_chk_taban.set(d.get("taban", True))
                self.cp_chk_kategori.set(d.get("kategori", False))
                self.cp_chk_resim.set(d.get("resim", True))
                self.cp_yaratici_mod.set(d.get("yaratici_mod", "off"))
                self.cp_cakisma_mod.set(d.get("cakisma_mod", "rename"))
                self._creator_text_cp = d.get("yaratici_liste", "")

            if "lr" in ayarlar:
                d = ayarlar["lr"]
                self.lr_kaynak.set(d.get("kaynak", ""))
                self.lr_chk_taban.set(d.get("taban", True))
                self.lr_chk_kategori.set(d.get("kategori", True))
                self.lr_chk_resim.set(d.get("resim", True))
                self.lr_yaratici_mod.set(d.get("yaratici_mod", "off"))
                self.lr_cakisma_mod.set(d.get("cakisma_mod", "rename"))
                self._creator_text_lr = d.get("yaratici_liste", "")

            if "tm" in ayarlar:
                d = ayarlar["tm"]
                self.tm_kaynak.set(d.get("kaynak", ""))
                self.tm_hedef.set(d.get("hedef", ""))
                self.tm_chk_puan.set(d.get("puan", True))
                self.tm_chk_eski.set(d.get("eski", True))
                self.tm_min_puan.set(d.get("min_puan", 4.0))
                self.tm_cakisma_mod.set(d.get("cakisma_mod", "rename"))
        except Exception:
            pass

    def ayarlari_uygula_widget(self):
        """Apply the geometry saved from a previous run, once widgets exist."""
        geo = getattr(self, "_pending_geometry", None)
        if geo:
            try:
                self.geometry(geo)
            except Exception:
                pass

    def kapatirken_kaydet(self):
        ayarlar = {
            "lang": self.lang,
            "theme": self.theme,
            "geometry": self.geometry(),
            "api_key": self.api_key.get(),
            "cp": {
                "kaynak": self.cp_kaynak.get(), "taban": self.cp_chk_taban.get(), "kategori": self.cp_chk_kategori.get(),
                "resim": self.cp_chk_resim.get(), "yaratici_mod": self.cp_yaratici_mod.get(), "cakisma_mod": self.cp_cakisma_mod.get(),
                "yaratici_liste": self.metin_kutusunu_oku(self.cp_yaratici_kutu),
            },
            "lr": {
                "kaynak": self.lr_kaynak.get(), "taban": self.lr_chk_taban.get(), "kategori": self.lr_chk_kategori.get(),
                "resim": self.lr_chk_resim.get(), "yaratici_mod": self.lr_yaratici_mod.get(), "cakisma_mod": self.lr_cakisma_mod.get(),
                "yaratici_liste": self.metin_kutusunu_oku(self.lr_yaratici_kutu),
            },
            "tm": {
                "kaynak": self.tm_kaynak.get(), "hedef": self.tm_hedef.get(), "puan": self.tm_chk_puan.get(),
                "eski": self.tm_chk_eski.get(), "min_puan": self.tm_min_puan.get(), "cakisma_mod": self.tm_cakisma_mod.get(),
            },
        }
        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(ayarlar, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
        self._hash_cache_kaydet()
        self.destroy()

    def _hash_cache_yukle(self):
        if os.path.exists(HASH_CACHE_PATH):
            try:
                with open(HASH_CACHE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _hash_cache_kaydet(self):
        try:
            with open(HASH_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.hash_cache, f)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def klasor_sec(self, degisken):
        yol = filedialog.askdirectory()
        if yol:
            degisken.set(yol)

    def log_yaz(self, mesaj):
        self.log_kutusu.configure(state="normal")
        self.log_kutusu.insert("end", mesaj + "\n")
        self.log_kutusu.see("end")
        self.log_kutusu.configure(state="disabled")

    def get_hash(self, filepath):
        """SHA-256 hash with a size+mtime cache so re-scanning an
        already-processed library doesn't re-hash unchanged files
        (optimization / optimizasyon)."""
        try:
            stat = os.stat(filepath)
            cache_key = filepath
            cached = self.hash_cache.get(cache_key)
            if cached and cached.get("mtime") == stat.st_mtime and cached.get("size") == stat.st_size:
                return cached["hash"]
        except Exception:
            stat = None

        self.log_yaz(t("log_hash_reading", self.lang))
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                sha256.update(chunk)
        digest = sha256.hexdigest()

        if stat is not None:
            self.hash_cache[filepath] = {"mtime": stat.st_mtime, "size": stat.st_size, "hash": digest}
        return digest

    def dosya_temizle_adi(self, isim):
        for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
            isim = isim.replace(c, "_")
        return isim.strip() or "_"

    def bos_klasorleri_temizle(self, baslangic_dizini):
        temizlenen = 0
        for root, dirs, files in os.walk(baslangic_dizini, topdown=False):
            for name in dirs:
                klasor_yolu = os.path.join(root, name)
                if not os.listdir(klasor_yolu):
                    try:
                        os.rmdir(klasor_yolu)
                        temizlenen += 1
                    except Exception:
                        pass
        if temizlenen > 0:
            self.istatistik_bos_klasor += temizlenen
            self.log_yaz(t("log_empty_folders", self.lang, count=temizlenen))

    def dosyalari_tasi(self, dosya_adi, kaynak_klasor, hedef_tam_yol, cakisma_kodu, islem_tipi):
        if not os.path.exists(hedef_tam_yol):
            try:
                os.makedirs(hedef_tam_yol)
            except Exception:
                self.log_yaz(t("log_folder_error", self.lang))
                return

        base_adi = os.path.splitext(dosya_adi)[0]
        aranan = base_adi + "."
        basarili_tasima = False

        for f in os.listdir(kaynak_klasor):
            if f.startswith(aranan) or f == dosya_adi:
                eski = os.path.join(kaynak_klasor, f)
                yeni = os.path.join(hedef_tam_yol, f)

                if os.path.abspath(eski) == os.path.abspath(yeni):
                    continue

                if os.path.exists(yeni):
                    if cakisma_kodu == "skip":
                        self.log_yaz(t("log_skipped_exists", self.lang, file=f))
                        continue
                    elif cakisma_kodu == "rename":
                        isim, uzanti = os.path.splitext(f)
                        sayac = 1
                        while os.path.exists(yeni):
                            yeni = os.path.join(hedef_tam_yol, f"{isim}_{sayac}{uzanti}")
                            sayac += 1
                        self.log_yaz(t("log_renamed", self.lang, file=os.path.basename(yeni)))
                    elif cakisma_kodu == "overwrite":
                        try:
                            os.remove(yeni)
                        except Exception:
                            pass
                try:
                    shutil.move(eski, yeni)
                    basarili_tasima = True
                    if cakisma_kodu != "rename" or not os.path.exists(yeni):
                        self.log_yaz(t("log_moved", self.lang, folder=os.path.basename(hedef_tam_yol)))
                except Exception:
                    self.log_yaz(t("log_move_failed", self.lang))

        if basarili_tasima:
            if islem_tipi in ["checkpoint", "lora"]:
                self.istatistik_tasinan += 1
            else:
                self.istatistik_ayiklanan += 1

    # ------------------------------------------------------------------
    # Main engine
    # ------------------------------------------------------------------
    def baslat_thread(self, mod):
        if mod == "checkpoint":
            kaynak = self.cp_kaynak.get()
            hedef = kaynak
            config = {"taban": self.cp_chk_taban.get(), "kategori": self.cp_chk_kategori.get(), "resim": self.cp_chk_resim.get(),
                      "y_mod": self.cp_yaratici_mod.get(), "y_liste": self.metin_kutusunu_oku(self.cp_yaratici_kutu), "cakisma": self.cp_cakisma_mod.get()}
            if not kaynak:
                return messagebox.showwarning(t("dialog_warning_title", self.lang), t("dialog_warning_no_folder", self.lang))
        elif mod == "lora":
            kaynak = self.lr_kaynak.get()
            hedef = kaynak
            config = {"taban": self.lr_chk_taban.get(), "kategori": self.lr_chk_kategori.get(), "resim": self.lr_chk_resim.get(),
                      "y_mod": self.lr_yaratici_mod.get(), "y_liste": self.metin_kutusunu_oku(self.lr_yaratici_kutu), "cakisma": self.lr_cakisma_mod.get()}
            if not kaynak:
                return messagebox.showwarning(t("dialog_warning_title", self.lang), t("dialog_warning_no_folder", self.lang))
        else:
            kaynak, hedef = self.tm_kaynak.get(), self.tm_hedef.get()
            config = {"puan": self.tm_chk_puan.get(), "min_p": self.tm_min_puan.get(), "eski": self.tm_chk_eski.get(), "cakisma": self.tm_cakisma_mod.get()}
            if not kaynak or not hedef:
                return messagebox.showwarning(t("dialog_warning_title", self.lang), t("dialog_warning_no_scan_trash", self.lang))

        if self.islem_devam_ediyor:
            return
        self.btn_cp.configure(state="disabled")
        self.btn_lr.configure(state="disabled")
        self.btn_tm.configure(state="disabled")
        threading.Thread(target=self.ana_motor, args=(mod, kaynak, hedef, config), daemon=True).start()

    def ana_motor(self, mod, kaynak, hedef, config):
        self.islem_devam_ediyor = True

        self.istatistik_tasinan = 0
        self.istatistik_ayiklanan = 0
        self.istatistik_bos_klasor = 0
        self.progress_bar.set(0)
        self.lbl_yuzde.configure(text="%0")
        self.lbl_durum.configure(text=f'{t("status_label_prefix", self.lang)} {t("status_running", self.lang)}')

        api = self.api_key.get()
        headers = {"Authorization": f"Bearer {api}"} if api else {}
        model_gecmisi = {}

        hedef_yaraticilar = []
        if mod in ["checkpoint", "lora"] and config["y_mod"] == "list":
            hedef_yaraticilar = [x.strip().lower() for x in config["y_liste"].split("\n") if x.strip()]

        self.log_yaz(t("log_system_started", self.lang, mode=mod.upper()))

        islem_listesi = []
        for root, dirs, files in os.walk(kaynak):
            for file in files:
                if file.endswith((".safetensors", ".ckpt")):
                    islem_listesi.append((root, file))

        toplam_model = len(islem_listesi)
        self.log_yaz(t("log_total_models", self.lang, count=toplam_model))

        unknown_base = t("unknown_base", self.lang)
        unknown_creator = t("unknown_creator", self.lang)

        for index, (root, file) in enumerate(islem_listesi):
            dosya_yolu = os.path.join(root, file)
            if not os.path.exists(dosya_yolu):
                continue

            base_adi = os.path.splitext(file)[0]
            self.log_yaz(t("log_model", self.lang, file=file))

            resim_var = any(os.path.exists(os.path.join(root, base_adi + ext)) for ext in [".png", ".jpg"])
            json_var = any(os.path.exists(os.path.join(root, base_adi + ext)) for ext in [".json", ".civitai.info"])

            m_id, t_taban_raw, t_yaratici = None, None, unknown_creator
            t_tags = []
            api_lazim, model_verisi = True, None

            for info_p in [os.path.join(root, base_adi + ".json"), os.path.join(root, base_adi + ".civitai.info")]:
                if os.path.exists(info_p):
                    try:
                        with open(info_p, "r", encoding="utf-8") as f:
                            j = json.load(f)
                            m_id = j.get("modelId") or j.get("id")
                            t_taban_raw = j.get("baseModel")
                            t_yaratici = j.get("creator", {}).get("username", unknown_creator)
                            t_tags = j.get("tags", [])
                            if mod in ["checkpoint", "lora"] and config["y_mod"] == "off" and resim_var and (not config.get("kategori") or t_tags):
                                api_lazim = False
                    except Exception:
                        pass
                    break

            if mod == "temizle":
                api_lazim = True

            if api_lazim:
                if m_id:
                    url = f"https://{API_DOMAIN}/api/v1/model-versions/{m_id}"
                else:
                    url = f"https://{API_DOMAIN}/api/v1/model-versions/by-hash/{self.get_hash(dosya_yolu)}"
                try:
                    cevap = self.session.get(url, headers=headers, timeout=10)
                    if cevap.status_code == 200:
                        model_verisi = cevap.json()
                        m_id = model_verisi.get("modelId")
                        t_taban_raw = model_verisi.get("baseModel", t_taban_raw)

                        kategori_lazim = config.get("kategori") and not t_tags
                        yaratici_lazim = config.get("y_mod") != "off" and t_yaratici == unknown_creator

                        if mod in ["checkpoint", "lora"] and m_id and (yaratici_lazim or kategori_lazim):
                            try:
                                model_ana_veri = self.session.get(f"https://{API_DOMAIN}/api/v1/models/{m_id}", headers=headers, timeout=5)
                                if model_ana_veri.status_code == 200:
                                    ana_json = model_ana_veri.json()
                                    if yaratici_lazim:
                                        t_yaratici = ana_json.get("creator", {}).get("username", unknown_creator)
                                    if kategori_lazim:
                                        t_tags = ana_json.get("tags", [])
                            except Exception:
                                pass

                        if mod in ["checkpoint", "lora"] and not json_var and config.get("resim"):
                            try:
                                json_yolu = os.path.join(root, base_adi + ".json")
                                with open(json_yolu, "w", encoding="utf-8") as jf:
                                    if t_yaratici != unknown_creator:
                                        model_verisi["creator"] = {"username": t_yaratici}
                                    if t_tags:
                                        model_verisi["tags"] = t_tags
                                    json.dump(model_verisi, jf, indent=4)
                                self.log_yaz(t("log_api_saved", self.lang))
                            except Exception:
                                pass
                except Exception:
                    self.log_yaz(t("log_api_failed", self.lang))

            t_taban = self.dosya_temizle_adi(normalize_base_model(t_taban_raw, unknown_base))
            t_yaratici = self.dosya_temizle_adi(t_yaratici)

            t_kategori = ""
            if mod in ["checkpoint", "lora"] and config.get("kategori"):
                t_tags_lower = []
                for tag in t_tags:
                    if isinstance(tag, str):
                        t_tags_lower.append(tag.lower())
                    elif isinstance(tag, dict) and "name" in tag:
                        t_tags_lower.append(str(tag["name"]).lower())

                if "concept" in t_tags_lower or "konsept" in t_tags_lower:
                    t_kategori = t("category_concept", self.lang)
                elif "background" in t_tags_lower or "arkaplan" in t_tags_lower:
                    t_kategori = t("category_background", self.lang)

            if mod == "temizle" and model_verisi:
                v_id = model_verisi.get("id")
                rating = model_verisi.get("stats", {}).get("rating", 0)
                if config["puan"] and 0 < rating < config["min_p"]:
                    self.log_yaz(t("log_extracting_rating", self.lang, rating=rating))
                    self.dosyalari_tasi(file, root, os.path.join(hedef, t("folder_low_rated", self.lang)), config["cakisma"], mod)
                    continue
                if config["eski"] and m_id:
                    if m_id in model_gecmisi:
                        kayitli = model_gecmisi[m_id]
                        if v_id > kayitli["v_id"]:
                            self.dosyalari_tasi(kayitli["file"], kayitli["root"], os.path.join(hedef, t("folder_old_versions", self.lang)), config["cakisma"], mod)
                            model_gecmisi[m_id] = {"file": file, "v_id": v_id, "root": root}
                        elif v_id < kayitli["v_id"]:
                            self.dosyalari_tasi(file, root, os.path.join(hedef, t("folder_old_versions", self.lang)), config["cakisma"], mod)
                            continue
                    else:
                        model_gecmisi[m_id] = {"file": file, "v_id": v_id, "root": root}

            elif mod in ["checkpoint", "lora"]:
                if config["resim"] and not resim_var and model_verisi and model_verisi.get("images"):
                    try:
                        r_img = self.session.get(model_verisi["images"][0]["url"], timeout=10).content
                        with open(os.path.join(root, base_adi + ".png"), "wb") as f:
                            f.write(r_img)
                        self.log_yaz(t("log_cover_downloaded", self.lang))
                    except Exception:
                        pass

                yol_parcalari = [kaynak]
                if config["taban"] and t_taban != unknown_base:
                    yol_parcalari.append(t_taban)
                if config["kategori"] and t_kategori:
                    yol_parcalari.append(t_kategori)
                if config["y_mod"] == "all" and t_yaratici != unknown_creator:
                    yol_parcalari.append(t_yaratici)
                elif config["y_mod"] == "list" and t_yaratici != unknown_creator:
                    if t_yaratici.lower() in hedef_yaraticilar:
                        yol_parcalari.append(t_yaratici)

                dinamik_hedef = os.path.join(*yol_parcalari)
                self.dosyalari_tasi(file, root, dinamik_hedef, config["cakisma"], mod)

            ilerleme_orani = (index + 1) / toplam_model if toplam_model > 0 else 1
            self.progress_bar.set(ilerleme_orani)
            self.lbl_yuzde.configure(text=f"%{int(ilerleme_orani * 100)}")
            if api_lazim:
                time.sleep(0.5)

        self.bos_klasorleri_temizle(kaynak)
        self._hash_cache_kaydet()

        ozet_metni = t(
            "summary_text", self.lang,
            moved=self.istatistik_tasinan,
            extracted=self.istatistik_ayiklanan,
            empty=self.istatistik_bos_klasor,
        )

        self.log_yaz(f'{t("log_summary_title", self.lang)}\n{ozet_metni}')
        self.lbl_durum.configure(text=f'{t("status_label_prefix", self.lang)} {t("status_done", self.lang)}')
        self.islem_devam_ediyor = False
        self.btn_cp.configure(state="normal")
        self.btn_lr.configure(state="normal")
        self.btn_tm.configure(state="normal")
        messagebox.showinfo(t("dialog_report_title", self.lang), ozet_metni)


if __name__ == "__main__":
    app = LoraLibrarianApp()
    app.mainloop()
