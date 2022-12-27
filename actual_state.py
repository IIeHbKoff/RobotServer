class ActualState:

    _instance = None

    right_wheel: int = 0
    left_wheel: int = 0

    head_h_angle: int = 90
    head_v_angle: int = 0
    right_arm_v_angle: int = 0
    left_arm_v_angle: int = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ActualState, cls).__new__(cls)
        return cls._instance
