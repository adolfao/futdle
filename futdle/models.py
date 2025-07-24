from futdle import db

class Time(db.Model):
    __tablename__ = 'times'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    cores = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False) 
    ano_fundacao = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Time {self.nome}>'
