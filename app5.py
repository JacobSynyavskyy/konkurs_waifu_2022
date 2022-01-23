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

class Chalange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waifu1 = db.Column(db.Integer)
    waifu2 = db.Column(db.Integer)   
    result = db.Column(db.Text)
    
    def __repr__(self):
        return 'Chalange %r' % self.id

# як варіант в адресі буде шифруватися інформація про вайфу 

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        
        return redirect("/chelenger")
    else:
        list_waifu = Waifu.query.order_by(Waifu.raiting.desc()).all()
        lst_waifu = []
        for i in range(len(list_waifu)):
            lst_waifu.append({"num":i, "waifu":list_waifu[i]})
        return render_template("index_waifu.html", list_waifu=lst_waifu)
        
@app.route('/chelenger', methods=["POST", "GET"])
def chelenger():

    id1 = random.randint(1,wife)
    id2 = id1
    while(id1 == id2):
        id2 = random.randint(1,wife)

    waifu1 = Waifu.query.get(id1)
    waifu2 = Waifu.query.get(id2)     

    if request.method == "POST":
        change1 = 1
        change2 = -1
        my_id = request.form.get("my_id")
        if my_id == "На головну":
            list_waifu = Waifu.query.order_by(Waifu.raiting.desc()).all()
            return render_template("index_waifu.html", list_waifu=list_waifu)            
        elif my_id == 'Обрати першу вайфу':
            waifu1.raiting += 1
            waifu2.raiting -= 1
            change1 = '+1'
            change2 = '-1'
        elif my_id == 'Обрати другу вайфу':
            waifu1.raiting -= 1
            waifu2.raiting += 1
            change1 = '-1'
            change2 = '+1'
        elif my_id == 'Не знаю жодної':
            waifu1.raiting -= 1
            waifu2.raiting -= 1
            change1 = '-1'
            change2 = '-1'
        elif my_id == 'Далі':
            return redirect('/chelenger')
        try:
            db.session.commit()
            return render_template("result.html", waifu1=waifu1, waifu2=waifu2, change1=change1, change2=change2)
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
    return render_template("result.html", waifu1=waifu1, waifu2=waifu2, change1=change1, change2=change2)


@app.route('/<int:id>', methods=["POST", "GET"])
def print_waifu(id):
    waifu = Waifu.query.get(id)
    if request.method == "POST":
        return redirect(f'/{id+1}')
    else:
        return render_template("waifu.html", waifu=waifu)


if __name__ == "__main__":
    app.run(debug=True)