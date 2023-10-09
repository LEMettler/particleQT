from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QStyledItemDelegate
from handler import *
import warnings
warnings.filterwarnings("ignore")
from PyQt6.QtGui import QPalette, QColor, QBrush

from matplotlib.backends.backend_qtagg import FigureCanvas
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

        self.label_info = QtWidgets.QLabel()
        self.label_info.setMinimumSize(QtCore.QSize(200, 0))
        self.label_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label_info.setObjectName("label_info")


        self.label_forces = QtWidgets.QLabel()
        self.label_forces.setMinimumSize(QtCore.QSize(200, 0))
        self.label_forces.setObjectName("label_forces")

        self.combobox_particle_group = QtWidgets.QComboBox()
        self.combobox_particle_group.addItems(['Leptons', 'Bosons', 'Baryons', 'Mesons'])
        self.combobox_particle_group.currentTextChanged.connect(self.onParticleGroupSelected)

        self.btn_add_initial = QtWidgets.QPushButton()
        self.btn_add_initial.setObjectName("btn_add_initial")
        self.btn_add_initial.clicked.connect(self.onAddFinalClicked)

        #self.btn_remove = QtWidgets.QPushButton()
        #self.btn_remove.setObjectName("btn_remove")

        self.btn_add_final = QtWidgets.QPushButton()
        self.btn_add_final.setObjectName("btn_add_final")
        self.btn_add_final.clicked.connect(self.onAddFinalClicked)


        self.table_initial = QtWidgets.QTableView()
        self.table_initial.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_initial.setObjectName("table_initial")
        self.table_initial.setMinimumWidth(700)
        self.table_initial.setMaximumHeight(125)
        self.table_initial.setMinimumHeight(125)

        self.table_final = QtWidgets.QTableView()
        self.table_final.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_final.setObjectName("table_final")
        self.table_final.setMinimumWidth(700)
        self.table_final.setMaximumHeight(125)
        self.table_final.setMinimumHeight(125)


        self.table_sum = QtWidgets.QTableView()
        self.table_sum.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.table_sum.setObjectName("table_sum")
        self.table_sum.setMinimumWidth(700)
        self.table_sum.setMaximumHeight(125)
        self.table_sum.setMinimumHeight(125)

        self.table_selection = QtWidgets.QTableView()
        self.table_selection.setMinimumWidth(300)
        self.table_selection.setMinimumHeight(500)
        self.table_selection.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows) #++
        self.table_selection.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection) #++
        self.table_selection.setObjectName("table_selection")

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, 20))
        self.menubar.setObjectName("menubar")


        #----------------------------
        self.layout = QtWidgets.QGridLayout()
        self.MainWindow.setLayout(self.layout)


        self.layout.addWidget(self.combobox_particle_group, 0, 0, 1, 2)
        self.layout.addWidget(self.table_selection, 1, 0, 5, 2)
        self.layout.addWidget(self.btn_add_initial, 6, 0)
        self.layout.addWidget(self.btn_add_final, 6, 1)


        self.layout.addWidget(self.canvas_equation, 0, 3, 1, 3)
        self.layout.addWidget(self.label_forces, 0, 7, 1, 1)
        #self.layout.addWidget(self.label_info, 1, 6)

        self.layout.addWidget(self.table_sum, 1, 3, 2, 6, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.table_initial,3, 3, 2, 6)
        self.layout.addWidget(self.table_final, 5, 3, 2, 6)
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

#######################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++
#######################################################

    def onParticleGroupSelected(self):
        selected_group = self.combobox_particle_group.currentText().lower()
        data = self.handler.getTable(selected_group)
        self.table_selection.setModel(data)

    
    def onAddInitialClicked(self):
        try:
            selected_index = self.table_selection.selectionModel().selectedRows()[0].row()
            self.handler.addInitial(self.selected_type, selected_index)
            self.updateInitialTable()
            self.updateSumTable()
            self.updateEquationCanvas()
            self.updateForces()
        except:
            print('please select a particle first')

    def onAddFinalClicked(self):
        try:
            selected_index = self.table_selection.selectionModel().selectedRows()[0].row()
            self.handler.addFinal(self.selected_type, selected_index)
            self.updateFinalTable()
            self.updateSumTable()
            self.updateEquationCanvas()
            self.updateForces()
        except:
            print('please select a particle first')

    def onRemoveClicked(self):
        self.removeSelection()
        self.updateInitialTable()
        self.updateFinalTable()
        self.updateSumTable()
        self.updateEquationCanvas()
        self.updateForces()

    def updateInitialTable(self):
        self.table_initial.setModel(self.handler.getInitial())

        
    def updateFinalTable(self):
        self.table_final.setModel(self.handler.getFinal())

    def updateSumTable(self):
        self.table_sum.setModel(self.handler.getBothSums())



#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "particleQT"))
        self.label_info.setText(_translate("MainWindow", r"A + B \rightarrow X + Y"))
        self.label_forces.setText(_translate("MainWindow", "forces"))
        self.btn_add_initial.setText(_translate("MainWindow", "add initial"))
        self.btn_add_final.setText(_translate("MainWindow", "add final"))


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
    
