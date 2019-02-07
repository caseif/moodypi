#!/usr/bin/python3

import time

import RPi.GPIO as gpio

CHAN_R = 36
CHAN_G = 38
CHAN_B = 40

CYCLE_FREQ = 600

class LightController:
    def __init__(self):
        self.color_r = 0
        self.color_g = 0
        self.color_b = 0

        gpio.setmode(gpio.BOARD)

        gpio.setup(CHAN_R, gpio.OUT, initial=gpio.LOW)
        gpio.setup(CHAN_G, gpio.OUT, initial=gpio.LOW)
        gpio.setup(CHAN_B, gpio.OUT, initial=gpio.LOW)

        self.pwm_r = gpio.PWM(CHAN_R, CYCLE_FREQ)
        self.pwm_g = gpio.PWM(CHAN_G, CYCLE_FREQ)
        self.pwm_b = gpio.PWM(CHAN_B, CYCLE_FREQ)

        self.pwm_r.start(100)
        self.pwm_g.start(100)
        self.pwm_b.start(100)

    def set_color(self, r, g, b):
        self.color_r = r
        self.color_g = g
        self.color_b = b
        self.pwm_r.ChangeDutyCycle(r * 100)
        self.pwm_g.ChangeDutyCycle(g * 100)
        self.pwm_b.ChangeDutyCycle(b * 100)

    def cleanup(self):
        GPIO.cleanup

if __name__ == "__main__":
    controller = LightController()

    fade_time = 100000
    t = 0

    while True:
        r = 0
        g = 0
        b = 0

        if t < fade_time:
            r = 1 - abs(t / fade_time)
        elif t >= fade_time * 2:
            r = 1 - abs((t - fade_time * 3) / fade_time)

        if t < fade_time * 2:
            g = 1 - abs((t - fade_time * 1) / fade_time)

        if t >= fade_time:
            b = 1 - abs((t - fade_time * 2) / fade_time)

        controller.set_color(r, g, b)

        t += 1
        if t >= fade_time * 3:
            t = 0
