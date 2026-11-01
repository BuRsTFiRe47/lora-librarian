# -*- coding: utf-8 -*-
"""
LoRA Librarian
==============
AI model (Checkpoint / LoRA) kütüphanenizi otomatik olarak düzenleyen,
eksik kapak/etiket verisini Civitai'den tamamlayan ve düşük puanlı ya
da eski sürümleri ayıklayan modern, çift dilli masaüstü uygulaması.
Windows / macOS / Linux (PySide6 / Qt 6).

A modern, bilingual desktop app that automatically organizes your AI
model (Checkpoint / LoRA) library, fills in missing cover/tag data
from Civitai, and separates out low-rated or outdated versions.
Windows / macOS / Linux (PySide6 / Qt 6).

License: MIT
"""

import sys
import time

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QPlainTextEdit,
    QProgressBar, QStackedWidget, QScrollArea, QFrame, QFileDialog, QMessageBox,
    QButtonGroup,
)

from lang import t
import engine as E
from engine import (
    Engine, APP_VERSION, LANG_CODES, LANG_LABELS, CONFLICT_CODES, CONFLICT_KEYS,
    CREATOR_CODES, CREATOR_KEYS, RENAME_MODE_CODES, RENAME_MODE_KEYS, messagebox,
)
from breeze import build_qss, Check, Combo, PathField, plain


class Bridge(QObject):
    """Thread-safe path from engine worker threads to the UI thread."""
    log = Signal(str)
    progress = Signal(float)
    status = Signal(str)
    busy = Signal(bool)
    message = Signal(str, str, str)


