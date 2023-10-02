# from flask import Flask, jsonify
# from pymongo import MongoClient
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Connect to the MongoDB database
# client = MongoClient('mongodb+srv://Firedrakesin:Garubb66@cluster0.iodwiy3.mongodb.net/')
# db = client['Book-Store']
# collection = db['Book_data']

# @app.route("/get_books")
# def get_books():
#     # Use the collection object, not mongo.db
#     books = collection.find()
    
#     book_list = []
#     for book in books:
#         book_list.append({
#             'title': book['title']
#         })
    
#     return jsonify({'books': book_list})

# if __name__ == "__main__":
#     app.run(debug=True, port=5001)
