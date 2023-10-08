from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QStyledItemDelegate
from handler import *
import warnings
warnings.filterwarnings("ignore")
from PyQt6.QtGui import QPalette, QColor, QBrush

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, handler): #++
        self.MainWindow = MainWindow #++
        self.handler = handler #++

        self.width, self.heigth = 1200, 600

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(self.width, self.heigth)

        #---------------
        self.canvas_equation = FigureCanvas(Figure(figsize=(5,0.75)))
        self.ax_equation = self.canvas_equation.figure.subplots()
        self.ax_equation.set_xlim(0,1)
        self.ax_equation.set_ylim(0,1)
        self.ax_equation.axis('off')
        self.text_equation = self.ax_equation.text(0.5, 0.5, r'$A + B \rightarrow X + Y$', fontsize=20, ha='center', va='center')
        #---------------

        self.label_equation = QtWidgets.QLabel()
        self.label_equation.setObjectName("label_equation")

        self.label_info = QtWidgets.QLabel()
        self.label_info.setMinimumSize(QtCore.QSize(200, 0))
        self.label_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label_info.setObjectName("label_info")


        self.label_forces = QtWidgets.QLabel()
        self.label_forces.setMinimumSize(QtCore.QSize(200, 0))
        self.label_forces.setObjectName("label_forces")

        self.layoutWidget = QtWidgets.QWidget()
        self.layoutWidget.setObjectName("layoutWidget")

        self.layout_particle_group = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.layout_particle_group.setContentsMargins(0, 0, 0, 0)
        self.layout_particle_group.setObjectName("layout_particle_group")

        self.rbtn_leptons = QtWidgets.QRadioButton(parent=self.layoutWidget)
        self.rbtn_leptons.setObjectName("rbtn_leptons")
        self.layout_particle_group.addWidget(self.rbtn_leptons)
        self.rbtn_leptons.type = 'leptons'

        self.rbtn_bosons = QtWidgets.QRadioButton(parent=self.layoutWidget)
        self.rbtn_bosons.setObjectName("rbtn_bosons")
        self.layout_particle_group.addWidget(self.rbtn_bosons)
        self.rbtn_bosons.type = 'bosons'

        self.rbtn_baryons = QtWidgets.QRadioButton(parent=self.layoutWidget)
        self.rbtn_baryons.setObjectName("rbtn_baryons")
        self.layout_particle_group.addWidget(self.rbtn_baryons)
        self.rbtn_baryons.type = 'baryons'

        self.rbtn_mesons = QtWidgets.QRadioButton(parent=self.layoutWidget)
        self.rbtn_mesons.setObjectName("rbtn_mesons")
        self.layout_particle_group.addWidget(self.rbtn_mesons)
        self.rbtn_mesons.type = 'mesons'

        self.btn_add_initial = QtWidgets.QPushButton()
        self.btn_add_initial.setObjectName("btn_add_initial")

        self.btn_remove = QtWidgets.QPushButton()
        self.btn_remove.setObjectName("btn_remove")

        self.btn_add_final = QtWidgets.QPushButton()
        self.btn_add_final.setObjectName("btn_add_final")



        self.table_initial = QtWidgets.QTableView()
        self.table_initial.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_initial.setObjectName("table_initial")
        self.table_initial.setMinimumWidth(600)

        self.table_final = QtWidgets.QTableView()
        self.table_final.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_final.setObjectName("table_final")
        self.table_final.setMinimumWidth(600)



        self.table_initial_sum = QtWidgets.QTableView()
        self.table_initial_sum.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.table_initial_sum.setObjectName("table_initial_sum")
        self.table_initial_sum.setMinimumWidth(600)
        self.table_initial_sum.setMaximumHeight(60)

        self.table_final_sum = QtWidgets.QTableView()
        self.table_final_sum.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.table_final_sum.setObjectName("table_final_sum")
        self.table_final_sum.setMinimumWidth(600)
        self.table_final_sum.setMaximumHeight(60)


        self.table_selection = QtWidgets.QTableView()
        self.table_selection.setGeometry(QtCore.QRect(390, 100, 361, 192))
        self.table_selection.setMinimumWidth(600)
        self.table_selection.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows) #++
        self.table_selection.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection) #++
        self.table_selection.setObjectName("table_selection")

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, 20))
        self.menubar.setObjectName("menubar")


        #----------------------------
        self.layout = QtWidgets.QGridLayout()
        self.MainWindow.setLayout(self.layout)

        #self.layout.addWidget(self.label_equation, 0, 4, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.canvas_equation, 0, 4, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label_forces, 2, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.layoutWidget, 2, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter) #partice type selection
        self.layout.addWidget(self.table_selection, 1, 3, 3, 8, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.btn_add_initial, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_remove, 5, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.btn_add_final, 5, 9, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.table_initial, 6, 1, 2, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.table_final, 6, 6, 2, 5, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.table_initial_sum, 9, 1, 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.table_final_sum, 9, 6, 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label_info, 10, 0, 1, 11, alignment=Qt.AlignmentFlag.AlignCenter)


        
    
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        #----------------------------------------------------- #++
        # Connect radio buttons to a slot
        self.rbtn_leptons.setChecked(True)
        #self.changeSelection()
        self.selected_type = self.rbtn_leptons.type
        self.table_selection.setModel(self.handler.getTable(self.selected_type))


        self.rbtn_leptons.toggled.connect(self.onGroupButtonClicked)
        self.rbtn_bosons.toggled.connect(self.onGroupButtonClicked)
        self.rbtn_baryons.toggled.connect(self.onGroupButtonClicked)
        self.rbtn_mesons.toggled.connect(self.onGroupButtonClicked)

        self.btn_add_initial.clicked.connect(self.onAddInitialClicked)
        self.btn_remove.clicked.connect(self.onRemoveClicked)
        self.btn_add_final.clicked.connect(self.onAddFinalClicked)

        self.table_initial.clicked.connect(self.changeSelection)
        self.table_final.clicked.connect(self.changeSelection)
        self.selected_table = None

        self.table_initial.setModel(self.handler.getInitial())
        self.table_final.setModel(self.handler.getFinal())
        #self.table_initial_sum.setModel(self.handler.getInitialSum())
        #self.table_final_sum.setModel(self.handler.getFinalSum())

        #resize tables
        for i in range(20):
            self.table_selection.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)        
            self.table_initial.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)        
            self.table_final.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) 
            #self.table_initial_sum.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)        
            #self.table_final_sum.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) 


    def changeSelection(self):
            try:
                new_selection = self.MainWindow.sender()
                if new_selection == self.table_initial:
                    self.selected_table = 'initial'
                    self.table_final.selectionModel().clearSelection()
                else:
                    self.selected_table = 'final'
                    self.table_initial.selectionModel().clearSelection()
            except:
                print('error of changeSelection()')

    def onGroupButtonClicked(self):
        radioButton = self.MainWindow.sender()
        if radioButton.isChecked():
            self.selected_type = radioButton.type
            data = self.handler.getTable(self.selected_type)
            self.table_selection.setModel(data)

    def onAddInitialClicked(self):
        try:
            selected_index = self.table_selection.selectionModel().selectedRows()[0].row()
            self.handler.addInitial(self.selected_type, selected_index)
            self.updateInitialTable()
            self.updateSumTables()
            self.updateEquationCanvas()
            self.updateForces()
        except:
            print('please select a particle first')

    def onAddFinalClicked(self):
        try:
            selected_index = self.table_selection.selectionModel().selectedRows()[0].row()
            self.handler.addFinal(self.selected_type, selected_index)
            self.updateFinalTable()
            self.updateSumTables()
            self.updateEquationCanvas()
            self.updateForces()
        except:
            print('please select a particle first')

    def onRemoveClicked(self):
        self.removeSelection()
        self.updateInitialTable()
        self.updateFinalTable()
        self.updateSumTables()
        self.updateEquationCanvas()
        self.updateForces()


    def updateInitialTable(self):
        self.table_initial.setModel(self.handler.getInitial())

        
    def updateFinalTable(self):
        self.table_final.setModel(self.handler.getFinal())

    def updateSumTables(self):
        self.table_initial_sum.setModel(self.handler.getInitialSum())
        self.table_final_sum.setModel(self.handler.getFinalSum())

    
    def updateForces(self):
        bool_em, bool_strong, bool_weak = self.handler.checkForces()
        line = f'EM: {bool_em}\nStrong: {bool_strong}\nWeak: {bool_weak}'
        self.label_forces.setText(line)


    def removeSelection(self):
        try:
            if self.selected_table == 'initial':
                selected_index = self.table_initial.selectionModel().selectedRows()[0].row()
                self.handler.removeInitial(selected_index)
            else:
                selected_index = self.table_final.selectionModel().selectedRows()[0].row()
                self.handler.removeFinal(selected_index)
        except:
            print('error in removal')
        self.updateEquationCanvas()

    def updateEquationCanvas(self):
        new_eq = self.handler.getEquation()
        self.text_equation.set_text(new_eq)
        self.text_equation.figure.canvas.draw()
        self.label_info.setText(new_eq[1:-1])

#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_equation.setText(_translate("MainWindow", "equation"))
        self.label_info.setText(_translate("MainWindow", "equation"))
        self.label_forces.setText(_translate("MainWindow", "forces"))
        self.rbtn_leptons.setText(_translate("MainWindow", "Leptons"))
        self.rbtn_bosons.setText(_translate("MainWindow", "Bosons"))
        self.rbtn_baryons.setText(_translate("MainWindow", "Baryons"))
        self.rbtn_mesons.setText(_translate("MainWindow", "Mesons"))
        self.btn_add_initial.setText(_translate("MainWindow", "add initial"))
        self.btn_add_final.setText(_translate("MainWindow", "add final"))
        self.btn_remove.setText(_translate("MainWindow", "remove"))


########################################################################
########################################################################
########################################################################
if __name__ == "__main__":
    import sys
    handler = Handler()

    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, handler)
    
    MainWindow.show()
    sys.exit(app.exec())
    
