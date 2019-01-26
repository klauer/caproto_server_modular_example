from caproto.server import pvproperty, PVGroup
from caproto import ChannelType


class User(PVGroup):
    name = pvproperty(read_only=True,
                      dtype=ChannelType.STRING)
    say_hello = pvproperty(value=0,
                           dtype=ChannelType.INT)
    use_machine = pvproperty(value=0,
                             dtype=ChannelType.INT)

    def __init__(self, prefix, id, name, ioc):
        super().__init__(f'{prefix}user:{id}:')
        self.id = id
        self.uses = None
        self._name = name
        self.ioc = ioc

    @name.startup
    async def name(self, instance, async_lib):
        await self.name.write(self._name)

    @say_hello.putter
    async def say_hello(self, instance, value):
        print(f"hi, I'm {self.name.value}")

    @use_machine.putter
    async def use_machine(self, instance, value):
        self.ioc.messages.put(
            {'cmd': 'use_machine',
             'user': self.id,
            'machine': value})
