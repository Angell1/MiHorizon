from marshmallow import Schema, fields,post_load,ValidationError



class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

class UserSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Integer(required=True)

    @post_load
    def make(self, data, **kwargs):
        return User(**data)

data = {
    'name': '',
    'age': 23
}

try:
    schema = UserSchema()
    users = schema.load(data)
    print(schema.dump(users))
except ValidationError as err:
    print(err.messages)

