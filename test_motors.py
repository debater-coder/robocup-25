from gpiozero import PhaseEnableMotor

rl = PhaseEnableMotor(17, 4, pwm=True)
fl = PhaseEnableMotor(22, 27, pwm=True)
rr = PhaseEnableMotor(9, 10, pwm=True)
fr = PhaseEnableMotor(11, 5, pwm=True)
