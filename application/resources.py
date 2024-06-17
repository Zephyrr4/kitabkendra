from flask_restful import Api, Resource,reqparse
from werkzeug.sansio.response import Response
from .models import *
api=Api()

parser=reqparse.RequestParser()
# =====Section+=====
parser.add_argument('section_name')
parser.add_argument('section_description')

# =======Book++=====
parser.add_argument('book_name')
parser.add_argument('book_description')
parser.add_argument('book_author')
parser.add_argument('book_price')
parser.add_argument('section_id')

class Bookapi (Resource):
    def get(self,book_id):
        this_book=Book.query.get(book_id)
        if this_book:
            book={}
            book['book_id']=this_book.book_id
            book['book_name']=this_book.book_name
            book['book_description']=this_book.book_description
            book['book_author']=this_book.book_author
            book['book_price']=this_book.book_price
            book['section_name']=this_book.section.section_name
            return book
        return "Book ID Not Found",404
    def post(self):
        args= parser.parse_args()
        new_book=Book(book_name=args['book_name'],book_description=args['book_description'],book_author=args['book_author'],book_price=args['book_price'],section_id=args['section_id'])
        db.session.add(new_book)
        db.session.commit()
        return "Book added Successfully",201
    def put(self,book_id):
        args= parser.parse_args()
        this_book=Book.query.get(book_id)
        if this_book:
            this_book.book_name=args['book_name']
            this_book.book_description=args['book_description']
            this_book.book_author=args['book_author']
            this_book.book_price=args['book_price']
            this_book.section_id=args['section_id']
            db.session.commit()
            return "Successfully Updated",201
        return "Book ID Not Found",404
    
    def delete(self,book_id):
        this_book=Book.query.get(book_id)
        if this_book:
            db.session.delete(this_book)
            db.session.commit()
            return "Deleted Successfully",201
        return "Book ID Not Found",404



class Sectionapi(Resource):
    def get(self,section_id):
        this_section=Section.query.get(section_id)
        if this_section:
            section={}
            section['section_id']=this_section.section_id 
            section['section_name']=this_section.section_name
            section['section_description']=this_section.section_description
            section['Books Available']=len(this_section.book)
            return section
        return "Section ID Not Found",404

    def post(self):
        args= parser.parse_args()
        new_section=Section(section_name=args['section_name'],section_description=args['section_description'])
        db.session.add(new_section)
        db.session.commit()
        return "Created successfully", 201
    def put(self,section_id):
        args= parser.parse_args()
        this_section=Section.query.get(section_id)
        if this_section:
            this_section.section_name=args['section_name']
            this_section.section_description=args['section_description']
            db.session.commit()
            return 'Updated successfully',201
        return "Section ID Not Found",404

    def delete(self,section_id):
        this_section=Section.query.get(section_id)
        if this_section:
            db.session.delete(this_section)
            db.session.commit()
            return "Deleted Successfully",201
        return "Section ID Not Found",404
    
class Userapi(Resource):
    def get(self,user_id):
        this_user=User.query.get(user_id)
        if this_user:
            user={}
            user['user_id']=this_user.user_id
            user['user_name']=this_user.user_name
            user['email']=this_user.email
            userbook=this_user.userbook
            user['books']={}
            for each in userbook:
                user['books'][each.book_id]={'book_name':each.book.book_name,
                                             'status':each.status,
                                             'issued_date':each.issued_date,
                                             'returned_date':each.revoke_date
                                             }
            return user
        return "User Not Found"

# ====api add resources=====
api.add_resource(Bookapi, '/api/book/<book_id>','/api/book')
api.add_resource(Sectionapi, '/api/section/<section_id>','/api/section')
api.add_resource(Userapi,'/api/user/<user_id>')
        