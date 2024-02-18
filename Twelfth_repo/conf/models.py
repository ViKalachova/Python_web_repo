from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table


Base = declarative_base()

student_m2m_grade = Table(
    "student_m2m_grade",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("student", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("grade", Integer, ForeignKey("grades.id", ondelete="CASCADE")),
)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(250), nullable=False)
    students = relationship("Student", cascade="all, delete", backref="groups")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250), nullable=False)
    grades = relationship("Grade", secondary=student_m2m_grade, backref="students", passive_deletes=True)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE"))

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250), nullable=False)
    subjects = relationship("Subject", cascade="all, delete", backref="professor")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(250), nullable=False)
    professor_id = Column(Integer, ForeignKey(Professor.id, ondelete="CASCADE"))
    grades = relationship("Grade", cascade="all, delete", backref="subjects")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    received_date = Column(Date, nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete="CASCADE"))
