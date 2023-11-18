# -*- encoding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import LargeBinary, Column, Integer, String, Float, DateTime
from sqlalchemy.sql.sqltypes import DATETIME, TIMESTAMP

from app import db, login_manager

from app.base.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class Suffix(db.Model):

    __tablename__ = 'Suffix'

    id = Column(Integer, primary_key=True)
    suffix = Column(String, unique=True, nullable=False)
    Timestamp = Column(DateTime, unique=True, nullable=False)
    build = Column(String, unique=False, nullable=True)
    desc = Column(String, unique=False, nullable=True)
    hidden = Column(db.Boolean, unique=False, nullable=True)


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            
            setattr(self, property, value)

    def __repr__(self):
        return '<Suffix: %s>' % self.suffix

class Sfssum(db.Model):

    __tablename__ = 'Sfssum'

    id = Column(Integer, primary_key=True)
    suffix = Column(String, nullable=False)
    BizMetric = Column(Integer)
    ReqOpRate = Column(Float)
    AchiOpRate = Column(Float)
    AvgLat = Column(Float)
    TotalKBps = Column(Float)
    RdKBps = Column(Float)
    WrtKBps = Column(Float)
    RunSec = Column(Integer)
    Cl = Column(Integer)
    ClProc = Column(Integer)
    AvgFileSizeKB = Column(Integer)
    ClDataSetMiB = Column(Integer)
    StartDataSetMiB = Column(Integer)
    InitFileSetMiB = Column(Integer)
    MaxFileSpaceMiB = Column(Integer)
    WorkloadName = Column(String)
    ValidRun = Column(String)
    

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)

    def __repr__(self):
        return '<Sfsnum: {} {}>'.format(self.suffix, self.BizMetric) 

class ArrayMetric(db.Model):

    __tablename__ = 'ArrayMetric'

    id = Column(Integer, primary_key=True)
    suffix = Column(String, nullable=False)
    Timestamp = Column(DateTime)
    SpaCpu = Column(Float)
    SpbCpu = Column(Float)
    SpaTotalIOPS = Column(Float)
    SpbTotalIOPS = Column(Float)
    SpaAvgIOPS = Column(Float)
    SpbAvgIOPS = Column(Float)
    SpaRdKBPS = Column(Float)
    SpbRdKBPS = Column(Float)
    SpaWrtKBPS = Column(Float)
    SpbWrtKBPS = Column(Float)
    SpaAvgRdSize = Column(Float)
    SpbAvgRdSize = Column(Float)
    SpaAvgWrtSize = Column(Float)
    SpbAvgWrtSize = Column(Float)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
               
            setattr(self, property, value)

    def __repr__(self):
        return '<ArrayMetric: {} {}>'.format(self.suffix, self.Timestamp )

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
