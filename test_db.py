from app import create_app, db
import os

app = create_app()

with app.app_context():
    if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')):
        os.mkdir('instance')
    db.create_all()
    print("Database created successfully.")
