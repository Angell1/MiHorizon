import datetime as dt
from marshmallow import Schema, fields
from marshmallow import pprint

class TestCaseSchema(Schema):
    id = fields.Int()
    test_pro = fields.Str()
    test_id = fields.Str()
    test_target = fields.Str()
    test_level = fields.Str()
    test_condition = fields.Str()
    test_input = fields.Str()
    test_step = fields.Str()
    test_output = fields.Str()
    is_connect = fields.Int()
    test_module = fields.Str()
    # email = fields.Email()
    # created_at = fields.DateTime()

class TestCase(object):
    def __init__(self, id, test_pro,test_id,test_target,test_level,test_condition,test_input,test_step,test_output,is_connect,test_module):
        self.id = id
        self.test_pro = test_pro
        self.test_id = test_id
        self.test_target = test_target
        self.test_level = test_level
        self.test_condition = test_condition
        self.test_input = test_input
        self.test_step = test_step
        self.test_output = test_output
        self.is_connect = is_connect
        self.test_module = test_module
        # self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)






