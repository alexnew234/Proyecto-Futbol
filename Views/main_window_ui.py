# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QListView, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(919, 585)
        self.actionEquipos = QAction(MainWindow)
        self.actionEquipos.setObjectName(u"actionEquipos")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AddressBookNew))
        self.actionEquipos.setIcon(icon)
        self.actionEquipos.setMenuRole(QAction.MenuRole.NoRole)
        self.actionParticipantes = QAction(MainWindow)
        self.actionParticipantes.setObjectName(u"actionParticipantes")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ContactNew))
        self.actionParticipantes.setIcon(icon1)
        self.actionParticipantes.setMenuRole(QAction.MenuRole.NoRole)
        self.actionPartidos = QAction(MainWindow)
        self.actionPartidos.setObjectName(u"actionPartidos")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkOffline))
        self.actionPartidos.setIcon(icon2)
        self.actionPartidos.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentRevert))
        self.actionSalir.setIcon(icon3)
        self.actionSalir.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_calendario = QWidget()
        self.page_calendario.setObjectName(u"page_calendario")
        self.verticalLayout_4 = QVBoxLayout(self.page_calendario)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_titulo = QLabel(self.page_calendario)
        self.label_titulo.setObjectName(u"label_titulo")

        self.verticalLayout_4.addWidget(self.label_titulo)

        self.treeWidget_partidos = QTreeWidget(self.page_calendario)
        self.treeWidget_partidos.setObjectName(u"treeWidget_partidos")
        self.treeWidget_partidos.setAlternatingRowColors(True)
        self.treeWidget_partidos.setHeaderHidden(True)

        self.verticalLayout_4.addWidget(self.treeWidget_partidos)

        self.stackedWidget.addWidget(self.page_calendario)
        self.page_clasificacion = QWidget()
        self.page_clasificacion.setObjectName(u"page_clasificacion")
        self.label_3 = QLabel(self.page_clasificacion)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(210, 20, 121, 31))
        self.scrollArea_bracket = QScrollArea(self.page_clasificacion)
        self.scrollArea_bracket.setObjectName(u"scrollArea_bracket")
        self.scrollArea_bracket.setGeometry(QRect(10, 80, 561, 401))
        self.scrollArea_bracket.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 559, 399))
        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 40, 49, 16))
        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(220, 40, 71, 16))
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(440, 40, 49, 16))
        self.scrollArea_bracket.setWidget(self.scrollAreaWidgetContents)
        self.stackedWidget.addWidget(self.page_clasificacion)
        self.page_equipos = QWidget()
        self.page_equipos.setObjectName(u"page_equipos")
        
        # Layout principal responsivo para la página de equipos
        main_layout_equipos = QHBoxLayout(self.page_equipos)
        main_layout_equipos.setContentsMargins(10, 10, 10, 10)
        main_layout_equipos.setSpacing(10)
        
        self.list_Teams = QListView(self.page_equipos)
        self.list_Teams.setObjectName(u"list_Teams")
        self.list_Teams.setMinimumWidth(120)
        self.list_Teams.setMaximumWidth(200)
        
        self.groupBox_detalles = QGroupBox(self.page_equipos)
        self.groupBox_detalles.setObjectName(u"groupBox_detalles")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_detalles)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        self.tableWidget = QTableWidget(self.groupBox_detalles)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_2.addWidget(self.tableWidget)
        
        # Layout vertical para botones
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)
        
        self.pushButton_anadir_equipo = QPushButton(self.page_equipos)
        self.pushButton_anadir_equipo.setObjectName(u"pushButton_anadir_equipo")

        buttons_layout.addWidget(self.pushButton_anadir_equipo)

        self.pushButton_editar_equipo = QPushButton(self.page_equipos)
        self.pushButton_editar_equipo.setObjectName(u"pushButton_editar_equipo")

        buttons_layout.addWidget(self.pushButton_editar_equipo)

        self.pushButton_eliminar_equipo = QPushButton(self.page_equipos)
        self.pushButton_eliminar_equipo.setObjectName(u"pushButton_eliminar_equipo")

        buttons_layout.addWidget(self.pushButton_eliminar_equipo)
        
        buttons_layout.addStretch()
        
        self.list_Teams_layout = QVBoxLayout()
        self.list_Teams_layout.addWidget(self.list_Teams)
        self.list_Teams_layout.addLayout(buttons_layout)
        
        list_container = QWidget()
        list_container.setLayout(self.list_Teams_layout)
        
        main_layout_equipos.addWidget(list_container, 1)
        main_layout_equipos.addWidget(self.groupBox_detalles, 3)

        self.stackedWidget.addWidget(self.page_equipos)
        self.page_participantes = QWidget()
        self.page_participantes.setObjectName(u"page_participantes")
        self.verticalLayout = QVBoxLayout(self.page_participantes)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.page_participantes)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.comboBox = QComboBox(self.page_participantes)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.label_filtrar = QLabel(self.page_participantes)
        self.label_filtrar.setObjectName(u"label_filtrar")

        self.verticalLayout.addWidget(self.label_filtrar)

        self.label_buscar = QLabel(self.page_participantes)
        self.label_buscar.setObjectName(u"label_buscar")

        self.verticalLayout.addWidget(self.label_buscar)

        self.tableWidget_2 = QTableWidget(self.page_participantes)
        if (self.tableWidget_2.columnCount() < 9):
            self.tableWidget_2.setColumnCount(9)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(7, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(8, __qtablewidgetitem13)
        self.tableWidget_2.setObjectName(u"tableWidget_2")

        self.verticalLayout.addWidget(self.tableWidget_2)

        self.pushButton_nuevo_participante = QPushButton(self.page_participantes)
        self.pushButton_nuevo_participante.setObjectName(u"pushButton_nuevo_participante")

        self.verticalLayout.addWidget(self.pushButton_nuevo_participante)

        self.pushButton_generar_rondas = QPushButton(self.page_participantes)
        self.pushButton_generar_rondas.setObjectName(u"pushButton_generar_rondas")

        self.verticalLayout.addWidget(self.pushButton_generar_rondas)

        self.stackedWidget.addWidget(self.page_participantes)
        self.page_resultados = QWidget()
        self.page_resultados.setObjectName(u"page_resultados")
        self.groupBox_datos_generales = QGroupBox(self.page_resultados)
        self.groupBox_datos_generales.setObjectName(u"groupBox_datos_generales")
        self.groupBox_datos_generales.setGeometry(QRect(20, 10, 551, 91))
        self.label_fecha = QLabel(self.groupBox_datos_generales)
        self.label_fecha.setObjectName(u"label_fecha")
        self.label_fecha.setGeometry(QRect(30, 40, 49, 16))
        self.label_hora = QLabel(self.groupBox_datos_generales)
        self.label_hora.setObjectName(u"label_hora")
        self.label_hora.setGeometry(QRect(190, 40, 49, 16))
        self.label__arbitro = QLabel(self.groupBox_datos_generales)
        self.label__arbitro.setObjectName(u"label__arbitro")
        self.label__arbitro.setGeometry(QRect(380, 40, 49, 16))
        self.groupBox = QGroupBox(self.page_resultados)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 110, 551, 381))
        self.label_equipo_local = QLabel(self.groupBox)
        self.label_equipo_local.setObjectName(u"label_equipo_local")
        self.label_equipo_local.setGeometry(QRect(40, 30, 101, 31))
        self.label_equipo_visitante = QLabel(self.groupBox)
        self.label_equipo_visitante.setObjectName(u"label_equipo_visitante")
        self.label_equipo_visitante.setGeometry(QRect(310, 30, 121, 31))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(210, 40, 21, 16))
        self.spinBox_GOLES_LOCAL = QSpinBox(self.groupBox)
        self.spinBox_GOLES_LOCAL.setObjectName(u"spinBox_GOLES_LOCAL")
        self.spinBox_GOLES_LOCAL.setGeometry(QRect(40, 90, 68, 23))
        self.spinBox_GOLES_LOCAL.setMaximum(20)
        self.spinBox_goles_visitante = QSpinBox(self.groupBox)
        self.spinBox_goles_visitante.setObjectName(u"spinBox_goles_visitante")
        self.spinBox_goles_visitante.setGeometry(QRect(340, 90, 68, 23))
        self.spinBox_goles_visitante.setMaximum(20)
        self.tabWidget = QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 140, 501, 221))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tableWidget_local = QTableWidget(self.tab)
        if (self.tableWidget_local.columnCount() < 4):
            self.tableWidget_local.setColumnCount(4)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_local.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_local.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_local.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_local.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        self.tableWidget_local.setObjectName(u"tableWidget_local")
        self.tableWidget_local.setGeometry(QRect(10, 10, 471, 181))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tableWidget_visitante = QTableWidget(self.tab_2)
        if (self.tableWidget_visitante.columnCount() < 4):
            self.tableWidget_visitante.setColumnCount(4)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_visitante.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_visitante.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_visitante.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_visitante.setHorizontalHeaderItem(3, __qtablewidgetitem21)
        self.tableWidget_visitante.setObjectName(u"tableWidget_visitante")
        self.tableWidget_visitante.setGeometry(QRect(10, 10, 471, 181))
        self.tabWidget.addTab(self.tab_2, "")
        self.stackedWidget.addWidget(self.page_resultados)

        self.verticalLayout_3.addWidget(self.stackedWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 919, 33))
        self.menuCreditos = QMenu(self.menubar)
        self.menuCreditos.setObjectName(u"menuCreditos")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuCreditos.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.toolBar.addAction(self.actionEquipos)
        self.toolBar.addAction(self.actionParticipantes)
        self.toolBar.addAction(self.actionPartidos)
        self.toolBar.addAction(self.actionSalir)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionEquipos.setText(QCoreApplication.translate("MainWindow", u"Equipos", None))
        self.actionParticipantes.setText(QCoreApplication.translate("MainWindow", u"Participantes", None))
        self.actionPartidos.setText(QCoreApplication.translate("MainWindow", u"Partidos", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.label_titulo.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Calendario del torneo</span></p></body></html>", None))
        ___qtreewidgetitem = self.treeWidget_partidos.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Estado", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u00c1rbitro", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Fecha", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Enfrentamiento", None));
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Fase Final</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Cuartos", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Semifinales", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Final", None))
        self.groupBox_detalles.setTitle(QCoreApplication.translate("MainWindow", u"Detalles", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Posici\u00f3n", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Curso", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Color Camiseta", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Escudo", None));
        self.pushButton_anadir_equipo.setText(QCoreApplication.translate("MainWindow", u"A\u00f1adir equipo", None))
        self.pushButton_editar_equipo.setText(QCoreApplication.translate("MainWindow", u"Editar equipo", None))
        self.pushButton_eliminar_equipo.setText(QCoreApplication.translate("MainWindow", u"Eliminar equipo", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"(Todos/Jugador/\u00c1rbitro)", None))
        self.label_filtrar.setText(QCoreApplication.translate("MainWindow", u"Filtrar por:", None))
        self.label_buscar.setText(QCoreApplication.translate("MainWindow", u"Buscar:", None))
        ___qtablewidgetitem5 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem6 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Fecha Nacimiento", None));
        ___qtablewidgetitem7 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Jugador", None));
        ___qtablewidgetitem8 = self.tableWidget_2.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Curso", None));
        ___qtablewidgetitem9 = self.tableWidget_2.horizontalHeaderItem(4)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u00c1rbitro", None));
        ___qtablewidgetitem10 = self.tableWidget_2.horizontalHeaderItem(5)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Posici\u00f3n", None));
        ___qtablewidgetitem11 = self.tableWidget_2.horizontalHeaderItem(6)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Tarjetas Amarillas", None));
        ___qtablewidgetitem12 = self.tableWidget_2.horizontalHeaderItem(7)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Tarjetas Rojas", None));
        ___qtablewidgetitem13 = self.tableWidget_2.horizontalHeaderItem(8)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Goles", None));
        self.pushButton_nuevo_participante.setText(QCoreApplication.translate("MainWindow", u"Nuevo Participante", None))
        self.pushButton_generar_rondas.setText(QCoreApplication.translate("MainWindow", u"Generar Rondas", None))
        self.groupBox_datos_generales.setTitle(QCoreApplication.translate("MainWindow", u"Datos Generales", None))
        self.label_fecha.setText(QCoreApplication.translate("MainWindow", u"Fecha: ", None))
        self.label_hora.setText(QCoreApplication.translate("MainWindow", u"Hora", None))
        self.label__arbitro.setText(QCoreApplication.translate("MainWindow", u"\u00c1rbitro", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Marcador Global", None))
        self.label_equipo_local.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Equipo Local</span></p></body></html>", None))
        self.label_equipo_visitante.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Equipo Visitante</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">VS</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem14 = self.tableWidget_local.horizontalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem15 = self.tableWidget_local.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Goles", None));
        ___qtablewidgetitem16 = self.tableWidget_local.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Tarjetas Amarillas", None));
        ___qtablewidgetitem17 = self.tableWidget_local.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Tarjetas Rojas", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Jug Locales", None))
        ___qtablewidgetitem18 = self.tableWidget_visitante.horizontalHeaderItem(0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem19 = self.tableWidget_visitante.horizontalHeaderItem(1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Goles", None));
        ___qtablewidgetitem20 = self.tableWidget_visitante.horizontalHeaderItem(2)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Tarjetas Amarillas", None));
        ___qtablewidgetitem21 = self.tableWidget_visitante.horizontalHeaderItem(3)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Tarjetas Rojas", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Jug Visitantes", None))
        self.menuCreditos.setTitle(QCoreApplication.translate("MainWindow", u"Cr\u00e9ditos", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainWindow", u"Ayuda", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

