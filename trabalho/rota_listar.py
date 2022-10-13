from modelo import *


@app.route("/listar/<string:classe>")
def listar(classe):
    if classe == "Pessoa":
        dados = db.session.query(Pessoa).all()
    elif classe =="Treino":
        dados = db.session.query(Treino).all()
    elif classe =="Exercicio":
        dados = db.session.query(Exercicio).all()
    lista_jsons = [ x.json() for x in dados ]
    resposta = jsonify(lista_jsons)
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