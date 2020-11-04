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




class TaskSchema(Schema):
    id = fields.Int()
    taskname = fields.Str()
    task_id = fields.Str()
    moudle_id = fields.Str()
    moudle_name = fields.Str()
    task_type = fields.Str()
    task_context = fields.Str()


class Task(object):
    def __init__(self, id,taskname,task_id, moudle_id,moudle_name,task_type,task_context):
        self.id = id
        self.taskname = taskname
        self.task_id = task_id
        self.moudle_id = moudle_id
        self.moudle_name = moudle_name
        self.task_type = task_type
        self.task_context = task_context

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)



class MoudleSchema(Schema):
    id = fields.Int()
    moudle_name = fields.Str()
    test_filename = fields.Str()
    test_classname = fields.Str()


class Moudle(object):
    def __init__(self, id,moudle_name,test_filename, test_classname):
        self.id = id
        self.moudle_name = moudle_name
        self.test_filename = test_filename
        self.test_classname = test_classname


    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)



class Testcaseinput(object):
    def __init__(self, filename, classname,funcname,testid):
        self.filename = filename
        self.classname = classname
        self.funcname = funcname
        self.testid = testid

class TestcaseinputSchema(Schema):
    filename = fields.Str(required=True)
    classname = fields.Str(required=True)
    funcname = fields.Str(required=True)
    testid = fields.Str(required=True)

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

    @validates('testid')
    def validate_funcname(self, value):
        if len(value) == 0:
            raise ValidationError('testid is null.')

    @post_load
    def make_user(self,data, **kwargs):
        return Testcaseinput(**data)


class Testreportlist(object):
    def __init__(self, testid):
        self.testid = testid


class TestreportlistSchema(Schema):
    testid = fields.Str()

    @validates('testid')
    def validate_filename(self, value):
        pass
        # if len(value) == 0:
        #     raise ValidationError('testid is null.')

    @post_load
    def make_user(self,data, **kwargs):
        if data:
            return Testreportlist(**data)
        else:
            return



class Taskinput(object):
    def __init__(self, moudleid, task_name,task_type,date1,date2,date3):
        self.moudleid = moudleid
        self.task_name = task_name
        self.task_type = task_type
        self.date1 = date1
        self.date2 = date2
        self.date3 = date3

class TaskinputSchema(Schema):
    moudleid = fields.Int(required=True)
    task_name = fields.Str(required=True)
    task_type = fields.Str(required=True)
    date1 = fields.Str(required=True)
    date2 = fields.Str(required=True)
    date3 = fields.Str(required=True)

    # @validates('filename')
    # def validate_filename(self, value):
    #     if len(value) == 0:
    #         raise ValidationError('filename is null.')
    #
    # @validates('classname')
    # def validate_classname(self, value):
    #     if len(value) == 0:
    #         raise ValidationError('classname is null.')
    #
    # @validates('funcname')
    # def validate_funcname(self, value):
    #     if len(value) == 0:
    #         raise ValidationError('funcname is null.')
    #
    # @validates('testid')
    # def validate_funcname(self, value):
    #     if len(value) == 0:
    #         raise ValidationError('testid is null.')

    @post_load
    def make_user(self,data, **kwargs):
        return Taskinput(**data)
