from config import *
import os
#Linkar O treino com exercicio
#sqlviewer

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    email = db.Column(db.String(254))

    tipo = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'pessoa',
        'polymorphic_on': tipo
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





class Aluno(Pessoa):
    id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
    }
    ativo = db.Column(db.Boolean)
    valor_mensalidade = db.Column(db.String(254))
    #trei_id = db.Column(db.Integer, db.ForeignKey(Treino.id),
     #                   nullable=False)

    def __str__(self):
        return super().__str__() + f', Ativo={self.ativo}, '

class Treino(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(254))
    tipo = db.Column(db.String(254))
    exercicios = db.relationship("Exercicio", backref="treino")
    alunos = db.relationship('Aluno', secondary='treinoaluno')

    def __str__(self):
        return f' Treino : {self.tipo}, Series: {self.series}'
class Exercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    maquina = db.Column(db.String(254))

    exer_id = db.Column(db.Integer, db.ForeignKey(Treino.id),
                        nullable=False)

    def __str__(self) -> str:
        return f"nome = {self.nome}, na maquina: {self.maquina},{self.treino}"


treinoaluno = db.Table('treinoaluno', db.metadata,
                       db.Column('id_treino', db.Integer,
                                 db.ForeignKey(Treino.id)),
                       db.Column('id_aluno', db.Integer,
                                 db.ForeignKey(Aluno.id))
                       )

# Teste Aluno

if os.path.exists(arquivobd):
    os.remove(arquivobd)


db.create_all()

t1 = Treino(series='4x10', tipo='perna_inicante')
t2 = Treino(series='4x10', tipo='bicipes')
db.session.add(t1)
db.session.add(t2)
db.session.commit()


a1 = Aluno(nome='José Augusto', email='joséaugusto@gmail.com',
             ativo=True)
a2 = Aluno(nome='José Augusto', email='joséaugusto@gmail.com',
             ativo=True)
a3 = Aluno(nome='José Augusto', email='joséaugusto@gmail.com',
             ativo=True)
#print(f'Aluno: {jose}\n')
db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.commit()

print(a1)



ex = Exercicio(nome='Agachamento No Smith', maquina='Polia Smith', treino=t1)
ex2 = Exercicio(nome='Afundo Bulgaro', maquina='Livre', treino=t1)
ex3 = Exercicio(nome='ASTDVASTDVCSAOUDTACV', maquina='Livre', treino=t1)


db.session.add(ex)
db.session.add(ex2)
db.session.add(ex3)
db.session.commit()
#print(type(t1))


t1.alunos.append(a1)
t2.alunos.append(a1)
db.session.add(t1)
db.session.commit()

print(t1)

print()
print ('Retornando Todas os Exercicios de um Treino:')
for t in t1.exercicios:
    print(f'\t{t}')


