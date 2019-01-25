from caproto.server import pvproperty
from caproto import ChannelType

from pvdict import PVDict

class User(PVDict):
    def __init__(self, id, name):
        super().__init__(f'user:{id}:')
        self.id = id
        self.name = name
        self.uses = None
        self.pvprops['name'] = pvproperty(
                name = f'{self.pvprefix}name',
                value = self.name,
                read_only = True,
                dtype = ChannelType.STRING)
        self.pvprops['say_hello'] = pvproperty(
                name = f'{self.pvprefix}say_hello',
                value = 0,
                dtype = ChannelType.INT,
                doc = self,
                put = User.say_hello)
        self.pvprops['use_machine'] = pvproperty(
                name = f'{self.pvprefix}use_machine',
                value = 0,
                dtype = ChannelType.INT,
                doc = self,
                put = User.use_machine)

    async def say_hello(self, instance, value):
        user = instance.__doc__
        print(f"hi, I'm {user.name}")

    async def use_machine(self, instance, value):
        user = instance.__doc__
        self.messages.put({'cmd': 'use_machine', 'user': user.id,
            'machine': value})

