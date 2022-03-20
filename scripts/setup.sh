virtual_name=.venv

python3 -m venv $virtual_name

source ./$virtual_name/bin/activate

pip install -r ./requirements/local.txt
