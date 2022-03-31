from flask import Blueprint, jsonify, request
import stripe
import os
import json
from app.models import Animal

payments = Blueprint('payments', __name__, url_prefix='/pay')

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def checkTotal(cart):
    """
    return the proper payment amount for this cart's items
    """
    # loop through the cart items
    # grab their price from my SQL database (what I know is the correct price -> server side operations can't be manipulated by the user)
    # calculate the proper total for this cart
    total = 0
    for animal in cart['animals']:
        p = Animal.query.get(cart['animals'][animal]['data']['id']).price
        total += p*cart['animals'][animal]['quantity']
    print(total, round(total, 2) == round(cart['total'], 2))
    # convert to cents before returning
    return int(total*100) if round(total, 2) == round(cart['total'], 2) else None

def getCustomer(user):
    """
    check stripe for existing customer data for this user
    otherwise create a new stripe customer
    """
    try:
        customer = stripe.Customer.retrieve(user['uid'])
    except:
        customer = stripe.Customer.create(id=user['uid'], name=user['displayName'], email=user['email'])
    return customer

@payments.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        # Create a payment intent with the order amount and currency type
        data = json.loads(request.data)
        print(f"cart: total: {data['cart']['total']} size: {data['cart']['size']}\nUser: {data['user']['uid']} {data['user']['email']}")
        intent = stripe.PaymentIntent.create(
            amount=checkTotal(data['cart']),
            currency='usd',
            customer=getCustomer(data['user']),
            payment_method_types=['card']
        )
        return jsonify({'clientSecret': intent['client_secret']}), 200
    except Exception as e:
        print(str(e))
        return jsonify(error=str(e)), 403

