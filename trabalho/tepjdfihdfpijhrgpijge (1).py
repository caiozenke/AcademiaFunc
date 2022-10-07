from config import *

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    type = db.Column(db.String(50))

    __mapper_args__= {
        'polymorphic_identity':'pessoa', 
        'polymorphic_on': type
    }



class Personal(Pessoa):
    id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), primary_key = True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    a = db.Column(db.String(50))


    alunos = db.relationship('Aluno', backref='personal', foreign_keys=[aluno_id]) 

    #aqui vai os alunos

    __mapper_args__= {
        'polymorphic_identity': 'personal',
    }


class Aluno(Pessoa):
    id = db.Column(db.Integer, db.ForeignKey("pessoa.id"), primary_key = True)
    b = db.Column(db.String(50))


    

    #personal_id = db.Column(db.Integer, db.ForeignKey(Personal.id))
    #ersonal = db.relationship("Personal", back_populates="alunos")


    __mapper_args__= {
        'polymorphic_identity': 'aluno',
    }


if os.path.exists(arquivobd):
    os.remove(arquivobd)
db.create_all()

per =  Personal(nome = "dodbde", a = "personal 1")
a = Aluno(nome = "hfduegfuweg", b = "asd", personal = [per])
a1 = Aluno(nome = "dsfoufgsghf", b = "asdddddddd", personal = [per])

db.session.add(a)
db.session.add(a1)
db.session.add(per)

db.session.commit()