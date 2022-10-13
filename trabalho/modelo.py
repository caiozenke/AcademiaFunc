
from sqlalchemy import true
from config import *



class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(254))
    email = db.Column(db.String(254),unique = True) #Unique Valor
    idade = db.Column (db.Integer) #Apenas Inteiros
    cpf = db.Column(db.String(254) , unique = True)

    funcao = db.Column(db.String(50))


    __mapper_args__= {
        'polymorphic_identity':'pessoa', 
        'polymorphic_on':funcao
        }

    def __str__(self):
        return f' Nome:{self.nome}, Cpf: {self.cpf}, Email:{self.email}, Idade:{self.idade}, Funcao:{self.funcao}'


    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "idade":self.idade,
            "cpf":self.cpf,
            "tipo": self.funcao,
        }
            

class Professor(Pessoa):
    id = db.Column(db.Integer , db.ForeignKey('pessoa.id'), primary_key =True)
    
    __mapper_args__= {
        'polymorphic_identity':'professor', 
        }


    salario =  db.Column(db.Float)

    def __str__(self):
        return super().__str__() + f", salario:{self.salario}"

    def json(self):
        j1 = super().json()
        j1.update({'Salario':self.salario})
        return j1



class Personal(Pessoa):
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'),primary_key= True)

    __mapper_args__= {
        'polymorphic_identity':'personal', 
        }

    alunos = db.relationship('Aluno', secondary='alunopersonal')

    quantidade_alunos = db.Column(db.Integer)
    def __str__(self):
        return super().__str__() + f', Tem {self.quantidade_alunos} de Alunos '


    def json(self):
        j1 = super().json()
        j1.update({'Quantidade':self.quantidade_alunos})
        return j1



class Aluno(Pessoa):
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'),primary_key=True)

    __mapper_args__= {
        'polymorphic_identity':'aluno', 
        }
    treinos = db.relationship('Treino', secondary='treinoaluno')
    plano = db.Column(db.String(254))
    ativo = db.Column(db.Boolean)
    valor_mensalidade = db.Column(db.Integer)

    def __str__(self):
        return super().__str__() + f', Ativo:{self.ativo}, plano:{self.plano}, valor da mensalidade:{self.valor_mensalidade}'

    def json(self):
        j1 = super().json()
        j1.update({'Plano':self.plano},{'Ativo':self.ativo},{'Valor da mensalidade':self.valor_mensalidade})
        return j1



class Treino(db.Model):
    id = db.Column(db.Integer ,primary_key = True)
    series = db.Column(db.String(254))
    tipo = db.Column(db.String(254))
    exercicios = db.relationship('Exercicio', backref ='treino')

    def __str__(self) -> str:
        return f', series:{self.series}, Tipo de Treino:{self.tipo}'

    def json(self):
        j1 = super().json()
        j1.update({'Serie': self.series},{'Tipo': self.tipo})
        return j1


class Exercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exer_id = db.Column(db.Integer, db.ForeignKey(Treino.id), 
                          nullable=False)
    nome = db.Column(db.String(254))
    maquina = db.Column(db.String(254))
    
    def __str__(self) -> str:
        return f"nome = {self.nome}, na maquina: {self.maquina},{self.treino}"


    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "maquina": self.maquina,
            "exer_id": self.exer_id,
            'exercicio':self.treno
        }



#Tabelas Interelacionais
alunopersonal = db.Table('alunopersonal',db.metadata,
                        db.Column('personal_id',db.Integer,db.ForeignKey(Personal.id)),
                        db.Column('aluno_id',db.Integer, db.ForeignKey(Aluno.id),unique= True) #Unique Pois o Aluno so pode ter um Personal  1xN
                        )


treinoaluno = db.Table('treinoaluno', db.metadata,
                       db.Column('id_aluno', db.Integer,
                                 db.ForeignKey(Aluno.id)),
                       db.Column('id_treino', db.Integer,
                                 db.ForeignKey(Treino.id))
                       )


if os.path.exists(arquivobd):
    os.remove(arquivobd)


db.create_all()

#teste classe pessoa
p  = Pessoa(nome  = 'Caio zenke' , email = 'caiolzenke@gmail.com' ,cpf = '111.323.232-00' , idade=18)
db.session.add(p)
db.session.commit()


#teste classe professor 
prof = Professor(nome ='Nicolas' , email = 'asdihasd@gmail.com' ,cpf='111.323.322-00', idade=18 , salario = 1850)
db.session.add(prof)
db.session.commit()

#Teste Personal
per = Personal(nome ='Carlão Gren' , email = 'carlãodelas@gmail.com' ,cpf='111.323.232-10', idade=18 , quantidade_alunos = 32)
per2 = Personal(nome ='Hasda Unique' , email = 'Hasda@gmail.com' ,cpf='111.323.232-22', idade=22 , quantidade_alunos = 32)
db.session.add(per)
db.session.add(per2)
db.session.commit()


#Teste Aluno 
a = Aluno(nome= 'Thai', email='thaisd@gmail.com', cpf= '111.323.222-00',idade=20, plano = 'Black' , ativo=True, valor_mensalidade = 320)
a2 = Aluno(nome= 'Mia Malkova', email='malkova@gmail.com', cpf= '111.323.222-01',idade=20, plano = 'Black' , ativo=True, valor_mensalidade = 320)
a3 = Aluno(nome= 'Violet Myres', email='myres@gmail.com', cpf= '111.323.222-02',idade=20, plano = 'Black' , ativo=True, valor_mensalidade = 320)
a4 = Aluno(nome= 'Lana Rhoades', email='rhoades@gmail.com', cpf= '111.323.222-03',idade=20, plano = 'Black' , ativo=True, valor_mensalidade = 320)

db.session.add(a)
db.session.add(a2)
db.session.add(a3)
db.session.commit()


#Teste AlunoPersonal
per.alunos.append(a)
per.alunos.append(a2)
per.alunos.append(a3)
db.session.add(per)


#per2.alunos.append(a) #teste do unique
#db.session.add(per2)
db.session.commit()

#Teste Treino
t1 = Treino(series='4x10',tipo='perna_inicante')
t2 = Treino(series='4x10', tipo='bicipes')
db.session.add(t1)
db.session.add(t1)
db.session.commit()


#Teste Exercicios

ex = Exercicio(nome='Agachamento No Smith', maquina = 'Polia Smith' ,treino= t1 )
ex2 = Exercicio(nome='Afundo Bulgaro', maquina = 'Livre' ,treino= t1 )

db.session.add(ex)
db.session.add(ex2)
db.session.commit()



a.treinos.append(t1)
a.treinos.append(t2)
db.session.add(a)
db.session.commit()


print()
print ('Retornando Todas os Exercicios de um Treino:')
for t in t1.exercicios:
    print(f'\t{t}')


print(f'Alunos do Personal {per.nome}:')
for a in per.alunos:
    print(f'\t{a.nome}')

print()



# retornando Dados
print('Retornando Todos os Função,Nomes e ID das Pessoas')
for pessoas in db.session.query(Pessoa).all():
    print(f'\t {pessoas.funcao} = {pessoas.nome}: {pessoas.id}')

