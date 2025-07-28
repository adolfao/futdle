from futdle import db
import unicodedata

class Time(db.Model):
  __tablename__ = 'times'

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), unique=True, nullable=False)
  cores = db.Column(db.String(50), nullable=False)
  estado = db.Column(db.String(2), nullable=False) 
  ano_fundacao = db.Column(db.Integer, nullable=False)

  def nome_arquivo(self):
    nome_normalizado = unicodedata.normalize('NFKD', self.nome)
    nome_normalizado = ''.join([c for c in nome_normalizado if not unicodedata.combining(c)])
    nome_normalizado = nome_normalizado.lower().replace(' ', '').replace('ç', 'c')
    return nome_normalizado

  def __repr__(self):
    return f'<Time {self.nome}>'
