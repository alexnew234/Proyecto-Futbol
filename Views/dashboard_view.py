from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 10, 0, 0)

        self.lbl_titulo = QLabel("")
        self.lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #B71C1C;")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setFixedHeight(30)
        layout.addWidget(self.lbl_titulo)

        self.btn_config_reloj = QPushButton("")
        self.btn_config_reloj.setCursor(Qt.PointingHandCursor)
        self.btn_config_reloj.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                padding: 8px 15px;
                border-radius: 5px;
                background-color: #444;
                color: #ddd;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #555;
                color: white;
                border-color: #777;
            }
            """
        )
        layout_btn_reloj = QHBoxLayout()
        layout_btn_reloj.addWidget(self.btn_config_reloj)
        layout_btn_reloj.setAlignment(Qt.AlignCenter)
        layout.addLayout(layout_btn_reloj)

        self.image_container = QLabel()
        self.image_container.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_container)

        grid = QGridLayout()
        grid.setSpacing(15)

        self.btn_partidos = QPushButton("")
        self.btn_resultados = QPushButton("")
        self.btn_equipos = QPushButton("")
        self.btn_participantes = QPushButton("")

        estilo_boton = """
            QPushButton {
                font-size: 18px;
                padding: 15px;
                min-width: 200px;
                min-height: 80px;
                border-radius: 10px;
                background-color: #3c3c3c;
                border: 2px solid #555;
            }
            QPushButton:hover {
                background-color: #B71C1C;
                border: 2px solid #ff5555;
            }
        """

        for btn in (
            self.btn_partidos,
            self.btn_resultados,
            self.btn_equipos,
            self.btn_participantes,
        ):
            btn.setStyleSheet(estilo_boton)
            btn.setCursor(Qt.PointingHandCursor)

        grid.addWidget(self.btn_partidos, 0, 0)
        grid.addWidget(self.btn_resultados, 0, 1)
        grid.addWidget(self.btn_equipos, 1, 0)
        grid.addWidget(self.btn_participantes, 1, 1)

        grid_container = QWidget()
        grid_container.setLayout(grid)
        layout.addWidget(grid_container)
        layout.addStretch()

        self.retranslate_ui()

    def retranslate_ui(self):
        self.lbl_titulo.setText(QCoreApplication.translate("DashboardView", "Panel de Control RFEF"))
        self.btn_config_reloj.setText(
            QCoreApplication.translate("DashboardView", "\u2699 Configuración del Reloj")
        )
        self.btn_partidos.setText(QCoreApplication.translate("DashboardView", "Gestión de Partidos"))
        self.btn_resultados.setText(
            QCoreApplication.translate("DashboardView", "Resultados / Clasificación")
        )
        self.btn_equipos.setText(QCoreApplication.translate("DashboardView", "Equipos"))
        self.btn_participantes.setText(QCoreApplication.translate("DashboardView", "Participantes"))

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
