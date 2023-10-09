import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui
import warnings
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

class Handler:
    def __init__(self):
        self.df_leptons = pd.read_csv('tables/leptons.csv').rename(columns={'baryonnumber': 'Baryon', 'leptonnumber': 'Lepton'})
        self.df_baryons = pd.read_csv('tables/baryons.csv').rename(columns={'baryonnumber': 'Baryon', 'leptonnumber': 'Lepton'})
        self.df_mesons = pd.read_csv('tables/mesons.csv').rename(columns={'baryonnumber': 'Baryon', 'leptonnumber': 'Lepton'})
        self.df_bosons = pd.read_csv('tables/bosons.csv').rename(columns={'baryonnumber': 'Baryon', 'leptonnumber': 'Lepton'})
        self.type_dict = {'leptons': self.df_leptons,
                          'mesons': self.df_mesons,
                          'baryons': self.df_baryons,
                          'bosons': self.df_bosons}

        self.df_initial = pd.DataFrame(columns=self.df_baryons.columns)
        self.df_final = pd.DataFrame(columns=self.df_baryons.columns)        
        self.sum_cols = ['Q', 'J', 'P', 'Baryon', 'Lepton', 'T', 'T_3', 'I', 'I_3', 'S', 'C', 'B', 'T.1', 'L_e', 'L_mu', 'L_tau']
        

    def getTable(self, particle_type):
        mask_columns = ['name', 'symbol', 'Q', 'J', 'quarks']
        if particle_type == 'leptons':
            return PandasModel(self.df_leptons[mask_columns])
        elif particle_type == 'mesons':
            return PandasModel(self.df_mesons[mask_columns])
        elif particle_type == 'bosons':
            return PandasModel(self.df_bosons[mask_columns])
        else:
            return PandasModel(self.df_baryons[mask_columns])
        
    def getInitial(self):
        return PandasModel(self.df_initial.drop(columns=['idx']))
    
    def getFinal(self):
        return PandasModel(self.df_final.drop(columns=['idx']))        
    
    def getEquation(self):
        lhs = r' + '.join(self.df_initial.symbol.tolist())
        rhs = r' + '.join(self.df_final.symbol.tolist())

        return r'$ ' + lhs + r' \rightarrow ' + rhs + r' $'
        
    def getInitialSum(self):
        df = self.df_initial.copy()[self.sum_cols]

        df_vals = {'Q': [df.Q.sum()],
                   'J': [df.J.sum()],
                   'P': [df.P.product()],
                   'Baryon': [df.Baryon.sum()],
                   'Lepton': [df.Lepton.sum()],
                   'T': [df['T'].sum()],
                   'T_3': [df.T_3.sum()],
                   'I': [df.I.sum()],
                   'I_3': [df.I_3.sum()],
                   'S': [df.S.sum()],
                   'C': [df.C.sum()],
                   'B': [df.B.sum()],
                   'T.1': [df['T.1'].sum()],
                   'L_e': [df.L_e.sum()],
                   'L_mu': [df.L_mu.sum()],
                   'L_tau': [df.L_tau.sum()]}
        return PandasModelColorSelection(pd.DataFrame().from_dict(df_vals), self.getConservations()[0])
        
    
    def getFinalSum(self):
        df = self.df_final.copy()[self.sum_cols]
        df_vals = {'Q': [df.Q.sum()],
                   'J': [df.J.sum()],
                   'P': [df.P.product()],
                   'Baryon': [df.Baryon.sum()],
                   'Lepton': [df.Lepton.sum()],
                   'T': [df['T'].sum()],
                   'T_3': [df.T_3.sum()],
                   'I': [df.I.sum()],
                   'I_3': [df.I_3.sum()],
                   'S': [df.S.sum()],
                   'C': [df.C.sum()],
                   'B': [df.B.sum()],
                   'T.1': [df['T.1'].sum()],
                   'L_e': [df.L_e.sum()],
                   'L_mu': [df.L_mu.sum()],
                   'L_tau': [df.L_tau.sum()]}
        return PandasModelColorSelection(pd.DataFrame().from_dict(df_vals), self.getConservations()[0])
    
    def getBothSums(self):
        df = self.df_initial.copy()[self.sum_cols]
        dict_initial = {' ': ['Initial'],
                        'Q': [df.Q.sum()],
                   'J': [df.J.sum()],
                   'P': [df.P.product()],
                   'Baryon': [df.Baryon.sum()],
                   'Lepton': [df.Lepton.sum()],
                   'T': [df['T'].sum()],
                   'T_3': [df.T_3.sum()],
                   'I': [df.I.sum()],
                   'I_3': [df.I_3.sum()],
                   'S': [df.S.sum()],
                   'C': [df.C.sum()],
                   'B': [df.B.sum()],
                   'T.1': [df['T.1'].sum()],
                   'L_e': [df.L_e.sum()],
                   'L_mu': [df.L_mu.sum()],
                   'L_tau': [df.L_tau.sum()]}
        
        df = self.df_final.copy()[self.sum_cols]
        dict_final = {' ': ['Final'],
                    'Q': [df.Q.sum()],
                   'J': [df.J.sum()],
                   'P': [df.P.product()],
                   'Baryon': [df.Baryon.sum()],
                   'Lepton': [df.Lepton.sum()],
                   'T': [df['T'].sum()],
                   'T_3': [df.T_3.sum()],
                   'I': [df.I.sum()],
                   'I_3': [df.I_3.sum()],
                   'S': [df.S.sum()],
                   'C': [df.C.sum()],
                   'B': [df.B.sum()],
                   'T.1': [df['T.1'].sum()],
                   'L_e': [df.L_e.sum()],
                   'L_mu': [df.L_mu.sum()],
                   'L_tau': [df.L_tau.sum()]}
        
        ret_df = pd.concat((pd.DataFrame().from_dict(dict_initial), pd.DataFrame().from_dict(dict_final)))
        list_conservation = []
        for i, key in enumerate(dict_initial.keys()):
            if key == ' ':
                pass
            elif key == 'J':
                #special case J: must both be .0 or .5
                J_comp = (dict_initial['J'][0]%1.0 == 0.0) == (dict_final['J'][0]%1.0 == 0.0)
                list_conservation.append(i)
            elif key == 'T':
                T_comp = (dict_initial['T'][0]%1.0 == 0.0) == (dict_final['T'][0]%1.0 == 0.0)
                list_conservation.append(i)
            else:
                if dict_initial[key] == dict_final[key]:
                    list_conservation.append(i)

        return PandasModelColorSelection(ret_df, list_conservation)

        


    def getConservations(self):
        df = self.df_initial.copy()[self.sum_cols]

        dict_initial = {'Q': [df.Q.sum()],
                   'J': [df.J.sum()],
                   'P': [df.P.product()],
                   'Baryon': [df.Baryon.sum()],
                   'Lepton': [df.Lepton.sum()],
                   'T': [df['T'].sum()],
                   'T_3': [df.T_3.sum()],
                   'I': [df.I.sum()],
                   'I_3': [df.I_3.sum()],
                   'S': [df.S.sum()],
                   'C': [df.C.sum()],
                   'B': [df.B.sum()],
                   'T.1': [df['T.1'].sum()],
                   'L_e': [df.L_e.sum()],
                   'L_mu': [df.L_mu.sum()],
                   'L_tau': [df.L_tau.sum()]}
        
        df = self.df_final.copy()[self.sum_cols]
        dict_final = {'Q': [df.Q.sum()],
                   'J': [df.J.sum()],
                   'P': [df.P.product()],
                   'Baryon': [df.Baryon.sum()],
                   'Lepton': [df.Lepton.sum()],
                   'T': [df['T'].sum()],
                   'T_3': [df.T_3.sum()],
                   'I': [df.I.sum()],
                   'I_3': [df.I_3.sum()],
                   'S': [df.S.sum()],
                   'C': [df.C.sum()],
                   'B': [df.B.sum()],
                   'T.1': [df['T.1'].sum()],
                   'L_e': [df.L_e.sum()],
                   'L_mu': [df.L_mu.sum()],
                   'L_tau': [df.L_tau.sum()]}
        
        dict_conservation = {}
        list_conservation = []
        for i, key in enumerate(dict_initial.keys()):
            if key == 'J':
                #special case J: must both be .0 or .5
                J_comp = (dict_initial['J'][0]%1.0 == 0.0) == (dict_final['J'][0]%1.0 == 0.0)
                dict_conservation['J'] = J_comp
                list_conservation.append(i)
            elif key == 'T':
                T_comp = (dict_initial['T'][0]%1.0 == 0.0) == (dict_final['T'][0]%1.0 == 0.0)
                dict_conservation['T'] = T_comp
                list_conservation.append(i)
            else:
                dict_conservation[key] = dict_initial[key] == dict_final[key]
                if dict_initial[key] == dict_final[key]:
                    list_conservation.append(i)

        return list_conservation, dict_conservation


    def checkForces(self):
        dict_conservation = self.getConservations()[1]

        em_conservation_list = ['Q', 'J', 'P', 'Baryon', 'Lepton', 'I_3', 'S', 'C', 'B', 'T.1', 'L_e', 'L_mu', 'L_tau']
        strong_conservation_list = ['Q', 'J', 'P', 'Baryon', 'Lepton', 'I', 'I_3', 'S', 'C', 'B', 'T.1', 'L_e', 'L_mu', 'L_tau']
        weak_conservation_list = ['Q', 'J', 'Baryon', 'Lepton', 'T_3', 'L_e', 'L_mu', 'L_tau']

        em_conservation, strong_conservation, weak_conservation = True, True, True

        for emc in em_conservation_list:
            if not dict_conservation[emc]:
                em_conservation = False
                break

        for sc in strong_conservation_list:
            if not dict_conservation[sc]:
                strong_conservation = False
                break

        for wc in weak_conservation_list:
            if not dict_conservation[wc]:
                weak_conservation = False
                break

        return em_conservation, strong_conservation, weak_conservation


    def addInitial(self, particle_type, index):
        row = self.type_dict[particle_type].query('index == @index')
        self.df_initial = pd.concat([self.df_initial, row]).reset_index(drop=True)

        
    def addFinal(self, particle_type, index):
        row = self.type_dict[particle_type].query('index == @index')
        self.df_final = pd.concat([self.df_final, row]).reset_index(drop=True)
        
    def removeInitial(self, index):
        self.df_initial = self.df_initial.drop(index, axis=0).reset_index(drop=True)
        
    def removeFinal(self, index):
        self.df_final = self.df_final.drop(index, axis=0).reset_index(drop=True)

    


#source: https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
            

###################################################
#based on https://stackoverflow.com/questions/70101883/coloring-row-in-qtableview-instead-of-cell
class PandasModelColorSelection(QtCore.QAbstractTableModel):
    def __init__(self, data, list_highlights, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.list_highlights = list_highlights
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
            if role == QtCore.Qt.ItemDataRole.BackgroundRole:
                col = index.column()
                if col in self.list_highlights:
                    return QtGui.QColor('green')

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]
        return None
                

    