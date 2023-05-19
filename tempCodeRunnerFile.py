# Create a layout for the bottom buttons
bottom_buttons_layout = QHBoxLayout()
bottom_buttons_layout.addWidget(la_main_groupbox, alignment=Qt.AlignBottom | Qt.AlignLeft)
bottom_buttons_layout.addWidget(serial_com_groupbox, alignment=Qt.AlignBottom | Qt.AlignRight)