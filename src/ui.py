from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QSize
from api import CurrencyConverterAPI
from datetime import datetime
import os


class CurrencyConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real Time Currency Converter")
        self.api = CurrencyConverterAPI()
        self.rates = {}

        script_dir = os.path.dirname(os.path.abspath(__file__))
        style_path = os.path.join(script_dir, "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as style_file:
                self.setStyleSheet(style_file.read())

        self.init_ui()

    def init_ui(self):
        # Layouts
        main_layout = QVBoxLayout()
        top_label_layout = QVBoxLayout()
        middle_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        icon_path = os.path.join(project_dir, "img", "euro.png")
        self.setWindowIcon(QIcon(icon_path))

        # Top Label
        self.welcome_label = QLabel("Welcome to Currency Converter")
        self.welcome_label.setObjectName("header")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        self.exchange_info_label = QLabel("Fetching exchange rates...")
        self.exchange_info_label.setObjectName("info_label")
        self.exchange_info_label.setAlignment(Qt.AlignCenter)

        # Input/Output Fields
        self.from_currency_combo = QComboBox()
        self.from_currency_combo.addItems(["Loading..."])
        self.to_currency_combo = QComboBox()
        self.to_currency_combo.addItems(["Loading..."])

        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Enter amount")
        self.input_amount.setMinimumWidth(100)

        self.output_amount = QLineEdit()
        self.output_amount.setReadOnly(True)
        self.output_amount.setMinimumWidth(100)

        # Swap Button
        self.swap_button = QPushButton()
        path_to_swap_icon = os.path.join(project_dir, "img", "ikona.png")
        self.swap_button.setIcon(QIcon(path_to_swap_icon))
        self.swap_button.setIconSize(QSize(32, 32))
        self.swap_button.clicked.connect(self.swap_currency)
        self.swap_button.setFixedWidth(40)

        # Convert Button
        self.convert_button = QPushButton("Convert")
        self.convert_button.setObjectName("convert")
        self.convert_button.clicked.connect(self.convert_currency)

        # Adding Widgets
        top_label_layout.addWidget(self.welcome_label)
        top_label_layout.addWidget(self.exchange_info_label)

        middle_layout.addWidget(self.from_currency_combo, stretch=1)
        middle_layout.addWidget(self.input_amount, stretch=2)
        middle_layout.addWidget(self.swap_button, stretch=0)
        middle_layout.addWidget(self.to_currency_combo, stretch=1)
        middle_layout.addWidget(self.output_amount, stretch=2)

        bottom_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(top_label_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

        # Setting the main layout
        self.setLayout(main_layout)

        # Set fixed size for the window
        self.setFixedSize(850, 400)

        # Fetch currency rates
        self.fetch_exchange_rates()

    def fetch_exchange_rates(self):
        data = self.api.fetch_currencies()
        if data:
            self.rates = data["conversion_rates"]
            self.update_currency_list()

            last_update_raw = data['time_last_update_utc']
            last_update_datetime = datetime.strptime(last_update_raw, "%a, %d %b %Y %H:%M:%S %z")
            formatted_date = last_update_datetime.strftime("%d-%m-%Y %H:%M:%S GMT")
            self.exchange_info_label.setText(f"Base: USD | Last updated: {formatted_date}")
        else:
            self.exchange_info_label.setText("Failed to fetch exchange rates!")

    def update_currency_list(self):
        currencies = list(self.rates.keys())
        self.from_currency_combo.clear()
        self.to_currency_combo.clear()
        self.from_currency_combo.addItems(currencies)
        self.to_currency_combo.addItems(currencies)

        if "EUR" in currencies:
            self.to_currency_combo.setCurrentText("EUR")

    def convert_currency(self):
        try:
            amount = float(self.input_amount.text())
            from_currency = self.from_currency_combo.currentText()
            to_currency = self.to_currency_combo.currentText()

            if from_currency in self.rates and to_currency in self.rates:
                converted = amount * (self.rates[to_currency] / self.rates[from_currency])
                self.output_amount.setText(f"{converted:.2f}")
            else:
                self.output_amount.setText("Invalid currency")
        except ValueError:
            self.output_amount.setText("Invalid input")
        except Exception as e:
            self.output_amount.setText("Conversion error")
            print(f"Error: {e}")

    def swap_currency(self):

        from_currency = self.from_currency_combo.currentText()
        to_currency = self.to_currency_combo.currentText()

        self.from_currency_combo.setCurrentText(to_currency)
        self.to_currency_combo.setCurrentText(from_currency)

        try:
            amount = float(self.input_amount.text())
            self.input_amount.setText(self.output_amount.text())
            self.output_amount.setText(f"{amount:.2f}")
        except ValueError:
            pass
