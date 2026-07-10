# -*- coding: utf-8 -*-
"""
黑金 QR 工坊 v2.0.0  桌面端（PyQt5 + QWebEngineView）
作者：军哥懂保  微信：xunijiayuan
单人本地版  预留接口 window.TechQR
打包：pyinstaller --noconfirm --onefile --windowed --name HeiJinQR
       --add-data "黑金二维码工坊.html;." --add-data "assets;assets" main.py
"""
import sys
import os
import traceback
import ctypes

# 修复 Microsoft Store 版 Python 加载 PyQt5 Qt DLL 失败问题
try:
    import PyQt5 as _pyqt5
    _qt_bin = os.path.join(os.path.dirname(_pyqt5.__file__), 'Qt5', 'bin')
    if os.path.isdir(_qt_bin):
        ctypes.windll.kernel32.SetDllDirectoryW(_qt_bin)
except Exception:
    pass

from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings


def resource_path(relative):
    """兼容 PyInstaller 打包后的资源路径（_MEIPASS）与开发态。"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("黑金 QR 工坊 v2.0.0  |  军哥懂保 · 微信 xunijiayuan")
        self.resize(1180, 840)
        self.setMinimumSize(900, 640)

        self.browser = QWebEngineView()
        html_path = resource_path("黑金二维码工坊.html")
        # 若找不到资源给出友好提示
        if not os.path.exists(html_path):
            self.browser.setHtml(
                "<div style='font-family:sans-serif;padding:40px;color:#d4af37;background:#0d0b08;height:100%'>"
                "<h2>资源缺失</h2><p>未找到 黑金二维码工坊.html</p>"
                "<p>路径：%s</p><p>作者：军哥懂保  微信：xunijiayuan</p></div>" % html_path
            )
        else:
            self.browser.setUrl(QUrl.fromLocalFile(html_path))

        # 启用 WebEngine 高级特性
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)

        self.setCentralWidget(self.browser)

        # 状态栏：作者信息
        sb = QStatusBar()
        sb.setStyleSheet("background:#0d0b08;color:#c9b78a;border-top:1px solid rgba(212,175,55,0.3);")
        author_lbl = QLabel("  作者：军哥懂保   |   微信：xunijiayuan   |   单人本地版   ")
        author_lbl.setStyleSheet("color:#d4af37;font-weight:bold;")
        info_lbl = QLabel("黑金QR工坊 v2.0.0  ")
        info_lbl.setStyleSheet("color:#8a7a4e;")
        sb.addWidget(author_lbl)
        sb.addPermanentWidget(info_lbl)
        self.setStatusBar(sb)

    def closeEvent(self, e):
        self.browser.deleteLater()
        super().closeEvent(e)


def install_excepthook():
    def hook(exc_type, exc_value, tb):
        msg = "".join(traceback.format_exception(exc_type, exc_value, tb))
        print(msg, file=sys.stderr)
        try:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "黑金QR工坊 - 运行错误",
                "程序发生异常，请联系作者：\n\n军哥懂保  微信：xunijiayuan\n\n" + msg[:1500])
        except Exception:
            pass
    sys.excepthook = hook


def main():
    # 高 DPI
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName("黑金QR工坊")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("军哥懂保")

    install_excepthook()

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
