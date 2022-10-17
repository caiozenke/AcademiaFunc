import json
from config import *


#Preciso de uma tabela ralacional entre os alunos e personais, para poder relação entre alunos e personais
#TENTEI USAR LISTA REVERSA COMO USEI NO TREINO PARA ALUNO ,POREM DAR UM ERRO

class Pessoa(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    email = db.Column(db.String(254))
    
    tipo = db.Column(db.String(50))


    __mapper_args__= {
        'polymorphic_identity':'pessoa', 
        'polymorphic_on':tipo
        }
    
    def __str__(self):
        return f'{self.nome}, email ={self.email} , Função: {self.tipo}'

    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
        }


class Professor(Pessoa):
    id = db.Column(db.Integer ,db.ForeignKey('pessoa.id'),primary_key=True)
    __mapper_args__= {
        'polymorphic_identity':'professor', 
        }

    salario =  db.Column(db.String(254))

    def __str__(self):
        return super().__str__() + f", salario= {self.salario}"

    def json(self):
        json1 = super().json()
        json1.update({"salario":self.salario})
        return json1

class Personal(Pessoa):
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'),primary_key =True)
    __mapper_args__= {
        'polymorphic_identity': 'personal',
    }

    quantidade_alunos = db.Column(db.String(254))
    def __str__(self):
        return super().__str__() + f', Tem {self.quantidade_alunos} de Alunos '

    def json(self):
        json2 = super().json()
        json2.update({"quantidade_alunos":self.quantidade_alunos})
        return json2

class Treino(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    series = db.Column(db.String(254))
    tipo = db.Column(db.String(254))
    exercicios = db.relationship("Exercicio", backref="treino")
    alunos =  db.relationship('Aluno', backref = 'treino')


    def __str__(self):
        return f' Treino : {self.tipo}, Series: {self.series}'

    def json(self):
        temp =  {
            "id": self.id,
            "series": self.series,
            "tipo": self.tipo,
            "exercicios": self.tipo
        }
        alunos = []
        for s in self.alunos:
            alunos.append(s.json())
        temp.update({"alunos":alunos})
        return temp



class Aluno(Pessoa):
    id = db.Column(db.Integer,db.ForeignKey('pessoa.id'),primary_key =True)
    __mapper_args__= {
        'polymorphic_identity': 'aluno',
    }
    ativo = db.Column(db.Boolean)
    valor_mensalidade = db.Column(db.String(254))
    trei_id = db.Column(db.Integer, db.ForeignKey(Treino.id), 
                          nullable=False)

    def __str__(self):
        return super().__str__() + f', Ativo={self.ativo}, {self.treino} '

    def json(self):
        json3 = super().json()
        json3.update({"ativo":self.ativo})
        json3.update({"valor_mensalidade":self.valor_mensalidade})
        json3.update({"trei_id":self.trei_id})
        return json3


class Exercicio(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    nome = db.Column(db.String(254))
    maquina = db.Column(db.String(254))
    exer_id = db.Column(db.Integer, db.ForeignKey(Treino.id), 
                          nullable=False)
    
    def __str__(self) -> str:
        return f"nome = {self.nome}, na maquina: {self.maquina},{self.treino}"

    
    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "maquina": self.maquina,
            "exer_id": self.exer_id
        }



#teste

if __name__=="__main__":

    if os.path.exists(arquivobd):
        os.remove(arquivobd)

    db.create_all()

    #Teste Professor
    caio = Professor(nome="Caio Luan Zenke", 
                email="caiozdbja@gmail.com", salario=7)

    print(f'Professor: {caio}\n')

    db.session.add(caio)
    db.session.commit()


    #teste Personal
    zenke = Personal(nome= 'Jorgao', email='ajbncsabcai@',quantidade_alunos ='30')
    print(f'Personal: {zenke}\n')
    db.session.add(zenke)
    db.session.commit()


    #Teste Treino 
    t1 = Treino(series='4x10',tipo='perna_inicante')

    db.session.add(t1)
    db.session.commit()

    #Teste Aluno
    jose = Aluno(nome='José Augusto', email='joséaugusto@gmail.com' , ativo =True,treino= t1)
    print(f'Aluno: {jose}\n' )
    db.session.add(jose)
    db.session.commit()



    print ('Retornando Todas As Pessoas:')
    for p in db.session.query(Pessoa).all():
        print (f'\t{p}')

    print()
    #for a in zenke.personais:
    #        print(f'Busca dos Alunos do Personal {zenke.nome}:\n\t{a}')




    #exercicios

    ex = Exercicio(nome='Agachamento No Smith', maquina = 'Polia Smith' ,treino= t1 )
    ex2 = Exercicio(nome='Afundo Bulgaro', maquina = 'Livre' ,treino= t1 )


    db.session.add(ex)
    db.session.add(ex2)
    db.session.commit()

    print ('Retornando Todas os Exercicios de um Treino:')
    for t in t1.exercicios:
        print(f'\t{t}')


