# -*- coding: utf-8 -*-
"""
Shared look & feel (KDE Breeze-Dark inspired: slate background, coral accent)
and the small custom widgets used by both LoRA Librarian and Preview Smith.

Paylaşılan görünüm (KDE Breeze-Dark esinli: arduvaz zemin, mercan vurgu) ve
özel bileşenler. / Shared theme + custom widgets.

License: MIT
"""

import re

from PySide6.QtCore import Qt, QRectF, QPointF, QPoint, QSize
from PySide6.QtGui import QColor, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QLineEdit, QPushButton, QFileDialog, QHBoxLayout,
    QWidget, QMenu, QWidgetAction, QAbstractButton,
)

# Colours measured from the reference screenshot (Breeze Dark + coral accent)
PALETTES = {
    "dark": {
        "bg": "#2c3746", "ctrl": "#323e4f", "ctrl_hover": "#3b4859", "inset": "#252e3a",
        "border": "#606974", "soft": "#46515f", "track": "#414a58",
        "text": "#eff0f1", "muted": "#a3acb8", "disabled": "#6f7883",
        "accent": "#f77067", "accent_hover": "#f98a82", "accent_press": "#e85f55",
        "accent_dim": "#925357", "danger": "#da4453", "log_bg": "#1f2732", "log_text": "#cfd6de",
        "on_accent": "#ffffff", "check_box": "#6f7883",
    },
    "light": {
        "bg": "#eff0f1", "ctrl": "#f7f8f9", "ctrl_hover": "#e4e7ea", "inset": "#fcfcfc",
        "border": "#bdc3c7", "soft": "#d3d7da", "track": "#cdd1d5",
        "text": "#232629", "muted": "#5e6773", "disabled": "#9aa1a8",
        "accent": "#ec6258", "accent_hover": "#f07268", "accent_press": "#d9524a",
        "accent_dim": "#f3b4af", "danger": "#da4453", "log_bg": "#f6f7f8", "log_text": "#31373d",
        "on_accent": "#ffffff", "check_box": "#8a9199",
    },
}

_state = {"theme": "dark"}


def pal():
    return PALETTES[_state["theme"]]


def plain(text):
    """Strip leading emoji / symbols so labels stay flat and monochrome
    (the reference style has no colourful emoji)."""
    return re.sub(r"^[^\w]+", "", text or "").strip()


