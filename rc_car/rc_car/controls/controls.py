import time
from gpiozero import LED, PWMLED


class Movement():

    def __init__(self):
        self.MAX_DELTA_T = 0.15  # Amout of time the command is executed.

        self.forward_last_t = 0
        self.backwards_last_t = 0
        self.left_last_t = 0
        self.right_last_t = 0
        self.pwm_val = 0

        # Initialize pins
        self.steerL = LED(15)
        self.steerR = LED(18)
        self.front_motorA = PWMLED(2)
        self.front_motorB = PWMLED(3)
        self.back_motorA = PWMLED(4)
        self.back_motorB = PWMLED(14)

    def execute(self, comm):
        if comm[0] == 'f':
            self.forward_last_t = time.time()
            self.pwm_val = float(comm[1:])
        elif comm[0] == 'b':
            self.backwards_last_t = time.time()
            self.pwm_val = float(comm[1:])
        elif comm[0] == 'l':
            self.left_last_t = time.time()
        elif comm[0] == 'r':
            self.right_last_t = time.time()
        self.update()

    def update(self):
        cur_t = time.time()

        # Forward / Backwards movement
        if ((cur_t - self.forward_last_t) <= self.MAX_DELTA_T):
            self.front_motorA.value = self.pwm_val
            self.front_motorB.value = 0 
            self.back_motorA.value = self.pwm_val
            self.back_motorB.value = 0
        elif ((cur_t - self.backwards_last_t) <= self.MAX_DELTA_T):
            self.front_motorA.value = 0
            self.front_motorB.value = self.pwm_val 
            self.back_motorA.value = 0
            self.back_motorB.value = self.pwm_val
        else:
            self.front_motorA.value = 0
            self.front_motorB.value = 0 
            self.back_motorA.value = 0
            self.back_motorB.value = 0

        # L/R steering
        if ((cur_t - self.left_last_t) <= self.MAX_DELTA_T):
            self.steerL.on()
            self.steerR.off()
        elif ((cur_t - self.right_last_t) <= self.MAX_DELTA_T):
            self.steerL.off()
            self.steerR.on()
        else:
            self.steerL.off()
            self.steerR.off()


