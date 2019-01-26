from caproto.server import pvproperty, PVGroup, run, ioc_arg_parser, SubGroup

import time
from threading import Thread
from user import User
from machine import Machine
from queue import Queue

class Group(PVGroup):
    test = pvproperty()
    blub = pvproperty()

class SimpleIOC(PVGroup):
    value1 = pvproperty()
    messages = Queue()

users = {}
machines = {}
ioc = None

def run_dispatcher():
    while(True):
        if not ioc.messages.empty():
            msg = ioc.messages.get()
            print(f'got message: {msg}')
            try:
                handle_message(msg)
            except Exception:
                ...
        time.sleep(0.5)

def handle_message(message):
    if message['cmd'] == "use_machine":
        user = users[message['user']]
        machine = machines[message['machine']]
        user.uses = machine.id
        machine.used_by = user.id
        print(f'User {user.id} now uses machine {machine.id}')

if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
            default_prefix='toy:',
            desc='a toy IOC server'
    )

    ioc = SimpleIOC(**ioc_options)

    prefix = ioc_options['prefix']
    for i in range(1,5):
        u = User(prefix, i, f'user_{i}', ioc=ioc)
        users[u.id] = u
        ioc.pvdb.update(**u.pvdb)

    for i in range(1,3):
        m = Machine(prefix, i, f'machine_{i}')
        machines[m.id] = m
        ioc.pvdb.update(**m.pvdb)

    other_groups = {}
    for i in range(1,6):
        group = Group(prefix=f'{prefix}group{i}:')
        other_groups[i] = group
        ioc.pvdb.update(**group.pvdb)

    dispatcher_thread = Thread(target=run_dispatcher)
    dispatcher_thread.start()

    run(ioc.pvdb, **run_options)