def build_qss(theme):
    _state["theme"] = theme if theme in PALETTES else "dark"
    p = pal()
    return f"""
    QWidget {{ color: {p['text']}; font-size: 13px; font-family: "Noto Sans", "Segoe UI", "SF Pro Text", "Helvetica Neue", Arial, sans-serif; }}
    QMainWindow, QWidget#root {{ background: {p['bg']}; }}
    QScrollArea {{ border: none; background: transparent; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}
    QStackedWidget, QWidget#page {{ background: transparent; }}
    QLabel {{ background: transparent; }}

    QFrame#header {{ background: {p['bg']}; border: none; border-bottom: 1px solid {p['soft']}; }}
    QFrame#vline {{ background: {p['soft']}; border: none; max-width: 1px; min-width: 1px; }}
    QFrame#card {{ background: transparent; border: 1px solid {p['soft']}; border-radius: 4px; }}

    QLabel#muted {{ color: {p['muted']}; font-size: 12px; }}
    QLabel#title {{ font-size: 18px; font-weight: 700; }}
    QLabel#version {{ color: {p['muted']}; font-size: 11px; }}
    QLabel#bold {{ font-weight: 700; }}
    QLabel#percent {{ color: {p['accent']}; font-size: 15px; font-weight: 700; }}
    QLabel#status {{ font-weight: 700; }}
    QLabel#value {{ color: {p['accent']}; font-weight: 700; }}

    QLineEdit, QPlainTextEdit {{
        background: {p['inset']}; border: 1px solid {p['border']}; border-radius: 4px; padding: 6px 8px;
        selection-background-color: {p['accent']}; selection-color: white;
    }}
    QLineEdit:hover, QPlainTextEdit:hover {{ border: 1px solid {p['muted']}; }}
    QLineEdit:focus, QPlainTextEdit:focus {{ border: 1px solid {p['accent']}; }}
    QLineEdit:disabled, QPlainTextEdit:disabled {{ color: {p['disabled']}; border: 1px solid {p['soft']}; }}
    QPlainTextEdit#log {{
        background: {p['log_bg']}; color: {p['log_text']}; border: 1px solid {p['soft']};
        font-family: Consolas, Menlo, "DejaVu Sans Mono", monospace; font-size: 12px;
    }}

    QComboBox {{
        background: {p['ctrl']}; border: 1px solid {p['border']}; border-radius: 4px;
        padding: 5px 30px 5px 10px; min-height: 20px;
    }}
    QComboBox:hover {{ background: {p['ctrl_hover']}; }}
    QComboBox:focus {{ border: 1px solid {p['accent']}; }}
    QComboBox::drop-down {{ border: none; width: 26px; }}
    QComboBox::down-arrow {{ image: none; }}
    QComboBox QAbstractItemView {{
        background: {p['ctrl']}; color: {p['text']}; border: 1px solid {p['border']};
        selection-background-color: {p['accent']}; selection-color: white; outline: none; padding: 2px;
    }}

    QPushButton {{
        background: {p['ctrl']}; border: 1px solid {p['border']}; border-radius: 4px; padding: 6px 14px;
        color: {p['text']};
    }}
    QPushButton:hover {{ background: {p['ctrl_hover']}; border: 1px solid {p['muted']}; }}
    QPushButton:pressed {{ background: {p['inset']}; }}
    QPushButton:disabled {{ color: {p['disabled']}; background: {p['bg']}; border: 1px solid {p['soft']}; }}

    QPushButton#nav {{
        text-align: left; background: transparent; border: none; border-radius: 0; padding: 10px 16px;
        color: {p['text']}; font-size: 14px;
    }}
    QPushButton#nav:hover {{ background: {p['ctrl']}; }}
    QPushButton#nav:checked {{ background: {p['accent']}; color: {p['on_accent']}; }}

    QPushButton#seg, QPushButton#segL, QPushButton#segR {{
        border: 1px solid {p['border']}; border-radius: 0; padding: 5px 12px; margin-left: -1px; background: {p['ctrl']};
    }}
    QPushButton#seg:hover, QPushButton#segL:hover, QPushButton#segR:hover {{ background: {p['ctrl_hover']}; }}
    QPushButton#seg:checked, QPushButton#segL:checked, QPushButton#segR:checked {{
        background: {p['accent']}; color: {p['on_accent']}; border: 1px solid {p['accent']};
    }}
    QPushButton#segL {{ border-top-left-radius: 4px; border-bottom-left-radius: 4px; margin-left: 0; }}
    QPushButton#segR {{ border-top-right-radius: 4px; border-bottom-right-radius: 4px; }}

    QPushButton[role="action"] {{
        background: {p['accent']}; color: {p['on_accent']}; font-size: 14px; font-weight: 700;
        border: 1px solid {p['accent_press']}; border-radius: 4px; padding: 10px 34px; min-height: 20px;
    }}
    QPushButton[role="action"]:hover {{ background: {p['accent_hover']}; border: 1px solid {p['accent_hover']}; }}
    QPushButton[role="action"]:pressed {{ background: {p['accent_press']}; }}
    QPushButton[role="action"]:disabled {{ background: {p['ctrl']}; color: {p['disabled']}; border: 1px solid {p['soft']}; }}
    QPushButton#cancel {{ background: {p['danger']}; border: 1px solid {p['danger']}; }}
    QPushButton#cancel:hover {{ background: #e4606c; border: 1px solid #e4606c; }}

    QPushButton#histitem {{ text-align: left; background: transparent; border: none; border-radius: 3px; padding: 6px 10px; }}
    QPushButton#histitem:hover {{ background: {p['accent']}; color: {p['on_accent']}; }}
    QPushButton#histdel {{ background: transparent; border: none; border-radius: 3px; padding: 4px 9px; color: {p['muted']}; }}
    QPushButton#histdel:hover {{ background: {p['danger']}; color: white; }}
    QMenu {{ background: {p['ctrl']}; border: 1px solid {p['border']}; border-radius: 4px; padding: 4px; }}
    QMenu::item {{ padding: 6px 12px; color: {p['disabled']}; }}
    QToolTip {{ background: {p['ctrl']}; color: {p['text']}; border: 1px solid {p['border']}; padding: 4px 6px; }}

    QProgressBar {{ background: {p['track']}; border: none; border-radius: 4px; min-height: 8px; max-height: 8px; color: transparent; }}
    QProgressBar::chunk {{ background: {p['accent_dim']}; border: 1px solid {p['accent']}; border-radius: 4px; }}

    QSlider::groove:horizontal {{ height: 4px; background: {p['track']}; border-radius: 2px; }}
    QSlider::sub-page:horizontal {{ background: {p['accent']}; border-radius: 2px; }}
    QSlider::handle:horizontal {{
        background: {p['ctrl']}; border: 1px solid {p['border']}; width: 16px; height: 16px; margin: -7px 0; border-radius: 9px;
    }}
    QSlider::handle:horizontal:hover {{ border: 1px solid {p['accent']}; }}

    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
    QScrollBar::handle:vertical {{ background: {p['border']}; border-radius: 3px; min-height: 30px; }}
    QScrollBar::handle:vertical:hover {{ background: {p['muted']}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QDialog {{ background: {p['bg']}; }}
    QMessageBox {{ background: {p['bg']}; }}
    """


