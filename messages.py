from marshmallow import Schema,fields,validate
from dataclasses import dataclass

@dataclass
class Student():
    name : str
    age : int
    registered : bool

    admission : int = 1995

    def is_adult(self):
        return self.age>=18
            

class StudentSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=5,max=150))
    registered = fields.Bool(required=True)

