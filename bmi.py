from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from instr import *

class BMIResultWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initUI()
        self.calculate_bmi()
        self.parent = parent

    def initUI(self):
        self.setWindowTitle("BMI Result")
        self.resize(500, 500)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("BMI RESULT")
        title.setFont(QFont(font_family, font_title_size, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont(font_family, font_normal_size))
        layout.addWidget(self.result_label)

        # Buttons
        btn_layout = QHBoxLayout()

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.prevwindow)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)

        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(exit_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def prevwindow(self):
        self.parent.show()
        self.close()

    def calculate_bmi(self):
        weight = user_data["berat"]
        height_m = user_data["tinggi"] / 100

        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)

        # Classification
        if bmi < 18.5:
            classification = "Underweight"
        elif bmi < 25:
            classification = "Normal"
        elif bmi < 30:
            classification = "Overweight"
        else:
            classification = "Obese"

        # Healthy range
        healthy_min = round(18.5 * height_m ** 2, 1)
        healthy_max = round(24.9 * height_m ** 2, 1)

        # Target BMI 22
        target_weight = round(22 * height_m ** 2, 1)
        diff = round(target_weight - weight, 1)

        # Ponderal Index
        ponderal_index = round(weight / (height_m ** 3), 2)

        result_text = f"""
{int(bmi)} kg/m²   ({classification})

Healthy BMI range:
18.5 - 24.9 kg/m²

Healthy weight for the height:
{healthy_min} kg - {healthy_max} kg

Gain/Loss:
{"Gain" if diff > 0 else "Lose"} {abs(diff)} kg to reach a BMI of 22 kg/m²

Ponderal Index:
{int(ponderal_index)} kg/m³
"""

        self.result_label.setText(result_text)
