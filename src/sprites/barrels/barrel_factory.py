from .color_barrel import ColorBarrel

class BarrelFactory:
    @classmethod
    def create_barrel(cls, obj_dict, groups):
        print("Making a turret!")
        if obj_dict.name == "color_barrel":
            return ColorBarrel(obj_dict.x, obj_dict.y, obj_dict.color, obj_dict.barrel_type, groups)
