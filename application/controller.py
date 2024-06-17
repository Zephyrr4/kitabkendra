from flask import Flask,flash, render_template,redirect,url_for,request
from flask import current_app as app
from .models import *
from flask_login import login_user ,logout_user ,login_required,current_user
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os


USERLIMIT=5
def date_checker(user_id):
    revoke_user=UserBooks.query.filter(UserBooks.user_id==user_id,UserBooks.revoke_date<=datetime.now()).all()
    for user in revoke_user:
        user.status='Returned'
    db.session.commit()
    return
def date_checker_all():
    revoke_user=UserBooks.query.filter(UserBooks.revoke_date<=datetime.now()).all()
    for user in revoke_user:
        user.status='Returned'
    db.session.commit()
    return


@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.user_id!=1:
            return redirect(url_for('user_dashboard'))
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_login'))


@app.route('/login',methods=["GET","POST"])
def user_login():
    if request.method=="POST":
        user_n=request.form.get('user_name')
        user_pwd=request.form.get('password')
        user=User.query.filter_by(user_name=user_n).first()
        if user:
            if user.password==user_pwd:
                if user.type=='general':
                    login_user(user)    
                    return redirect(url_for('user_dashboard'))
                else:
                    login_user(user)
                    return redirect('/admin_dashboard')
            else:
                flash("* Wrong password, please try again")
                return render_template('login.html')
        else:
            flash("* Username not found.")
            return  render_template('login.html')
    return render_template('login.html')
 
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=='POST':
        user_name=request.form.get('user_name')
        f_name=request.form.get('f_name')
        l_name=request.form.get('l_name')
        email=request.form.get('email')
        pswd=request.form.get('password')
        cur_user=User.query.filter_by(user_name=user_name).first()
        if cur_user:
            flash("* Username is already there.")
            return redirect(url_for('register'))
        else:
            user_first=User.query.first()
            if user_first:
                new_user=User(user_name=user_name,first_name=f_name,last_name=l_name,email=email,password=pswd)
            else:
                new_user=User(user_name=user_name,first_name=f_name,last_name=l_name,email=email,password=pswd,type='admin')
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html')

# ===== USER - CONTROLLER ===

@app.route('/dashboard')
@login_required
def user_dashboard():
    current_user
    user_id=current_user.user_id
    all_section=Section.query.all()
    date_checker(user_id)
    user_details=User.query.filter_by(user_id=user_id).first()
    user_request_book=UserBooks.query.filter_by(user_id=user_id,status="Requested").order_by(UserBooks.userbooks_id.desc())
    user_issued_book=UserBooks.query.filter_by(user_id=user_id,status="Issued").order_by(UserBooks.userbooks_id.desc())
    user_returned_book=UserBooks.query.filter_by(user_id=user_id,status="Returned").order_by(UserBooks.userbooks_id.desc())
    return render_template('user_dashboard.html',user_details=user_details,all_section=all_section,user_request_book=user_request_book,user_returned_book=user_returned_book,user_issued_book=user_issued_book)

@app.route('/mybooks')
@login_required
def user_mybooks():
    current_user
    user_id=current_user.user_id
    date_checker(user_id)
    user_details=User.query.filter_by(user_id=user_id).first()
    user_request_book=UserBooks.query.filter_by(user_id=user_id,status="Requested").order_by(UserBooks.userbooks_id.desc()).all()
    user_issued_book=UserBooks.query.filter_by(user_id=user_id,status="Issued").order_by(UserBooks.userbooks_id.desc()).all()
    user_returned_book=UserBooks.query.filter_by(user_id=user_id,status="Returned").order_by(UserBooks.userbooks_id.desc()).all()
    return render_template('user_mybooks.html',user_details=user_details,user_request_book=user_request_book,user_returned_book=user_returned_book,user_issued_book=user_issued_book)

@app.route('/profile',methods=['POST','GET'])
@login_required
def user_profile():
    if request.method=="POST":
        user=User.query.get(current_user.user_id)
        user.user_name=request.form.get('user_name')
        user.first_name=request.form.get('f_name')
        user.last_name=request.form.get('l_name')
        user.email=request.form.get('email')
        usr_pwd=request.form.get('password')
        user.password=request.form.get('password')
        db.session.commit()
        return redirect(url_for('user_profile'))
    return render_template('user_profile.html',user_details=current_user)

# =====UserBook====REQUEST=====
@app.route('/<user_id>/add_book/<book_id>')
def user_request_book(user_id,book_id):
    issued_book_count=UserBooks.query.filter_by(user_id=user_id,status='Issued').all()
    if len(issued_book_count) < USERLIMIT:
        new_user_book=UserBooks(user_id=user_id,book_id=book_id)
        db.session.add(new_user_book)
        db.session.commit()
    else:
        flash("You have reached the maximum number of books allowed per user.")
    return redirect(url_for('user_dashboard'))

