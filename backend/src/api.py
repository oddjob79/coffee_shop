import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import logging
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, get_token_auth_header

app = Flask(__name__)
setup_db(app)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

# @app.route('/headers')
# @requires_auth('get:drinks')
# def headers(token):
#     print(token)
#     return 'These are a few of my favourite things'


# '''
# @TODO implement endpoint
#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''
@app.route('/drinks')
def retrieve_drinks():
    drinks = Drink.query.all()
    if drinks is None:
        abort(404)

    short_drinks = [dr.short() for dr in drinks]

    if short_drinks is None:
        print('unable to get short_drinks')
        abort(404)
    else:
        return jsonify({
            'success': True,
            'drinks': short_drinks
        })



# '''
# @TODO implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drink_details(token):
    drinks = Drink.query.all()
    if drinks is None:
        abort(404)

    long_drinks = [dr.long() for dr in drinks]
    if long_drinks is None:
        print('unable to get short_drinks')
        abort(404)

    return jsonify({
        'success': True,
        'drinks': long_drinks
    })



# '''
# @TODO implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(token):
    new_title = request.form.get('title', None)
    new_recipe = request.form.get('recipe', None)

    # new_title = request.json.get('title', None)
    # new_recipe = request.json.get('recipe', None)

    # logging.debug('new title & recipe = ' + new_title + ', ' + new_recipe)

    # if missing info needed to create drink then abort 400
    if (new_title is None) or (new_recipe is None):
        abort(400)
    # else attempt insert data into db
    else:
        new_drink = Drink(title=new_title, recipe=new_recipe)
        try:
            new_drink.insert()
        except:
            abort(422)

    # locate id of newly created drink
    created_drink = Drink.query.filter(Drink.title==new_title, Drink.recipe==new_recipe).one_or_none()

    if created_drink is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'drinks': created_drink.long()
        })



# '''
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_existing_drink(token, id):
    # Retreieve updated data from form
    upd_title = request.form.get('title', None)
    upd_recipe = request.form.get('recipe', None)

    # if no new details sent, then abort 400
    if (upd_title is None) and (upd_recipe is None):
        abort(400)
    # else attempt update
    else:
        # locate drink to be updated
        upd_drink = Drink.query.filter(Drink.id == id).one_or_none()
        # if no match found - abort 404
        if upd_drink is None:
            print ('ID not found')
            abort(404)
        else:
            if upd_title is not None:
                upd_drink.title = upd_title
            if upd_recipe is not None:
                upd_drink.recipe = upd_recipe
            try:
                upd_drink.update()
            except:
                abort(422)

    return jsonify({
        'success': True,
        'drinks': upd_drink.long()
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


# '''
# @TODO implement error handler for AuthError
#     error handler should conform to general task above
# '''
# error handler found on Stack Overflow
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
