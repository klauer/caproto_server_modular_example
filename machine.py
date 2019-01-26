from caproto.server import pvproperty, PVGroup
from caproto import ChannelType


class Machine(PVGroup):
    name = pvproperty(read_only=True,
                      dtype=ChannelType.STRING)
    startup = pvproperty(value=0,
                         dtype=ChannelType.INT)

    def __init__(self, prefix, id, name):
        super().__init__(f'{prefix}machine:{id}:')
        self.id = id
        self._name = name
        self.used_by = None

    @name.startup
    async def name(self, instance, value):
        await self.name.write(self._name)
        print(f"{self.name.value} is starting up")
