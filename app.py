from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\PYTHON\\flask_API\\clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    Alina = Client(client_first_name='Alina',
                   client_second_name='Bobobva',
                   client_phone_number=80996852525,
                   client_age=35,
                   client_home_city='Lviv')

    Roman = Client(client_first_name='Roman',
                   client_second_name='Popov',
                   client_phone_number=80996856987,
                   client_age=30,
                   client_home_city='Lviv')

    Yulia = Client(client_first_name='Yulia',
                   client_second_name='Venuk',
                   client_phone_number=80979078866,
                   client_age=22,
                   client_home_city='Lviv')

    db.session.add(Alina)
    db.session.add(Roman)
    db.session.add(Yulia)

    test_agent = Agent(first_name='William',
                       last_name='Herschel',
                       email='test@test.com',
                       password='P@ssw0rd')

    db.session.add(test_agent)
    db.session.commit()
    print('Database seeded!')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World! '


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello Bogdan')


@app.route('/clients', methods=['GET'])
def clients():
    clients_list = Client.query.all()
    result = client_schema.dump(clients_list, many=True)
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = Agent.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        agent = Agent(first_name=first_name, last_name=last_name, email=email,
                      password=password)
        db.session.add(agent)
        db.session.commit()
        return jsonify(message="Agent created successfully."), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = Agent.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/client_details/<int:client_id>', methods=["GET"])
def client_details(client_id: int):
    client = Client.query.filter_by(client_id=client_id).first()
    if client:
        result = client_schema.dump(client)
        return jsonify(result)
    else:
        return jsonify(message="That client does not exist"), 404


@app.route('/add_client', methods=['POST'])
@jwt_required
def add_client():
    client_phone_number = request.form['client_phone_number']
    test = Client.query.filter_by(
        client_phone_number=client_phone_number).first()
    if test:
        return jsonify(
            "There is already a client by that client_phone_number"), 409
    else:
        client_first_name = request.form['client_first_name']
        client_second_name = request.form['client_second_name']
        client_phone_number = int(request.form['client_phone_number'])
        client_age = int(request.form['client_age'])
        client_home_city = request.form['client_home_city']

        new_client = Client(client_first_name=client_first_name,
                            client_second_name=client_second_name,
                            client_phone_number=client_phone_number,
                            client_age=client_age,
                            client_home_city=client_home_city)

        db.session.add(new_client)
        db.session.commit()
        return jsonify(message="You added a client"), 201


@app.route('/update_client', methods=['PUT'])
@jwt_required
def update_client():
    client_id = int(request.form['client_id'])
    client = Client.query.filter_by(client_id=client_id).first()
    if client:
        client.client_first_name = request.form['client_first_name']
        client.client_second_name = request.form['client_second_name']
        client.client_phone_number = int(request.form['client_phone_number'])
        client.client_age = int(request.form['client_age'])
        client.client_home_city = request.form['client_home_city']
        db.session.commit()
        return jsonify(message="You updated a client"), 202
    else:
        return jsonify(message="That client does not exist"), 404


@app.route('/remove_client/<int:client_id>', methods=['DELETE'])
@jwt_required
def remove_client(client_id: int):
    client = Client.query.filter_by(client_id=client_id).first()
    if client:
        db.session.delete(client)
        db.session.commit()
        return jsonify(message="You deleted a client"), 202
    else:
        return jsonify(message="That client does not exist"), 404


# database models
class Agent(db.Model):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Client(db.Model):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    client_first_name = Column(String)
    client_second_name = Column(String)
    client_phone_number = Column(Integer)
    client_age = Column(Integer)
    client_home_city = Column(String)


class AgentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class ClientSchema(ma.Schema):
    class Meta:
        fields = ('client_id', 'client_first_name', 'client_second_name',
                  'client_phone_number', 'client_age', 'client_home_city')


agent_schema = AgentSchema()
agents_schema = AgentSchema()

client_schema = ClientSchema()
clients_schema = ClientSchema()

if __name__ == '__main__':
    app.run()
