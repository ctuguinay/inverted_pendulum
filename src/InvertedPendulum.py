# This file contains the drawing part for various systems. Given a state vector
# Will return an imageself.

import numpy as np
import cv2


class InvertedPendulum:
    def __init__(self):
        self.prev_angular_velocity = 0
        self.prev_t = 0

    def step(self, state_vec, t=None):
        """state vector :
        x0 : position of the cart
        x1 : veclocity of the cart
        x2 : angle of pendulum. In ref frame with x as forward of the cart and y as up.
        Angle with respect to ground plane
        x3 : angular velocity of the pendulum
        """
        CART_POS = state_vec[0]
        BOB_ANG = state_vec[2] * 180.0 / np.pi  # degrees
        LENGTH_OF_PENDULUM = 110.0

        IM = np.zeros((512, 512, 3), dtype="uint8")

        # Ground line
        cv2.line(IM, (0, 450), (IM.shape[1], 450), (19, 69, 139), 4)

        # Mark ground line
        XSTART = -5.0
        XEND = 5.0
        for xd in np.linspace(XSTART, XEND, 11):
            x = int((xd - XSTART) / (XEND - XSTART) * IM.shape[0])

            cv2.circle(IM, (x, 450), 5, (0, 255, 0), -1)

            cv2.putText(
                IM,
                str(xd),
                (x - 15, 450 + 15),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.8,
                (200, 200, 250),
                1,
            )

        # Draw Wheels of the cart
        wheel_1_pos = int((CART_POS - 1.2 - XSTART) / (XEND - XSTART) * IM.shape[0])
        wheel_2_pos = int((CART_POS + 1.2 - XSTART) / (XEND - XSTART) * IM.shape[0])

        cv2.circle(IM, (wheel_1_pos, 415), 25, (255, 255, 255), 6)
        cv2.circle(IM, (wheel_2_pos, 415), 25, (255, 255, 255), 6)
        cv2.circle(IM, (wheel_1_pos, 415), 2, (255, 255, 255), -1)
        cv2.circle(IM, (wheel_2_pos, 415), 2, (255, 255, 255), -1)

        # Cart base
        cart_base_start = int((CART_POS - 2.5 - XSTART) / (XEND - XSTART) * IM.shape[0])
        cart_base_end = int((CART_POS + 2.5 - XSTART) / (XEND - XSTART) * IM.shape[0])

        cv2.line(IM, (cart_base_start, 380), (cart_base_end, 380), (255, 255, 255), 6)

        # Pendulum hinge
        pendulum_hinge_x = int((CART_POS - XSTART) / (XEND - XSTART) * IM.shape[0])
        pendulum_hinge_y = 380
        cv2.circle(IM, (pendulum_hinge_x, pendulum_hinge_y), 10, (255, 255, 255), -1)

        # Pendulum
        pendulum_bob_x = int(LENGTH_OF_PENDULUM * np.cos(BOB_ANG / 180.0 * np.pi))
        pendulum_bob_y = int(LENGTH_OF_PENDULUM * np.sin(BOB_ANG / 180.0 * np.pi))
        cv2.circle(
            IM,
            (pendulum_hinge_x + pendulum_bob_x, pendulum_hinge_y - pendulum_bob_y),
            10,
            (255, 255, 255),
            -1,
        )
        cv2.line(
            IM,
            (pendulum_hinge_x, pendulum_hinge_y),
            (pendulum_hinge_x + pendulum_bob_x, pendulum_hinge_y - pendulum_bob_y),
            (255, 255, 255),
            3,
        )

        # Initialize angular velocity and angular acceleration.
        # Angular velocity only stays 0 if there is no prev angle set yet
        # and angular acceleration only stays 0 if there is no prev acceleration
        # set yet.
        angular_velocity = 0
        angular_acceleration = 0

        # Calculate angular velocity (change in angle over time)
        # Since the angle is in degrees, we need to convert it to radians for consistency
        if t is not None:
            if hasattr(self, "prev_angle"):  # If previous angle is stored
                delta_t = t - self.prev_t  # Time elapsed since previous step
                delta_angle = (
                    BOB_ANG - self.prev_angle
                )  # Change in angle since previous step
                angular_velocity = (
                    delta_angle / delta_t
                )  # Angular velocity (degrees per second)
                # Convert to radians per second
                state_vec[3] = angular_velocity * np.pi / 180.0

                # Calculate angular acceleration
                if hasattr(self, "prev_angular_velocity"):
                    delta_angular_velocity = (
                        angular_velocity - self.prev_angular_velocity
                    )
                    angular_acceleration = delta_angular_velocity / delta_t
            self.prev_angular_velocity = angular_velocity
            self.prev_angle = BOB_ANG  # Store current angle for next step
            self.prev_t = t  # Store current time for next step

        # Mark the current angle
        angle_display = BOB_ANG % 360
        if angle_display > 180:
            angle_display = -360 + angle_display
        cv2.putText(
            IM,
            "theta=" + str(np.round(angle_display, 4)) + " deg",
            (pendulum_hinge_x - 15, pendulum_hinge_y - 15),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            0.8,
            (200, 200, 250),
            1,
        )

        # Display on top
        if t is not None:
            angular_velocity_display = (
                state_vec[3] * 180.0 / np.pi
            )  # Convert angular velocity from radians per second to degrees per second
            cv2.putText(
                IM,
                "t=" + str(np.round(t, 4)) + "sec",
                (15, 15),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.8,
                (200, 200, 250),
                1,
            )
            cv2.putText(
                IM,
                "POS=" + str(np.round(CART_POS, 4)) + " m",
                (15, 55),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.8,
                (200, 200, 250),
                1,
            )
            cv2.putText(
                IM,
                "ANG=" + str(np.round(BOB_ANG, 4)) + " degrees",
                (15, 35),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.8,
                (200, 200, 250),
                1,
            )
            cv2.putText(
                IM,
                "ANG_VEL=" + str(np.round(angular_velocity_display, 4)) + " deg/s",
                (15, 75),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.8,
                (200, 200, 250),
                1,
            )
            cv2.putText(
                IM,
                "ANG_ACC=" + str(np.round(angular_acceleration, 4)) + " deg/s^2",
                (15, 95),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.8,
                (200, 200, 250),
                1,
            )

        return IM


if __name__ == "__main__":
    syst = InvertedPendulum()

    x = 0.0
    sx = 1.0
    theta = np.pi / 3
    stheta = np.pi / 3
    t = 0.0
    while True:
        # x += sx*0.1
        # theta += stheta*1.
        # if( x > 5 ):
        #     sx = -1.
        # if( x < -5 ):
        #     sx = 1.0

        # theta = -9.8 / 1.5 * np.cos( t ) + 95.0 + 9.8/1.5

        rendered = syst.step([x, 0, theta, 0])
        cv2.imshow("im", rendered)

        if cv2.waitKey(30) == ord("q"):
            break

        t += 30.0 / 1000.0
