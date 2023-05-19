import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
dogs = Blueprint('dogs', 'dog')


@dogs.route('/', methods=['GET'])
def dogs_index():
    result = models.Dog.select()
    print('result of dog select query')
    print(result)

    dog_dicts = [model_to_dict(dog) for dog in result]
    
    return jsonify({
        'data': dog_dicts,
        'message': f"Successfully found {len(dog_dicts)} dogs",
        'status': 200
    }), 200

@dogs.route('/<id>', methods=['GET'])
def get_one_dog(id):
    dog = models.Dog.get_by_id(id)
    print(dog)
    return jsonify(
        data=model_to_dict(dog),
        message="Success!!!",
        status=200
    ), 200


@dogs.route('/', methods=['POST'])
def create_dogs():
    payload = request.get_json() # this is like req.body express 
    print(payload)
    new_dog = models.Dog.create(name=payload['name'], age=payload['age'], breed=payload['breed'])
    print(new_dog) # just prints the ID -- check sqlite3 to see the data 

    dog_dict = model_to_dict(new_dog)
    return jsonify(
        data=dog_dict,
        message="Sucessfully created dog!",
        status=201
    ), 201


# DELETE / DESTROY 
# DELETE api/v1/dogs/<id>
@dogs.route('/<id>', methods=['DELETE'])
def delete_dog(id):
    # we are trying to delete the dog with the id that comes through as a param 
    # check here for now: http://docs.peewee-orm.com/en/latest/peewee/querying.html#deleting-records
    delete_query = models.Dog.delete().where(models.Dog.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)

    #TODO: write logic -- if no rows were deleted return 
    # some message that tells that the delete did not happen 

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} dog with id {id}",
        status=200
    ), 200

# PUT UPDATE ROUTE 
# PUT api/v1/dogs/<id>
@dogs.route('/<id>', methods=['PUT'])
def update_dog(id):
    payload = request.get_json()
    print(payload)

    
    models.Dog.update(**payload).where(models.Dog.id == id).execute() 
    # updated_dog = models.Dog.get_by_id(id)
    # updated_dog_dict = model_to_dict(updated_dog)

    return jsonify(
        data=model_to_dict(models.Dog.get_by_id(id)), # same as lines 107, 108 
        message="resource updated successfully",
        status=200
    ),200
