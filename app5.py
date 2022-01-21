from flask import Flask, url_for, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
client = app.test_client()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waifu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
wife = 40

def encoder_link():
    answer = ""
    for i in range(9):
        X = random.randint(1,wife)
        if i == 0:
            answer += f'/{X}'
        else:
             answer += f'-{X}'
    return answer
    
class Waifu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300)) 
    anime = db.Column(db.String(300))
    link = db.Column(db.Text)
    raiting = db.Column(db.Integer, default=1200)
    
    def __repr__(self):
        return 'Waifu %r' % self.id

# як варіант в адресі буде шифруватися інформація про вайфу


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return redirect(encoder_link())
    else:
        list_waifu = Waifu.query.order_by(Waifu.raiting.desc()).all()
        return render_template("index_waifu.html", list_waifu=list_waifu)
        
@app.route('/<int:A>-<int:B>-<int:id1>-<int:C>-<int:D>-<int:id2>-<int:E>-<int:F>-<int:G>', methods=["POST", "GET"])
def chelenger(A,B,id1,C,D,id2,E,F,G):
    waifu1 = Waifu.query.get(id1)
    waifu2 = Waifu.query.get(id2)     

    if request.method == "POST":
        my_id = request.form.get("my_id")
        if my_id == 'Обрати першу вайфу':
            waifu1.raiting += 1
            waifu2.raiting -= 1
        elif my_id == 'Обрати другу вайфу':
            waifu1.raiting -= 1
            waifu2.raiting += 1
        else:
            waifu1.raiting -= 1
            waifu2.raiting -= 1   
        # if True:
        try:
            db.session.commit()
            return redirect(encoder_link())
        except:
            return "При редагуванні БД сталася якась бебра"
    else:
        return render_template("chalanger.html", waifu1=waifu1, waifu2=waifu2)

@app.route('/test')
def result():
    waifu1 = Waifu.query.get(1)
    waifu2 = Waifu.query.get(2)
    change1 = '+9'
    change2 = '-8'
    return render_template("result.html", waifu1=waifu1, waifu2=waifu2, change1=change1, change2=change2,)


@app.route('/<int:id>', methods=["POST", "GET"])
def print_waifu(id):
    waifu = Waifu.query.get(id)
    if request.method == "POST":
        return redirect(f'/{id+1}')
    else:
        return render_template("waifu.html", waifu=waifu)


if __name__ == "__main__":
    app.run(debug=True)