class Check(QCheckBox):
    """Breeze-style checkbox: rounded square, accent border + white tick."""
    BOX = 18

    def __init__(self, text=""):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(28)

    def sizeHint(self):
        return QSize(self.BOX + 10 + self.fontMetrics().horizontalAdvance(self.text()) + 4, 28)

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        c = pal()
        y = (self.height() - self.BOX) / 2
        box = QRectF(1.5, y + 0.5, self.BOX - 1, self.BOX - 1)
        on = self.isChecked()
        hot = self.underMouse() and self.isEnabled()
        border = QColor(c["accent"]) if on else QColor(c["accent_hover"] if hot else c["check_box"])
        p.setPen(QPen(border, 1.4))
        p.setBrush(QColor(c["inset"]))
        p.drawRoundedRect(box, 3, 3)
        if on:
            tick = QPen(QColor(c["text"]), 2)
            tick.setCapStyle(Qt.RoundCap)
            tick.setJoinStyle(Qt.RoundJoin)
            p.setPen(tick)
            p.setBrush(Qt.NoBrush)
            x0, y0 = box.left(), box.top()
            w = box.width()
            p.drawPolyline(QPolygonF([QPointF(x0 + w * 0.24, y0 + w * 0.54),
                                      QPointF(x0 + w * 0.44, y0 + w * 0.74),
                                      QPointF(x0 + w * 0.78, y0 + w * 0.30)]))
        p.setPen(QColor(c["text"] if self.isEnabled() else c["disabled"]))
        p.drawText(QRectF(self.BOX + 10, 0, self.width() - self.BOX - 10, self.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, self.text())


def _chevron(p, cx, cy, size, color, width=1.6):
    pen = QPen(QColor(color), width)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    p.drawPolyline(QPolygonF([QPointF(cx - size, cy - size / 2), QPointF(cx, cy + size / 2), QPointF(cx + size, cy - size / 2)]))


class Combo(QComboBox):
    """QComboBox with a thin chevron (matches the reference)."""
    def __init__(self):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, e):
        super().paintEvent(e)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        _chevron(p, self.width() - 15, self.height() / 2, 4.5, pal()["text"] if self.isEnabled() else pal()["disabled"])


class _ArrowButton(QAbstractButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(26, 24)
        self.setFocusPolicy(Qt.NoFocus)

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if self.underMouse():
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(pal()["ctrl_hover"]))
            p.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 3, 3)
        _chevron(p, self.width() / 2, self.height() / 2, 4.5, pal()["text"])


class _HistoryLineEdit(QLineEdit):
    """Line edit with a ▾ button inside its right edge."""
    def __init__(self, text=""):
        super().__init__(text)
        self.arrow = _ArrowButton(self)
        self.setTextMargins(0, 0, 28, 0)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.arrow.move(self.width() - self.arrow.width() - 3, (self.height() - self.arrow.height()) // 2)


class PathField(QWidget):
    """Folder path input with a recent-folders DROPDOWN (▾ inside the field)
    and a Browse button. Replaces the old separate history window.

    history()  -> live list of recent folders
    remember() -> add a folder to the history (moves it to the top)
    forget()   -> remove a folder from the history
    """

    def __init__(self, text, on_text, history, remember, forget, browse_text, tooltip, empty_text, dialog_title=""):
        super().__init__()
        self._history, self._remember, self._forget = history, remember, forget
        self._empty_text, self._dialog_title = empty_text, dialog_title
        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        self.edit = _HistoryLineEdit(text)
        self.edit.textChanged.connect(on_text)
        self.edit.arrow.setToolTip(tooltip)
        self.edit.arrow.clicked.connect(self.show_history)
        self.browse = QPushButton(browse_text)
        self.browse.setCursor(Qt.PointingHandCursor)
        self.browse.clicked.connect(self._browse)
        h.addWidget(self.edit, 1)
        h.addWidget(self.browse)

    def text(self):
        return self.edit.text()

    def setText(self, s):
        self.edit.setText(s)

    def _browse(self):
        folder = QFileDialog.getExistingDirectory(self.window(), self._dialog_title, self.edit.text() or "")
        if folder:
            self.edit.setText(folder)
            self._remember(folder)

    def _pick(self, menu, path):
        self.edit.setText(path)
        self._remember(path)
        menu.close()

    def show_history(self):
        items = list(self._history())
        menu = QMenu(self)
        menu.setFixedWidth(max(260, self.edit.width()))
        if not items:
            a = menu.addAction(self._empty_text)
            a.setEnabled(False)
        fm = self.fontMetrics()
        rows = []
        for path in items:
            row = QWidget()
            hl = QHBoxLayout(row)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(2)
            b = QPushButton(fm.elidedText(path, Qt.ElideMiddle, menu.width() - 90))
            b.setObjectName("histitem")
            b.setToolTip(path)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, pth=path: self._pick(menu, pth))
            d = QPushButton("✕")
            d.setObjectName("histdel")
            d.setCursor(Qt.PointingHandCursor)
            hl.addWidget(b, 1)
            hl.addWidget(d)
            rows.append(row)

            def remove(_=False, pth=path, r=row):
                self._forget(pth)
                r.hide()
                rows.remove(r)
                if not rows:
                    menu.close()
                else:
                    menu.adjustSize()
            d.clicked.connect(remove)
            wa = QWidgetAction(menu)
            wa.setDefaultWidget(row)
            menu.addAction(wa)
        menu.exec(self.edit.mapToGlobal(QPoint(0, self.edit.height() + 2)))