# =====UserBook====Issued=====
@app.route('/issue/<user_id>/<book_id>')
def user_issued_book(user_id,book_id):
    current_date=datetime.now()
    # RETURN DATE
    return_date=current_date+timedelta(days=7)
    user_book=UserBooks.query.filter_by(user_id=user_id,book_id=book_id).order_by(UserBooks.userbooks_id.desc()).first()
    user_book.issued_date=current_date
    user_book.revoke_date=return_date
    user_book.status='Issued'
    db.session.commit()
    return redirect('/admin_dashboard')

# ====userbook===return===from==user==side===
@app.route('/return/book/<book_id>')
def return_book(book_id):
    thisbook=UserBooks.query.filter_by(user_id=current_user.user_id,book_id=book_id).order_by(UserBooks.userbooks_id.desc()).first()
    thisbook.status='Returned'
    thisbook.revoke_date=datetime.now()
    db.session.commit()
    return redirect(url_for('user_dashboard'))

# ===readbook===
@app.route('/read/book/<book_id>',methods=['POST','GET'])
@login_required
def book_read(book_id):
    rating=Rating.query.filter_by(user_id=current_user.user_id,book_id=book_id).first()
    current_user
    book_details=Book.query.filter_by(book_id=book_id).first()
    return render_template('book_read.html',book_details=book_details,rating=rating)

# =====RATING====
@app.route('/rating/<book_id>',methods=['POST'])
@login_required
def rating(book_id):
    current_user
    book=Book.query.filter_by(book_id=book_id).first()
    rate=request.form.get('rating')
    comment=request.form.get('comment')
    rating=Rating.query.filter_by(user_id=current_user.user_id,book_id=book_id).first()
    if rating:
        rating.rating=rate
        rating.comments=comment
        db.session.commit()
    else:
        if rate:
            new_rating=Rating(user_id=current_user.user_id,book_id=book_id,rating=rate,comments=comment)
        else:
            new_rating=Rating(user_id=current_user.user_id,book_id=book_id,comments=comment)
        db.session.add(new_rating)
        db.session.commit()
    ratting=Rating.query.filter_by(book_id=book_id).all()
    t_rate=sum([r.rating for r in ratting if r.rating])
    book.book_rating=round(t_rate/len(ratting),1)
    db.session.commit()
    return redirect(url_for('book_read',book_id=book_id))

# ======PAYMENT===
@app.route('/payment/book/<book_id>')
@login_required
def payment(book_id):
    book=Book.query.filter_by(book_id=book_id).first()
    return render_template('/payment.html',book=book)


# =======User Search======
@app.route('/search')
def search():
    searchthis= request.args.get('search')
    if searchthis:
        srch='%'+'%'.join(searchthis.split())+'%'
        srch_book_name=Book.query.filter(Book.book_name.like(srch)).all()
        srch_section_name=Section.query.filter(Section.section_name.like(srch)).all()
        srch_author_name=Book.query.filter(Book.book_author.like(srch)).all()
        return render_template("user_search.html",srch_book_name=srch_book_name,srch_section_name=srch_section_name,srch_author_name=srch_author_name,search=searchthis)
    return redirect(url_for('user_dashboard'))

#******* ADMIN - CONTROLLER ******

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    date_checker_all()
    book=Book.query.all()
    rating_list=[book.book_rating for book in book]
    all_section=Section.query.all()
    section={section.section_name:len(section.book) for section in all_section}
    plt.clf()
    # All-rating Histogram
 
    plt.hist(rating_list)
    plt.ylabel("Frequency")
    plt.xlabel('Rating')
    plt.savefig("static/all-rating.png")
    plt.show()

    # Barchart book-section
    plt.clf()
    # plt.figure(figsize=(8,4))
    section_list=list(section.keys())
    book_count=list(section.values())
    plt.bar(section_list,book_count, color="lightseagreen")
    plt.ylabel("Book-count")
    plt.xlabel('Section')
    plt.savefig('static/book-count.png')
    user_books=UserBooks.query.order_by(UserBooks.userbooks_id.desc()).all()
    pending_count=UserBooks.query.filter_by(status="Requested").count()
    return render_template('admin_dashboard.html',user_books=user_books,pending_count=pending_count,book=book,section=all_section)

# *****BOOKS*****
@app.route('/admin/books')
@login_required
def admin_book():
    all_books=Book.query.all()
    return render_template('admin_books.html',all_books=all_books)

# *****SECTION*****

@app.route('/admin/sections')
@login_required
def admin_section():
    all_section=Section.query.all()
    return render_template('admin_section.html',all_section=all_section)

@app.route('/admin/<book_id>/users')
@login_required
def admin_user(book_id):
    rating=Rating.query.filter_by(book_id=book_id).all()
    book=Book.query.get(book_id)
    user_books=UserBooks.query.filter_by(book_id=book_id,status='Issued').all()
    return render_template('admin_book_user.html',user_books=user_books,book=book,rating=rating)

@app.route('/admin/<section_id>/book')
@login_required
def admin_section_book(section_id):
    section=Section.query.get(section_id)
    return render_template('admin_section_book.html',section=section)

