from main import db

class Usuarios(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    senha = db.Column(db.String(254))
    email = db.Column(db.String(100))
    cpf = db.Column(db.Integer)

class Cursos(db.Model):
    curso_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)
    nomeCurso = db.Column(db.String(100))
    descricao = db.Column(db.String(254))
    diasSemanaCurso = db.Column(db.String(100))
    dataInicial = db.Column(db.Date)
    dataFinal = db.Column(db.Date)
    cargaHoraria = db.Column(db.Integer)

class CursoProfessor(db.Model):
    prof_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curso_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)

class CursoAluno(db.Model):
    curso_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)
    prof_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)