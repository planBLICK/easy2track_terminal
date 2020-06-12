import platform
if "Linux pi" in platform._syscmd_uname('-a'):
    from amplepi import AmplePi
else:
    from amplenopi import AmpleNoPi


class Ample(AmplePi if "Linux pi" in platform._syscmd_uname('-a') else AmpleNoPi):

    def __init__(self):
        pass

    def __del__(self):
        pass

    def test(self):
        return self

    def all_on(self):
        return self

    def all_off(self):
        return self

    def update(self):
        return self

    def red(self):
        return self

    def yellow(self):
        return self

    def green(self):
        return self

    def blink(self, times=3, intervall=0.6):
        return self


