import sys

def main_gui(args):
    from qtpy import QtWidgets
    from launcher_dialog import LauncherDialog

    app = QtWidgets.QApplication(args)
    launcher = LauncherDialog()
    launcher.show()

    app.exec_()


if __name__ == '__main__':
    main_gui(sys.argv)
