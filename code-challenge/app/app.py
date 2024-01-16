from os import SEEK_DATA
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import HeroPower, Power, db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)



@app.route('/')
def home():
    return 'My heroes app'

@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    heroes = Hero.query.all()
    heroes_data = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': hero_power.power.id, 'name': hero_power.power.name, 'description': hero_power.power.description, 'strength': hero_power.strength} for hero_power in hero.powers]
        } for hero in heroes
    ]
    response = make_response(jsonify(heroes_data), 200)
    return response

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)

    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        response = make_response(jsonify(hero_data), 200)
    else:
        response = make_response(jsonify({'error': 'Hero not found'}), 404)

    return response

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    response = make_response(jsonify(powers_data), 200)
    return response

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)

    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        response = make_response(jsonify(power_data), 200)
    else:
        response = make_response(jsonify({'error': 'Power not found'}), 404)

    return response

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)

    if power:
        data = request.get_json()
        new_description = data.get('description')

        if new_description and len(new_description) >= 20:
            power.description = new_description
            db.session.commit()

            updated_power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }

            response = make_response(jsonify(updated_power_data), 200)
        else:
            response = make_response(jsonify({'errors': ['Validation error: Description must be present and at least 20 characters long']}), 400)
    else:
        response = make_response(jsonify({'error': 'Power not found'}), 404)

    return response

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if strength not in ['Strong', 'Weak', 'Average']:
        response = make_response(jsonify({'errors': ['Validation error: Strength must be one of the following values: \'Strong\', \'Weak\', \'Average']}), 400)
    else:
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero and power:
            new_hero_power = HeroPower(strength=strength, power=power, hero=hero)
            db.session.add(new_hero_power)
            db.session.commit()

            hero_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
            }

            response = make_response(jsonify(hero_data), 200)
        else:
            response = make_response(jsonify({'errors': ['Validation error: Hero or Power not found']}), 400)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
