from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QRadioButton,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QVBoxLayout,
    QComboBox,
    QScrollArea,
)
from PySide6.QtGui import QFont


class ChangeAccountValue(QWidget):
    account_value_changed = Signal(str, name="AccountValueChanged")

    def __init__(self):
        super().__init__()

        self.lbl_account_value = QLabel()
        btnChangeAcctValue = QPushButton("Change Acct Value")
        btnChangeAcctValue.clicked.connect(self.onChangeAcctAction)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Account Value:"))
        layout.addWidget(self.lbl_account_value)
        layout.setSpacing(20)
        layout.addWidget(btnChangeAcctValue)
        layout.addStretch()
        self.setLayout(layout)

    def set_account_value_lbl(self, acct_value_txt: str):
        self.lbl_account_value.setText(acct_value_txt)

    def onChangeAcctAction(self):
        text, ok_pressed = QInputDialog.getText(
            None, "Account Value", "Enter new account value:"
        )
        if ok_pressed:
            self.account_value_changed.emit(text)


class ChartTypeGroup(QGroupBox):
    chart_type_changed = Signal(str, name="ChartTypeChanged")

    def __init__(self, charttypes: list[str], preferred:str):
        super().__init__()
        self.setTitle("Chart Type")
        layout = QHBoxLayout()
        for charttype in charttypes:
            radio_button = QRadioButton(charttype)
            if charttype == preferred:
                radio_button.setChecked(True)
            radio_button.toggled.connect(self.on_charttype_changed)
            layout.addWidget(radio_button)
        layout.addStretch()
        layout.setSpacing(10)
        self.setLayout(layout)

    def on_charttype_changed(self):
        s: str = self.sender().text()
        self.chart_type_changed.emit(s)


class CurrentDIGroup(QGroupBox):
    current_duration_changed = Signal(str)
    current_interval_changed = Signal(str)

    def __init__(self):
        super().__init__()
        font = QFont("Arial", 20)

        self.setTitle("Current")
        layout = QHBoxLayout()
        col1_layout = QVBoxLayout()
        col2_layout = QVBoxLayout()

        self.lbl_duration = QLabel("Duration")
        self.lbl_interval = QLabel("Interval")
        self.cb_duration = QComboBox()
        self.cb_interval = QComboBox()
        self.cb_duration.setFont(font)
        self.cb_interval.setFont(font)

        col1_layout.addWidget(self.lbl_duration)
        col1_layout.addWidget(self.cb_duration)
        col1_layout.addStretch()
        col2_layout.addWidget(self.lbl_interval)
        col2_layout.addWidget(self.cb_interval)
        col2_layout.addStretch()

        layout.addLayout(col1_layout)
        layout.addLayout(col2_layout)
        layout.addStretch()

        self.cb_duration.currentTextChanged.connect(self.on_CurrentDurationChanged)
        self.cb_interval.currentTextChanged.connect(self.on_CurrentIntervalChanged)

        self.setLayout(layout)

    def loadDurations(self, durations: list[str]):
        self.cb_duration.addItems(durations)

    def loadIntervals(self, intervals: list[str]):
        self.cb_interval.addItems(intervals)

    def setCurrentDuration(self, duration_txt):
        self.cb_duration.setCurrentText(duration_txt)

    def setCurrentInterval(self, interval_txt) -> str:
        self.cb_interval.setCurrentText(interval_txt)

    def on_CurrentDurationChanged(self, duration: str):
        self.current_duration_changed.emit(duration)

    def on_CurrentIntervalChanged(self, interval: str):
        self.current_interval_changed.emit(interval)


class FavoriteDIGroup(QGroupBox):
    favorite_di_changed = Signal(str, name="FavoriteChanged")

    def __init__(self):
        super().__init__()
        self.setTitle("Favorites")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def addFavorites(self, favorites_list: list[str]):
        for favorite in favorites_list:
            btn = QPushButton(favorite)
            btn.clicked.connect(self.btnClicked)
            self.layout.addWidget(btn)
        self.layout.addStretch()

    def btnClicked(self):
        favorite = self.sender().text()
        self.favorite_di_changed.emit(favorite)


class TickerBtnScrollArea(QScrollArea):
    ticker_changed = Signal(str, name="TickerChanged")

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        content_widget = QWidget()
        # content_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setWidget(content_widget)

        main_tb_layout = QVBoxLayout()
        content_widget.setLayout(main_tb_layout)

        ticker_button_group = QGroupBox("Tickers")
        self.ticker_button_group_layout = QVBoxLayout()
        ticker_button_group.setLayout(self.ticker_button_group_layout)

        main_tb_layout.addWidget(ticker_button_group)
        main_tb_layout.addStretch()

    def addTickers(self, ticker_list: list[str]):
        for ticker in ticker_list:
            button = QPushButton(ticker)
            button.clicked.connect(self.btnClicked)
            self.ticker_button_group_layout.addWidget(button)
        self.ticker_button_group_layout.addStretch()

    def btnClicked(self):
        ticker: str = self.sender().text()
        self.ticker_changed.emit(ticker)
