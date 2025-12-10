import os
import ayon_api
import subprocess
import qdarkstyle
from dotenv import load_dotenv
from qtpy import QtWidgets


class LauncherDialog(QtWidgets.QMainWindow):

    def __init__(self):
        super(LauncherDialog, self).__init__()

        self.setStyleSheet(qdarkstyle.load_stylesheet())

        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Ayon SMKS Launcher")
        
        bundle_selection_widget = QtWidgets.QWidget()
        bundle_selection_layout = QtWidgets.QHBoxLayout()
        bundle_selection_widget.setLayout(bundle_selection_layout)

        self.bundle_label = QtWidgets.QLabel("Select a bundle:")
        self.bundle_selection = QtWidgets.QComboBox()
        self.bundles_to_launcher_version = {}

        bundle_selection_layout.addWidget(self.bundle_label)
        bundle_selection_layout.addWidget(self.bundle_selection)

        self.launch_button = QtWidgets.QPushButton("Launch!")
        self.launch_button.clicked.connect(self.launch_ayon_bundle)
        
        self.main_layout.addWidget(bundle_selection_widget, 0, 0)
        self.main_layout.addWidget(self.launch_button, 1, 0)

        self.get_bundle_data_from_ayon()


    def get_bundle_data_from_ayon(self):
        # Load service user credentials and use to connect to ayon
        load_dotenv()
        ayon_api.init_service()

        bundles = sorted(ayon_api.get_bundles().get("bundles") or [], key=lambda bundle: bundle.get("name"))
        for bundle in bundles:
            self.bundles_to_launcher_version[bundle.get("name")] = bundle.get("installerVersion")
            self.bundle_selection.addItem(bundle.get("name"))

    def launch_ayon_bundle(self):
        # Launch ayon against selected bundle
        curr_bundle = self.bundle_selection.currentText()
        curr_bundle_launcher_version = self.bundles_to_launcher_version.get(curr_bundle)
        
        ayon_launcher_path = "C:/Program Files/Ynput/AYON {}/ayon_console.exe".format(curr_bundle_launcher_version or "")
        cmd = [f"{ayon_launcher_path}", "--bundle", f"{curr_bundle}"]

        # Remove ayon keys to have a new clean env for connection
        sanitized_env = {}
        for key,value in os.environ.items():
            if "AYON" in key:
                continue
            else:
                sanitized_env[key] = value

        try:
            subprocess.Popen(cmd, env=sanitized_env)
        except Exception as e:
            print("Failed to launch AYON bundle {} in subprocess: {}".format(curr_bundle, e))
