import base45
import cbor2
import json
import os
import sys
import zlib
import win32com.client
import qdarkgraystyle
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QDialog, qApp
from cose.messages import CoseMessage
from dateutil.relativedelta import relativedelta

from try_1 import Ui_Main


# Checking for the presence of the Scantech device
def dev_check():
    present = 0
    wmi = win32com.client.GetObject("winmgmts:")
    for usb in wmi.InstancesOf("Win32_USBHub"):
        if r"USB\VID_040B&PID_6543" in usb.DeviceID:
            present = 1
    if present != 1:
        print("The Scantech device is not present! Please connect it and try again!")
        print("Scantech устройството не е открито! Моля свържете го и опитайте отново!")
        print("Exiting...")
        os.system("PING -n 7 127.0.0.1>nul")
        exit()


# Checking at the beginning
dev_check()

# Abbreviation : country
CO = {'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria',
      'CH': 'Switzerland', 'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia',
      'ES': 'Spain', 'FI': 'Finland', 'FR': 'France', 'GE': 'Georgia', 'GR': 'Greece', 'HR': 'Croatia', 'HU': 'Hungary',
      'IE': 'Ireland', 'IS': 'Iceland', 'IT': 'Italy', 'LI': 'Liechtenstein', 'LT': 'Lithuania', 'LU': 'Luxembourg',
      'LV': 'Latvia', 'MA': 'Morocco', 'MT': 'Malta', 'NL': 'Netherlands', 'NO': 'Norway', 'PL': 'Poland',
      'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden', 'SG': 'Singapore', 'SI': 'Slovenia', 'SK': 'Slovakia',
      'SM': 'San Marino', 'UA': 'Ukraine', 'VA': 'Vatican', 'GB': 'Great Britain'}

# dick, date_from, j_whole = 1, 2, 3


def reset():  # restarts the whole program
    os.execl(sys.executable, "kurec.py", *sys.argv)


def exception():
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.")  # prompt
    print("Check the input language and the keyboard for blocked keys.")     # prompt
    print("Try again or with different certificate.")                        # prompt
    print("Restarting...")                                                   # prompt
    os.system("PING -n 5 127.0.0.1>nul")                                     # wait time before restarting

""""
# Checking validity
def validity(j_whole, var, date_from, vall):
    today = datetime.today().date()  # getting today's date
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    if var == 1:
        Date = datetime.fromtimestamp(j_whole['4']).date()
    elif var != 1:
        Date = date_from + relativedelta(months=vall)
    # Comparing the date of expire against today
    if today < Date:  # Valid cert
        # Doing it like that so no additional .bat files are needed
        os.system("color 20")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is valid!" '
                  '"Information">nul')
        reset()
    else:  # Invalid cert
        # Doing it like that so no additional .bat files are needed
        os.system("color c0")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is invalid!" '
                  '"Attention!" /i:E>nul')
        reset()
"""


