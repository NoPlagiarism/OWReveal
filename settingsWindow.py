import sys

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QApplication, QMainWindow)
from stylesheet import DARK_STYLE


class SettingButton(QPushButton):
    ENABLED_STYLESHEET = "background-color: #404040;"
    DISABLED_STYLESHEET = "background-color: #101010;"

    def __init__(self, *args, state=False, **kwargs):
        super(SettingButton, self).__init__(*args, **kwargs)
        self.state: bool = None
        self.setCheckable(True)
        self.clicked.connect(self.change_state)
        self.change_state(state)

    def change_state(self, checked):
        if checked:
            self.setStyleSheet(self.ENABLED_STYLESHEET)
            self.setText("OFF")
        else:
            self.setStyleSheet(self.DISABLED_STYLESHEET)
            self.setText("ON")
        self.state = checked


class SettingsWindow(QWidget):
    SIZE_X, SIZE_Y = 580, 445
    START_X = 0.01
    START_Y = 0.01

    def get_geometry_from_percent(self, ax, ay, w, h):
        x, y = self.size().width(), self.size().height()
        return QRect(int(x * (self.START_X + ax)), int(y * (self.START_Y + ay)),
                     int(w * x), int(h * y))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setWindowTitle("Settings")
        self.setFixedSize(self.SIZE_X, self.SIZE_Y)
        self.buttons = list()

        # INIT UI
        self.btn_1 = SettingButton(self)
        self.lbl_1 = QLabel("Auto start scanning when opening the app", parent=self)

        self.btn_2 = SettingButton(self)
        self.lbl_2 = QLabel("Stop scanning after a DEMO LINK is found", parent=self)

        self.btn_3 = SettingButton(self)
        self.lbl_3 = QLabel("Auto download DEMO after LINK is found", parent=self)

        self.btn_4 = SettingButton(self)
        self.lbl_4 = QLabel("Use the browser to download (doesn't work with auto download)", parent=self)

        self.btn_5 = SettingButton(self)
        self.lbl_5 = QLabel("Add suspects to database <a href=\"https://zahar.one/owrev\">(zahar.one/owrev)</a>",
                            parent=self)
        self.lbl_5.setOpenExternalLinks(True)

        self.lbl_download = QLabel("*" * 50 + "Download location when not using the browser" + "*" * 50, parent=self)
        self.lbl_download.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_browse = QPushButton("Browse", parent=self)
        self.path_lne = QLineEdit(parent=self)
        self.open_path_btn = QPushButton("Open", parent=self)

        self.lbl_download2 = QLabel("*" * 200, parent=self)
        self.lbl_download2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_6 = SettingButton(self)
        self.lbl_6 = QLabel("Rename downloaded demos to ", parent=self)
        self.lne_6 = QLineEdit(parent=self)

        self.btn_7 = SettingButton(self)
        self.lbl_7 = QLabel("Auto delete DEMO after it is analyzed", parent=self)

        self.lbl_api = QLabel("<a href=\"https://steamcommunity.com/dev/apikey\">API Key:</a>", parent=self)
        self.lbl_api.setOpenExternalLinks(True)
        self.lne_api = QLineEdit(parent=self)

        self.btn_analyze = QPushButton("Analyze a demo", parent=self)
        self.lbl_project_link = QLabel("<a href=\"https://github.com/ZaharX97/OWReveal\">v4.6.1 - https://github.com/ZaharX97/OWReveal</a>", parent=self)
        self.lbl_project_link.setOpenExternalLinks(True)
        self.lbl_project_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_save = QPushButton("Save settings", parent=self)

        self.update_geometry()

    def update_geometry(self):
        self.btn_1.setGeometry(self.get_geometry_from_percent(0, 0, 0.13, 0.06))
        self.lbl_1.setGeometry(self.get_geometry_from_percent(0.15, 0, 0.8, 0.06))
        self.btn_2.setGeometry(self.get_geometry_from_percent(0, 0.08, 0.13, 0.06))
        self.lbl_2.setGeometry(self.get_geometry_from_percent(0.15, 0.08, 0.8, 0.06))
        self.btn_3.setGeometry(self.get_geometry_from_percent(0, 0.16, 0.13, 0.06))
        self.lbl_3.setGeometry(self.get_geometry_from_percent(0.15, 0.16, 0.8, 0.06))
        self.btn_4.setGeometry(self.get_geometry_from_percent(0, 0.24, 0.13, 0.06))
        self.lbl_4.setGeometry(self.get_geometry_from_percent(0.15, 0.24, 0.8, 0.06))
        self.btn_5.setGeometry(self.get_geometry_from_percent(0, 0.32, 0.13, 0.06))
        self.lbl_5.setGeometry(self.get_geometry_from_percent(0.15, 0.32, 0.8, 0.06))
        self.lbl_download.setGeometry(self.get_geometry_from_percent(-self.START_X, 0.4, 1, 0.06))
        self.btn_browse.setGeometry(self.get_geometry_from_percent(0, 0.48, 0.13, 0.06))
        self.path_lne.setGeometry(self.get_geometry_from_percent(0.15, 0.48, 0.5, 0.06))
        self.open_path_btn.setGeometry(self.get_geometry_from_percent(0.7, 0.48, 0.2, 0.06))
        self.lbl_download2.setGeometry(self.get_geometry_from_percent(-self.START_X, 0.56, 1, 0.06))
        self.btn_6.setGeometry(self.get_geometry_from_percent(0, 0.64, 0.13, 0.06))
        self.lbl_6.setGeometry(self.get_geometry_from_percent(0.15, 0.64, 0.4, 0.06))
        self.lne_6.setGeometry(self.get_geometry_from_percent(0.6, 0.64, 0.35, 0.06))
        self.btn_7.setGeometry(self.get_geometry_from_percent(0, 0.72, 0.13, 0.06))
        self.lbl_7.setGeometry(self.get_geometry_from_percent(0.15, 0.72, 0.8, 0.06))
        self.lbl_api.setGeometry(self.get_geometry_from_percent(0, 0.8, 0.13, 0.06))
        self.lne_api.setGeometry(self.get_geometry_from_percent(0.15, 0.8, 0.8, 0.06))
        self.btn_analyze.setGeometry(self.get_geometry_from_percent(0, 0.92, 0.2, 0.06))
        self.lbl_project_link.setGeometry(self.get_geometry_from_percent(0.22, 0.92, 0.5, 0.06))
        self.btn_save.setGeometry(self.get_geometry_from_percent(0.77, 0.92, 0.2, 0.06))


if __name__ == '__main__':
    class SettingsEx(QMainWindow, SettingsWindow):
        pass
    app = QApplication([])
    app.setStyleSheet(DARK_STYLE)
    widget = SettingsEx()
    widget.setWindowTitle("Settings")
    widget.show()
    sys.exit(app.exec())
