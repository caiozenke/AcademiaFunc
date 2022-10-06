from modelo import *
from rota_listar import *

@app.route("/")
def inicio():
    return 'Agora vai pegar fogo'

app.run(debug=True, host="0.0.0.0")