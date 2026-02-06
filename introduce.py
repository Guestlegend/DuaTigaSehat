from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QRadioButton, QGroupBox,
    QMessageBox, QScrollArea
)

from instr import *
from bmi import *
from calorie import *

class IntroductionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_appear()
        self.show()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        scroll_layout = QVBoxLayout(content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Selamat Datang di DuaTigaSehat 💚")
        subtitle = QLabel("Mulai langkah sehatmu hari ini juga!")
        form_sub = QLabel("Harap mengisi data pengguna terlebih dahulu sebelum memilih program kesehatan.")
        title.setFont(QFont(font_family, font_title_size, QFont.Bold))
        subtitle.setFont(QFont(font_family, font_subtitle_size))
        scroll_layout.addWidget(title, alignment = Qt.AlignCenter) 
        scroll_layout.addWidget(subtitle, alignment = Qt.AlignCenter) 
        scroll_layout.addSpacing(30)
        scroll_layout.addWidget(form_sub, alignment = Qt.AlignCenter) 
        scroll_layout.addSpacing(15)

        #Form
        self.nama_label = QLabel("Isi nama kamu")
        self.umur_label = QLabel("Berapa umurmu?")
        self.gender_label = QLabel("Apa jenis kelamin Anda?")
        self.tinggidanberat_label = QLabel("Masukkan tinggi dan berat badan")

        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Nama")

        self.umur_input = QLineEdit()
        self.umur_input.setPlaceholderText("Umur")

        gender_layout = QHBoxLayout()
        self.radio_man = QRadioButton("Laki-Laki")
        self.radio_woman = QRadioButton("Perempuan")
        gender_layout.addWidget(self.radio_man)
        gender_layout.addWidget(self.radio_woman)

        self.tinggi_input = QLineEdit()
        self.tinggi_input.setPlaceholderText("Tinggi Badan (cm)")

        self.berat_input = QLineEdit()
        self.berat_input.setPlaceholderText("Berat Badan (kg)")

        form_group = QGroupBox("Data Pengguna")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)

        form_layout.addWidget(self.nama_label)
        form_layout.addWidget(self.nama_input)
        form_layout.addWidget(self.umur_label)
        form_layout.addWidget(self.umur_input)
        form_layout.addWidget(self.gender_label)
        form_layout.addLayout(gender_layout)
        form_layout.addWidget(self.tinggidanberat_label)
        form_layout.addWidget(self.tinggi_input)
        form_layout.addWidget(self.berat_input)

        form_group.setLayout(form_layout)
        scroll_layout.addWidget(form_group)

        #Pilihan program
        program_group = QGroupBox("Pilih program")
        program_layout = QHBoxLayout()

        self.radio_bmi = QRadioButton("BMI Calculator")
        self.radio_fitness = QRadioButton("Fitness Tracker")

        program_layout.addWidget(self.radio_bmi)
        program_layout.addWidget(self.radio_fitness)

        program_group.setLayout(program_layout)
        program_layout.setAlignment(Qt.AlignCenter)
        scroll_layout.addSpacing(10)
        scroll_layout.addWidget(program_group)

        #Submit
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_data)
        scroll_layout.addWidget(submit_btn)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def submit_data(self):
        if not all([self.nama_input.text(), self.umur_input.text(), self.tinggi_input.text(), self.berat_input.text()]):
            QMessageBox.warning(self, "Error", "Jangan dikosongkan ya..")
            return
        
        if not all([self.umur_input.text().isdigit(), self.tinggi_input.text().isdigit(), self.berat_input.text().isdigit()]):
            QMessageBox.warning(self, "Error", "Umur, tinggi, dan berat badan harus angka ya..")
            return
        
        if not (self.radio_man.isChecked() or self.radio_woman.isChecked()):
            QMessageBox.warning(self, "Error", "Gender Anda?")
            return
        
        if not (self.radio_bmi.isChecked() or self.radio_fitness.isChecked()):
            QMessageBox.warning(self, "Error", "Pilih salah satu program!")
            return
        
        user_data["nama"] = self.nama_input.text()
        user_data["umur"] = int(self.umur_input.text())
        user_data["tinggi"] = float(self.tinggi_input.text())
        user_data["berat"] = float(self.berat_input.text())

        if self.radio_man.isChecked():
            user_data["gender"] = "Laki-Laki"
        else:
            user_data["gender"] = "Perempuan"

        if self.radio_bmi.isChecked():
            user_data["program"] = "BMI Calculator"
        else:
            user_data["program"] = "Fitness Tracker"

        QMessageBox.information(
            self,
            "Data Tersimpan",
            f"Nama: {user_data['nama']}\n"
            f"Program dipilih: {user_data['program']}"
        )

        #Next window
        if user_data["program"] == "BMI Calculator":
            self.bmi_window = BMIResultWindow(parent=self)
            self.bmi_window.show()
            self.hide()
        else:
            self.macro_window = MacroCalculatorWindow(parent=self)
            self.macro_window.show()
            self.hide()
        
    def set_appear(self):
        self.setWindowTitle(app_name)
        self.resize(win_width, win_height)

app = QApplication([])
mw = IntroductionPage()
app.exec_()
