#![no_std]
use embedded_hal::digital::OutputPin;
use embedded_hal::pwm::SetDutyCycle;
use rp_pico::hal::gpio::Error;

pub struct Motor<'a> {
    pub pwm: &'a mut dyn SetDutyCycle<Error = Error>,
    pub dir: &'a mut dyn OutputPin<Error = Error>,
}

impl<'a> Motor<'a> {
    pub fn stop(&mut self) {
        self.pwm.set_duty_cycle_fully_off().unwrap();
    }

    pub fn speed(&mut self, speed: i8) {
        assert!(speed.abs() <= 100);

        if speed > 0 {
            self.dir.set_high().unwrap();
        } else {
            self.dir.set_low().unwrap();
        }

        self.pwm
            .set_duty_cycle_percent(speed.abs().try_into().unwrap())
            .unwrap();
    }
}
