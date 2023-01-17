from flask import Flask, jsonify, abort, request, Response, render_template
from library import Library

# ==============================================================================
# #Create the flask server object
# ==============================================================================
app = Flask(__name__)

# ==============================================================================
# Create the library object with 3 books
# ==============================================================================
lib = Library()
lib.addBook("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 12301)
lib.addBook("Da Vinci Code", "D. Brown", 11244)
lib.addBook("Twenty Thousand Leagues Under The Sea", "J. Verne", 23900)


# ==============================================================================
# Handle abort message
# ==============================================================================


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# ==============================================================================
# Routes definition to expose a REST API
# ==============================================================================

@app.route('/')
#@app.route('/library/', methods=['GET'])
def all_book():
    response = lib.serialize()
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route('/library/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    books = lib.getBook(isbn)
    if books:
        print(books[0].serialize())
        response = jsonify(books[0].serialize())
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.status = 201
        return response
    else:
        abort(404, description="No book with ISBN ")


@app.route('/library/', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':
        form = request.form
        if 'isbn' in form and 'title' in form and 'author' in form:
            lib.addBook(form['title'], form['author'], form['isbn'])
            response = Response("The book was added successful")
            response.status = 201
            response.location = "library" + str(form['isbn'])
            return response
        else:
            abort(400, description="Error book information ")
    else:
        return'''
        <form action="/library" method="POST">
            ISBN : <input type="text" name="isbn"> <br/>
            Titre : <input type="text" name="title"> <br/>
            Auteur : <input type="text" name="author"> <br/>
            <input type="submit" value="Envoyer"> <br/>
            </form>
        '''


@app.route('/library/<int:isbn>/<string:author>/<string:title>', methods=['PUT'])
def edit_book(isbn, author, title):
    books = lib.getBook(isbn)
    if books:
        books[0].setTitle(title)
        books[0].setAuthor(author)
        books[0].setIbsn(isbn)
        response = jsonify(books[0].serialize())
        response.status = 200
        return response
    else:
        abort(404, description="No book with ISBN ")


@app.route('/library/<int:isbn>', methods=['DELETE'])
def del_book_by_isbn(isbn):
    books = lib.getBook(isbn)
    if books:
        lib.delBook(isbn)
        print(f"Deleted : {books[0].serialize()}")
        response = jsonify(books[0].serialize())
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        response.status = 200
        return response
    else:
        abort(404, description="No book with ISBN ")


@app.route('/all')
def getHtmlBooks():
    return render_template('library.html', books=lib.allBooks())


@app.route('/second')
def second():
    return "Bienvenu sur cette nouvelle page!"


if __name__ == '__main__':
    app.run()
