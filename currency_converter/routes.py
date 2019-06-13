from flask import Blueprint, jsonify, request
from currency_converter.currency_converter import get_ccy_converter

bp = Blueprint('app_routes', __name__, url_prefix='/currency_converter')

@bp.route("/")
def index():
    return "Welcome to the currency convertor app"


@bp.route('/rates', methods=['GET'])
def get_rates():
    ccy_converter = get_ccy_converter()
    rates = {'timestamp': ccy_converter.timestamp,
             'base': ccy_converter.base,
             'rates': ccy_converter.rates}
    return jsonify(rates)


@bp.route('/convert', methods=['GET'])
def convert():
    from_ccy = request.args.get('from_ccy', '')
    to_ccy = request.args.get('to_ccy', '')
    amount = float(request.args.get('amount', ''))
    ccy_converter = get_ccy_converter()
    converted_amount = ccy_converter.convert(amount, from_ccy, to_ccy)
    result = {'from_ccy': from_ccy, 'to_ccy': to_ccy,
              'amount': amount, 'converted_amount': converted_amount}
    return jsonify(result)



