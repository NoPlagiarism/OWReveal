from PyQt6.QtCore import Qt, QRect, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QApplication,
                             QGridLayout, QHBoxLayout, QVBoxLayout, QLayoutItem, QSizePolicy)
from stylesheet import DARK_STYLE
import sys


class IndicLabel(QLabel):
    going_stylesheet = "font: 14pt; color: green"
    stopped_stylesheet = "font: 14pt; color: red"

    def __init__(self, *args, **kwargs):
        super(IndicLabel, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._stopped = None

    @property
    def stopped(self) -> bool:
        return self._stopped

    @stopped.setter
    def stopped(self, new):
        if new != self._stopped:
            if not new:
                self.setText("Looking for OW DEMO link")
                self.setStyleSheet(self.going_stylesheet)
            else:
                self.setText("Not looking for anything")
                self.setStyleSheet(self.stopped_stylesheet)
            self._stopped = new


class ToggleScanBtn(QPushButton):
    def __init__(self, *args, **kwargs):
        super(ToggleScanBtn, self).__init__(*args, **kwargs)
        self._stopped = True

    @property
    def stopped(self) -> bool:
        return self._stopped

    @stopped.setter
    def stopped(self, new):
        if new != self._stopped:
            self.setText("Start") if new else self.setText("Stop")
            self._stopped = new


class DemosCounter(QLabel):
    def __init__(self, *args, **kwargs):
        super(DemosCounter, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._demos = 0
        self.update_()

    def update_(self):
        self.setText(f"Total DEMOs: {self._demos}")

    def increment_demo(self):
        self._demos += 1
        self.update_()

    @property
    def demos(self) -> int:
        return self._demos

    @demos.setter
    def demos(self, a):
        self._demos = a
        self.update_()


class PrevLinkTimer(QLabel):
    reset_timer_sig = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PrevLinkTimer, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("No LINK found")
        self.timer = QTimer()
        self.timer.setTimerType(Qt.TimerType.VeryCoarseTimer)
        self.seconds = None
        self.reset_timer_sig.connect(self.reset_timer)

    @pyqtSlot()
    def reset_timer(self):
        self.seconds = 0
        self.update_label()
        self.timer.start(60000)
        self.timer.timeout.connect(self.on_timer)

    def on_timer(self):
        self.seconds += 1
        self.update_label()

    def update_label(self):
        self.setText(f"LINK found {self.seconds} minutes ago")


class MainApp(QMainWindow):
    SIZE_X, SIZE_Y = 805, 350
    START_X = 0.005
    START_Y = 0.01

    def get_geometry_from_percent(self, ax, ay, w, h):
        x, y = self.size().width(), self.size().height()
        return QRect(int(x * (self.START_X + ax)), int(y * (self.START_Y + ay)),
                     int(w * x), int(h * y))

    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(self.SIZE_X, self.SIZE_Y)

        # INIT UI

        self.interface_sel = QComboBox(self)
        self.interface_sel.addItem("Select one interface")

        self.lbl_indicator = IndicLabel(self)
        self.lbl_indicator.stopped = True

        self.start_btn = ToggleScanBtn(self)
        self.start_btn.stopped = True

        # TODO: MAKE A MENU ON RIGHT CLICK (COPY URL | COPY DEMO NAME)
        self.url_edit = QLineEdit(self)
        self.url_edit.setReadOnly(True)

        self.demos_counter = DemosCounter(self)

        self.prev_link_timer = PrevLinkTimer(self)
        self.prev_link_timer.reset_timer_sig.emit()

        self.switch_stats_kills = QPushButton("Show Kills")
        self.switch_stats_kills.setParent(self)

        self.download_demo = QPushButton("Download DEMO")
        self.download_demo.setParent(self)

        self.prev_round = QPushButton("<")
        self.prev_round.setParent(self)
        self.next_round = QPushButton(">")
        self.next_round.setParent(self)

        self.round_switch = QComboBox(self)
        self.round_switch.addItem("Round ??")

        self.map_lbl = QLabel("cs_office")
        self.map_lbl.setParent(self)
        self.map_lbl.setStyleSheet("font: 11pt; color: green")
        self.map_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.server_lbl = QLabel("EU North")
        self.server_lbl.setParent(self)
        self.server_lbl.setStyleSheet("font: 11pt; color: pink")
        self.server_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_to_watchlist = QPushButton("Add to WatchList")
        self.add_to_watchlist.setParent(self)

        self.show_watchlist = QPushButton("WatchList")
        self.show_watchlist.setParent(self)

        self.show_links = QPushButton("LINK List")
        self.show_links.setParent(self)

        self.show_settings = QPushButton("Settings")
        self.show_settings.setParent(self)

        self.update_geometry()

    def update_geometry(self):
        self.interface_sel.setGeometry(self.get_geometry_from_percent(0, 0, 0.785, 0.08))
        self.lbl_indicator.setGeometry(self.get_geometry_from_percent(0, 0.1, 0.785, 0.12))
        self.start_btn.setGeometry(self.get_geometry_from_percent(0.8, 0, 0.18, 0.2))
        self.url_edit.setGeometry(self.get_geometry_from_percent(0, 0.24, 0.99, 0.09))
        self.demos_counter.setGeometry(self.get_geometry_from_percent(0, 0.33, 0.12, 0.08))
        self.prev_link_timer.setGeometry(self.get_geometry_from_percent(0.13, 0.33, 0.5, 0.08))
        self.switch_stats_kills.setGeometry(self.get_geometry_from_percent(0.65, 0.33, 0.13, 0.08))
        self.download_demo.setGeometry(self.get_geometry_from_percent(0.8, 0.33, 0.19, 0.08))
        self.prev_round.setGeometry(self.get_geometry_from_percent(0.8, 0.42, 0.03, 0.08))
        self.round_switch.setGeometry(self.get_geometry_from_percent(0.83, 0.42, 0.13, 0.08))
        self.next_round.setGeometry(self.get_geometry_from_percent(0.96, 0.42, 0.03, 0.08))
        self.map_lbl.setGeometry(self.get_geometry_from_percent(0.8, 0.51, 0.19, 0.08))
        self.server_lbl.setGeometry(self.get_geometry_from_percent(0.8, 0.60, 0.19, 0.08))
        self.add_to_watchlist.setGeometry(self.get_geometry_from_percent(0.8, 0.69, 0.19, 0.08))
        self.show_watchlist.setGeometry(self.get_geometry_from_percent(0.8, 0.78, 0.19, 0.08))
        self.show_links.setGeometry(self.get_geometry_from_percent(0.8, 0.87, 0.09, 0.08))
        self.show_settings.setGeometry(self.get_geometry_from_percent(0.9, 0.87, 0.09, 0.08))

    def resizeEvent(self, a0) -> None:
        self.update_geometry()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(DARK_STYLE)
    window = MainApp("Another OW Revealer 2")
    window.show()
    sys.exit(app.exec())
