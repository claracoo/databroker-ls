from bluesky.plans import count
from ophyd.sim import hw
from databroker import Broker
from bluesky import RunEngine


RE = RunEngine()
db = Broker.named("local")
hw = hw()
RE.subscribe(db.insert)

for i in range(5):
    RE(count([hw.det], num=3))