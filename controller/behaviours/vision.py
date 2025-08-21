import py_trees
import typing
import cv2
import numpy as np

orangeLower = np.array([20, 86, 6])
orangeUpper = np.array([35, 255, 153])


class Vision(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

        self.blackboard = self.attach_blackboard_client(name="Vision Processing")

        self.blackboard.register_key(
            "posetree", access=py_trees.common.Access.WRITE, required=True
        )

        self.cap: cv2.VideoCapture | None = None

    def setup(self, **kwargs: typing.Any):
        self.cap = cv2.VideoCapture(0)

    def update(self) -> py_trees.common.Status:
        if not self.cap:
            self.logger.error("Capture not initialised")
            return py_trees.common.Status.FAILURE

        _, frame = self.cap.read()

        if frame is None:
            return py_trees.common.Status.RUNNING

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        width, height = frame.shape[:2]
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, orangeLower, orangeUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
                cv2.imwrite(
                    "circled_frame.png",
                    cv2.resize(frame, (int(height / 2), int(width / 2))),
                )

        return py_trees.common.Status.RUNNING
