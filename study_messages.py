from dataclasses import dataclass
from marshmallow import Schema,validate,fields

@dataclass
class Student():
    name: str
    age: int

    def is_adult(self):
        return self.age>=18


class StudentSchema(Schema):
    name = fields.String(required=True,validate=validate.Length(min=3))
    age = fields.Integer(required=True)
