from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True # use false for production
db = SQLAlchemy(app)


class Aws(db.Model):
    name = Column(String(100), unique=True, nullable=False, primary_key=True)
    description = Column(String(100), nullable=False)

    # def __init__(self,name,description):
    #     self.name = name
    #     self.description = description
    
    def __repr__(self):
        return "<Name: {}, Description: {}>".format(self.name, self.description)

    def fromJSON(self, json_rec):
        if 'name' in json_rec:
            self.name = json_rec['name']
            self.description = json_rec['description']

class Profiles(db.Model):
    id = Column(Integer, primary_key=True, autoincrement="auto")
    fullname = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    password = Column(String(100))

    def __init__(self, fullname, username, email, phone, password):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password

def load_file_into_table(target, connection, **kw):
    import json

    with open('list.json') as fp:
        full_data = fp.read()
        fp.close()
        json_data = json.loads(full_data)
    print("Found {0} records".format(len(json_data)))
    for rec in json_data:
        rec_details = rec['field']
        p = Aws()
        p.fromJSON(rec_details)
        db.session.add(p)
    db.session.commit()


listen(Aws.__table__, 'after_create', load_file_into_table)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


@app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)

# When the Flask app is shutting down, close the database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()



@app.route("/", methods=['GET'])
def get_list():
    records = Aws.query.order_by(Aws.name.asc())
    names = Aws.query.order_by(Aws.name.asc()).first()
    return render_template('index.html', aws=records, names=names)

@app.route("/<a_name>", methods=['GET'])
def change_list(a_name):
    records = Aws.query.order_by(Aws.name.asc())
    names = Aws.query.get(a_name)
    return render_template('index.html', aws=records, names=names)

@app.route('/data', methods=['POST'])
def make_list():
    if request.content_type  == 'application/json':
        request_text = request.json
        if 'name' in request_text:
            print(request_text)
            p = Aws(request_text['name'], request_text['description'])
        else:
            response = jsonify({'message': 'Invalid fields specified'})
            response.status_code = 400
            return response

        db.session.add(p)
        db.session.commit()
        response = jsonify({
            'name': p.name,
            'description': p.description,
        })
        response.status_code = 201
        return response
    else:
        response = jsonify({'message': 'Invalid format of data in the request'})
        response.status_code = 400
        return response

@app.route("/subscription", methods=['GET'])
def get_subscriptions():
    return render_template('subscriptions.html')

@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe():
    return render_template('subscribe.html')

@app.route("/profile", methods=['GET'])
def profile():
    return render_template('subscribe.html')

@app.route("/registration", methods=['GET', 'POST'])
def registration():

    if request.form:
        try:
            person = Profiles(fullname=request.form.get("name"),username = request.form.get("uname"), email = request.form.get("email"), phone = request.form.get("num"), password = request.form.get("pass"))
            db.session.add(person)
            db.session.commit()
            return redirect("/", person=person)
        except Exception as e:
            print("Failed to add person")
            print(e)


    return render_template('registration.html')

