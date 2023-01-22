from flask import Flask
from random import choice
from flask import request

about_me = {
   "name": "Евгений",
   "surname": "Юрченко",
   "email": "eyurchenko@specialist.ru"
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
       "rating": 4
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
       "rating": 2
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
       "rating": 3
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так.",
       "rating": 5
   },
]

# TODO: добавьте .gitignore в проект

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello_world():
   return 'Hello, World!'

@app.route("/about")
def about():
   return about_me

@app.route("/quotes")
def get_quotes():
    return quotes

@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    for qoute in quotes:
        if qoute['id'] == quote_id:
            return qoute
    return f'Quote with id={quote_id} no found', 404

@app.route('/quotes/count', methods = ['GET'])
def get_quotes_count():
    return {'count':len(quotes)}

@app.route('/quotes/random')
def random_quoute():
    return choice(quotes)

@app.route('/quotes', methods = ['POST'])
def create_quote():
    new_quote = request.json
    if not 'rating' in new_quote or new_quote['rating'] > 5:
        new_quote['rating'] = 1
    last_quote = quotes[-1]
    new_id = last_quote['id'] + 1
    new_quote['id'] = new_id
    quotes.append(new_quote)
    return new_quote, 201

@app.route("/quotes/<int:quote_id>", methods = ['PUT'])
def edit_quote(quote_id):
    new_quote = request.json
    if new_quote['rating'] > 5:
        del new_quote['rating']
    for quote in quotes:
        if quote['id'] == quote_id:
            for key, value in quote.items():
                # TODO: вместо "== None" в питоне рекомендуется писать "is None"
                #  в данной ситуации лучше так:
                #  if new_quote.get(key):
                if not new_quote.get(key) == None:
                    quote[key] = new_quote.get(key)
            return quote, 201
    return f'Quote with id={quote_id} no found', 404
    
@app.route("/quotes/<int:quote_id>", methods = ['DELETE'])
def delete_quote(quote_id):
    # TODO: ненужно перебирать элементы списка по индексам, в питоне есть инструмент для прямого перебора элементов
    for i in range(len(quotes)):
        if quotes[i]['id'] == quote_id:
            del quotes[i]
            return f'Quote with id={quote_id} was deleted', 200
    return f'Quote with id={quote_id} no found', 404

@app.route("/qoutes/filter", methods = ['GET'])
def filter():
    filtered_results = []
    args_filter = request.args.to_dict()
    if 'rating' in args_filter:
        args_filter['rating'] = int(args_filter['rating'])
    for quote in quotes:
        count = 0
        for key, value in quote.items():
            if quote[key] == args_filter.get(key):
                count +=1
        # TODO: убирайте отладочные print'ы из итогового кода
        print(count)
        if count == len(args_filter):
            filtered_results.append(quote['text'])
    return filtered_results, 200

@app.route("/quotes/rating", methods = ['GET'])
def rating():
    rating_diapazon_results = []
    args_diap = request.args.to_dict()
    args_diap['minrating'] = int(args_diap['minrating'])
    args_diap['maxrating'] = int(args_diap['maxrating']) 
    for quote in quotes:
            if args_diap['minrating'] <= quote['rating'] <= args_diap['maxrating']:
                rating_diapazon_results.append(quote['text'])
    return rating_diapazon_results, 200


if __name__ == '__main__':
   app.run(debug=True)