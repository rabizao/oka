# Machine Learning workflow
from pprint import pprint

from idict import idict, let
from idict.function.classification import fit, predict
from idict.function.evaluation import split
from sklearn.ensemble import RandomForestClassifier as RF

d = idict.fromtoy() >> split >> let(fit, algorithm=RF, Xin="Xtr", yin="ytr") >> let(predict, Xin="Xts")
print(d.z)
# ...

pprint(d.history)
# ...
