from collections import deque
from typing import Deque

from numpy import cos, sin

from src.consts import GRAVITY


class DoublePendulum:
    def __init__(
        self,
        m1: float,
        m2: float,
        l1: float,
        l2: float,
        theta1: float,
        theta2: float,
        dtheta1: float = 0,
        dtheta2: float = 0,
        dt: float = 5e-2,
        g: float = GRAVITY,
        trail_length: int = 2500,
    ) -> None:

        # pendulum properties
        self.m1: float = m1
        self.m2: float = m2
        self.l1: float = l1
        self.l2: float = l2

        # initial conditions
        self.theta1: float = theta1
        self.theta2: float = theta2
        self.dtheta1: float = dtheta1
        self.dtheta2: float = dtheta2

        # physics/simulation constants to use
        self.g: float = g
        self.dt: float = dt

        # positions
        self.x1: float = self.l1 * sin(self.theta1)
        self.y1: float = -self.l1 * cos(self.theta1)
        self.x2: float = self.x1 + self.l2 * sin(self.theta2)
        self.y2: float = self.y1 - self.l2 * cos(self.theta2)

        # trail
        self.trail: Deque[tuple[float, float]] = deque(maxlen=trail_length)

    def update(self):
        self._update_positions()
        self.trail.append((self.x2, self.y2))

    def _update_positions(self):
        denom = 2 * self.m1 + self.m2 - self.m2 * cos(2 * self.theta1 - 2 * self.theta2)
        d2theta1 = (
            -self.g * (2 * self.m1 + self.m2) * sin(self.theta1)
            - self.m2 * self.g * sin(self.theta1 - 2 * self.theta2)
            - 2
            * sin(self.theta1 - self.theta2)
            * self.m2
            * (self.dtheta2**2 * self.l2 + self.dtheta1**2 * self.l1 * cos(self.theta1 - self.theta2))
        ) / (self.l1 * denom)

        d2theta2 = (
            2
            * sin(self.theta1 - self.theta2)
            * (
                self.dtheta1**2 * self.l1 * (self.m1 + self.m2)
                + self.g * (self.m1 + self.m2) * cos(self.theta1)
                + self.dtheta2**2 * self.l2 * self.m2 * cos(self.theta1 - self.theta2)
            )
        ) / (self.l2 * denom)

        self.dtheta1 += d2theta1 * self.dt
        self.dtheta2 += d2theta2 * self.dt

        self.theta1 += self.dtheta1 * self.dt
        self.theta2 += self.dtheta2 * self.dt

        self.x1 = self.l1 * sin(self.theta1)
        self.y1 = -self.l1 * cos(self.theta1)

        self.x2 = self.x1 + self.l2 * sin(self.theta2)
        self.y2 = self.y1 - self.l2 * cos(self.theta2)
