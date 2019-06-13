# INSTRUCTIONS

# clone to a local folder

git clone git@github.com:xulochavez/currency_converter.git

# This will create currency_converter folder

# cd into currency_converter folder

# create virtualenv

# install requirements
pip install -r requirements

# install currency_converter package
pip install .

# initialise database
init_db.sh

# run flask server
run.sh

# example query with curl
curl -i "http://localhost:5000/currency_converter/convert?from_ccy=PLN&to_ccy=EUR&amount=200"
