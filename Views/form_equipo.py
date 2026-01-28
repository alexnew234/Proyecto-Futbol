from PySide6.QtWidgets import QWidget
# Importamos la interfaz que acabas de generar
from Views.form_window_ui import Ui_Form 

class FormEquipoView(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)