class MainWindow(QMainWindow):
    NAV = [("cp", "tab_checkpoint"), ("lr", "tab_lora"), ("tm", "tab_clean"), ("rn", "tab_rename"), ("dup", "tab_duplicate")]

    def __init__(self):
        super().__init__()
        self.eng = Engine()
        self.bridge = Bridge()
        self.eng.on_log = self.bridge.log.emit
        self.eng.on_progress = self.bridge.progress.emit
        self.eng.on_status = self.bridge.status.emit
        self.eng.on_busy = self.bridge.busy.emit
        self.eng.creator_text_getter = self._creator_text
        messagebox.handler = self.bridge.message.emit

        self.bridge.log.connect(self._append_log)
        self.bridge.progress.connect(self._set_progress)
        self.bridge.status.connect(lambda s: self.lbl_status.setText(s))
        self.bridge.busy.connect(self._set_busy)
        self.bridge.message.connect(self._show_message)

        self.current_page = "cp"
        self._log_cache = ""
        self.creator_boxes = {}
        self.action_buttons = []
        self.path_fields = []

        geo = getattr(self.eng, "_pending_geometry", None) or "1180x800"
        try:
            w, h = [int(x) for x in str(geo).lower().split("+")[0].split("x")]
            self.resize(max(900, w), max(640, h))
        except Exception:
            self.resize(1180, 800)

        self.apply_theme()
        self.build_ui()

    # ------------------------------------------------------------ helpers
    @property
    def lang(self):
        return self.eng.lang

    def apply_theme(self):
        QApplication.instance().setStyleSheet(build_qss(self.eng.theme))

    def _creator_text(self, kind):
        box = self.creator_boxes.get(kind)
        if box is not None:
            return box.toPlainText().strip()
        return (self.eng._creator_text_cp if kind == "cp" else self.eng._creator_text_lr) or ""

    def _stash_creator_text(self):
        self.eng._creator_text_cp = self._creator_text("cp")
        self.eng._creator_text_lr = self._creator_text("lr")

    # ----------------------------------------------------------- UI build
    def build_ui(self):
        self.setWindowTitle(t("app_title", self.lang))
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._build_header())

        mid = QHBoxLayout()
        mid.setContentsMargins(0, 0, 0, 0)
        mid.setSpacing(0)
        mid.addWidget(self._build_sidebar())
        vline = QFrame()
        vline.setObjectName("vline")
        mid.addWidget(vline)
        pages_wrap = QWidget()
        pw = QVBoxLayout(pages_wrap)
        pw.setContentsMargins(16, 14, 8, 8)
        pw.addWidget(self._build_pages())
        mid.addWidget(pages_wrap, 1)
        outer.addLayout(mid, 5)
        outer.addWidget(self._build_log(), 2)

        self.show_page(self.current_page)
        if self._log_cache:
            self.log_box.setPlainText(self._log_cache)
            self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())
        else:
            self._append_log(t("log_ready", self.lang))

    def _segmented(self, labels, current, on_click):
        box = QWidget()
        h = QHBoxLayout(box)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        grp = QButtonGroup(box)
        grp.setExclusive(True)
        for i, text in enumerate(labels):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setObjectName("seg")
            b.setCursor(Qt.PointingHandCursor)
            if i == 0:
                b.setProperty("segpos", "L")
            b.setChecked(i == current)
            b.clicked.connect(lambda _=False, idx=i: on_click(idx))
            grp.addButton(b, i)
            h.addWidget(b)
        # rounded ends
        btns = grp.buttons()
        btns[0].setObjectName("segL")
        btns[-1].setObjectName("segR")
        if len(btns) == 1:
            btns[0].setObjectName("seg")
        for b in btns:
            b.style().unpolish(b)
            b.style().polish(b)
        box._grp = grp
        return box

    def _build_header(self):
        header = QFrame()
        header.setObjectName("header")
        h = QHBoxLayout(header)
        h.setContentsMargins(20, 12, 20, 12)

        tv = QVBoxLayout()
        tv.setSpacing(0)
        a = QLabel("LoRA Librarian")
        a.setObjectName("title")
        b = QLabel(f"v{APP_VERSION}")
        b.setObjectName("version")
        tv.addWidget(a)
        tv.addWidget(b)
        h.addLayout(tv)
        h.addStretch(1)

        lbl = QLabel(plain(t("api_key_label", self.lang)))
        lbl.setObjectName("bold")
        h.addWidget(lbl)
        self.api_edit = QLineEdit(self.eng.api_key.get())
        self.api_edit.setEchoMode(QLineEdit.Password)
        self.api_edit.setFixedWidth(220)
        self.api_edit.textChanged.connect(self.eng.api_key.set)
        h.addWidget(self.api_edit)
        h.addSpacing(16)

        langs = self._segmented([LANG_LABELS[c] for c in LANG_CODES], LANG_CODES.index(self.lang) if self.lang in LANG_CODES else 0, self._on_lang)
        h.addWidget(langs)
        h.addSpacing(10)
        themes = self._segmented([t("theme_dark", self.lang), t("theme_light", self.lang)], 0 if self.eng.theme == "dark" else 1, self._on_theme)
        h.addWidget(themes)
        return header

    def _on_lang(self, idx):
        code = LANG_CODES[idx]
        if code == self.eng.lang:
            return
        self._stash_creator_text()
        self.eng.lang = code
        self.creator_boxes = {}
        self.build_ui()

    def _on_theme(self, idx):
        self.eng.theme = "dark" if idx == 0 else "light"
        self.apply_theme()

    def _build_sidebar(self):
        side = QWidget()
        side.setFixedWidth(210)
        v = QVBoxLayout(side)
        v.setContentsMargins(0, 10, 0, 0)
        v.setSpacing(2)
        self.nav_group = QButtonGroup(side)
        self.nav_group.setExclusive(True)
        self.nav_buttons = {}
        for key, label_key in self.NAV:
            b = QPushButton(plain(t(label_key, self.lang)).replace("&", "&&"))
            b.setObjectName("nav")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, k=key: self.show_page(k))
            self.nav_group.addButton(b)
            self.nav_buttons[key] = b
            v.addWidget(b)
        v.addStretch(1)
        return side

    def show_page(self, key):
        self.current_page = key
        keys = [k for k, _ in self.NAV]
        self.stack.setCurrentIndex(keys.index(key))
        self.nav_buttons[key].setChecked(True)

    def _build_pages(self):
        self.stack = QStackedWidget()
        self.action_buttons = []
        self.path_fields = []
        builders = {"cp": self._page_cp, "lr": self._page_lr, "tm": self._page_tm, "rn": self._page_rn, "dup": self._page_dup}
        for key, _ in self.NAV:
            page = QWidget()
            page.setObjectName("page")
            lay = QVBoxLayout(page)
            lay.setContentsMargins(0, 0, 8, 0)
            lay.setSpacing(10)
            builders[key](lay)
            lay.addStretch(1)
            sc = QScrollArea()
            sc.setWidgetResizable(True)
            sc.setWidget(page)
            self.stack.addWidget(sc)
        return self.stack

    # ----------------------------------------------------- small builders
    def _card(self):
        f = QFrame()
        f.setObjectName("card")
        return f

    def _label(self, text, name=None, wrap=False):
        l = QLabel(text)
        if name:
            l.setObjectName(name)
        l.setWordWrap(wrap)
        return l

    def _path_row(self, grid, row, var, label_text):
        grid.addWidget(self._label(label_text, "bold"), row, 0)
        e = self.eng
        field = PathField(
            var.get(), var.set, lambda: e.klasor_gecmisi, e._gecmise_ekle,
            lambda p: e.klasor_gecmisi.remove(p) if p in e.klasor_gecmisi else None,
            t("browse", self.lang), t("history_window_title", self.lang), t("history_empty", self.lang),
        )
        grid.addWidget(field, row + 1, 0)
        self.path_fields.append((field, var))

    def _path_card(self, lay, var, label_text, var2=None):
        c = self._card()
        g = QGridLayout(c)
        g.setContentsMargins(14, 12, 14, 14)
        g.setColumnStretch(0, 1)
        g.setVerticalSpacing(6)
        self._path_row(g, 0, var, label_text)
        if var2 is not None:
            self._path_row(g, 2, var2, t("folder_trash", self.lang))
        lay.addWidget(c)

    def _start(self, mod):
        """Remember the folders in use (typed paths too), then run."""
        import os
        for field, _var in self.path_fields:
            p = field.text().strip()
            if p and os.path.isdir(p):
                self.eng._gecmise_ekle(p)
        self.eng.baslat_thread(mod)

    def _switch(self, text, var):
        s = Check(text)
        s.setChecked(bool(var.get()))
        s.toggled.connect(var.set)
        return s

    def _combo(self, display_values, current_display, on_change):
        cb = Combo()
        cb.addItems(display_values)
        cb.setCurrentIndex(max(0, display_values.index(current_display)) if current_display in display_values else 0)
        cb.currentIndexChanged.connect(on_change)
        cb.setMinimumWidth(190)
        return cb

    def _coded_combo(self, codes, keys, var):
        values = [t(keys[c], self.lang) for c in codes]
        cur = var.get() if var.get() in codes else codes[0]
        cb = self._combo(values, t(keys[cur], self.lang), lambda i: var.set(codes[i]))
        return cb

    def _conflict_row(self, lay, var, label_key="conflict_label"):
        row = QHBoxLayout()
        row.setContentsMargins(10, 0, 0, 0)
        row.addWidget(self._label(t(label_key, self.lang), "bold"))
        row.addWidget(self._coded_combo(CONFLICT_CODES, CONFLICT_KEYS, var))
        row.addStretch(1)
        lay.addLayout(row)

    def _action_button(self, lay, text_key, obj, mod):
        b = QPushButton(t(text_key, self.lang).replace("&", "&&"))
        b.setObjectName(obj)
        b.setProperty("role", "action")
        b.setCursor(Qt.PointingHandCursor)
        b.clicked.connect(lambda: self._start(mod))
        self.action_buttons.append(b)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(b)
        row.addStretch(1)
        lay.addSpacing(6)
        lay.addLayout(row)

    # -------------------------------------------------------------- pages
    def _settings_block(self, lay, kind):
        e = self.eng
        pre = "cp" if kind == "cp" else "lr"
        taban, resim, kat = getattr(e, f"{pre}_chk_taban"), getattr(e, f"{pre}_chk_resim"), getattr(e, f"{pre}_chk_kategori")
        ymod, cak = getattr(e, f"{pre}_yaratici_mod"), getattr(e, f"{pre}_cakisma_mod")

        sw = QVBoxLayout()
        sw.setContentsMargins(10, 2, 0, 2)
        sw.addWidget(self._switch(t("switch_base_model", self.lang), taban))
        sw.addWidget(self._switch(t("switch_fetch_meta", self.lang), resim))
        sw.addWidget(self._switch(t("switch_category", self.lang), kat))
        lay.addLayout(sw)

        c = self._card()
        g = QGridLayout(c)
        g.setContentsMargins(14, 12, 14, 14)
        g.addWidget(self._label(t("creator_folder_label", self.lang), "bold"), 0, 0)
        box = QPlainTextEdit()
        box.setFixedHeight(90)
        box.setPlainText(e._creator_text_cp if kind == "cp" else e._creator_text_lr)
        box.setEnabled(ymod.get() == "list")
        self.creator_boxes[kind] = box

        def on_mode(i):
            ymod.set(CREATOR_CODES[i])
            box.setEnabled(CREATOR_CODES[i] == "list")
        g.addWidget(self._coded_combo_cb(CREATOR_CODES, CREATOR_KEYS, ymod, on_mode), 0, 1, Qt.AlignLeft)
        g.addWidget(self._label(t("creator_hint", self.lang), "muted", wrap=True), 1, 0, 1, 2)
        g.addWidget(box, 2, 0, 1, 2)
        g.setColumnStretch(1, 1)
        lay.addWidget(c)

        self._conflict_row(lay, cak)

    def _coded_combo_cb(self, codes, keys, var, cb_extra):
        values = [t(keys[c], self.lang) for c in codes]
        cur = var.get() if var.get() in codes else codes[0]
        return self._combo(values, t(keys[cur], self.lang), cb_extra)

    def _page_cp(self, lay):
        self._path_card(lay, self.eng.cp_kaynak, t("folder_checkpoint", self.lang))
        self._settings_block(lay, "cp")
        self._action_button(lay, "btn_organize_checkpoint", "act_cp", "checkpoint")

    def _page_lr(self, lay):
        self._path_card(lay, self.eng.lr_kaynak, t("folder_lora", self.lang))
        self._settings_block(lay, "lr")
        self._action_button(lay, "btn_organize_lora", "act_lr", "lora")

    def _page_tm(self, lay):
        e = self.eng
        self._path_card(lay, e.tm_kaynak, t("folder_scan", self.lang), e.tm_hedef)
        sw = QVBoxLayout()
        sw.setContentsMargins(10, 2, 0, 2)
        sw.addWidget(self._switch(t("switch_old_versions", self.lang), e.tm_chk_eski))
        sw.addWidget(self._switch(t("switch_low_rating", self.lang), e.tm_chk_puan))
        lay.addLayout(sw)

        row = QHBoxLayout()
        row.setContentsMargins(46, 0, 0, 0)
        row.addWidget(self._label(t("min_rating_label", self.lang)))
        sl = QSlider(Qt.Horizontal)
        sl.setRange(0, 50)
        sl.setValue(int(round(e.tm_min_puan.get() * 10)))
        sl.setFixedWidth(220)
        val = QLabel(f"{e.tm_min_puan.get():.1f}")
        val.setFixedWidth(34)

        def on_slide(v):
            e.tm_min_puan.set(v / 10.0)
            val.setText(f"{v / 10.0:.1f}")
        sl.valueChanged.connect(on_slide)
        row.addWidget(sl)
        row.addWidget(val)
        row.addStretch(1)
        lay.addLayout(row)

        self._conflict_row(lay, e.tm_cakisma_mod, "conflict_trash_label")
        self._action_button(lay, "btn_start_clean", "act_tm", "temizle")

    def _page_rn(self, lay):
        e = self.eng
        self._path_card(lay, e.rn_kaynak, t("folder_lora", self.lang))
        info = self._card()
        il = QVBoxLayout(info)
        il.setContentsMargins(14, 10, 14, 10)
        il.addWidget(self._label(t("rename_info_text", self.lang), "muted", wrap=True))
        lay.addWidget(info)

        row = QHBoxLayout()
        row.setContentsMargins(10, 0, 0, 0)
        row.addWidget(self._label(t("rename_mode_label", self.lang), "bold"))
        row.addWidget(self._coded_combo(RENAME_MODE_CODES, RENAME_MODE_KEYS, e.rn_mode))
        row.addStretch(1)
        lay.addLayout(row)

        sw = QVBoxLayout()
        sw.setContentsMargins(10, 2, 0, 2)
        sw.addWidget(self._switch(t("switch_fill_trigger", self.lang), e.rn_chk_trigger))
        sw.addWidget(self._switch(t("switch_use_samples", self.lang), e.rn_chk_samples))
        lay.addLayout(sw)

        self._conflict_row(lay, e.rn_cakisma_mod)
        self._action_button(lay, "btn_start_rename", "act_rn", "rename")

    def _page_dup(self, lay):
        e = self.eng
        self._path_card(lay, e.dup_kaynak, t("folder_scan", self.lang), e.dup_hedef)
        info = self._card()
        il = QVBoxLayout(info)
        il.setContentsMargins(14, 10, 14, 10)
        il.addWidget(self._label(t("dup_info_text", self.lang), "muted", wrap=True))
        lay.addWidget(info)
        self._conflict_row(lay, e.dup_cakisma_mod, "conflict_trash_label")
        self._action_button(lay, "btn_start_duplicate", "act_dup", "duplicate")

    # ---------------------------------------------------------------- log
    def _build_log(self):
        c = self._card()
        c.setContentsMargins(0, 0, 0, 0)
        v = QVBoxLayout(c)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(6)
        top = QHBoxLayout()
        self.lbl_status = self._label(f'{t("status_label_prefix", self.lang)} {t("status_waiting", self.lang)}', "status")
        top.addWidget(self.lbl_status)
        top.addStretch(1)
        save = QPushButton(t("btn_save_log", self.lang))
        save.setCursor(Qt.PointingHandCursor)
        save.clicked.connect(self.save_log)
        top.addWidget(save)
        self.lbl_percent = self._label("%0", "percent")
        top.addWidget(self.lbl_percent)
        v.addLayout(top)
        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(14)
        v.addWidget(self.progress)
        self.log_box = QPlainTextEdit()
        self.log_box.setObjectName("log")
        self.log_box.setReadOnly(True)
        v.addWidget(self.log_box, 1)
        wrap = QWidget()
        wl = QVBoxLayout(wrap)
        wl.setContentsMargins(16, 8, 16, 16)
        wl.addWidget(c)
        return wrap

    def _append_log(self, msg, cache=True):
        if cache:
            self._log_cache += msg + "\n"
        self.log_box.appendPlainText(msg)
        sb = self.log_box.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_progress(self, frac):
        frac = max(0.0, min(1.0, frac))
        self.progress.setValue(int(frac * 1000))
        self.lbl_percent.setText(f"%{int(frac * 100)}")

    def _set_busy(self, busy):
        for b in self.action_buttons:
            b.setEnabled(not busy)

    def _show_message(self, kind, title, text):
        (QMessageBox.warning if kind == "warning" else QMessageBox.information)(self, title, text)

    def save_log(self):
        content = self.log_box.toPlainText()
        if not content.strip():
            return
        name = f"lora-librarian-log-{time.strftime('%Y%m%d-%H%M%S')}.txt"
        path, _ = QFileDialog.getSaveFileName(self, "", name, "Text (*.txt);;All files (*)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            QMessageBox.warning(self, t("dialog_warning_title", self.lang), t("log_save_failed", self.lang))

    # -------------------------------------------------------------- close
    def closeEvent(self, ev):
        self._stash_creator_text()
        self.eng.ayarlari_kaydet(f"{self.width()}x{self.height()}")
        super().closeEvent(ev)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
