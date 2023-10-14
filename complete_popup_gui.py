from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from handler import *

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure


class CompleteDialog(QDialog):
    def __init__(self, handler):
        super().__init__()
        self.setWindowTitle("Complete interaction")

        self.handler = handler
        self.interactionBuilder = InteractionBuilder(self.handler, [], 1)


        label_title_forces = QtWidgets.QLabel('Forces')
        label_title_forces.setFont(QtGui.QFont('Arial', 12))

        self.checkbox_em = QtWidgets.QCheckBox('EM')
        self.checkbox_strong = QtWidgets.QCheckBox('Strong')
        self.checkbox_weak = QtWidgets.QCheckBox('Weak')
        self.checkbox_em.setCheckState(Qt.CheckState.Checked)
        self.checkbox_strong.setCheckState(Qt.CheckState.Checked)
        self.checkbox_weak.setCheckState(Qt.CheckState.Checked)

        label_title_n_particles = QtWidgets.QLabel('Final particles to add')
        label_title_n_particles.setFont(QtGui.QFont('Arial', 12))

        self.combobox_n_particles = QtWidgets.QComboBox()
        self.combobox_n_particles.addItems(['1', '2', '3', '4'])
        #self.combobox_n_particles.currentTextChanged.connect()

        self.btn_find_interactions = QtWidgets.QPushButton('Calculate')
        self.btn_find_interactions.clicked.connect(self.onCalculateClicked)

        self.canvas_equation = FigureCanvas(Figure(figsize=(3,0.75)))
        self.ax_equation = self.canvas_equation.figure.subplots()
        self.ax_equation.set_xlim(0,1)
        self.ax_equation.set_ylim(0,1)
        self.ax_equation.axis('off')
        self.text_equation = self.ax_equation.text(0.5, 0.5, r'$\mathrm{Initial} \rightarrow \mathrm{Final}$', fontsize=20, ha='center', va='center')
        

        self.btn_left = QtWidgets.QPushButton('<-')
        self.btn_choose = QtWidgets.QPushButton('Choose')
        self.btn_right = QtWidgets.QPushButton('->')


        self.layout_calculating = QtWidgets.QVBoxLayout()
        self.layout_calculating.addWidget(label_title_forces)
        self.layout_calculating.addWidget(self.checkbox_em)
        self.layout_calculating.addWidget(self.checkbox_strong)
        self.layout_calculating.addWidget(self.checkbox_weak)
        self.layout_calculating.addWidget(label_title_n_particles)
        self.layout_calculating.addWidget(self.combobox_n_particles)
        self.layout_calculating.addWidget(self.btn_find_interactions)

        self.layout_btns = QtWidgets.QHBoxLayout()
        self.layout_btns.addWidget(self.btn_left)
        self.layout_btns.addWidget(self.btn_choose)
        self.layout_btns.addWidget(self.btn_right)

        self.layout_preview = QtWidgets.QVBoxLayout()
        self.layout_preview.addWidget(self.canvas_equation)
        self.layout_preview.addLayout(self.layout_btns)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.layout_calculating)
        self.layout.addLayout(self.layout_preview)

        self.setLayout(self.layout)


    def onCalculateClicked(self):
        list_forces = []
        empty = True
        if self.checkbox_weak.isChecked():
            list_forces.append('weak')
            empty = False
        if self.checkbox_em.isChecked():
            list_forces.append('em')
            empty = False
        if self.checkbox_strong.isChecked():
            list_forces.append('strong')
            empty = False

        if empty:
            self.updateEquationCanvas(r'\mathrm{Mark at least one force.}')
        else:
            n_particles = int(self.combobox_n_particles.currentText())
            self.interactionBuilder.list_forces = list_forces
            self.interactionBuilder.n_particles = n_particles
            self.interactionBuilder.buildInteraction()

            self.updateDisplay()


#TODO: change checkboxes to a selection above the canvas
#
#show equations on display
#

    def updateEquationCanvas(self, text):
        self.text_equation.set_text(text)
        self.text_equation.figure.canvas.draw()


    def updateDisplay(self):
        print('update Display')
        pass