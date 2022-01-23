import random

from flask import Flask, url_for, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from calc_rating import ELO


app = Flask(__name__)
client = app.test_client()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waifu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
wife = 40
    
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
    change1 = db.Column(db.Text)
    change2 = db.Column(db.Text)
    
    def __repr__(self):
        return 'Chalange %r' % self.id

# як варіант в адресі буде шифруватися інформація про вайфу 

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        ch = len(Chalange.query.all()) + 1
        id1 = random.randint(1,wife)
        id2 = id1
        while(id1 == id2):
            id2 = random.randint(1,wife)        
        chalange = Chalange(id=ch, waifu1=id1, waifu2=id2)
        
        try:
            db.session.add(chalange)
            db.session.commit()
            return redirect(f"/chelenger-{ch}")
        except:
            return "При додаванні челенджу сталася якась бебра" 
        
        
    else:
        list_waifu = Waifu.query.order_by(Waifu.raiting.desc()).all()
        lst_waifu = []
        for i in range(len(list_waifu)):
            lst_waifu.append({"num":i, "waifu":list_waifu[i]})
        return render_template("index_waifu.html", list_waifu=lst_waifu)

# @app.route('/test/t')
# def test():
    # return render_template("test.html")
        
@app.route('/chelenger-<int:id>', methods=["POST", "GET"])
def chelenger(id):
    chelenge = Chalange.query.get(id)
    if chelenge.result != None:
        return redirect(f"/result-{id}")
    waifu1 = Waifu.query.get(chelenge.waifu1)
    waifu2 = Waifu.query.get(chelenge.waifu2)     

    if request.method == "POST":
        change1 = 1
        change2 = -1
        my_id = request.form.get("my_id")
        if my_id == "На головну":
            list_waifu = Waifu.query.order_by(Waifu.raiting.desc()).all()
            return render_template("index_waifu.html", list_waifu=list_waifu)            
        R = ELO(waifu1.raiting, waifu2.raiting, my_id)
        waifu1.raiting -= R[0]
        waifu2.raiting -= R[1]        
        chelenge.result = my_id
        if R[0] > 0:
            chelenge.change1 = f'+{R[0]}'
        else:
            chelenge.change1 = f'{R[0]}'
        if R[1] > 0:
            chelenge.change2 = f'+{R[1]}'
        else:
            chelenge.change2 = f'{R[1]}'        
        try:
        #if True:
            db.session.add(chelenge)
            db.session.commit()
        except:
        #else:
            return "При редагуванні БД сталася якась бебра" 
        return redirect(f'/result-{id}')
    else:
        return render_template("chalanger.html", waifu1=waifu1, waifu2=waifu2)

@app.route('/result-<int:id>', methods=["POST", "GET"])
def result(id):
    if request.method == "POST":
        my_id = request.form.get("my_id")
        if my_id == 'Далі':
            ch = len(Chalange.query.all()) + 1
            id1 = random.randint(1,wife)
            id2 = id1
            while(id1 == id2):
                id2 = random.randint(1,wife)        
            chalange = Chalange(id=ch, waifu1=id1, waifu2=id2)
            try:
                db.session.add(chalange)
                db.session.commit()
                return redirect(f'/chelenger-{ch}')
            except:
                return "При додаванні челенджу сталася якась бебра" 

    else:
        chelenge = Chalange.query.get(id)
        waifu1 = Waifu.query.get(chelenge.waifu1)
        waifu2 = Waifu.query.get(chelenge.waifu2) 
        return render_template("result.html", waifu1=waifu1, waifu2=waifu2, chelenge=chelenge)


@app.route('/<int:id>', methods=["POST", "GET"])
def print_waifu(id):
    waifu = Waifu.query.get(id)
    if request.method == "POST":
        return redirect(f'/{id+1}')
    else:
        return render_template("waifu.html", waifu=waifu)


if __name__ == "__main__":
    app.run(debug=True)