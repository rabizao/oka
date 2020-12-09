from aiuna.step.dataset import Dataset
from kururu.tool.communication.lazycache import setcache
from kururu.tool.enhancement.attribute.binarize import Binarize
from kururu.tool.enhancement.attribute.pca import PCA
from kururu.tool.enhancement.instance.sampling.over.rnd import ROS_, ROS
from kururu.tool.evaluation.metric import Metric, Metricb
from kururu.tool.evaluation.split import Split
from kururu.tool.learning.supervised.classification.svm import SVM, SVMb
from oka.io import get, send

setcache("mysql://tatu:kururu@localhost/tatu")

# data = File("iris.arff").data
data = Dataset("abalone").data
print("id:", data.id, "X shape", data.X.shape)
print("X 1st row:\t\t\t", data.X[:1])
print()

data = data >> Binarize * Split * ROS * PCA(n=4) * SVM ** Metric
print("id:", data.id, "X shape", data.X.shape)
print("X 1st row:\t\t\t", data.X[:1])
print()

print("Predictions (z):\t", data.z.tolist())
print("Accuracy (r)):\t\t", data.r)
print()

send(data, url="http://localhost:5000")

data2 = get(data.id, url="http://localhost:5000")
if data:
    print("X 1st row:", data.X[:1])
