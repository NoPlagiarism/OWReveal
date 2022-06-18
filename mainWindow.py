from PyQt6.QtCore import Qt, QRect, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QApplication, QCheckBox,
                             QGridLayout, QHBoxLayout, QVBoxLayout, QLayoutItem, QSizePolicy, QSpacerItem)
from PyQt6.QtGui import QPixmap
from stylesheet import DARK_STYLE
from PIL import Image
from PIL.ImageQt import ImageQt
import sys
from enum import IntEnum


class PlayerSide(IntEnum):
    CT = 0
    T = 1


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


class Player(QWidget):
    def __init__(self, *args, side, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.rank_translate = dict()
        for i in range(19):
            im = Image.open(rf"resources\csgo_rank_icons\{0}.png")
            im = im.resize((46, 26))
            self.rank_translate[i] = QPixmap.fromImage(ImageQt(im))

        self.lay = QHBoxLayout(self)
        self.setLayout(self.lay)

        self.checkbox = QCheckBox()

        self.name = QLabel("???")
        self.name.setStyleSheet("color: blue;") if side == PlayerSide.CT else self.name.setStyleSheet("color: red;")

        self.icon = QLabel()
        self.icon.setFixedSize(46, 26)
        self.icon.setPixmap(self.rank_translate[0])

        self.kad = QLabel("0/0/0")
        self.setup_ui_ct() if side == PlayerSide.CT else self.setup_ui_t()

    def setup_ui_ct(self):
        self.lay.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        self.lay.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignLeft)
        self.lay.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignRight)
        self.lay.addWidget(self.kad, alignment=Qt.AlignmentFlag.AlignRight)

    def setup_ui_t(self):
        self.lay.addWidget(self.kad, alignment=Qt.AlignmentFlag.AlignLeft)
        self.lay.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignLeft)
        self.lay.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignRight)
        self.lay.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignRight)


class RoundStatsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(RoundStatsWidget, self).__init__(*args, **kwargs)
        self.rank_translate = dict()
        for i in range(19):
            self.rank_translate[i] = QPixmap(rf"resources\csgo_rank_icons\{i}.png")

        self.main_lay = QHBoxLayout(self)
        self.setLayout(self.main_lay)
        self.ct_lay = QVBoxLayout()
        self.t_lay = QVBoxLayout()
        self.main_lay.addLayout(self.ct_lay)
        self.main_lay.addLayout(self.t_lay)

    def testy(self):
        for _ in range(5):
            self.ct_lay.addWidget(Player(side=0))
        for _ in range(5):
            self.t_lay.addWidget(Player(side=1))


class Kill(QWidget):
    def __init__(self, *args, p1=None, weapon=None, p2=None, **kwargs):
        super(Kill, self).__init__(*args, **kwargs)

        self.lay = QHBoxLayout(self)
        self.setLayout(self.lay)
        self.p1_lbl = QLabel()
        self.weapon = QLabel()
        self.p2_lbl = QLabel()

        self.p1_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weapon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lay.addWidget(self.p1_lbl)
        self.lay.addWidget(self.weapon)
        self.lay.addWidget(self.p2_lbl)

        if (p1 is not None) and (weapon is not None) and (p2 is not None):
            self.update_data(p1, weapon, p2)

    def update_data(self, p1, weapon, p2):
        """pi - (nickname, site)"""
        self.p1_lbl.setText(p1[0])
        self.weapon.setText(weapon)
        self.p2_lbl.setText(p2[0])

        self.p1_lbl.setStyleSheet("color: red") if p1[1] == PlayerSide.T else self.p1_lbl.setStyleSheet("color: blue")
        self.p2_lbl.setStyleSheet("color: red") if p1[1] == PlayerSide.T else self.p1_lbl.setStyleSheet("color: blue")


class KillsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(KillsWidget, self).__init__(*args, **kwargs)

        self.main_lay = QHBoxLayout(self)
        self.setLayout(self.main_lay)
        self.a_lay = QVBoxLayout()
        self.b_lay = QVBoxLayout()
        self.main_lay.addLayout(self.a_lay)
        self.main_lay.addLayout(self.b_lay)

    def testy(self):
        for _ in range(5):
            self.a_lay.addWidget(Kill(p1=("PTN", PlayerSide.T), weapon="suicide", p2=("PTN", PlayerSide.CT)))
        for _ in range(5):
            self.b_lay.addWidget(Kill(p1=("PTN", PlayerSide.CT), weapon="suicide", p2=("PTN", PlayerSide.T)))


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
        self.setFixedSize(self.SIZE_X, self.SIZE_Y)
        self.stats_active = True

        # INIT UI

        self.interface_sel = QComboBox(self)
        self.interface_sel.addItem("Select one interface")

        self.lbl_indicator = IndicLabel(self)
        self.lbl_indicator.stopped = True

        self.start_btn = ToggleScanBtn("Start", parent=self)
        self.start_btn.stopped = True

        # TODO: MAKE A MENU ON RIGHT CLICK (COPY URL | COPY DEMO NAME)
        self.url_edit = QLineEdit(self)
        self.url_edit.setReadOnly(True)

        self.demos_counter = DemosCounter(self)

        self.prev_link_timer = PrevLinkTimer(self)
        self.prev_link_timer.reset_timer_sig.emit()

        self.switch_stats_kills = QPushButton("Show Kills", parent=self)
        self.switch_stats_kills.clicked.connect(self._toggle_stats_frame)

        self.download_demo = QPushButton("Download DEMO", parent=self)

        self.prev_round = QPushButton("<", parent=self)
        self.next_round = QPushButton(">", parent=self)

        self.round_switch = QComboBox(self)
        self.round_switch.addItem("Round ??")

        self.map_lbl = QLabel("cs_office", parent=self)
        self.map_lbl.setStyleSheet("font: 11pt; color: green")
        self.map_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.server_lbl = QLabel("EU North", parent=self)
        self.server_lbl.setStyleSheet("font: 11pt; color: pink")
        self.server_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_to_watchlist = QPushButton("Add to WatchList", parent=self)

        self.show_watchlist = QPushButton("WatchList", parent=self)

        self.show_links = QPushButton("LINK List", parent=self)

        self.show_settings = QPushButton("Settings", parent=self)

        self.ct_score_lbl = QLabel("0", parent=self)
        self.t_score_lbl = QLabel("0", parent=self)

        self.round_stats = RoundStatsWidget(parent=self)
        self.round_stats.testy()

        self.kills = KillsWidget(parent=self)
        self.kills.testy()
        if self.stats_active:
            self.kills.hide()

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
        self.ct_score_lbl.setGeometry(self.get_geometry_from_percent(0.15, 0.42, 0.1, 0.08))
        self.t_score_lbl.setGeometry(self.get_geometry_from_percent(0.65, 0.42, 0.1, 0.08))
        self.round_stats.setGeometry(self.get_geometry_from_percent(0, 0.5, 0.75, 0.49))
        self.kills.setGeometry(self.get_geometry_from_percent(0, 0.5, 0.75, 0.49))

    def resizeEvent(self, a0) -> None:
        self.update_geometry()

    def _toggle_stats_frame(self):
        if self.stats_active:
            self.round_stats.hide()
            self.kills.show()
            self.switch_stats_kills.setText("Show Stats")
        else:
            self.kills.hide()
            self.round_stats.show()
            self.switch_stats_kills.setText("Show Kills")
        self.stats_active = not self.stats_active


if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(DARK_STYLE)
    window = MainApp("Another OW Revealer 2")
    window.show()
    sys.exit(app.exec())
