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
@app.route('/library/', methods=['GET'])
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


@app.route('/library/', methods=['POST'])
def add_book():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        if 'isbn' in json and 'title' in json and 'author' in json:
            lib.addBook(json['title'], json['author'], json['isbn'])
            response = Response("The book was added successful")
            response.status = 201
            return response
        else:
            abort(400, description="Error book information ")


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


if __name__ == '__main__':
    app.run()
