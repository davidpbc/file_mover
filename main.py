import os
import fnmatch
import random
import string
import magic
from mover_ui import QtWidgets, Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog


class FileMover:
    def __init__(self, types, origin, destination):
        self.types = types
        self.origin = origin
        self.destination = destination
        self.files = {}

    def find_files(self):
        result = {}
        if os.path.isdir(self.origin):
            for root, dirs, files in os.walk(self.origin):
                for name in files:
                    for tp in self.types:
                        if tp in magic.from_file(
                            os.path.join(root, name),
                            mime=True
                        ):
                            key = name
                            if result.get(name):
                                key = self.rename_file(name)
                            result[key] = os.path.join(
                                root,
                                name
                            )
        self.files.update(result)

    def check_file(self, name):
        if os.path.isfile(os.path.join(self.destination, name)):
            return True
        return False

    def rename_file(self, name):
        chars = string.ascii_uppercase + string.digits
        old_name = os.path.splitext(name)
        ext = old_name[-1]
        pref = old_name[0]
        suffix = []
        for x in range(4):
            suffix.append(random.choice(chars))
        suff = ''.join(suffix)
        return "{}_{}{}".format(pref, suff, ext)

    def move_files(self):
        total = 0
        for key, value in self.files.items():
            if value != os.path.join(self.destination, key):
                print('{}, {}'.format(value, os.path.join(
                    self.destination, key)))
                name = key
                while self.check_file(name):
                    name = self.rename_file(name)
                os.rename(value, os.path.join(
                    self.destination, name))
                total += 1
        print('{} Archivos Movidos.'.format(total))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.btn_orig_find.clicked.connect(self.get_origin_folder)
        self.btn_dest_find.clicked.connect(self.get_destination_folder)
        self.btn_process.clicked.connect(self.process_files)

    def get_origin_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            options=options
        )
        self.txt_origin.setText(dir_name)

    def get_destination_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            options=options
        )
        self.txt_destination.setText(dir_name)

    def process_files(self):
        types = []
        if self.chk_video.isChecked():
            types.append('video')
        if self.chk_audio.isChecked():
            types.append('audio')
        if self.chk_text.isChecked():
            types.append('text')
        if self.chk_image.isChecked():
            types.append('image')
        if self.chk_app.isChecked():
            types.append('application')

        origin = self.txt_origin.text()
        destination = self.txt_destination.text()

        if os.path.isdir(origin) and os.path.isdir(destination):
            fm = FileMover(types, origin, destination)
            fm.find_files()
            print(fm.files)
            print('Total: {} archivos encontrados'.format(len(fm.files)))
            fm.move_files()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
