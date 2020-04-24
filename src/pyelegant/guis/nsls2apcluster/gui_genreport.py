import sys
from qtpy import QtCore, QtGui, QtWidgets
from qtpy import uic
from qtpy.QtWidgets import QFileDialog

#from window_genreport_main import Ui_MainWindow

from copy import deepcopy
from functools import partial

#class SlurmPartitionModel(QtCore.QAbstractListModel):
    #""""""

    #def __init__(self, *args, **kwargs):
        #"""Constructor"""

        #super(SlurmPartitionModel, self).__init__(*args, **kwargs)
        #self.partition_list = [
            #'normal', 'short', 'debug', 'long', 'longlong', 'low', 'high']

    #def data(self, index, role):
        #""""""

        #if role == QtCore.Qt.DisplayRole:
            #text = self.partition_list[index.row()]
            #return text

    #def rowCount(self, index):
        #""""""
        #return len(self.partition_list)

class DialogCalcOptMap(QtWidgets.QDialog):
    """"""

    def __init__(self, xy_or_px, old_new_opt_set_names, opt_dict,
                 *args, **kwargs):
        """Constructor"""

        if xy_or_px == 'xy':
            self.is_xy = True
        elif xy_or_px == 'px':
            self.is_xy = False
        else:
            raise ValueError('"xy_or_px" must be either "xy" or "px"')

        super().__init__(*args, **kwargs)
        uic.loadUi(f'window_genreport_calc_opt_map_{xy_or_px}.ui', self)

        self.lineEdit_opt_set_name.setText(old_new_opt_set_names['old'])

        self.change_optional_settings_visibility(False)
        self.checkBox_show_optional.clicked.connect(
            self.change_optional_settings_visibility)

        self.spinBox_n_turns.setValue(opt_dict['n_turns'])
        self.lineEdit_xmin.setText(f'{opt_dict["xmin"]:.6g}')
        self.lineEdit_xmax.setText(f'{opt_dict["xmax"]:.6g}')
        self.spinBox_nx.setValue(opt_dict['nx'])
        if self.is_xy:
            self.lineEdit_ymin.setText(f'{opt_dict["ymin"]:.6g}')
            self.lineEdit_ymax.setText(f'{opt_dict["ymax"]:.6g}')
            self.spinBox_ny.setValue(opt_dict['ny'])
        else:
            self.lineEdit_delta_min.setText(f'{opt_dict["delta_min"] * 1e2:.6g}')
            self.lineEdit_delta_max.setText(f'{opt_dict["delta_max"] * 1e2:.6g}')
            self.spinBox_ndelta.setValue(opt_dict['ndelta'])

        self.lineEdit_x_offset.setText(f'{opt_dict["x_offset"]:.6g}')
        self.lineEdit_y_offset.setText(f'{opt_dict["y_offset"]:.6g}')
        self.lineEdit_delta_offset.setText(f'{opt_dict["delta_offset"]:.6g}')

        if 'remote_opts' in opt_dict:
            self.groupBox_remote_opts.setChecked(True)
            self.change_remote_opts_visibility(True)

            remote_opts = opt_dict['remote_opts']
            if 'partition' in remote_opts:
                self.checkBox_partition.setChecked(True)
                i = self.comboBox_partition.findText(remote_opts['partition'])
                self.comboBox_partition.setCurrentIndex(i)
            else:
                self.checkBox_partition.setChecked(False)
            if 'ntasks' in remote_opts:
                self.checkBox_ntasks.setChecked(True)
                self.spinBox_ntasks.setValue(remote_opts['ntasks'])
            else:
                self.checkBox_ntasks.setChecked(False)
            if 'time' in remote_opts:
                self.checkBox_time.setChecked(True)
                self.lineEdit_time.setText(remote_opts['time'])
            else:
                self.checkBox_time.setChecked(False)
            if 'diag_mode' in remote_opts:
                self.checkBox_diag_mode.setChecked(True)
                i = self.comboBox_diag_mode.findText(str(remote_opts['diag_mode']))
                self.comboBox_diag_mode.setCurrentIndex(i)
            else:
                self.checkBox_diag_mode.setChecked(False)
        else:
            self.groupBox_remote_opts.setChecked(False)
            self.change_remote_opts_visibility(False)

        self.old_new_opt_set_names = old_new_opt_set_names
        self.opt_dict = opt_dict

        self.accepted.connect(self.update_opt_dict)

        self.groupBox_remote_opts.clicked.connect(
            self.change_remote_opts_visibility)

    def change_remote_opts_visibility(self, visible):
        """"""

        obj_list_in_remote_opts = [
            self.checkBox_partition, self.comboBox_partition,
            self.checkBox_ntasks, self.spinBox_ntasks,
            self.checkBox_time, self.lineEdit_time,
            self.checkBox_diag_mode, self.comboBox_diag_mode,
        ]

        for obj in obj_list_in_remote_opts:
            obj.setEnabled(visible)

    def update_opt_dict(self):
        """"""

        self.old_new_opt_set_names['new'] = self.lineEdit_opt_set_name.text()

        self.opt_dict['n_turns'] = self.spinBox_n_turns.value()
        self.opt_dict['xmin'] = float(self.lineEdit_xmin.text())
        self.opt_dict['xmax'] = float(self.lineEdit_xmax.text())
        self.opt_dict['nx'] = self.spinBox_nx.value()
        if self.is_xy:
            self.opt_dict['ymin'] = float(self.lineEdit_ymin.text())
            self.opt_dict['ymax'] = float(self.lineEdit_ymax.text())
            self.opt_dict['ny'] = self.spinBox_ny.value()
        else:
            self.opt_dict['delta_min'] = float(
                self.lineEdit_delta_min.text()) * 1e-2
            self.opt_dict['delta_max'] = float(
                self.lineEdit_delta_max.text()) * 1e-2
            self.opt_dict['ndelta'] = self.spinBox_ndelta.value()

        self.opt_dict['x_offset'] = float(self.lineEdit_x_offset.text())
        self.opt_dict['y_offset'] = float(self.lineEdit_y_offset.text())
        self.opt_dict['delta_offset'] = float(self.lineEdit_delta_offset.text())
        if self.groupBox_remote_opts.isChecked():
            remote_opts = {}
            if self.checkBox_partition.isChecked():
                remote_opts['partition'] = self.comboBox_partition.currentText()
            if self.checkBox_ntasks.isChecked():
                remote_opts['ntasks'] = self.spinBox_ntasks.value()
            if self.checkBox_time.isChecked():
                time_str = self.lineEdit_time.text().strip()
                if time_str:
                    remote_opts['time'] = time_str
            if self.checkBox_diag_mode.isChecked():
                remote_opts['diag_mode'] = bool(
                    self.comboBox_diag_mode.currentText())
            self.opt_dict['remote_opts'] = remote_opts
        else:
            if 'remote_opts' in self.opt_dict:
                del self.opt_dict['remote_opts']

    def change_optional_settings_visibility(self, visible):
        """"""

        obj_list = [
            self.label_9, self.lineEdit_x_offset,
            self.label_10, self.lineEdit_y_offset,
            self.label_11, self.lineEdit_delta_offset,
            self.groupBox_remote_opts,
        ]

        if visible:
            for obj in obj_list:
                obj.show()
        else:
            for obj in obj_list:
                obj.hide()

