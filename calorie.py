from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QRadioButton, QGroupBox,
    QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from instr import *

class MacroCalculatorWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()
        self.calculate_macro()

    def initUI(self):
        self.setWindowTitle("Macro Calculator")
        self.resize(520, 650)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        # ===== TITLE =====
        title = QLabel("MACRO CALCULATOR")
        title.setFont(QFont(font_family, font_title_size, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Tentukan kebutuhan makronutrien harianmu")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # ===== ACTIVITY LEVEL =====
        act_group = QGroupBox("Activity Level")
        act_layout = QVBoxLayout()

        self.act_sedentary = QRadioButton("Sedentary (0–1x exercise / week)")
        self.act_light = QRadioButton("Lightly Active (2–3x exercise / week)")
        self.act_moderate = QRadioButton("Moderately Active (4–5x exercise / week)")
        self.act_active = QRadioButton("Very Active (6–7x exercise / week)")

        act_layout.addWidget(self.act_sedentary)
        act_layout.addWidget(self.act_light)
        act_layout.addWidget(self.act_moderate)
        act_layout.addWidget(self.act_active)

        act_group.setLayout(act_layout)
        layout.addWidget(act_group)

        # ===== GOAL =====
        goal_group = QGroupBox("Goal")
        goal_layout = QVBoxLayout()

        self.goal_loss = QRadioButton("Weight Loss (−0.5 kg / week)")
        self.goal_maintain = QRadioButton("Maintain Weight")
        self.goal_gain = QRadioButton("Weight Gain (+0.5 kg / week)")

        goal_layout.addWidget(self.goal_loss)
        goal_layout.addWidget(self.goal_maintain)
        goal_layout.addWidget(self.goal_gain)

        goal_group.setLayout(goal_layout)
        layout.addWidget(goal_group)

        # ===== CALCULATE BUTTON =====
        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.calculate_macro)
        layout.addWidget(calc_btn)

        # ===== RESULT =====
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont(font_family, font_normal_size))
        layout.addWidget(self.result_label)

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.prevwindow)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)

        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(exit_btn)
        layout.addLayout(btn_layout)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def prevwindow(self):
        self.parent.show()
        self.close()

    def calculate_macro(self):
        weight = user_data["berat"]
        height = user_data["tinggi"]
        age = user_data["umur"]
        gender = user_data["gender"]

        # ===== BMR =====
        if gender == "Laki-Laki":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

        # ===== ACTIVITY FACTOR =====
        if self.act_sedentary.isChecked():
            tdee = bmr * 1.2
        elif self.act_light.isChecked():
            tdee = bmr * 1.375
        elif self.act_moderate.isChecked():
            tdee = bmr * 1.55
        else:
            tdee = bmr * 1.725

        # ===== GOAL =====
        if self.goal_loss.isChecked():
            calories = tdee - 500
        elif self.goal_gain.isChecked():
            calories = tdee + 500
        else:
            calories = tdee

        calories = int(calories)
        kj = int(calories * 4.184)

        # ===== MACRO SPLIT =====
        protein_g = int((0.25 * calories) / 4)
        carbs_g = int((0.50 * calories) / 4)
        fat_g = int((0.25 * calories) / 9)

        sugar_max = int((0.10 * calories) / 4)
        satfat_max = int((0.10 * calories) / 9)

        # ===== RESULT TEXT =====
        self.result_label.setText(f"""
Protein
{protein_g} grams/day
Range: 65 – 186

Carbs
Includes Sugar
{carbs_g} grams/day
Range: 232 – 393

Fat
Includes Saturated Fat
{fat_g} grams/day
Range: 49 – 87

Sugar
< {sugar_max} grams/day

Saturated Fat
< {satfat_max} grams/day

Food Energy
{calories} Calories/day
or {kj} kJ/day

Note:
Hasil ini hanya sebatas testing saja, bukan pengganti saran medis.  
""")