from modelo import *

@app.route("/atualizar/<string:classe>", methods=['put'])
def atualizar(classe):
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})
    dados = request.get_json()  
    try:  
        if classe == "Pessoa":
                if 'id' not in dados: # não tem o atributo id?
                    resposta = jsonify({"resultado": "erro", 
                            "detalhes": "Atributo id não encontrado"})
                else:
                    id = dados['id']
                    alguem = Pessoa.query.get(id) # localizar a pessoa
                    if alguem is None: # se não encontrou
                        resposta = jsonify({"resultado": "erro", 
                                    "detalhes": f"Objeto não encontrado, id: {id}"})
                    else:
                        # atualizar os campos (esta parte dá pra melhorar :-)
                        alguem.nome = dados['nome'] # if dados['nome'] is not None else alguem.nome
                        alguem.email = dados['email']
                        alguem.idade = dados['idade']
                        alguem.cpf = dados['cpf']
                        alguem.funcao = dados['funcao']
                        db.session.commit()  # efetivar a atualização
        else:
                resposta = jsonify({"resultado": "erro", "detalhes": f"Classe não encontrada: {classe}"})
            
                
        
    except Exception as e: 
        resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta  

''' 
RESULTADOS DE TESTES:
$ curl -X PUT -d '{"id":1, "nome":"Teresa", "email":"te@gmail.com", "telefone":"123456789"}' -H "Content-Type:application/json" localhost:5000/atualizar/Pessoa 
{
  "detalhes": "ok", 
  "resultado": "ok"
}
$ curl localhost:5000/retornar/Pessoa/1
{
  "detalhes": {
    "email": "te@gmail.com", 
    "id": 1, 
    "nome": "Teresa", 
    "telefone": "123456789"
  }, 
  "resultado": "ok"
}
curl -X PUT -d '{"nome":"Paulo", "email":"pa@gmail.com", "telefone":"123456789"}' -H "Content-Type:application/json" localhost:5000/atualizar/Pessoa 
{
  "detalhes": "Atributo id n\u00e3o encontrado", 
  "resultado": "erro"
}
AUSÊNCIA DO CAMPO TELEFONE:
$ curl -X PUT -d '{"id":1, "nome":"Teresa", "email":"te@gmail.com"}' -H "Content-Type:application/json" localhost:5000/atualizar/Pessoa {
  "detalhes": "'telefone'", 
  "resultado": "erro"
}
'''
