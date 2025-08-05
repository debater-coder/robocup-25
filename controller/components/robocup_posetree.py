from posetree import CustomFramePoseTree


class RobocupPoseTree(CustomFramePoseTree):
    """This project's posetree implementaton."""

    def _get_transform(self, parent_frame: str, child_frame: str, timestamp: float):
        raise NotImplementedError()
