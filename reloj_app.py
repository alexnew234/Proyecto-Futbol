import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

from Views.reloj_widget import RelojDigital, ModoReloj
from Views.reloj_config_view import RelojConfigView


def _build_clock_tab() -> QWidget:
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setAlignment(Qt.AlignCenter)

    reloj = RelojDigital()
    reloj.mode = ModoReloj.CLOCK
    reloj.is24Hour = True
    reloj.alarmEnabled = False
    reloj.setFixedSize(360, 90)
    reloj.start()

    layout.addWidget(reloj, 0, Qt.AlignCenter)
    return tab


def main() -> int:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Reloj Digital - Componente")

    layout = QVBoxLayout(window)
    layout.setContentsMargins(10, 10, 10, 10)

    tabs = QTabWidget()
    tabs.addTab(_build_clock_tab(), "Reloj")
    tabs.addTab(RelojConfigView(), "Configuracion")

    layout.addWidget(tabs)

    window.setMinimumSize(900, 520)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