class DialogCalcOptXYAper(QtWidgets.QDialog):
    """"""

    def __init__(self, old_new_opt_set_names, opt_dict, *args, **kwargs):
        """Constructor"""

        super().__init__(*args, **kwargs)
        uic.loadUi('window_genreport_calc_opt_xy_aper.ui', self)

        self.lineEdit_opt_set_name.setText(old_new_opt_set_names['old'])

        self.change_optional_settings_visibility(False)
        self.checkBox_show_optional.clicked.connect(
            self.change_optional_settings_visibility)

        self.spinBox_n_turns.setValue(opt_dict['n_turns'])
        self.lineEdit_abs_xmax.setText(f'{opt_dict["abs_xmax"]:.6g}')
        self.lineEdit_abs_ymax.setText(f'{opt_dict["abs_ymax"]:.6g}')
        self.spinBox_ini_ndiv.setValue(opt_dict['ini_ndiv'])
        self.spinBox_n_lines.setValue(opt_dict['n_lines'])

        self.checkBox_neg_y_search.setChecked(opt_dict['neg_y_search'])

        self.old_new_opt_set_names = old_new_opt_set_names
        self.opt_dict = opt_dict

        self.accepted.connect(self.update_opt_dict)

    def update_opt_dict(self):
        """"""

        self.old_new_opt_set_names['new'] = self.lineEdit_opt_set_name.text()

        self.opt_dict['n_turns'] = self.spinBox_n_turns.value()
        self.opt_dict['abs_xmax'] = float(self.lineEdit_abs_xmax.text())
        self.opt_dict['abs_ymax'] = float(self.lineEdit_abs_ymax.text())
        self.opt_dict['ini_ndiv'] = self.spinBox_ini_ndiv.value()
        self.opt_dict['n_lines'] = self.spinBox_n_lines.value()

        self.opt_dict['neg_y_search'] = self.checkBox_neg_y_search.isChecked()

    def change_optional_settings_visibility(self, visible):
        """"""

        obj_list = [self.checkBox_neg_y_search]

        if visible:
            for obj in obj_list:
                obj.show()
        else:
            for obj in obj_list:
                obj.hide()


