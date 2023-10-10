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
        self.text_equation = self.ax_equation.text(0.5, 0.5, r'$\mathrm{Initial} \rightarrow \mathrm{Final}$', fontsize=20, ha='center', va='center')
        #---------------

        self.label_info = QtWidgets.QLabel()
        self.label_info.setMinimumSize(QtCore.QSize(200, 0))
        self.label_info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label_info.setObjectName("label_info")


        self.label_forces = QtWidgets.QLabel()
        self.label_forces.setMinimumSize(QtCore.QSize(200, 0))
        self.label_forces.setObjectName("label_forces")
        self.label_forces.setFont(QtGui.QFont('Arial', 12))

        self.combobox_particle_group = QtWidgets.QComboBox()
        self.combobox_particle_group.addItems(['Leptons', 'Bosons', 'Baryons', 'Mesons'])
        self.combobox_particle_group.currentTextChanged.connect(self.onParticleGroupSelected)
        self.combobox_particle_group.setFont(QtGui.QFont('Arial', 12))

        self.btn_add_initial = QtWidgets.QPushButton()
        self.btn_add_initial.setObjectName("btn_add_initial")
        self.btn_add_initial.clicked.connect(self.onAddInitialClicked)
        self.btn_add_initial.setFont(QtGui.QFont('Arial', 12))


        self.btn_add_final = QtWidgets.QPushButton()
        self.btn_add_final.setObjectName("btn_add_final")
        self.btn_add_final.clicked.connect(self.onAddFinalClicked)
        self.btn_add_final.setFont(QtGui.QFont('Arial', 12))

        self.btn_complete = QtWidgets.QPushButton()
        self.btn_complete.setObjectName("btn_add_final")
        self.btn_complete.clicked.connect(self.onCompleteClicked)
        self.btn_complete.setFont(QtGui.QFont('Arial', 12))



        self.table_initial = QtWidgets.QTableView()
        self.table_initial.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_initial.setObjectName("table_initial")
        self.table_initial.setMinimumWidth(700)
        self.table_initial.setMaximumHeight(125)
        self.table_initial.setMinimumHeight(125)
        self.table_initial.setModel(self.handler.getInitial())
        self.table_initial.clicked.connect(self.changeSelection)
        self.table_initial.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_initial.customContextMenuRequested.connect(self.onRightClickDeleteMenu)


        self.table_final = QtWidgets.QTableView()
        self.table_final.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_final.setObjectName("table_final")
        self.table_final.setMinimumWidth(700)
        self.table_final.setMaximumHeight(125)
        self.table_final.setMinimumHeight(125)
        self.table_final.setModel(self.handler.getFinal())
        self.table_final.clicked.connect(self.changeSelection)
        self.selected_table = None
        self.table_final.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_final.customContextMenuRequested.connect(self.onRightClickDeleteMenu)
        

        self.table_sum = QtWidgets.QTableView()
        self.table_sum.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.table_sum.setObjectName("table_sum")
        #self.table_sum.setMaximumWidth(700)
        self.table_sum.setMaximumHeight(90)
        self.table_sum.setMinimumHeight(90)
        self.table_sum.setModel(self.handler.getBothSums())


        self.table_selection = QtWidgets.QTableView()
        self.table_selection.setMinimumWidth(300)
        self.table_selection.setMinimumHeight(500)
        self.table_selection.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows) #++
        self.table_selection.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection) #++
        self.table_selection.setObjectName("table_selection")
        self.table_selection.setModel(self.handler.getTable('leptons'))
        self.table_selection.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_selection.customContextMenuRequested.connect(self.onRightClickAddMenu)
        

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


        self.layout.addWidget(self.canvas_equation, 0, 3, 1, 2)
        self.layout.addWidget(self.label_forces, 0, 6, 1, 1)
        #self.layout.addWidget(self.label_info, 1, 7)
        self.layout.addWidget(self.btn_complete, 0, 7)

        labelInitialName = QtWidgets.QLabel('Initial particles')
        labelInitialName.setFont(QtGui.QFont('Arial', 16))
        labelFinalName = QtWidgets.QLabel('Final particles')
        labelFinalName.setFont(QtGui.QFont('Arial', 16))

        self.layout.addWidget(self.table_sum, 1, 3, 1, 6)
        self.layout.addWidget(self.table_initial,3, 3, 1, 6, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.table_final, 5, 3, 1, 6, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.layout.addWidget(labelInitialName, 2, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(labelFinalName, 4, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignBottom)

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.updateForces()

        #resize tables
        for i in range(5):
            self.table_selection.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)        
        for i in range(19):
            self.table_initial.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)        
            self.table_final.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) 
        for i in range(17):
            self.table_sum.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)        




