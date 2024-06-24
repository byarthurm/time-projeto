from flask import jsonify, request, session, redirect
from main import app, db
from model import Usuarios, Cursos, Salas, Turmas, Feriados
from sqlalchemy.orm import join
from datetime import datetime


# -----------------------------------------------------------------------------
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuarios.query.all()
    usuarios_list = []
    for usuario in usuarios:
        usuario_dict = {
            'user_id': usuario.user_id,
            'nome': usuario.nome,
            'funcao': usuario.funcao,
            'email': usuario.email,
            'cpf': usuario.cpf,
            'img': usuario.img
        }
        usuarios_list.append(usuario_dict)
    return jsonify(
        mensagem='Lista de Usuários',
        usuarios=usuarios_list)


@app.route('/curso', methods=['GET', 'OPTIONS'])
def get_cursos():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response

    cursos = Cursos.query.all()
    cursos_list = []
    for curso in cursos:
        curso_dict = {
            'curso_id': curso.curso_id,
            'user_id': curso.user_id,
            'nomeCurso': curso.nomeCurso,
            'descricao': curso.descricao,
            'cargaHoraria': curso.cargaHoraria
        }
        cursos_list.append(curso_dict)
    return jsonify(
        mensagem='Lista de cursos',
        cursos=cursos_list)
# -----------------------------------------------------------------------------
@app.route('/usuarios', methods=['POST'])
def post_usuario():
    data = request.json
    novo_usuario = Usuarios(
        nome=data.get('nome'),
        senha=data.get('senha'),  # Considerando que agora temos senha
        funcao=data.get('funcao'),
        email=data.get('email'),
        cpf=data.get('cpf'),
        img=data.get('img')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify(
        mensagem='Usuário cadastrado com sucesso',
        usuario={
            'user_id': novo_usuario.user_id,
            'nome': novo_usuario.nome,
            'funcao': novo_usuario.funcao,
            'email': novo_usuario.email,
            'cpf': novo_usuario.cpf,
            'img': novo_usuario.cpf})


@app.route('/cursos', methods=['POST'])
def post_curso():
    data = request.json
    novo_curso = Cursos(
        nomeCurso=data.get('nomeCurso'),
        descricao=data.get('descricao'),
        cargaHoraria=data.get('cargaHoraria'),
        user_id=data.get('user_id')
    )
    db.session.add(novo_curso)
    db.session.commit()
    return jsonify(
        mensagem='Curso cadastrado com sucesso',
        curso={
            'curso_id': novo_curso.curso_id,
            'nomeCurso': novo_curso.nomeCurso,
            'descricao': novo_curso.descricao,
            'cargaHoraria': novo_curso.cargaHoraria,
            'user_id': novo_curso.user_id})

# -----------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuarios.query.filter_by(email=email).first()

    if usuario and usuario.senha == senha:
        session['user_id'] = usuario.user_id
        return jsonify({
            'mensagem': 'Login com sucesso',
            'usuario': {
                'nome': usuario.nome,
                'email': usuario.email,
                'img': usuario.img
            }
        }), 200
    else:
        return jsonify({'mensagem': 'Email ou senha inválido'}), 401



# -----------------------------------------------------------------------------
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})

