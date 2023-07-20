import sys
import pandas as pd

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QRadioButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QMainWindow,
)

from view import (
    ChangeAccountValue,
    TickerBtnScrollArea,
    ChartTypeGroup,
    FavoriteDIGroup,
    CurrentDIGroup,
)
from model import Model


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.m = Model()

        self.change_acct_widget = ChangeAccountValue()
        account_value = self.m.getAccountValue()
        self.change_acct_widget.set_account_value_lbl(str(account_value))

        self.change_acct_widget.account_value_changed.connect(
            self.handle_change_acct_signal
        )
        self.ticker_btns_area = TickerBtnScrollArea()
        tickers = self.m.getTickers()
        self.ticker_btns_area.addTickers(tickers)
        self.ticker_btns_area.ticker_changed.connect(self.handle_ticker_changed_signal)

        self.chart_type_group = ChartTypeGroup(
            charttypes=self.m.charttypes, preferred=self.m.preselect_charttype
        )
        self.m.set_current_charttype(self.m.preselect_charttype)
        self.chart_type_group.chart_type_changed.connect(self.handle_chart_type_changed)

        self.favorites_di_group = FavoriteDIGroup()
        favorites = self.m.get_favorite_period_intervals()
        self.favorites_di_group.addFavorites(favorites)
        self.favorites_di_group.favorite_di_changed.connect(
            self.handle_favorite_di_changed
        )

        self.current_di_group = CurrentDIGroup()
        self.current_di_group.loadDurations(self.m.get_all_durations())
        self.current_di_group.loadIntervals(self.m.get_all_intervals())
        initial_duration, initial_interval = self.m.get_initial_duration_interval()
        self.current_di_group.setCurrentDuration(initial_duration)
        self.current_di_group.setCurrentInterval(initial_interval)
        self.current_di_group.current_duration_changed.connect(
            self.handle_current_duration_changed
        )
        self.current_di_group.current_interval_changed.connect(
            self.handle_current_interval_changed
        )

        self.LayoutWindow()

    def LayoutWindow(self):
        self.setWindowTitle("Lou Loves Eileen Trade")
        layout = QVBoxLayout()
        h1_layout = QHBoxLayout()
        h1_layout.addWidget(self.change_acct_widget)
        layout.addLayout(h1_layout)
        h2_layout = QGridLayout()
        h2_layout.setColumnStretch(0, 0)
        h2_layout.setColumnStretch(1, 0)
        h2_layout.setColumnStretch(2, 1)
        h2_layout.addWidget(self.ticker_btns_area, 0, 0, 3, 1)
        h2_layout.addWidget(self.chart_type_group, 0, 1, 1, -1)
        h2_layout.addWidget(self.current_di_group, 1, 2)
        h2_layout.addWidget(self.favorites_di_group, 1, 1)
        layout.addLayout(h2_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def handle_change_acct_signal(self, acct_value_txt: str):
        ok, acct_value_int = self.m.setAccountValue(acct_value_txt)
        if ok:
            self.change_acct_widget.set_account_value_lbl(str(acct_value_int))

    def handle_chart_type_changed(self, charttype: str):
        self.m.set_current_charttype(charttype)

    def handle_favorite_di_changed(self, data):
        duration, interval = [x.strip() for x in data.split("-")]
        self.current_di_group.setCurrentDuration(duration)
        self.current_di_group.setCurrentInterval(interval)

    def handle_current_duration_changed(self, currrent_duratiion: str):
        self.m.set_current_duration(currrent_duratiion)

    def handle_current_interval_changed(self, current_interval: str):
        self.m.set_current_interval(current_interval)

    def handle_ticker_changed_signal(self, ticker: str):
        print("Ticker =", ticker)
        print("Current Chart Type =", self.m.get_current_charttype())
        duration, interval = self.m.get_current_duration_interval()
        print("Duration =", duration)
        print("Interval =", interval)
        print("Signal ticker changed received in the parent:", ticker)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()

    mw.show()
    app.exec()
