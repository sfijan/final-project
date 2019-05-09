from peewee import *

database = PostgresqlDatabase('zavrsni', **{'user': 'postgres'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Competition(BaseModel):
    end_time = DateTimeField(null=True)
    name = TextField()
    public = BooleanField()
    start_time = DateTimeField(null=True)

    class Meta:
        table_name = 'competition'

class Task(BaseModel):
    maxpoints = IntegerField()
    memory_limit_kb = IntegerField(null=True)
    public = BooleanField()
    text = TextField()
    time_limit_ms = IntegerField(null=True)
    title = CharField()

    class Meta:
        table_name = 'task'

class Contains(BaseModel):
    competition = ForeignKeyField(column_name='competition_id', field='id', model=Competition, null=True)
    task = ForeignKeyField(column_name='task_id', field='id', model=Task, null=True)

    class Meta:
        table_name = 'contains'
        indexes = (
            (('task', 'competition'), True),
        )
        primary_key = False

class Language(BaseModel):
    name = TextField()
    version = TextField()

    class Meta:
        table_name = 'language'

class User(BaseModel):
    admin = BooleanField(null=True)
    email = CharField(unique=True)
    password_hash = CharField(null=True)
    username = CharField(unique=True)

    class Meta:
        table_name = 'user'

class ParticipatesIn(BaseModel):
    competition = ForeignKeyField(column_name='competition_id', field='id', model=Competition, null=True)
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=True)

    class Meta:
        table_name = 'participates_in'
        primary_key = False

class Submission(BaseModel):
    language = ForeignKeyField(column_name='language', field='id', model=Language)
    result = IntegerField(null=True)
    task = ForeignKeyField(column_name='task_id', field='id', model=Task)
    time = DateTimeField()
    user = ForeignKeyField(column_name='user_id', field='id', model=User, null=True)

    class Meta:
        table_name = 'submission'

class Test(BaseModel):
    input = TextField()
    output = TextField()
    task = ForeignKeyField(column_name='task', field='id', model=Task)

    class Meta:
        table_name = 'test'

class TestResult(BaseModel):
    points = IntegerField(null=True)
    stderr = TextField(null=True)
    submission = ForeignKeyField(column_name='submission_id', field='id', model=Submission)
    test = ForeignKeyField(column_name='test_id', field='id', model=Test)

    class Meta:
        table_name = 'test_result'
        primary_key = False

