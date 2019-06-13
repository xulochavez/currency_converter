from flask import Flask, jsonify




@app.route("/")
def index():
    return "Welcome to the currency convertor app"


def get_ccy_converter():
    pass


@app.route('/currency_convertor/rates', methods=['GET'])
def get_rates():
    rates = [c.as_dict() for c in FxRate.query.all()]
    return jsonify(rates)


