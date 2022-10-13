from modelo import *
# teste da rota: curl -d '{"nome":"James Kirk","email":"jakirk@gmail.com","tipo":"alunos"}' -X POST -H "Content-Type:application/json" localhost:5000/incluir/Pessoa

@app.route("/incluir/<string:classe>", methods=['post'])
def incluir(classe):
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})
    # receber as informações da nova pessoa
    dados = request.get_json() #(force=True) dispensa Content-Type na requisição
    try: # tentar executar a operação
      if classe == "Aluno":
        nova = Aluno(**dados) # criar a nova pesso
      elif classe == "Professor":
        nova = Professor(**dados) # criar a nova pessoa
      elif classe == "Personal":
        nova = Personal(**dados) # criar a nova pessoa   
      
      db.session.add(nova) # adicionar no BD
      db.session.commit() # efetivar a operação de gravação
    
    except Exception as e: # em caso de erro...
      # informar mensagem de erro
      resposta = jsonify({"resultado":"erro", "detalhes":str(e)})
    # adicionar cabeçalho de liberação de origem
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta # responder!