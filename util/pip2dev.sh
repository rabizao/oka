git clone https://github.com/davips/garoupa ../garoupa
git clone https://github.com/davips/akangatu ../akangatu
git clone https://github.com/davips/aiuna ../aiuna
git clone https://github.com/davips/tatu ../tatu

pip install -e .
pip uninstall -y tatu

pip install -e ../tatu
pip uninstall -y aiuna

pip install -e ../aiuna
pip uninstall -y akangatu

pip install -e ../akangatu
pip uninstall -y garoupa

pip install -e ../garoupa

python examples/transfer.py
