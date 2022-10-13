from modelo import *
from rota_listar import *
from rota_incluir import *

@app.route("/")
def inicio():
    return 'Aqui esta o nosso inicio'

app.run(debug=True, host="0.0.0.0")