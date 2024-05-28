from main import db

class Usuarios(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    senha = db.Column(db.String(254))
    funcao = db.Column(db.Integer)
    email = db.Column(db.String(100))
    cpf = db.Column(db.Integer)

class Cursos(db.Model):
    curso_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)
    nomeCurso = db.Column(db.String(100))
    descricao = db.Column(db.String(254))
    cargaHoraria = db.Column(db.Integer)

class CursoProfessor(db.Model):
    prof_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curso_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)

class CursoAluno(db.Model):
    curso_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)
    prof_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, foreign_key=True, autoincrement=True)

#------------------------------------------------------------------------------------#
class Salas(db.Model):
    sala_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numeroDaSala = db.Column(db.Integer)
    tipo = db.Column(db.Text)
    descricao = db.Column(db.Text)

class Turmas(db.Model):
    turma_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeDaTurma = db.Column(db.String(100))
    inicioAulas = db.Column(db.Date)
    finalAulas = db.Column(db.Date)
    diasDaSemana = db.Column(db.Text)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.curso_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.user_id'))
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.sala_id'))
    curso = db.relationship('Cursos', backref=db.backref('turmas'))
    usuario = db.relationship('Usuarios', backref=db.backref('turmas'))
    sala = db.relationship('Salas', backref=db.backref('turmas'))

class Feriados(db.Model):
    feriado_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datas = db.Column(db.Date)
    nomes = db.Column(db.Text)

class NLetivos(db.Model):
    nLetivo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datas = db.Column(db.Date)

class PossivelPonte(db.Model):
    ponte_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datas = db.Column(db.Date)