class MyMainWindow(QtWidgets.QMainWindow, Ui_Main):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        # super(MyMainWindow, self).__init__(parent=parent)
        qApp.installEventFilter(self)
        self.setupUi(self)

    def eventFilter(self, obj, event):
        var = 2
        today = datetime.today().date()  # getting today's date

        def validity(j_whole, var, date_from, vall):
            # Forming the date to check by adding the days from the .ini file to the date from the cert
            if var == 1:
                Date = datetime.fromtimestamp(j_whole['4']).date()
            elif var != 1:
                Date = date_from + relativedelta(months=vall)
            # Comparing the date of expire against today
            if today < Date:  # Valid cert
                os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is valid!" ''"Information">nul')
            else:  # Invalid cert
                os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is invalid!" ''"Attention!" /i:E>nul')

        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
            """
            if event.key() == Qt.Key_Enter:
                # print("Enter is pressed!")
                payload = self.lineEdit.text()
                payload = payload[4:]
                try:
                    decoded = base45.b45decode(payload)
                except:
                    exception()
                    reset() and sys.exit()
                # decompress using zlib
                decompressed = zlib.decompress(decoded)
                # decode COSE message (no signature verification done)
                cose = CoseMessage.decode(decompressed)
                # decode the CBOR encoded payload converting the information to readable json struct
                whole = (
                    json.dumps(cbor2.loads(cose.payload), ensure_ascii=False, indent=2, sort_keys=True, default=str))
                j_whole = json.loads(whole)
                dick = j_whole['-260']['1']  # the dic with the needed information for the funcs
                date_from = datetime.fromtimestamp(j_whole['6']).date()  # date issued/valid from
                self.placeholder_native_name.setText()
            """
            if event.key() == Qt.Key_Return:
                print("Return is pressed!")
                payload = self.lineEdit.text()
                payload = payload[4:]
                try:
                    decoded = base45.b45decode(payload)
                except:
                    exception()
                    reset() and sys.exit()
                # decompress using zlib
                decompressed = zlib.decompress(decoded)
                # decode COSE message (no signature verification done)
                cose = CoseMessage.decode(decompressed)
                # decode the CBOR encoded payload converting the information to readable json struct
                whole = (json.dumps(cbor2.loads(cose.payload), ensure_ascii=False, indent=2, sort_keys=True, default=str))
                j_whole = json.loads(whole)
                dick = j_whole['-260']['1']  # the dic with the needed information for the funcs
                date_from = datetime.fromtimestamp(j_whole['6']).date()  # date issued/valid from
                for k, v in dick.items():
                    if k == "r":  # recovery
                        if v is None:  # if empty will continue to the next sub-dic
                            continue
                        if j_whole['1'] == "BG":  # In BG this cert is 365 days, not 180. For now...
                            val = open("val_rec_bg.ini", "r")  # Opens it in read mode
                            vall = list(val)                   # Converting data to list
                            vall = int(vall[0])                # Taking the first (and only) item and convert it to int
                            val.close()                        # Closes the file
                        elif j_whole['1'] != "BG":
                            val = open("val_rec.ini", "r")     # Opens it in read mode
                            vall = list(val)                   # Converting data to list
                            vall = int(vall[0])                # Taking the first (and only) item and convert it to int
                            val.close()                        # Closes the file
                        self.placeholder_native_name.setText(str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
                        self.placeholder_en_name.setText(str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
                        self.placeholder_date_issued.setText(str(datetime.fromtimestamp(j_whole['6']).date()))
                        self.placeholder_valid_until.setText(str(datetime.fromtimestamp(j_whole['4']).date()))
                        self.placeholder_cert_id.setText(str(j_whole['-260']['1']['r'][0]['ci']))
                        for K, V in CO.items():
                            if j_whole['1'] == K:
                                c = V
                            elif len(j_whole['1']) > 2:
                                c = j_whole['1']
                        self.placeholder_CO.setText(str(c))
                        self.cert_type.setText("Recovery certificate")
                        break
                    elif k == "v":  # vaccine
                        if v is None:
                            continue
                        val = open("val_vac.ini", "r")
                        vall = list(val)
                        vall = int(vall[0])
                        val.close()
                        self.placeholder_native_name.setText(str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
                        self.placeholder_en_name.setText(str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
                        self.placeholder_date_issued.setText(str(datetime.fromtimestamp(j_whole['6']).date()))
                        self.placeholder_valid_until.setText(str(datetime.fromtimestamp(j_whole['4']).date()))
                        self.placeholder_cert_id.setText(str(j_whole['-260']['1']['v'][0]['ci']))
                        for K, V in CO.items():
                            if j_whole['1'] == K:
                                c = V
                            elif len(j_whole['1']) > 2:
                                c = j_whole['1']
                        self.placeholder_CO.setText(str(c))
                        self.cert_type.setText("Vaccination certificate")
                        break
                    elif k == "t":  # test cert
                        if v is None:
                            continue
                        var = 1
                        vall = "pft"
                        self.placeholder_native_name.setText(str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
                        self.placeholder_en_name.setText(str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
                        self.placeholder_date_issued.setText(str(datetime.fromtimestamp(j_whole['6']).date()))
                        self.placeholder_valid_until.setText(str(datetime.fromtimestamp(j_whole['4']).date()))
                        self.placeholder_cert_id.setText(str(j_whole['-260']['1']['t'][0]['ci']))
                        for K, V in CO.items():
                            if j_whole['1'] == K:
                                c = V
                            elif len(j_whole['1']) > 2:
                                c = j_whole['1']
                        self.placeholder_CO.setText(str(c))
                        self.cert_type.setText("Test certificate")
                validity(j_whole, var, date_from, vall)
                return 1
                #reset()
        return super(MyMainWindow, self).eventFilter(obj, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    # Available build in styles
    # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    # app.setStyle('Windows')
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())  # this one is form the internet
    sys.exit(app.exec_())

