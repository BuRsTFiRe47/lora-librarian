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

from PySide6.QtCore import Qt, QObject, Signal, QSize, QRectF
from PySide6.QtGui import QColor, QPainter, QLinearGradient, QBrush, QPen, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QSlider, QPlainTextEdit,
    QProgressBar, QStackedWidget, QScrollArea, QFrame, QFileDialog, QMessageBox,
    QDialog, QButtonGroup, QSizePolicy,
)

from lang import t
import engine as E
from engine import (
    Engine, APP_VERSION, LANG_CODES, LANG_LABELS, CONFLICT_CODES, CONFLICT_KEYS,
    CREATOR_CODES, CREATOR_KEYS, RENAME_MODE_CODES, RENAME_MODE_KEYS, messagebox,
)

# ----------------------------------------------------------------------
# Theme (black / blue)
# ----------------------------------------------------------------------
ACCENT = "#2f7bff"
ACCENT_HOVER = "#2569e0"
GRADIENT_STOPS = ["#050814", "#1e3a8a", "#38bdf8"]

ACTION_COLORS = [
    ("act_cp", "#2b7a0b", "#3e9915"), ("act_lr", "#0b5b7a", "#157199"), ("act_tm", "#b5261a", "#d63424"),
    ("act_rn", "#7a4a0b", "#996015"), ("act_dup", "#9333ea", "#7c3aed"),
]

PALETTES = {
    "dark": {
        "bg": "#05070c", "header": "#0a0e16", "card": "#0d1119", "hover": "#131a26",
        "text": "#e6ebf5", "side_text": "#a8b3c4", "border": "#1c2432", "log_bg": "#04060a",
        "muted": "#7d8aa0", "input": "#0a0e16", "btn_border": "#2a3547",
    },
    "light": {
        "bg": "#f1f4f9", "header": "#ffffff", "card": "#ffffff", "hover": "#dbe3f1",
        "text": "#16202f", "side_text": "#31435c", "border": "#dde3ee", "log_bg": "#eaeef5",
        "muted": "#5c6b81", "input": "#ffffff", "btn_border": "#ffffff",
    },
}


