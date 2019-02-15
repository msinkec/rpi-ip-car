import time
from gpiozero import LED, PWMLED


class Movement():

    def __init__(self):
        self.MAX_DELTA_T = 0.15  # Amout of time the command is executed.

        self.forward_last_t = 0
        self.backwards_last_t = 0
        self.left_last_t = 0
        self.right_last_t = 0
        self.boost_last_t = 0

        # Initialize pins
        self.steerL = LED(15)
        self.steerR = LED(18)
        self.front_motorA = PWMLED(2)
        self.front_motorB = PWMLED(3)
        self.back_motorA = PWMLED(4)
        self.back_motorB = PWMLED(14)

    def execute(self, comm):
        if comm == 'f':
            self.forward_last_t = time.time()
        elif comm == 'b':
            self.backwards_last_t = time.time()
        elif comm == 'l':
            self.left_last_t = time.time()
        elif comm == 'r':
            self.right_last_t = time.time()
        elif comm == 's':
            self.boost_last_t = time.time()
        self.update()

    def update(self):
        cur_t = time.time()

        if ((cur_t - self.boost_last_t) <= self.MAX_DELTA):
            pwm_val = 1
        else:
            pwm_val = 0.3

        # Forward / Backwards movement
        if ((cur_t - self.forward_last_t) <= self.MAX_DELTA_T):
            self.front_motorA.value = pwm_val
            self.front_motorB.value = 0 
            self.back_motorA.value = pwm_val
            self.back_motorB.value = 0
        elif ((cur_t - self.backward_last_t) <= self.MAX_DELTA_T):
            self.front_motorA.value = 0
            self.front_motorB.value = pwm_val 
            self.back_motorA.value = 0
            self.back_motorB.value = pwm_val
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


