from sqlalchemy import Column,Integer,String,create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dataclasses import dataclass

BASE = declarative_base()

@dataclass
class Student():
    name : str
    age : int 

class StudentSchema(BASE):
    __tablename__ = "studentsnew"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)

db = "postgresql://myuser:mypassword@localhost:5432/mydb"
try:
    engine = create_engine(db)
except Exception as e:
    print(e)

    
SessionLocal = sessionmaker(bind=engine)

BASE.metadata.create_all(engine)

s = Student(name="tanmay",age=16)

with SessionLocal() as session:
    schema = StudentSchema(
        name=s.name,
        age=s.age
    )
    session.add(schema)
    session.commit()
    session.refresh(schema)
    print(schema.id)

with SessionLocal() as session:
    res = session.query(StudentSchema).filter(StudentSchema.name=="tanmay",StudentSchema.age>14).all()
    for r in res:
        print(r.name)