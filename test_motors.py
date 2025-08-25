from gpiozero import PhaseEnableMotor

rl = PhaseEnableMotor(13, 6, pwm=True)
fl = PhaseEnableMotor(22, 27, pwm=True)
rr = PhaseEnableMotor(10, 9, pwm=True)
fr = PhaseEnableMotor(11, 5, pwm=True)
