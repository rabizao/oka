from aiuna.step.dataset import Dataset
from oka.io import get, send

iris = Dataset().data
send(iris)

# data = get(iris.id)
# print("X:", data.X)

