from caproto.server import pvproperty
from caproto import ChannelType

from pvdict import PVDict

class Machine(PVDict):
    def __init__(self, id, name):
        super().__init__(f'machine:{id}:')
        self.id = id
        self.name = name
        self.log = None
        self.used_by = None
        self.pvprops['name'] = pvproperty(
                name = f'{self.pvprefix}name',
                value = self.name,
                read_only = True,
                dtype = ChannelType.STRING)
        self.pvprops['startup'] = pvproperty(
                name = f'{self.pvprefix}startup',
                value = 0,
                dtype = ChannelType.INT,
                doc = self,
                put = Machine.startup)

    async def startup(self, instance, value):
        machine = instance.__doc__
        print(f"{machine.name} is starting up")
