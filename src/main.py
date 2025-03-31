import sys
from PyQt5.QtWidgets import QApplication
from ui import CurrencyConverterApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = CurrencyConverterApp()
    converter.show()
    sys.exit(app.exec_())
    