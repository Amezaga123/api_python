from flask import Flask, request, jsonify
from config import app, db
from models import Professor, Turma, Aluno, Atividade

@app.route('/professores', methods=['POST'])
def create_professor():
    data = request.get_json()
    professor = Professor(
        nome=data['nome'],
        idade=data['idade'],
        materia=data['materia'],
        observacoes=data.get('observacoes', '')
    )
    db.session.add(professor)
    db.session.commit()
    return jsonify({"message": "Professor criado com sucesso"}), 201

@app.route('/turmas', methods=['POST'])
def create_turma():
    data = request.get_json()
    turma = Turma(
        descricao=data['descricao'],
        ativo=data.get('ativo', True),
        professor_id=data['professor_id']
    )
    db.session.add(turma)
    db.session.commit()
    return jsonify({"message": "Turma criada com sucesso"}), 201

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    aluno = Aluno(
        nome=data['nome'],
        idade=data['idade'],
        data_nascimento=data['data_nascimento'],
        nota_primeiro_semestre=data['nota_primeiro_semestre'],
        nota_segundo_semestre=data['nota_segundo_semestre'],
        media_final=(data['nota_primeiro_semestre'] + data['nota_segundo_semestre']) / 2,
        turma_id=data['turma_id']
    )
    db.session.add(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno criado com sucesso"}), 201

# Rota: Criar nova atividade
@app.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()
    atividade = Atividade(
        id_disciplina=data['id_disciplina'],
        enunciado=data['enunciado'],
        respostas=data.get('respostas', [])
    )
    db.session.add(atividade)
    db.session.commit()
    return jsonify({"message": "Atividade criada com sucesso"}), 201

# Rota: Atualizar atividade existente
@app.route('/atividades/<int:id_atividade>/', methods=['PUT'])
def update_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        return jsonify({"error": "Atividade não encontrada"}), 404

    data = request.get_json()
    atividade.id_disciplina = data.get('id_disciplina', atividade.id_disciplina)
    atividade.enunciado = data.get('enunciado', atividade.enunciado)
    atividade.respostas = data.get('respostas', atividade.respostas)
    
    db.session.commit()
    return jsonify({
        "message": "Atividade atualizada com sucesso",
        "atividade": {
            "id_atividade": atividade.id_atividade,
            "id_disciplina": atividade.id_disciplina,
            "enunciado": atividade.enunciado,
            "respostas": atividade.respostas
        }
    }), 200

# Rota: Excluir atividade existente
@app.route('/atividades/<int:id_atividade>/', methods=['DELETE'])
def delete_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        return jsonify({"error": "Atividade não encontrada"}), 404

    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"message": "Atividade excluída com sucesso"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    print(app.url_map)  # Lista todas as rotas
    with app.app_context():
        db.create_all()
    app.run(debug=True)