def build_qss(theme):
    p = PALETTES.get(theme, PALETTES["dark"])
    action_css = "\n".join(
        f'QPushButton#{i} {{ background: {c}; }} QPushButton#{i}:hover {{ background: {h}; }} '
        f'QPushButton#{i}:disabled {{ background: {p["hover"]}; color: {p["muted"]}; }}'
        for i, c, h in ACTION_COLORS
    )
    return f"""
    QWidget {{ color: {p['text']}; font-size: 13px; }}
    QMainWindow, QWidget#root {{ background: {p['bg']}; }}
    QScrollArea {{ border: none; background: transparent; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}
    QStackedWidget {{ background: transparent; }}
    QWidget#page {{ background: transparent; }}

    QFrame#header {{ background: {p['header']}; border: none; }}
    QFrame#card {{ background: {p['card']}; border: 1px solid {p['border']}; border-radius: 14px; }}
    QFrame#card QLabel {{ background: transparent; }}

    QLabel {{ background: transparent; }}
    QLabel#muted {{ color: {p['muted']}; font-size: 12px; }}
    QLabel#title {{ font-size: 18px; font-weight: 700; }}
    QLabel#version {{ color: {p['muted']}; font-size: 11px; }}
    QLabel#bold {{ font-weight: 700; }}
    QLabel#percent {{ color: {ACCENT}; font-size: 16px; font-weight: 700; }}
    QLabel#status {{ font-weight: 700; }}

    QLineEdit, QPlainTextEdit, QComboBox {{
        background: {p['input']}; border: 1px solid {p['border']}; border-radius: 8px; padding: 7px 10px;
        selection-background-color: {ACCENT}; selection-color: white;
    }}
    QLineEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{ border: 1px solid {ACCENT}; }}
    QLineEdit:disabled, QPlainTextEdit:disabled {{ color: {p['muted']}; }}
    QPlainTextEdit#log {{
        background: {p['log_bg']}; color: {ACCENT}; font-family: Consolas, Menlo, "DejaVu Sans Mono", monospace;
        font-size: 12px; border: 1px solid {p['border']};
    }}

    QComboBox {{ padding-right: 28px; min-height: 20px; background: {ACCENT}; border: none; color: white; font-weight: 600; }}
    QComboBox:hover {{ background: {ACCENT_HOVER}; }}
    QComboBox::drop-down {{ border: none; width: 24px; }}
    QComboBox QAbstractItemView {{
        background: {p['card']}; color: {p['text']}; border: 1px solid {p['border']};
        selection-background-color: {ACCENT}; selection-color: white; outline: none;
    }}

    QPushButton {{
        background: transparent; border: 1px solid {p['border']}; border-radius: 12px; padding: 7px 14px;
        color: {p['side_text']};
    }}
    QPushButton:hover {{ background: {p['hover']}; }}
    QPushButton:disabled {{ color: {p['muted']}; }}

    QPushButton#nav {{ text-align: left; border: none; padding: 11px 14px; border-radius: 12px; color: {p['side_text']}; font-size: 13px; }}
    QPushButton#nav:hover {{ background: {p['hover']}; }}
    QPushButton#nav:checked {{ background: {ACCENT}; color: white; font-weight: 600; }}

    QPushButton#seg, QPushButton#segL, QPushButton#segR {{ border: 1px solid {p['border']}; border-radius: 0; padding: 6px 12px; color: {p['side_text']}; margin-left: -1px; }}
    QPushButton#seg:checked, QPushButton#segL:checked, QPushButton#segR:checked {{ background: {ACCENT}; color: white; border: 1px solid {ACCENT}; }}
    QPushButton#segL {{ border-top-left-radius: 12px; border-bottom-left-radius: 12px; margin-left: 0; }}
    QPushButton#segR {{ border-top-right-radius: 12px; border-bottom-right-radius: 12px; }}

    QPushButton#accent {{ background: {ACCENT}; color: white; border: 2px solid {p['btn_border']}; font-weight: 600; }}
    QPushButton#accent:hover {{ background: {ACCENT_HOVER}; }}
    QPushButton[role="action"] {{
        color: white; font-size: 14px; font-weight: 700; border: 2px solid {p['btn_border']};
        border-radius: 14px; padding: 12px 34px; min-height: 22px;
    }}
    {action_css}
    QPushButton#danger {{ background: #b5261a; color: white; border: none; padding: 5px 10px; }}
    QPushButton#danger:hover {{ background: #d63424; }}
    QPushButton#histitem {{ text-align: left; border: none; }}

    QProgressBar {{ background: {p['log_bg']}; border: 1px solid {p['border']}; border-radius: 8px; height: 14px; text-align: center; color: transparent; }}
    QProgressBar::chunk {{ background: {ACCENT}; border-radius: 7px; }}

    QSlider::groove:horizontal {{ height: 6px; background: {p['border']}; border-radius: 3px; }}
    QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 3px; }}
    QSlider::handle:horizontal {{ background: {ACCENT}; width: 16px; height: 16px; margin: -6px 0; border-radius: 8px; }}

    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 0; }}
    QScrollBar::handle:vertical {{ background: {p['border']}; border-radius: 5px; min-height: 30px; }}
    QScrollBar::handle:vertical:hover {{ background: {p['muted']}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QDialog {{ background: {p['bg']}; }}
    QMessageBox {{ background: {p['card']}; }}
    """


class GradientStrip(QWidget):
    """Thin near-black -> blue -> cyan accent line along the top edge."""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(4)

    def paintEvent(self, _e):
        g = QLinearGradient(0, 0, self.width(), 0)
        n = len(GRADIENT_STOPS) - 1
        for i, c in enumerate(GRADIENT_STOPS):
            g.setColorAt(i / n, QColor(c))
        QPainter(self).fillRect(self.rect(), QBrush(g))


