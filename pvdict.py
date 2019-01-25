class PVDict:
    def __init__(self, pvprefix):
        self.pvprefix = pvprefix
        self.pvprops = {}

    def exportPvs(self, pvprops):
        for k,v in self.pvprops.items():
            pvprops[f'{self.pvprefix}{k}'] = v
