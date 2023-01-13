from flask import jsonify


class Book:
    def __init__(self, title, author, isbn):
        self.__title = title
        self.__author = author
        self.__isbn = isbn

    def getTitle(self):
        return self.__title

    def getISBN(self):
        return int(self.__isbn)

    def getAuthor(self):
        return self.__author

    def setTitle(self, title):
        self.__title = title

    def setIbsn(self, isbn):
        self.__isbn = isbn

    def setAuthor(self, author):
        self.__author = author

    def serialize(self):
        return {"title": self.__title, "author": self.__author, "isbn": self.__isbn}


class Library:
    def __init__(self):
        self.__books = []

    def addBook(self, title, author, isbn):
        self.__books.append(Book(title, author, isbn))

    def editBook(self, title, author, isbn):
        result = list(filter(lambda l: l.getISBN() == isbn, self.__books))

    def getBook(self, i):
        result = list(filter(lambda l: l.getISBN() == i, self.__books))
        if result:
            return result
        else:
            return False

    def allBooks(self):
        return self.__books

    def delBook(self, i):
        self.__books = list(filter(lambda l: not l.getISBN() == i, self.__books))

    def serialize(self):
        return jsonify(books=[book.serialize() for book in self.__books])
