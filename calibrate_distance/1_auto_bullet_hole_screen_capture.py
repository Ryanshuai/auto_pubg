from PyQt5 import QtCore, QtGui, QtWidgets
from press_gun.generate_distance.auto_screen_capture import Key_Listener

from all_states import All_States


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        rect = 1520, 250, 1920, 1150
        rect = 1520, 250, 1920, 1000
        rect = 1520, 250, 1920, 900

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 50)
        Dialog.move(2120, 1000)
        Dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        Dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        Dialog.setFont(font)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 400, 50))
        self.label.setObjectName("label")

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.key_listener = Key_Listener(All_States(), rect=rect)
        self.key_listener.temp_qobject.state_str_signal[str].connect(self.retranslateUi)
        self.key_listener.start()

    def retranslateUi(self, text):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", text))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
