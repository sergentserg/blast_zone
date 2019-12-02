from .color_barrel import ColorBarrel

class BarrelFactory:
    @classmethod
    def create_barrel(cls, obj, groups):
        print("Making a turret!")
        if obj.name == "color_barrel":
            return ColorBarrel(obj.x, obj.y, obj.color, obj.barrel_type, groups)
