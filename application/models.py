from .database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    user_id = db.Column(db.Integer(),primary_key=True)
    user_name = db.Column(db.String(), nullable=False,unique=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(),nullable=False,unique=True)
    password = db.Column(db.String(),nullable=False)
    type = db.Column(db.String(), default= "general")
    def get_id(self):
        return str(self.user_id)
class Section(db.Model):
    section_id=db.Column(db.Integer(),primary_key=True)
    section_name=db.Column(db.String(),nullable=False)
    section_description=db.Column(db.String())
    book=db.relationship('Book', backref='section')
    books=db.relationship('Book',cascade='all,delete')
class Book(db.Model):
    book_id=db.Column(db.Integer(),primary_key=True)
    book_name=db.Column(db.String(),nullable=False)
    book_description=db.Column(db.String())
    book_author=db.Column(db.String(),nullable=False)
    book_price=db.Column(db.Integer(),nullable=False)
    book_rating=db.Column(db.Float(),default=0)
    section_id=db.Column(db.Integer(),db.ForeignKey("section.section_id"),nullable=False)
    # section=db.relationship('Section', backref='book')
    # section=db.relationship('Section',cascade='all,delete')
    userbooks=db.relationship('UserBooks',cascade='all,delete')
    rating=db.relationship('Rating',cascade='all,delete')
    

class UserBooks(db.Model):
    userbooks_id=db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    book_id=db.Column(db.Integer(),db.ForeignKey("book.book_id"),nullable=False)
    issued_date=db.Column(db.String())
    revoke_date=db.Column(db.String())
    status=db.Column(db.String(),  default='Requested')
    book=db.relationship('Book', backref='userbook')
    user=db.relationship('User',backref='userbook')

class Rating(db.Model):
    rating_id=db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    book_id=db.Column(db.Integer(),db.ForeignKey("book.book_id"),nullable=False)
    comments=db.Column(db.String())
    rating=db.Column(db.Float())