class MainWindow(QtWidgets.QMainWindow):
    """"""

    def __init__(self, *args, **kwargs):
        """Constructor"""

        super().__init__(*args, **kwargs)
        uic.loadUi('window_genreport_main.ui', self)

#class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    #""""""

    #def __init__(self, *args, obj=None, **kwargs):
        #"""Constructor"""

        #super(MainWindow, self).__init__(*args, **kwargs)
        #self.setupUi(self)

        self.all_nonlin_calc_types = [
            'xy_aper', 'fmap_xy', 'fmap_px', 'cmap_xy', 'cmap_px', 'tswa',
            'nonlin_chrom', 'mom_aper']

        self._set_default_calc_opt_sets()

        self.change_advanced_options_visibility(
            self.checkBox_show_advanced.checkState())
        self.checkBox_show_advanced.clicked.connect(
            self.change_advanced_options_visibility)

        self.checkBox_nonlin_include_all.clicked.connect(
            self.change_all_nonlin_calc_type_checkbox_states_include)
        self.checkBox_nonlin_recalc_all.clicked.connect(
            self.change_all_nonlin_calc_type_checkbox_states_recalc)
        self.checkBox_nonlin_replot_all.clicked.connect(
            self.change_all_nonlin_calc_type_checkbox_states_replot)

        for calc_type in self.all_nonlin_calc_types:
            obj = getattr(self, f'checkBox_nonlin_include_{calc_type}')
            obj.clicked.connect(self.uncheck_all_include)
            obj.clicked.connect(partial(
                getattr(self, 'change_state_recalc_replot_checkboxes'),
                calc_type))

            obj = getattr(self, f'checkBox_nonlin_recalc_{calc_type}')
            obj.clicked.connect(self.uncheck_all_recalc)

            obj = getattr(self, f'checkBox_nonlin_replot_{calc_type}')
            obj.clicked.connect(self.uncheck_all_replot)

        self.comboBox_nonlin_calc_opts_calc_type.currentIndexChanged.connect(
            self.update_nonlin_calc_opts_set_name_editor_combobox)
        self.update_nonlin_calc_opts_set_name_editor_combobox(0)

        self.update_nonlin_calc_opts_set_name_selector_comboboxes()

        self.pushButton_nonlin_calc_opts_set_edit.clicked.connect(
            self.open_calc_opt_edit_dialog)

        #self.slurm_partition_model = SlurmPartitionModel()
        #self.listView_partition_common.setModel(self.slurm_partition_model)

        #self.pushButton.clicked.connect(self.openFileNameDialog)
        #self.pushButton.clicked.connect(self.openFileNamesDialog)

    def open_calc_opt_edit_dialog(self):
        """"""

        calc_type = self.comboBox_nonlin_calc_opts_calc_type.currentText()
        opt_set_name = self.comboBox_nonlin_calc_opts_set_name.currentText()
        opts = self._calc_opts[calc_type][opt_set_name]

        old_new_opt_set_names = dict(old=opt_set_name, new=None)

        if calc_type == 'xy_aper':
            dialog = DialogCalcOptXYAper(old_new_opt_set_names, opts)
        elif calc_type in ('fmap_xy', 'cmap_xy'):
            dialog = DialogCalcOptMap('xy', old_new_opt_set_names, opts)
        elif calc_type in ('fmap_px', 'cmap_px'):
            dialog = DialogCalcOptMap('px', old_new_opt_set_names, opts)
        elif calc_type == 'tswa':
            raise NotImplementedError()
        elif calc_type == 'nonlin_chrom':
            raise NotImplementedError()
        elif calc_type == 'mom_aper':
            raise NotImplementedError()
        else:
            raise ValueError('Invalid "calc_type"')
        dialog.exec_()

        if old_new_opt_set_names['new'] is None:
            accepted = False
        else:
            accepted = True

        if accepted and (
            old_new_opt_set_names['old'] != old_new_opt_set_names['new']):

            self._calc_opts[calc_type][old_new_opt_set_names['new']] = \
                self._calc_opts[calc_type][old_new_opt_set_names['old']]
            del self._calc_opts[calc_type][old_new_opt_set_names['old']]

            i = self.comboBox_nonlin_calc_opts_set_name.currentIndex()
            self.comboBox_nonlin_calc_opts_set_name.removeItem(i)
            self.comboBox_nonlin_calc_opts_set_name.insertItem(
                i, old_new_opt_set_names['new'])
            self.comboBox_nonlin_calc_opts_set_name.setCurrentIndex(i)

            obj = getattr(self, f'comboBox_nonlin_{calc_type}_calc_opt_name')
            cur_text = obj.currentText()
            if cur_text == old_new_opt_set_names['old']:
                cur_text = old_new_opt_set_names['new']
            avail_set_names = list(self._calc_opts[calc_type])
            obj.clear()
            obj.addItems(avail_set_names)
            new_i = obj.findText(cur_text)
            obj.setCurrentIndex(new_i)

    def update_nonlin_calc_opts_set_name_selector_comboboxes(self):
        """"""

        for calc_type in self.all_nonlin_calc_types:
            obj = getattr(self, f'comboBox_nonlin_{calc_type}_calc_opt_name')
            current_text = obj.currentText()
            obj.clear()
            avail_set_names = list(self._calc_opts[calc_type])
            obj.addItems(avail_set_names)

            new_index = obj.findText(current_text)
            obj.setCurrentIndex(new_index)

    def update_nonlin_calc_opts_set_name_editor_combobox(self, index):
        """"""

        calc_type = self.comboBox_nonlin_calc_opts_calc_type.itemText(index)
        avail_set_names = list(self._calc_opts[calc_type])

        self.comboBox_nonlin_calc_opts_set_name.clear()
        self.comboBox_nonlin_calc_opts_set_name.addItems(avail_set_names)

    def _set_default_calc_opt_sets(self):
        """"""

        self._calc_opts = {k: {} for k in self.all_nonlin_calc_types}

        d = self._calc_opts['xy_aper'] = dict(production={
            'n_turns': 1024,
            'abs_xmax': 10e-3,
            'abs_ymax': 10e-3,
            'ini_ndiv': 51,
            'n_lines': 21,
            # Optional (below)
            'neg_y_search': False,
        })
        d['test'] = deepcopy(d['production'])
        d['test'].update({'n_turns': 128})

        d = self._calc_opts['fmap_xy'] = dict(production={
            'n_turns': 1024,
            'xmin': -10e-3,
            'xmax': +10e-3,
            'ymin': 0.0,
            'ymax': +5e-3,
            'nx': 201,
            'ny': 201,
            # Optional (below)
            'x_offset': 1e-6,
            'y_offset': 1e-6,
            'delta_offset': 0.0,
            # remote_opts:
            #     ntasks: 200
        })
        d['test'] = deepcopy(d['production'])
        d['test'].update({'nx': 21, 'ny': 21})

        d = self._calc_opts['fmap_px'] = dict(production={
            'n_turns': 1024,
            'delta_min': -0.05,
            'delta_max': +0.05,
            'xmin': -10e-3,
            'xmax': +10e-3,
            'ndelta': 201,
            'nx': 201,
            # Optional (below)
            'x_offset': 1e-6,
            'y_offset': 1e-6,
            'delta_offset': 0.0,
        })
        d['test'] = deepcopy(d['production'])
        d['test'].update({'nx': 21, 'ny': 21})

        d = self._calc_opts['cmap_xy'] = dict(
            production=deepcopy(self._calc_opts['fmap_xy']['production']))
        d['test'] = deepcopy(self._calc_opts['fmap_xy']['test'])
        d['test'].update({'n_turns': 128})

        d = self._calc_opts['cmap_px'] = dict(
            production=deepcopy(self._calc_opts['fmap_px']['production']))
        d['test'] = deepcopy(self._calc_opts['fmap_px']['test'])
        d['test'].update({'n_turns': 128})

        self._calc_opts['tswa'] = dict(production={
            'n_turns': 1024,
            'abs_xmax': 5e-3,
            'nx': 50,
            'abs_ymax': 3e-3,
            'ny': 50,
            # Optional (below)
            'x_offset': 1e-6,
            'y_offset': 1e-6,
            'remote_opts': {
                'partition': 'short',
                'time': '30:00',
            }
        })

        self._calc_opts['nonlin_chrom'] = dict(production={
            'n_turns': 1024,
            'delta_min': -3e-2,
            'delta_max': +3e-2,
            'ndelta': 100,
            # Optional (below)
            'x_offset': 1e-6,
            'y_offset': 1e-6,
            'delta_offset': 0.0,
            'remote_opts': {
                'partition': 'short',
                'time': '30:00',
            },
            'save_fft': False,
        })

        d = self._calc_opts['mom_aper'] = dict(production={
            'n_turns': 1024,
            'x_initial': 10e-6,
            'y_initial': 10e-6,
            'delta_negative_start': -0.1e-2,
            'delta_negative_limit': -5e-2,
            'delta_positive_start': 0.1e-2,
            'delta_positive_limit': 5e-2,
            'init_delta_step_size': 5e-3,
            'include_name_pattern': '[QSO]*',
        })
        d['test'] = deepcopy(d['production'])
        d['test'].update({'n_turns': 16, 'include_name_pattern': 'O*'})

    def change_state_recalc_replot_checkboxes(self, calc_type, include_checked):
        """"""

        obj = getattr(self, f'checkBox_nonlin_recalc_{calc_type}')
        obj.setEnabled(include_checked)
        obj = getattr(self, f'checkBox_nonlin_replot_{calc_type}')
        obj.setEnabled(include_checked)

    def uncheck_all_include(self, checked):
        """"""
        if not checked:
            self.checkBox_nonlin_include_all.setChecked(False)
    def uncheck_all_recalc(self, checked):
        """"""
        if not checked:
            self.checkBox_nonlin_recalc_all.setChecked(False)
    def uncheck_all_replot(self, checked):
        """"""
        if not checked:
            self.checkBox_nonlin_replot_all.setChecked(False)

    def change_all_nonlin_calc_type_checkbox_states_include(self, checked):
        """"""

        for calc_type in self.all_nonlin_calc_types:
            obj = getattr(self, f'checkBox_nonlin_include_{calc_type}')
            obj.setChecked(checked)

    def change_all_nonlin_calc_type_checkbox_states_recalc(self, checked):
        """"""

        for calc_type in self.all_nonlin_calc_types:
            obj = getattr(self, f'checkBox_nonlin_recalc_{calc_type}')
            obj.setChecked(checked)

    def change_all_nonlin_calc_type_checkbox_states_replot(self, checked):
        """"""

        for calc_type in self.all_nonlin_calc_types:
            obj = getattr(self, f'checkBox_nonlin_replot_{calc_type}')
            obj.setChecked(checked)


    def change_advanced_options_visibility(self, visible):
        """"""

        obj_list = [self.label_time_common, self.lineEdit_time_common]

        if visible:
            for obj in obj_list:
                obj.show()
        else:
            for obj in obj_list:
                obj.hide()



    def openFileNameDialog(self):
        """"""

        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self, "QFileDialog.getOpenFileNames()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

