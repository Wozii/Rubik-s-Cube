# Cube

## Technologies
- Python 3.8.3
- OpenCV 4.5.4
- Arduino
- STM32f103C8T6 Bluepill
- Stepper motors

## General Info
Rubik's cube solver using Python, OpenCV and Arduino. A smartphone camera is used to upload live video to the Python algorithm that will recognize the cube state and send a set of moves to the Arduino program uploaded to the STM32. The STM32 will then control 6 stepper motors to turn and solve the cube accordingly.

### Work in progress
- Kociemba's algorithm
