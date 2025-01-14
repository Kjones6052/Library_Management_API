from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:7Raffi!Codes7@localhost/library_db'


# Create a base class for our models
class Base(DeclarativeBase):
    pass
 
#Instantiate your SQLAlchemy database

db = SQLAlchemy(model_class = Base)

db.init_app(app) #adding our db extension to our app


# Define a simple Person model
class Person(Base):
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100))
    age: Mapped[int]

    #defining relationship attribute to Passport
    passport: Mapped['Passport'] = db.relationship(backpopulates = "person")
    

# Define a Passport model
class Passport(Base):
    __tablename__ = 'passports'
    passport_number: Mapped[int] = mapped_column(primary_key=True) #setting a constraint that the passport number needs to be unique
    expiration_date: Mapped[date]
    person_id: Mapped[int] = mapped_column(db.ForeignKey('persons.id'))  # Foreign key linking to Person table
    country: Mapped[str] = mapped_column(db.String(100))

    # Establish one-to-one relationship attribute
    person: Mapped['Person'] = db.relationship(back_populates="passport")


# Define a Department model
class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100))
	employees: Mapped[list['Employee']] = db.relationship(back_populates = "department") #One department can be connected to a List (Many) Employees

# Define an Employee model
class Employee(Base):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100))
    email: Mapped[str] = mapped_column(db.String(200))
    address: Mapped[str] = mapped_column(db.String(200))
    department_id: Mapped[int] = mapped_column(db.ForeignKey('departments.id'))  # Foreign key to Department

    # Relationship back to Department
    department: db.relationship Mapped['Department'] = db.relationship(back_populates='employees') #One Employee will connect to One Department
    

# Create an association table for the many-to-many relationship
student_course = db.Table(
    'student_course', Base.metadata,
    db.Column('student_id',  db.ForeignKey('students.id')),
    db.Column('course_id', db.ForeignKey('courses.id'))
)

# Define a Student model
class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(db.String(100))
	email: Mapped[str] = mapped_column(db.String(150), unique=True) #contraint to ensure that a students email is unique

    # Relationship with courses
    courses: Mapped[List['Course']] = db.relationship(secondary=student_course)

# Define a Course model
class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
	course_name: Mapped[str] = mapped_column(db.String(100))
	instructor_name: Mapped[str] = mapped_column(db.String(100))

    # Relationship with students
    students: Mapped[List["Student"]] = db.relationship(secondary=student_course)

# Create the table
with app.app_context():
	db.create_all()
			
app.run()