class Switch(QCheckBox):
    """iOS-style toggle (pill + knob) with the label to its right."""
    W, H = 40, 22

    def __init__(self, text=""):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(30)

    def sizeHint(self):
        s = super().sizeHint()
        return QSize(self.W + 12 + self.fontMetrics().horizontalAdvance(self.text()) + 4, max(30, s.height()))

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        y = (self.height() - self.H) / 2
        track = QRectF(1, y, self.W, self.H)
        on = self.isChecked()
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(ACCENT) if on else QColor(120, 130, 150, 120))
        p.drawRoundedRect(track, self.H / 2, self.H / 2)
        d = self.H - 6
        x = track.right() - d - 3 if on else track.left() + 3
        p.setBrush(QColor("white"))
        p.drawEllipse(QRectF(x, y + 3, d, d))
        p.setPen(QColor(PALETTES[getattr(self.window(), 'eng', None).theme if getattr(self.window(), 'eng', None) else 'dark']['text']))
        p.drawText(QRectF(self.W + 12, 0, self.width() - self.W - 12, self.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, self.text())


class Bridge(QObject):
    """Thread-safe path from engine worker threads to the UI thread."""
    log = Signal(str)
    progress = Signal(float)
    status = Signal(str)
    busy = Signal(bool)
    message = Signal(str, str, str)


class HistoryDialog(QDialog):
    def __init__(self, win, target_var, target_edit):
        super().__init__(win)
        self.win, self.var, self.edit = win, target_var, target_edit
        self.setWindowTitle(t("history_window_title", win.eng.lang))
        self.resize(560, 400)
        self.outer = QVBoxLayout(self)
        self.outer.setContentsMargins(14, 14, 14, 14)
        self._fill()

    def _fill(self):
        while self.outer.count():
            it = self.outer.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        eng = self.win.eng
        if not eng.klasor_gecmisi:
            lbl = QLabel(t("history_empty", eng.lang))
            lbl.setObjectName("muted")
            lbl.setAlignment(Qt.AlignCenter)
            self.outer.addWidget(lbl)
            return
        for yol in list(eng.klasor_gecmisi):
            row = QFrame()
            row.setObjectName("card")
            h = QHBoxLayout(row)
            h.setContentsMargins(6, 4, 6, 4)
            b = QPushButton(yol)
            b.setObjectName("histitem")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, y=yol: self._pick(y))
            d = QPushButton("✕")
            d.setObjectName("danger")
            d.clicked.connect(lambda _=False, y=yol: self._remove(y))
            h.addWidget(b, 1)
            h.addWidget(d)
            self.outer.addWidget(row)
        self.outer.addStretch(1)

    def _pick(self, yol):
        self.edit.setText(yol)
        self.win.eng._gecmise_ekle(yol)
        self.accept()

    def _remove(self, yol):
        if yol in self.win.eng.klasor_gecmisi:
            self.win.eng.klasor_gecmisi.remove(yol)
        self._fill()


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

        outer.addWidget(GradientStrip())
        outer.addWidget(self._build_header())

        mid = QHBoxLayout()
        mid.setContentsMargins(16, 14, 16, 8)
        mid.setSpacing(12)
        mid.addWidget(self._build_sidebar())
        mid.addWidget(self._build_pages(), 1)
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

        lbl = QLabel(t("api_key_label", self.lang))
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
        side.setFixedWidth(200)
        v = QVBoxLayout(side)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)
        self.nav_group = QButtonGroup(side)
        self.nav_group.setExclusive(True)
        self.nav_buttons = {}
        for key, label_key in self.NAV:
            b = QPushButton(t(label_key, self.lang).replace("&", "&&"))
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
        grid.addWidget(self._label(label_text, "bold"), row, 0, 1, 3)
        edit = QLineEdit(var.get())
        edit.textChanged.connect(var.set)
        hist = QPushButton("🕘")
        hist.setFixedWidth(40)
        hist.setCursor(Qt.PointingHandCursor)
        hist.clicked.connect(lambda: HistoryDialog(self, var, edit).exec())
        browse = QPushButton(t("browse", self.lang))
        browse.setObjectName("accent")
        browse.setCursor(Qt.PointingHandCursor)

        def pick():
            yol = QFileDialog.getExistingDirectory(self, "", edit.text() or "")
            if yol:
                edit.setText(yol)
                self.eng._gecmise_ekle(yol)
        browse.clicked.connect(pick)
        grid.addWidget(edit, row + 1, 0)
        grid.addWidget(hist, row + 1, 1)
        grid.addWidget(browse, row + 1, 2)

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

    def _switch(self, text, var):
        s = Switch(text)
        s.setChecked(bool(var.get()))
        s.toggled.connect(var.set)
        return s

    def _combo(self, display_values, current_display, on_change):
        cb = QComboBox()
        cb.addItems(display_values)
        cb.setCurrentIndex(max(0, display_values.index(current_display)) if current_display in display_values else 0)
        cb.currentIndexChanged.connect(on_change)
        cb.setCursor(Qt.PointingHandCursor)
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
        b.clicked.connect(lambda: self.eng.baslat_thread(mod))
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
