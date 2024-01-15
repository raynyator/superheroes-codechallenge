from app import app, db
from models import Power, Hero, HeroPower
from flask import current_app as APP
from random import choice, randint

with app.app_context():
    db.create_all()  

    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]
    for data in powers_data:
        power = Power(**data)
        db.session.add(power)

    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]
    for data in heroes_data:
        hero = Hero(**data)
        db.session.add(hero)

    db.session.commit()  

    strengths = ["Strong", "Weak", "Average"]
    for hero in Hero.query.all():
        for _ in range(randint(1, 3)):  
            power = Power.query.order_by(db.func.random()).first()  
            hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
            db.session.add(hero_power)

    db.session.commit()

print("🦸‍♀️ Done seeding!")
