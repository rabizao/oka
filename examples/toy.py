from aiuna.step.dataset import Dataset
from oka.io import get, send

iris = Dataset().data
print("iris id:", iris.id)
send(iris)
print("pushed!")

data = get(iris.id)
print("X:", data.X[:5])

