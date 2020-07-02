from __init__ import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cta.db'
db = SQLAlchemy(app)


class shareSession(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    session = db.Column(db.Text,nullable=True)

    def __repr__(self):
        return 'Session ' + str(self.id)
