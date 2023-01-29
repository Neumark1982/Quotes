from flask import Flask, request
import random
import sqlite3
from flask import g
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: в проекте не подключены миграции, отсутствует папка migrations

class QuoteModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   author = db.Column(db.String(32), unique=False)
   text = db.Column(db.String(255), unique=False)
   rating = db.Column(db.Integer)
   
   def __init__(self, author, text, rating):
       self.author = author
       self.text  = text
       self.rating = rating
       

   def to_dict(self):
       return {'id': self.id, 'author': self.author, 'text': self.text, 'rating': self.rating}

# Сериализация:
# Объект -> dict -> JSON

@app.route("/quotes", methods=['GET'])
def get_quotes():
    quotes = QuoteModel.query.all()
    quotes_dict = [quote.to_dict() for quote in quotes]
    return quotes_dict

@app.route("/quotes/<int:quote_id>", methods=['GET'])
def get_quote_by_id(quote_id):
   # TODO: тут вы выполняете два запроса к БД, вместо одного. Так делать не стоит!
   # Сначала получите объект, а потом с ним работайте
    if QuoteModel.query.get(quote_id) is None:
        return f"Quote with id={quote_id} not found", 404
    quote_id_result = QuoteModel.query.get(quote_id)
    return quote_id_result.to_dict(), 200
   
@app.route("/quotes/random", methods=["GET"])
def random_quote():
    qoutes = QuoteModel.query.all()
    qoutes_dict = [quote.to_dict() for quote in qoutes]
    return random.choice(qoutes_dict)


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    if not 'rating' in new_quote:
        new_quote['rating'] = random.randint(1, 5)
    # TODO: если рейтинг не задая явно(не получен с клиента), устанавливает его рандомно - плохая идея.
    # Правильнее задать фиксированное значение по умолчанию и лучше это сделать на уровне самого класса QuoteModel в конструкторе
    new_db_quote = QuoteModel(new_quote['author'], new_quote['text'], new_quote['rating'])
    db.session.add(new_db_quote)
    db.session.commit()
    return new_db_quote.to_dict(), 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    # TODO: тут таже проблема - лишние запросы к БД.
    if QuoteModel.query.get(quote_id) is None:
        return f"Quote with id={quote_id} not found", 404
    planned_changed_data = request.json
    quote_id_result = QuoteModel.query.get(quote_id)
    if 'text' in planned_changed_data:
        quote_id_result.text = planned_changed_data['text']
    if 'author' in planned_changed_data:
            quote_id_result.author = planned_changed_data['author']
    if 'rating' in planned_changed_data:
        quote_id_result.rating = planned_changed_data['rating']
    db.session.commit()
    return quote_id_result.to_dict(), 201

@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    # TODO: ну и тут
    if QuoteModel.query.get(quote_id) is None:
        return f"Quote with id={quote_id} not found", 404
    db.session.delete(QuoteModel.query.get(quote_id))
    db.session.commit()
    return f'Quote with id={quote_id} was deleted', 200

@app.route("/quotes/rating", methods = ['GET'])
def rating():
    rating_diapazon_results = []
    args_diap = request.args.to_dict()
    args_diap['minrating'] = int(args_diap['minrating'])
    args_diap['maxrating'] = int(args_diap['maxrating']) 
    # TODO: делать фильтрацию/выборку на уровне питона - неверно, фильтрацией должна заниматься БД
    for quote in QuoteModel.query.all():
            if args_diap['minrating'] <= quote.rating <= args_diap['maxrating']:
                rating_diapazon_results.append(quote.text)
    # TODO: нужно возвращать не только текст цитат, а цитаты полностью (с id, автором и т.д.)
    return rating_diapazon_results, 200

@app.route("/qoutes/filter", methods = ['GET'])
def filter():
    filtered_results = []
    args_filter = request.args.to_dict()
    if 'rating' in args_filter:
        args_filter['rating'] = int(args_filter['rating'])
    for quote in QuoteModel.query.all():
        count = 0        
        if quote.rating == args_filter.get('rating'):
            count +=1
        if quote.author == args_filter.get('author'):
            count +=1
        if count == len(args_filter):
                filtered_results.append(quote.text)
    return filtered_results, 200

if __name__ == "__main__":
    app.run(debug=True)