# -----------------------------------------------------------------------------
@app.route('/usuarios/<int:user_id>', methods=['PUT'])
def edit_usuario(user_id):
    usuario = Usuarios.query.get(user_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    data = request.json
    usuario.nome = data.get('nome', usuario.nome)
    usuario.senha = data.get('senha', usuario.senha)
    usuario.funcao = data.get('funcao', usuario.funcao)
    usuario.email = data.get('email', usuario.email)
    usuario.cpf = data.get('cpf', usuario.cpf)

    db.session.commit()

    return jsonify({'mensagem': 'Usuário atualizado com sucesso'}), 200


@app.route('/cursos/<int:curso_id>', methods=['PUT'])
def edit_curso(curso_id):
    curso = Cursos.query.get(curso_id)
    if not curso:
        return jsonify({'mensagem': 'Curso não encontrado'}), 404

    data = request.json
    curso.nomeCurso = data.get('nomeCurso', curso.nomeCurso)
    curso.descricao = data.get('descricao', curso.descricao)
    curso.cargaHoraria = data.get('cargaHoraria', curso.cargaHoraria)
    curso.user_id = data.get('user_id', curso.user_id)

    db.session.commit()

    return jsonify({'mensagem': 'Curso atualizado com sucesso'}), 200


# Rotas para exclusão de usuário e curso
@app.route('/usuarios/<int:user_id>', methods=['DELETE'])
def delete_usuario(user_id):
    usuario = Usuarios.query.get(user_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário deletado com sucesso'}), 200


@app.route('/cursos/<int:curso_id>', methods=['DELETE'])
def delete_curso(curso_id):
    curso = Cursos.query.get(curso_id)
    if not curso:
        return jsonify({'mensagem': 'Curso não encontrado'}), 404

    db.session.delete(curso)
    db.session.commit()

    return jsonify({'mensagem': 'Curso deletado com sucesso'}), 200


# Rotas para exibição, criação e edição de salas e turmas
@app.route('/salas', methods=['GET'])
def get_salas():
    salas = Salas.query.all()
    salas_list = [
        {'sala_id': sala.sala_id, 'numeroDaSala': sala.numeroDaSala, 'tipo': sala.tipo, 'descricao': sala.descricao} for
        sala in salas]
    return jsonify({'mensagem': 'Lista de salas', 'salas': salas_list})


@app.route('/salas', methods=['POST'])
def create_sala():
    data = request.json
    nova_sala = Salas(numeroDaSala=int(data['numeroDaSala']), tipo=data['tipo'], descricao=data['descricao'])
    db.session.add(nova_sala)
    db.session.commit()
    return jsonify({'mensagem': 'Sala criada com sucesso'}), 201


@app.route('/salas/<int:sala_id>', methods=['PUT'])
def edit_sala(sala_id):
    sala = Salas.query.get(sala_id)
    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'}), 404

    data = request.json
    sala.numeroDaSala = data.get('numeroDaSala', sala.numeroDaSala)
    sala.tipo = data.get('tipo', sala.tipo)
    sala.descricao = data.get('descricao', sala.descricao)

    db.session.commit()

    return jsonify({'mensagem': 'Sala atualizada com sucesso'}), 200


@app.route('/turmas', methods=['GET'])
def get_turmas():
    # Realiza a junção entre as tabelas turmas e usuarios
    query = db.session.query(Turmas, Usuarios.nome).outerjoin(Usuarios, Usuarios.user_id == Turmas.user_id)

    # Obtém todos os resultados da consulta
    results = query.all()

    # Lista de dicionários contendo os resultados
    turmas_list = [{'turma_id': turma[0].turma_id,
                    'nomeDaTurma': turma[0].nomeDaTurma,
                    'inicioAulas': turma[0].inicioAulas,
                    'finalAulas': turma[0].finalAulas,
                    'diasDaSemana': turma[0].diasDaSemana,
                    'curso_id': turma[0].curso_id,
                    'user_id': turma[0].user_id,
                    'sala_id': turma[0].sala_id,
                    'nomeUsuario': turma[1]} for turma in results]

    # Retorna os resultados como JSON
    return jsonify({'mensagem': 'Lista de turmas com nome do usuário', 'turmas': turmas_list})


@app.route('/turmas', methods=['POST'])
def create_turma():
    data = request.json
    nova_turma = Turmas(nomeDaTurma=data['nomeDaTurma'], inicioAulas=data['inicioAulas'], finalAulas=data['finalAulas'],
                        diasDaSemana=str(data['diasDaSemana']), curso_id=int(data['curso_id']), user_id=int(data['user_id']),
                        sala_id=int(data['sala_id']))
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({'mensagem': 'Turma criada com sucesso'}), 201

@app.route('/turmascalendario', methods=['GET'])
def get_turmascalendario():
    query = db.session.query(Turmas)
    results = query.all()
    _feriados = Feriados.query.all()
    feriados = []
    for fer in _feriados:
        feriados.append(fer.datas)

    print(_feriados)

    # Formato desejado para a data
    date_format = "%Y-%m-%d"

    # Criando a lista de turmas com a data formatada
    turmas_list = []
    for turma in results:
        if turma.inicioAulas is not None:
            print(turma.inicioAulas)
            print(turma.diasDaSemana)
            turmas_list.append({
                'id': turma.turma_id,
                'title': turma.nomeDaTurma,
                'rrule': {
                    'freq':'weekly',
                    'dtstart': turma.inicioAulas.strftime(date_format),
                    'until': turma.finalAulas.isoformat(),
                    'byweekday': eval(turma.diasDaSemana),
                },
                'exdate': feriados
            })
    print(turmas_list)

    return jsonify({'mensagem': 'Lista de turmas com nome do usuário', 'turmas': turmas_list})

    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({'mensagem': 'Turma criada com sucesso'}), 201


@app.route('/turmas/<int:turma_id>', methods=['PUT'])
def edit_turma(turma_id):
    turma = Turmas.query.get(turma_id)
    if not turma:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

    data = request.json
    turma.nomeDaTurma = data.get('nomeDaTurma', turma.nomeDaTurma)
    turma.inicioAulas = data.get('inicioAulas', turma.inicioAulas)
    turma.finalAulas = data.get('finalAulas', turma.finalAulas)
    turma.diasDaSemana = data.get('diasDaSemana', turma.diasDaSemana)
    turma.curso_id = data.get('curso_id', turma.curso_id)
    turma.user_id = data.get('user_id', turma.user_id)
    turma.sala_id = data.get('sala_id', turma.sala_id)

    db.session.commit()

    return jsonify({'mensagem': 'Turma atualizada com sucesso'}), 200


# Rotas para exclusão de salas e turmas
@app.route('/salas/<int:sala_id>', methods=['DELETE'])
def delete_sala(sala_id):
    sala = Salas.query.get(sala_id)
    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'}), 404

    db.session.delete(sala)
    db.session.commit()

    return jsonify({'mensagem': 'Sala deletada com sucesso'}), 200


@app.route('/turmas/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    turma = Turmas.query.get(turma_id)
    if not turma:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

    db.session.delete(turma)
    db.session.commit()

    return jsonify({'mensagem': 'Turma deletada com sucesso'}), 200

