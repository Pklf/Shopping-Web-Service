"""Flask Application routes."""
import json, threading
from flask import jsonify, request, current_app as app
from database.models import Product
from __init__ import db
from lib.lib_routes import get_exe_id, validate_positive_int_error, validate_zero_positive_int_error

lock = threading.Lock() # For ensuring mutual exclusion
exe_id = get_exe_id() # Server execution ID

@app.route("/api/product/query/<id>", methods=["GET"])
def query_prodcuct(id):
    """Query a product. Return format is json.
    Input: 
    1. product id
    Action:
    1. Returns all attributes of the product.
    """
    # validate the input data 
    if validate_positive_int_error(id):
        return jsonify({"exe_id": exe_id, "error": "id is not zero or a positive integer"}), 400

    # mutual exclusion
    with lock:
        # find Product in database
        product = Product.query.filter_by(id=id).first()

        # 404 error if Product is not found
        if not product:
            return jsonify({"exe_id": exe_id, "error": "product ID does not exist"}), 404

    response = product.to_json()
    response["exe_id"] = exe_id
    return response

@app.route("/api/product/buy/<id>", methods=["PUT"])
def buy_prodcuct(id):
    """Buy a product. Return format is json.
    Input: 
    1. product id
    2. credit-card number
    3. quantity want to buy
    Action:
    1. Updates the quantity in stock if >= 1
    2. return status
    - Success: Returns success and amount deducted from the credit card
    - Fail: Returns fail with reason(s).
    """
    error_msg = []

    if not request.data:
        return jsonify({"exe_id": exe_id, "error": "missing quantity, missing credit card number"}), 400

    data = json.loads(request.data)
    # validate the input data
    if validate_positive_int_error(id):
        error_msg.append("id is not zero or a positive integer")

    quantity_to_buy = data.get("quantity")
    if not quantity_to_buy:
        error_msg.append("missing quantity")
    elif validate_zero_positive_int_error(quantity_to_buy):
        error_msg.append("quantity is not a positive integer")

    credit_card = data.get("credit_card")
    if not credit_card or not credit_card.strip():
        error_msg.append("missing credit card number")
    elif len(credit_card) != 16:
        error_msg.append("incorrect credit card format (isn't 16 digits)")

    if error_msg:
        return jsonify({"exe_id": exe_id, "error": ", ".join(error_msg)}), 400

    # mutual exclusion
    with lock:
        # find Product in database
        product = Product.query.filter_by(id=id).first()

        # 404 error if Product is not found
        if not product:
            return jsonify({"exe_id": exe_id, "error": "product ID does not exist"}), 404
        
        # check if quantity in stock is sufficient
        if product.quantity < quantity_to_buy:
            return jsonify({"exe_id": exe_id, "status": "failure (insufficient quantity in stock)"})
        
        # update quantity in stock
        product.quantity -= quantity_to_buy
        amount_deducted = quantity_to_buy * product.price
        db.session.commit()

    return jsonify({"exe_id": exe_id, "status": "success", "amount_deducted": amount_deducted})

@app.route("/api/product/replenish/<id>", methods=["PUT"])
def replenish_prodcuct(id):
    """Replenish a product with quantity. Return format is json.
    Input:
    1. product id
    2. quantity want to replenish
    Action:
    1. replenish
    2. return status
    - Success: Returns success message and updated quantity in stock
    """
    error_msg = []

    if not request.data:
        return jsonify({"exe_id": exe_id, "error": "missing quantity"}), 400

    data = json.loads(request.data)
    # validate the input data
    if validate_positive_int_error(id):
        error_msg.append("id is not zero or a positive integer")

    quantity_to_replenish = data.get("quantity")
    if not quantity_to_replenish:
        error_msg.append("missing quantity")
    elif validate_zero_positive_int_error(quantity_to_replenish):
        error_msg.append("quantity is not a positive integer")

    if error_msg:
        print(error_msg)
        return jsonify({"exe_id": exe_id, "error": ", ".join(error_msg)}), 400
    
    # mutual exclusion
    with lock:
        # find Product in database
        product = Product.query.filter_by(id=id).first()

        # 404 error if Product is not found
        if not product:
            return jsonify({"exe_id": exe_id, "error": "product ID does not exist"}), 404

        # update quantity in stock
        product.quantity += quantity_to_replenish
        db.session.commit()

    return jsonify({"exe_id": exe_id, "status": "success", "id": int(id) , "current_quantity": product.quantity})