from flask import Flask


about_me = {
   "name": "Евгений",
   "surname": "Юрченко",
   "email": "eyurchenko@specialist.ru"
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
              "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },
]



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
    for i in range(len(quotes)):
        if quotes[i]['id'] == quote_id:
            return quotes[i]
    return f'Quote with id={quote_id} no found', 404

@app.route('/count')
def get_quotes_count():
    quotes_count = {'count':len(quotes)}
    return quotes_count


if __name__ == '__main__':
   app.run(debug=True)
