import datetime as dt
from marshmallow import Schema, fields,post_load,validates,ValidationError
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





class TestCaseresSchema(Schema):
    id = fields.Int()
    test_pro = fields.Str()
    test_caseid = fields.Str()
    test_target = fields.Str()
    test_level = fields.Str()
    test_condition = fields.Str()
    test_input = fields.Str()
    test_step = fields.Str()
    test_output = fields.Str()
    test_module = fields.Str()
    test_time = fields.DateTime()

class TestCaseres(object):
    def __init__(self, id,test_caseid,test_time, test_pro,test_target,test_level,test_condition,test_input,test_step,test_output,test_module):
        self.id = id
        self.test_pro = test_pro
        self.test_caseid = test_caseid
        self.test_time = test_time
        self.test_target = test_target
        self.test_level = test_level
        self.test_condition = test_condition
        self.test_input = test_input
        self.test_step = test_step
        self.test_output = test_output
        self.test_module = test_module


    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class Testcaseinput(object):
    def __init__(self, filename, classname,funcname):
        self.filename = filename
        self.classname = classname
        self.funcname = funcname

class TestcaseinputSchema(Schema):
    filename = fields.Str(required=True)
    classname = fields.Str(required=True)
    funcname = fields.Str(required=True)

    @validates('filename')
    def validate_filename(self, value):
        if len(value) == 0:
            raise ValidationError('filename is null.')

    @validates('classname')
    def validate_classname(self, value):
        if len(value) == 0:
            raise ValidationError('classname is null.')

    @validates('funcname')
    def validate_funcname(self, value):
        if len(value) == 0:
            raise ValidationError('funcname is null.')
    @post_load
    def make_user(self,data, **kwargs):
        return Testcaseinput(**data)