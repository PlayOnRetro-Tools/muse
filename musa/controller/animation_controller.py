from PyQt5.QtCore import QObject, pyqtSignal

from musa.dialog import FileDialogFactory
from musa.model.animation import AnimationsModel
from musa.model.frame import Frame
from musa.model.piece import Piece


class AnimationController(QObject):
    def __init__(self, model: AnimationsModel):
        super().__init__()
        self.model = model

        self.dummy_data()

    def add_frame(self, index: int):
        pass

    def add_animation(self):
        name = FileDialogFactory.name_input("New Animation", "Name:")
        if name:
            animation = self.model.create_animation(name)
            # Create first frame
            animation.add_frame(Frame(f"{name}_0"))

    def dummy_data(self):
        walk = self.model.create_animation("WALK")
        shoot = self.model.create_animation("SHOOT")
        jump = self.model.create_animation("JUMP")

        pieces = [
            Piece(name="FRONT_LEG_2", x=150, y=10, v_flip=True),
            Piece(name="HEAD_1", x=150, y=10, v_flip=True),
            Piece(name="BACK_LEG_3", x=160, y=22, v_flip=True),
            Piece(name="RIGHT_ARM_2", x=150, y=10, v_flip=True),
            Piece(name="LEFT_ARM_0", x=150, y=10, v_flip=True),
        ]

        walk.add_frame(Frame(name="WALK_1", pieces=pieces, ticks=4))
        walk.add_frame(Frame(name="WALK_2", pieces=pieces, ticks=4))
        walk.add_frame(Frame(name="WALK_3", pieces=pieces, ticks=4))
        walk.add_frame(Frame(name="WALK_4", pieces=pieces, ticks=4))

        shoot.add_frame(Frame(name="SHOOT_1", pieces=pieces, ticks=4))
        shoot.add_frame(Frame(name="SHOOT_2", pieces=pieces, ticks=4))
        shoot.add_frame(Frame(name="SHOOT_3", pieces=pieces, ticks=4))
        shoot.add_frame(Frame(name="SHOOT_4", pieces=pieces, ticks=4))

        jump.add_frame(Frame(name="JUMP_1", pieces=pieces, ticks=4))
        jump.add_frame(Frame(name="JUMP_2", pieces=pieces, ticks=4))
        jump.add_frame(Frame(name="JUMP_3", pieces=pieces, ticks=4))
        jump.add_frame(Frame(name="JUMP_4", pieces=pieces, ticks=4))
