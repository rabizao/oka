from aiuna.step.dataset import Dataset
from kururu.tool.communication.lazycache import Cache
from kururu.tool.enhancement.attribute.binarize import Binarize
from kururu.tool.enhancement.instance.sampling.over.rnd import ROS_
from oka.io import get, send
from tatu import Tatu

data = Dataset("iris").data
print("X 1st row:", data.X[:1])

data = data >> Binarize * Cache(Tatu("mysql://tatu:kururu@localhost/tatu", threaded=False)) * ROS_
# data = data >> Binarize * ROS_
print("X 1st row:", data.X[:1])

send(data, url="http://localhost:5000")

print()
data2 = get(data.id, url="http://localhost:5000")
if data:
    print("X 1st row:", data.X[:1])
