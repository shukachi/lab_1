
from __future__ import annotations
from model.color_math import ColorEngine, rgb_to_hsv, hsv_to_rgb


class ColorViewModel:
    def __init__(self, illuminant: str = "D65"):
        self.engine = ColorEngine(illuminant)

        self.gamut_strategy = "clip"      

        self.rgb = [255, 0, 0]
        self.xyz = [0.0, 0.0, 0.0]
        self.hsv = [0.0, 0.0, 0.0]
        self.warning = ""

        self._listeners = []
        self.recompute()

    def subscribe(self, fn):
        self._listeners.append(fn)

    def notify(self):
        for fn in self._listeners:
            fn(self)

    def recompute(self):
        self.xyz = self.engine.rgb_to_xyz(self.rgb)
        self.hsv = rgb_to_hsv(self.rgb)
        self.notify()

    def set_rgb(self, rgb):
        self.rgb = [int(round(min(255, max(0, c)))) for c in rgb]
        self.warning = ""
        self.recompute()

    def set_hsv(self, h, s, v):
        self.set_rgb(hsv_to_rgb(h, s, v))

    def set_xyz(self, xyz):
        rgb, clipped = self.engine.xyz_to_rgb(xyz, self.gamut_strategy)
        self.rgb = rgb
        if clipped:
            name = ("обрезание (Clipping)"
                    if self.gamut_strategy == "clip" else "масштабирование (Scaling)")
            self.warning = f" Цвет вне охвата sRGB — выполнено {name}."
        else:
            self.warning = ""
        self.recompute()

    def set_illuminant(self, name):
        self.engine.set_illuminant(name)     
        self.recompute()

    def set_gamut_strategy(self, s):
        self.gamut_strategy = s
        self.recompute()