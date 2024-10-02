from flask import Flask, make_response, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Set up the SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications for performance
app.json.compact = False  # Format JSON response in a more readable way

# Initialize the database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Pet model
class Pet(db.Model):
    __tablename__ = 'pets'  # Define the table name

    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Pet table
    name = db.Column(db.String(100), nullable=False)  # Pet's name
    species = db.Column(db.String(100), nullable=False)  # Pet's species

    def to_dict(self):  # Method to convert the Pet object to a dictionary
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species
        }

# Define the Book model
class Book(db.Model):
    __tablename__ = 'books'  # Define the table name

    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Book table
    title = db.Column(db.String(100), nullable=False)  # Book's title
    author = db.Column(db.String(100), nullable=False)  # Book's author

    def to_dict(self):  # Method to convert the Book object to a dictionary
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }

# Welcome message route
@app.route('/')
def index():
    body = {'message': 'Welcome to the pet and book directory!'}
    return make_response(body, 200)  # Return a welcome message with a 200 status

# Route to create a new pet
@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()  # Get JSON data from the request
    if not data or 'name' not in data or 'species' not in data:
        abort(400)  # Return a 400 error if required fields are missing
    
    new_pet = Pet(name=data['name'], species=data['species'])  # Create a new Pet instance
    db.session.add(new_pet)  # Add the new pet to the session
    db.session.commit()  # Commit the session to the database
    
    return jsonify(new_pet.to_dict()), 201  # Return the new pet as JSON with a 201 status

# Route to get all pets
@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()  # Query all pets from the database
    return jsonify([pet.to_dict() for pet in pets])  # Return all pets as a JSON list

# Route to get a single pet by ID
@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get_or_404(id)  # Query a pet by ID, return 404 if not found
    return jsonify(pet.to_dict())  # Return the pet as JSON

# Route to update a pet by ID
@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    pet = Pet.query.get_or_404(id)  # Query a pet by ID, return 404 if not found
    data = request.get_json()  # Get JSON data from the request

    # Update pet's name and species if provided in the request
    if 'name' in data:
        pet.name = data['name']
    if 'species' in data:
        pet.species = data['species']

    db.session.commit()  # Commit the session to save changes
    return jsonify(pet.to_dict())  # Return the updated pet as JSON

# Route to delete a pet by ID
@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get_or_404(id)  # Query a pet by ID, return 404 if not found
    db.session.delete(pet)  # Remove the pet from the session
    db.session.commit()  # Commit the session to delete the pet
    return jsonify({'message': 'Pet deleted successfully.'})  # Return a success message

# Book Directory Operations
# Route to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()  # Get JSON data from the request
    if not data or 'title' not in data or 'author' not in data:
        abort(400)  # Return a 400 error if required fields are missing
    
    new_book = Book(title=data['title'], author=data['author'])  # Create a new Book instance
    db.session.add(new_book)  # Add the new book to the session
    db.session.commit()  # Commit the session to the database
    
    return jsonify(new_book.to_dict()), 201  # Return the new book as JSON with a 201 status

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  # Query all books from the database
    return jsonify([book.to_dict() for book in books])  # Return all books as a JSON list

# Route to get a single book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)  # Query a book by ID, return 404 if not found
    return jsonify(book.to_dict())  # Return the book as JSON

# Route to update a book by ID
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)  # Query a book by ID, return 404 if not found
    data = request.get_json()  # Get JSON data from the request

    # Update book's title and author if provided in the request
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']

    db.session.commit()  # Commit the session to save changes
    return jsonify(book.to_dict())  # Return the updated book as JSON

# Route to delete a book by ID
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)  # Query a book by ID, return 404 if not found
    db.session.delete(book)  # Remove the book from the session
    db.session.commit()  # Commit the session to delete the book
    return jsonify({'message': 'Book deleted successfully.'})  # Return a success message

# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)  # Start the Flask application on port 5555 with debug mode enabled
