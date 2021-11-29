# Machine Learning workflow
from pprint import pprint

from idict import let, idict
from idict.function.classification import fit, predict
from idict.function.evaluation import split
from sklearn.ensemble import RandomForestClassifier as RF

d = (
        idict.fromtoy()
        >> split
        >> let(fit, algorithm=RF, config={"n_estimators": 55}, Xin="Xtr", yin="ytr")
        >> let(predict, Xin="Xts")
)

print(d.z)
# ...

pprint(d.history)
# ...
