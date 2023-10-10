import pandas as pd
import numpy as np
import itertools
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
        self.df_all_particles = pd.concat((self.df_leptons, self.df_bosons, self.df_baryons, self.df_mesons)).reset_index().sort_values('idx')

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
     
    def getBothSums(self):
        df = self.df_initial.copy()[self.sum_cols]
        dict_initial = df.sum().to_dict()
        dict_initial['J'] = df.P.product()

        df = self.df_final.copy()[self.sum_cols]
        dict_final = df.sum().to_dict()
        dict_final['J'] = df.P.product()

        
        ret_df = pd.concat((pd.DataFrame(dict_initial, index=[0]), pd.DataFrame(dict_final, index=[0])))
        list_conservation = []
        for i, key in enumerate(dict_initial.keys()):
            if key == ' ':
                pass
            elif key == 'J':
                #special case J: must both be .0 or .5
                J_comp = (dict_initial['J']%1.0 == 0.0) == (dict_final['J']%1.0 == 0.0)
                list_conservation.append(i)
            elif key == 'T':
                T_comp = (dict_initial['T']%1.0 == 0.0) == (dict_final['T']%1.0 == 0.0)
                list_conservation.append(i)
            else:
                if dict_initial[key] == dict_final[key]:
                    list_conservation.append(i)

        return PandasModelColorSelection(ret_df, list_conservation)


    def getBothSumsDataFrame(self):
        df = self.df_initial.copy()[self.sum_cols]
        dict_initial = df.sum().to_dict()
        dict_initial['J'] = df.P.product()

        df = self.df_final.copy()[self.sum_cols]
        dict_final = df.sum().to_dict()
        dict_final['J'] = df.P.product()
        
        ret_df = pd.concat((pd.DataFrame(dict_initial, index=[0]), pd.DataFrame(dict_final, index=[0])))
        list_conservation = []
        for i, key in enumerate(dict_initial.keys()):
            if key == ' ':
                pass
            elif key == 'J':
                #special case J: must both be .0 or .5
                J_comp = (dict_initial['J']%1.0 == 0.0) == (dict_final['J']%1.0 == 0.0)
                list_conservation.append(i)
            elif key == 'T':
                T_comp = (dict_initial['T']%1.0 == 0.0) == (dict_final['T']%1.0 == 0.0)
                list_conservation.append(i)
            else:
                if dict_initial[key] == dict_final[key]:
                    list_conservation.append(i)

        return ret_df
        

    def getConservations(self):
        df = self.df_initial.copy()[self.sum_cols]
        dict_initial = df.sum().to_dict()
        dict_initial['J'] = df.P.product()

        df = self.df_final.copy()[self.sum_cols]
        dict_final = df.sum().to_dict()
        dict_final['J'] = df.P.product()
        
        dict_conservation = {}
        list_conservation = []
        for i, key in enumerate(dict_initial.keys()):
            if key == 'J':
                #special case J: must both be .0 or .5
                J_comp = (dict_initial['J']%1.0 == 0.0) == (dict_final['J']%1.0 == 0.0)
                dict_conservation['J'] = J_comp
                list_conservation.append(i)
            elif key == 'T':
                T_comp = (dict_initial['T']%1.0 == 0.0) == (dict_final['T']%1.0 == 0.0)
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

    

##################################################
class InteractionBuilder:
    def __init__(self, input_interaction, list_forces, n_particles):
        self.input_handler = input_interaction
        self.list_forces = list_forces
        self.n_particles = n_particles

        self.viable_interactions = []

    def buildInteraction(self):
        em_conservation_list = ['Q', 'J', 'P', 'Baryon', 'Lepton', 'I_3', 'S', 'C', 'B', 'T.1', 'L_e', 'L_mu', 'L_tau']
        strong_conservation_list = ['Q', 'J', 'P', 'Baryon', 'Lepton', 'I', 'I_3', 'S', 'C', 'B', 'T.1', 'L_e', 'L_mu', 'L_tau']
        weak_conservation_list = ['Q', 'J', 'Baryon', 'Lepton', 'T_3', 'L_e', 'L_mu', 'L_tau']

        conservation_lists = []
        if 'weak' in self.list_forces:
            conservation_lists.append(weak_conservation_list)
        if 'em' in self.list_forces:
            conservation_lists.append(em_conservation_list)
        if 'strong' in self.list_forces:
            conservation_lists.append(strong_conservation_list)


        viable_idx_sets = []
        
        for conservation in self.list_forces:
            df_particles = self.input_handler.df_all_particles
            
            conservation_list = []
            if 'weak' == conservation:
                conservation_list = weak_conservation_list

            elif 'em' == conservation:
                conservation_lists = em_conservation_list
                df_particles = df_particles.query('Q != 0')
            else: #strong
                conservation_lists = strong_conservation_list
                df_particles.query('baryonnumber != 0 or J == 0 or J == 1') # strong force does not interact with leptons

            list_particles_idx = df_particles.idx.to_list()
            list_combinations = itertools.product(list_particles_idx, repeat=self.n_particles) #list of sets of n particle_idx


            df_sums = self.input_handler.getBothSumsDataFrame()
            df_sums = df_sums[conservation_list]

            #calc: differences in quantum number initial-final (list/dict)
            dict_diff = (df_sums.iloc[0] - df_sums.iloc[1]).to_dict()
            if 'P' in conservation_list:
                dict_diff['P'] = df_sums.P.iloc[0] * df_sums.P.iloc[1] #special case parity    

            for set_idx in list_combinations:
                #temporary interaction
                df_temp = df_particles.query('idx in @set_idx')[conservation_list]
                dict_temp = df_temp.sum().to_dict()
                if 'P' in conservation_list:
                    dict_temp['P'] = df_temp['P'].product()
            
                satisifies_conservation = True

                arr_diff = np.array(list(dict_diff.values()))
                arr_temp = np.array(list(dict_temp.values()))
                satisifies_conservation = all((arr_diff - arr_temp) == 0)

                
                #for qn in conservation_list:
                #    if dict_temp[qn] - dict_diff[qn] != 0:
                #        if (set_idx == (0,7)):
                #            print(qn)
                #        satisifies_conservation = False
                #        break

                #build an interaction in this configuration and append to viable solutions if not already by another proccess
                if satisifies_conservation:
                    viable_idx_sets.append(set_idx)
        
        reduced_idx_tuples = {tuple([i for i in np.sort(j)]) for j in viable_idx_sets}
        for red_set in reduced_idx_tuples:                     
            list_idx_final = list(red_set) + self.input_handler.df_final.idx.to_list()
            temp_handler = Handler()
            temp_handler.df_initial = self.input_handler.df_initial
            temp_handler.df_final = df_particles.query('idx in @list_idx_final')
            print(temp_handler.df_final.name.tolist())
            self.viable_interactions.append(temp_handler)


        


###################################################

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
                

    