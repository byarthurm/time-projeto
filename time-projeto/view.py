from flask import Flask, jsonify, request, session
from main import app, db
from model import Usuarios, Cursos, CursoAluno, CursoProfessor

# -----------------------------------------------------------------------------
@app.route('/user', methods=['GET'])
def get_user():
    users = Usuarios.query.all()
    users_dic = []
    for user in users:
        user_dic = {
            'user_id': user.user_id,
            'nome': user.nome,
            'senha': user.senha,
            'email': user.email,
            'cpf': user.cpf
        }
        users_dic.append(user_dic)
    return jsonify(
        mensagem='Lista de Usuarios',
        usuarios=users_dic)


@app.route('/curso', methods=['GET'])
def get_cursos():
    cursos = Cursos.query.all()
    cursos_dic = []
    for curso in cursos:
        curso_dic = {
            'curso_id': curso.curso_id,
            'user_id': curso.user_id,
            'nomeCurso': curso.nomeCurso,
            'descricao': curso.descricao,
            'diasSemanaCurso': curso.diasSemanaCurso,
            'dataInicial': curso.dataInicial,
            'dataFinal': curso.dataFinal,
            'cargaHoraria': curso.cargaHoraria
        }
        cursos_dic.append(curso_dic)
    return jsonify(
        mensagem='Lista de cursos',
        cursos=cursos_dic)
# -----------------------------------------------------------------------------
@app.route('/user', methods=['POST'])
def post_user():
    user = request.json
    novo_user = Usuarios(
        nome=user.get('nome'),
        senha=user.get('senha'),
        email=user.get('email'),
        cpf=user.get('cpf')
    )
    db.session.add(novo_user)
    db.session.commit()
    return jsonify(
        mensagem='Usuario cadastrado com sucesso',
        user={
            'user_id': novo_user.user_id,
            'nome': novo_user.nome,
            'senha': novo_user.senha,
            'email': novo_user.email,
            'cpf': novo_user.cpf})


@app.route('/curso', methods=['POST'])
def post_curso():
    curso = request.json
    novo_curso = Cursos(
        nomeCurso=curso.get('nomeCurso'),
        descricao=curso.get('descricao'),
        diasSemanaCurso=curso.get('diasSemanaCurso'),
        dataInicial=curso.get('dataInicial'),
        dataFinal = curso.get('dataFinal'),
        cargaHoraria = curso.get('cargaHoraria'),
        user_id = curso.get('user_id')
    )
    db.session.add(novo_curso)
    db.session.commit()
    return jsonify(
        mensagem='Curso cadastrado com sucesso',
        user={
            'curso_id': novo_curso.curso_id,
            'nomeCurso': novo_curso.nomeCurso,
            'descricao': novo_curso.descricao,
            'diasSemanaCurso': novo_curso.diasSemanaCurso,
            'dataInicial': novo_curso.dataInicial,
            'dataFinal': novo_curso.dataFinal,
            'cargaHoraria': novo_curso.cargaHoraria,
            'user_id': novo_curso.user_id})

# -----------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuarios = Usuarios.query.filter_by(email=email).first()
    if usuarios and usuarios.senha == senha:
        session['user_id'] = usuarios.user_id
        return jsonify({'mensagem': 'Login com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Email ou senha inválido'})

# -----------------------------------------------------------------------------
@app.route('/protected', methods=['GET'])
def protected():
    if 'id_usuario' in session:
        return jsonify({'mensagem': 'Rota Protegida'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

# -----------------------------------------------------------------------------

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})
# -----------------------------------------------------------------------------

@app.route('/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if 'user_id' in session:
        user = Usuarios.query.get(user_id)
        if user:
            data = request.json
            user.nome = data.get('nome', user.nome)
            db.session.commit()
            return jsonify(
                mensagem='Usuario atualizada com sucesso',
                user={
                    'user_id': user.user_id,
                    'nome': user.nome,
                }
            )
        else:
            return jsonify({'mensagem': 'Usuario não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

# ------------------------------- ATE AQUI ESTA TUDO FUNCIONANDO --------------------------------------
#
#
# @app.route('/curso/<int:curso_id>', methods=['PUT'])
# def edit_curso(curso_id):
#     if 'curso_id' in session:
#         curso = Cursos.query.get(curso_id)
#         if curso:
#             data = request.json
#             curso.nomeCurso = data.get('Nome', curso.nomeCurso)
#             curso.descricao = data.get('Nome', curso.descricao)
#             curso.diasSemanaCurso = data.get('Nome', curso.diasSemanaCurso)
#             curso.dataInicial = data.get('Nome', curso.dataInicial)
#             curso.dataFinal = data.get('Nome', curso.dataFinal)
#             curso.cargaHoraria = data.get('Nome', curso.cargaHoraria)
#             db.session.commit()
#             return jsonify(
#                 mensagem='Curso atualizada com sucesso',
#                 curso={
#                     'curso_id': curso.user_id,
#                     'nomeCurso': curso.nomeCurso,
#                     'descricao': curso.descricao,
#                     'diasSemanaCurso': curso.diasSemanaCurso,
#                     'dataInicial': curso.dataInicial,
#                     'dataFinal': curso.dataFinal,
#                     'cargaHoraria': curso.cargaHoraria,
#                 }
#             )
#         else:
#             return jsonify({'mensagem': 'Curso não encontrado'})
#     else:
#         return jsonify({'mensagem': 'Requer Autorização'})
# # -----------------------------------------------------------------------------
#
# @app.route('/user/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     if 'user_id' in session:
#         user = Usuarios.query.get(user_id)
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return jsonify({'mensagem': 'Usuario excluído com sucesso'})
#         else:
#             return jsonify({'mensagem': 'Usuario não encontrado'})
#     else:
#         return jsonify({'mensagem': 'Requer Autorização'})
#
#
# @app.route('/curso/<int:curso_id>', methods=['DELETE'])
# def delete_curso(curso_id):
#     if 'curso_id' in session:
#         curso = Cursos.query.get(curso_id)
#         if curso:
#             db.session.delete(curso)
#             db.session.commit()
#             return jsonify({'mensagem': 'Curso excluído com sucesso'})
#         else:
#             return jsonify({'mensagem': 'Curso não encontrado'})
#     else:
#         return jsonify({'mensagem': 'Requer Autorização'})