from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dbconnection import engine, session, exc
from Base import BaseEntity

Base = declarative_base()

class AnswerModel(Base,BaseEntity):
    __tablename__ = 'answer'
    __table_args__ = {'sqlite_autoincrement' : True}

    text = Column(String)
    questionID = Column(Integer)
    userID = Column(Integer)
    weight = Column(Integer)

    def __repr__(self):
        return self.text + 'Represent'

    def __str__(self):
        return self.text

    @staticmethod
    def save(questionID,userID,answerText):
        session.add(AnswerModel(questionID=questionID,userID=userID,text=answerText,weight=0))
        session.commit()
        
    @staticmethod
    def savereview(questionID,userID,answerText,weight):
        session.add(AnswerModel(questionID=questionID,userID=userID,text=answerText,weight=weight+1))
        session.commit()
    
    @staticmethod
    def updateAnswer(answerID, answerText):
        session.query(AnswerModel).filter_by(id = answerID).update({"text":answerText}, synchronize_session=False)
    
    @staticmethod
    def getAnswerID(uID, qID):   
        if engine.dialect.has_table(engine.connect(), "answer"):
            try:
                answer = session.query(AnswerModel).filter_by(questionID = qID, userID = uID).one()               
                return answer.id
            except exc.InvalidRequestError:
                return 0  
        else: 
            return 1
    
    @staticmethod
    def checkAnswerExist(uID, qID):
        if engine.dialect.has_table(engine.connect(), "answer"):
            try:
                answer = session.query(AnswerModel).filter_by(questionID = qID, userID = uID).one()               
                return 1
            except exc.InvalidRequestError:
                return 0
        else: 
            return 0
        
    
    @staticmethod
    def getTimeStamp(answerID):
        answer = session.query(AnswerModel).filter_by(id = answerID).one()
        return answer.created   

Base.metadata.create_all(engine)
