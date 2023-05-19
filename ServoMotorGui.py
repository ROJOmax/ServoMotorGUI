import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QGroupBox, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import serial

# Arduino serial communication settings
SERIAL_PORT = 'COM7'  # Change this to match the Arduino's serial port
BAUD_RATE = 9600

# Create a GUI window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Servo Motor Control")

# Create a layout for the window
layout = QVBoxLayout()

# Set the initial size of the window
window.resize(800, 500)

# Create a QLabel for the title
title_label = QLabel("Servo Motor Control")
title_label.setAlignment(Qt.AlignHCenter)
title_font = title_label.font()
title_font.setPointSize(20)
title_label.setFont(title_font)

# Create a layout for the title
title_layout = QVBoxLayout()
title_layout.addWidget(title_label)

# Add the title layout to the main layout
layout.addLayout(title_layout)

# Create labels for the servo motors
servo_labels = [
    QLabel("Base"),
    QLabel("Art 1"),
    QLabel("Art 2")
]

# Create sliders for each servo motor
servo_sliders = [
    QSlider(Qt.Horizontal),
    QSlider(Qt.Horizontal),
    QSlider(Qt.Horizontal)
]

# Create text boxes for entering degrees
degree_inputs = [
    QLineEdit(),
    QLineEdit(),
    QLineEdit()
]

# Create Send buttons for each servo motor
send_buttons = [
    QPushButton("Send"),
    QPushButton("Send"),
    QPushButton("Send")
]

# Create Open and Close buttons for Servo 4
open_button = QPushButton("Open")
close_button = QPushButton("Close")

# Create Connect and Disconnect buttons for serial communication
connect_button = QPushButton("Connect")
disconnect_button = QPushButton("Disconnect")

# Set fixed size for the push buttons
open_button.setFixedSize(80, 30)
close_button.setFixedSize(80, 30)
connect_button.setFixedSize(90, 30)
disconnect_button.setFixedSize(90, 30)

# Create a group box for "La Main" and its layout
la_main_groupbox = QGroupBox("La Main")
la_main_layout = QVBoxLayout()
la_main_groupbox.setLayout(la_main_layout)

# Add the Open and Close buttons to the "La Main" layout
la_main_layout.addWidget(open_button)
la_main_layout.addWidget(close_button)

# Create a group box for "Serial COM" and its layout
serial_com_groupbox = QGroupBox("Serial COM")
serial_com_layout = QVBoxLayout()
serial_com_groupbox.setLayout(serial_com_layout)

# Add the Connect and Disconnect buttons to the "Serial COM" layout
serial_com_layout.addWidget(connect_button)
serial_com_layout.addWidget(disconnect_button)

# Create a layout for the servo sliders, degree inputs, and send buttons
servo_control_layout = QVBoxLayout()
for label, slider, degree_input, send_button in zip(servo_labels, servo_sliders, degree_inputs, send_buttons):
    slider.setMinimum(0)
    slider.setMaximum(180)  
    slider.setTickInterval(1)
    slider.setSingleStep(1)
    servo_control_layout.addWidget(label)
    servo_control_layout.addWidget(slider)
    servo_control_layout.addWidget(degree_input)
    servo_control_layout.addWidget(send_button)
    servo_control_layout.addSpacing(10)

# Add the servo control layout to the main layout
layout.addLayout(servo_control_layout)

# Add the "La Main" group box to the bottom left corner
layout.addWidget(la_main_groupbox, alignment=Qt.AlignBottom | Qt.AlignLeft)

# Add the "Serial COM" group box to the bottom right corner
layout.addWidget(serial_com_groupbox, alignment=Qt.AlignBottom | Qt.AlignRight)

# Set the layout for the window
window.setLayout(layout)

# Initialize Arduino serial connection
arduino = None

# Function to handle slider value changes
def on_slider_changed(value, servo_index):
    if arduino:
        send_servo_position(servo_index, value)

# Function to send servo position to Arduino
def send_servo_position(servo_index, position):
    command = f"{servo_index},{position}\n"
    arduino.write(command.encode())

# Function to handle Open button click
def on_open_clicked():
    if arduino:
        send_servo_position(3, 180)  # Servo 4 position set to 180 degrees

# Function to handle Close button click
def on_close_clicked():
    if arduino:
        send_servo_position(3, 0)  # Servo 4 position set to 0 degrees

# Function to handle Connect button click
def on_connect_clicked():
    global arduino
    if not arduino:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
        connect_button.setEnabled(False)
        disconnect_button.setEnabled(True)

# Function to handle Disconnect button click
def on_disconnect_clicked():
    global arduino
    if arduino:
        arduino.close()
        arduino = None
        connect_button.setEnabled(True)
        disconnect_button.setEnabled(False)

# Function to handle Send button click for servo 1
def on_send1_clicked():
    if arduino:
        degree = int(degree_inputs[0].text())
        send_servo_position(0, degree)

# Function to handle Send button click for servo 2
def on_send2_clicked():
    if arduino:
        degree = int(degree_inputs[1].text())
        send_servo_position(1, degree)

# Function to handle Send button click for servo 3
def on_send3_clicked():
    if arduino:
        degree = int(degree_inputs[2].text())
        send_servo_position(2, degree)

# Connect slider value change events
for slider, servo_index in zip(servo_sliders, range(3)):
    slider.valueChanged.connect(lambda value, servo_index=servo_index: on_slider_changed(value, servo_index))

# Connect Open button click event
open_button.clicked.connect(on_open_clicked)

# Connect Close button click event
close_button.clicked.connect(on_close_clicked)

# Connect Connect button click event
connect_button.clicked.connect(on_connect_clicked)

# Connect Disconnect button click event
disconnect_button.clicked.connect(on_disconnect_clicked)

# Connect Send button click events
send_buttons[0].clicked.connect(on_send1_clicked)
send_buttons[1].clicked.connect(on_send2_clicked)
send_buttons[2].clicked.connect(on_send3_clicked)

# Disable Disconnect button initially
disconnect_button.setEnabled(False)

# Start the GUI application
window.show()
sys.exit(app.exec_())