#######################################################
#++++++++++++++++++++++++++++++++++++++++++++++++++++++
#######################################################
    def onCompleteClicked(self):
        pass

    def onRightClickAddMenu(self, event):
        self.menu = QtWidgets.QMenu(self.MainWindow)

        add_initial_action = QtGui.QAction('Add initial', self.MainWindow)
        add_initial_action.triggered.connect(lambda: self.addInitialPerMenu(event))
        add_final_action = QtGui.QAction('Add final', self.MainWindow)
        add_final_action.triggered.connect(lambda: self.addFinalPerMenu(event))
        
        self.menu.addAction(add_initial_action)
        self.menu.addAction(add_final_action)
        self.menu.popup(QtGui.QCursor.pos())

    def addInitialPerMenu(self, event):
        clicked_index = self.table_selection.rowAt(event.y())
        selected_type = self.combobox_particle_group.currentText().lower()

        self.handler.addInitial(selected_type, clicked_index)
        self.updateInitialTable()
        self.updateSumTable()
        self.updateEquationCanvas()
        self.updateForces()

    def addFinalPerMenu(self, event):
        clicked_index = self.table_selection.rowAt(event.y())
        selected_type = self.combobox_particle_group.currentText().lower()
        
        self.handler.addFinal(selected_type, clicked_index)
        self.updateFinalTable()
        self.updateSumTable()
        self.updateEquationCanvas()
        self.updateForces()


    def onRightClickDeleteMenu(self, event):
        self.menu = QtWidgets.QMenu(self.MainWindow)
        delete_action = QtGui.QAction('Delete', self.MainWindow)

        sender_table = self.MainWindow.sender()
        if sender_table == self.table_initial:
            delete_action.triggered.connect(lambda: self.deleteRowInitial(event))
        else:
            delete_action.triggered.connect(lambda: self.deleteRowFinal(event))

        self.menu.addAction(delete_action)
        self.menu.popup(QtGui.QCursor.pos())

    def deleteRowInitial(self, event):        
        clicked_index = self.table_initial.rowAt(event.y())
        self.handler.removeInitial(clicked_index)
        self.updateInitialTable()
        self.updateFinalTable()
        self.updateSumTable()
        self.updateEquationCanvas()
        self.updateForces()


    def deleteRowFinal(self, event):        
        clicked_index = self.table_final.rowAt(event.y())
        self.handler.removeFinal(clicked_index)        
        self.updateInitialTable()
        self.updateFinalTable()
        self.updateSumTable()
        self.updateEquationCanvas()
        self.updateForces()


    def onParticleGroupSelected(self):
        selected_group = self.combobox_particle_group.currentText().lower()
        data = self.handler.getTable(selected_group)
        self.table_selection.setModel(data)



    def onAddInitialClicked(self):
        try:
            selected_type = self.combobox_particle_group.currentText().lower()
            selected_index = self.table_selection.selectionModel().selectedRows()[0].row()
            self.handler.addInitial(selected_type, selected_index)
            self.updateInitialTable()
            self.updateSumTable()
            self.updateEquationCanvas()
            self.updateForces()
        except:
            print('please select a particle first')

    def onAddFinalClicked(self):
        try:
            selected_type = self.combobox_particle_group.currentText().lower()
            selected_index = self.table_selection.selectionModel().selectedRows()[0].row()
            self.handler.addFinal(selected_type, selected_index)
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
        #self.updateEquationCanvas()

    
    def updateEquationCanvas(self):
        new_eq = self.handler.getEquation()
        self.text_equation.set_text(new_eq)
        self.text_equation.figure.canvas.draw()
        self.label_info.setText(new_eq[1:-1])

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







#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "particleQT"))
        self.label_info.setText(_translate("MainWindow", r"\mathrm{Initial} \rightarrow \mathrm{Final}"))
        self.label_forces.setText(_translate("MainWindow", "forces"))
        self.btn_add_initial.setText(_translate("MainWindow", "Add initial"))
        self.btn_add_final.setText(_translate("MainWindow", "Add final"))
        self.btn_complete.setText(_translate("MainWindow", "Complete"))


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
    
