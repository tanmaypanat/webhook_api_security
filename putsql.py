from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

@dataclass
class Student:
    name: str
    age: int
    registered: bool
    admission: int = 1995

class StudentModel(Base):
    __tablename__ = "studentnew"
    id = Column(Integer,primary_key = True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    registered = Column(Boolean,nullable=False)
    admission =Column(Integer,nullable=False)
    
class pots(Base):
    __tablename__ = "pots"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables automatically
Base.metadata.create_all(engine)

student_dc = Student(name="Tanmay", age=12, registered=True, admission=2028)

with SessionLocal() as session:
    db_student = StudentModel(
        name=student_dc.name,
        age=student_dc.age,
        registered=student_dc.registered,
        admission=student_dc.admission
    )
    session.add(db_student)
    session.commit()
    session.refresh(db_student)  # refresh to get id
    print(f"Inserted student with ID: {db_student.id}")

with SessionLocal() as session:
    db_pot = pots(
        name="pan"
    )
    session.add(db_pot)
    session.commit()
    session.refresh(db_pot)
    print(f"Inserted student with ID: {db_pot.id}")


with SessionLocal() as session:
    students = session.query(StudentModel).filter(StudentModel.admission==2025,StudentModel.name=="Tanmay").all()
    for s in students:        
        print(s.id)