# *****ADD Section*****
@app.route('/admin/add_section',methods=['POST','GET'])
@login_required
def admin_add_section():
    all_section=Section.query.all()
    print(all_section)
    if request.method=='POST':
        section_name=request.form.get('section_name')
        section_description=request.form.get('section_description')
        if section_name:
            curr_section=Section.query.filter_by(section_name=section_name).first()
            if curr_section:
                return render_template('admin_add_section.html',warn_msg="Section name already preset.",all_section=all_section)
            else:
                new_section=Section(section_name=section_name,section_description=section_description)
                db.session.add(new_section)
                db.session.commit()
                flash("Section Added successfully!!")
                return redirect('/admin/add_section')
        flash("Something went wrong")
    return render_template('admin_add_section.html',all_section=all_section)

# *******ADD Book********
@app.route('/admin/add_book',methods=['POST','GET'])
@login_required
def admin_add_book():
    all_section=Section.query.all()
    all_books=Book.query.all()
    if request.method=='POST':
        book_name=request.form.get('book_name')
        book_description=request.form.get('book_description')
        author_name=request.form.get('author_name')
        price=request.form.get('price')
        section_id=request.form.get('section')
        if book_name and author_name and price and section_id:
            new_book=Book(book_name=book_name,book_description=book_description,book_author=author_name,book_price=price,section_id=section_id)
            db.session.add(new_book)
            db.session.commit()
            book_cover=request.files['book_cover']
            book_pdf=request.files['book_pdf']
            if book_cover.filename:
                new_cover=f'static/book_cover/book_{new_book.book_id}.jpeg'
                book_cover.save(new_cover)
            if book_pdf.filename:
                new_pdf=f'static/book_pdfs/book_{new_book.book_id}.pdf'
                book_pdf.save(new_pdf)
            flash("Book added successfully!!")
            return redirect(url_for('admin_add_book'))
        flash("Something went wrong")
    return render_template('admin_add_book.html',all_section=all_section,all_books=all_books)
    # return render_template('admin_add_book.html')

# *******Edit-Book*****
@app.route('/admin/book/<book_id>/edit',methods=['POST','GET'])
@login_required
def admin_edit_book(book_id):
    book=Book.query.get(book_id)
    all_section=Section.query.all()
    if request.method=='POST':
        book.book_name=request.form.get('book_name')
        book.book_description=request.form.get('book_description')
        book.book_author=request.form.get('author_name')
        book.book_price=request.form.get('price')
        book.section_id=request.form.get('section')
        db.session.commit()
        book_cover=request.files['book_cover']
        book_pdf=request.files['book_pdf']
        if book_cover.filename:
            new_cover=f'static/book_cover/book_{book.book_id}.jpeg'
            book_cover.save(new_cover)
        if book_pdf.filename:
            new_pdf=f'static/book_pdfs/book_{book.book_id}.pdf'
            book_pdf.save(new_pdf)
        flash("Book updated successfully!!")
        return redirect(url_for('admin_book'))
    return render_template("admin_edit_book.html",book=book,all_section=all_section)

# *****Delete-Book*******
@app.route('/delete/book/<book_id>')
def delete_book(book_id):
    thisbook=Book.query.filter_by(book_id=book_id).first()
    book_cover=f'static/book_cover/book_{book_id}.jpeg'
    book_pdf=f'static/book_pdfs/book_{book_id}.pdf'
    if os.path.isfile(book_cover):
        os.remove(book_cover)
    if os.path.isfile(book_pdf):
        os.remove(book_pdf)

    db.session.delete(thisbook)
    db.session.commit()
    flash("Book deleted successfully!!")
    return redirect(url_for('admin_book'))

# *******Edit-section******
@app.route('/admin/section/<section_id>/edit',methods=['POST','GET'])
def admin_edit_section(section_id):
    section=Section.query.get(section_id)
    if request.method=="POST":
        section.section_name=request.form.get('section_name')
        section.section_description=request.form.get('section_description')
        db.session.commit()
        flash("Section updated successfully!!")
        return redirect(url_for('admin_section'))
    return render_template('admin_edit_section.html',section=section)

# ****Delete-Section*****
@app.route('/delete/section/<section_id>')
@login_required
def section_delete(section_id):
    thissection=Section.query.filter_by(section_id=section_id).first()
    db.session.delete(thissection)
    db.session.commit()
    flash("Section deleted successfully!!")
    return redirect(url_for('admin_section'))

# ====admin-search=====
@app.route('/admin/search')
@login_required
def admin_search():
    searchthis= request.args.get('search')
    if searchthis:
        srch='%'+'%'.join(searchthis.split())+'%'
        srch_book_name=Book.query.filter(Book.book_name.like(srch)).all()
        srch_section_name=Section.query.filter(Section.section_name.like(srch)).all()
        srch_author_name=Book.query.filter(Book.book_author.like(srch)).all()
        return render_template("admin_search.html",srch_book_name=srch_book_name,srch_section_name=srch_section_name,srch_author_name=srch_author_name,search=searchthis)
    return redirect(url_for('admin_dashboard'))

# =======logout========
@app.route('/logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))