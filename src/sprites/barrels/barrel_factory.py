from .double_barrel import DoubleBarrel
from .power_barrel import PowerBarrel
from .rapidfire_barrel import RapidFireBarrel

class BarrelFactory:
    @classmethod
    def create_barrel(cls, obj_dict, groups):
        print("Making a turret!")
        if obj_dict.name == "double_barrel":
            return DoubleBarrel(obj_dict.x, obj_dict.y, groups)
        elif obj_dict.name == "power_barrel":
            return PowerBarrel(obj_dict.x, obj_dict.y, groups)
        elif obj_dict.name == "rapid_barrel":
            return RapidFireBarrel(obj_dict.x, obj_dict.y, groups)
