from modelo import *


@app.route("/listar/<string:classe>")
def listar(classe):
    # obter os dados da classe informada
    if classe == "Pessoa":
        dados = db.session.query(Pessoa).all()
    # converter dados para json
    lista_jsons = [ x.json() for x in dados ]
    # converter a lista do python para json
    resposta = jsonify(lista_jsons)
    # PERMITIR resposta para outras pedidos oriundos de outras tecnologias
    resposta.headers.add("Access-Control-Allow-Origin" ,server)
    return resposta

    '''
    exemplo de teste:
    $ curl localhost:5000/listar/Pessoa
    [
      {
        "pessoa": {
          "email": "caiozdbja@gmail.com", 
          "id": 1, 
          "nome": "Caio Luan Zenke", 
          "tipo": "professor"
        }, 

      }
    ]
'''