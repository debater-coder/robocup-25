from gpiozero import PhaseEnableMotor

rl = PhaseEnableMotor(3, 2, pwm=True)
fl = PhaseEnableMotor(17, 4, pwm=True)
rr = PhaseEnableMotor(22, 27, pwm=True)
fr = PhaseEnableMotor(9, 10, pwm=True)
