from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

caminho = "sqlite:///banco.db"
engine = create_engine(caminho)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Pessoa(Base):
    __tablename__ = "Pessoas"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    cpf = Column(String, unique=True, nullable=False)
    nome = Column(String)
    numero = Column(String)
    email = Column(String)
    data_nascimento = Column(Date)
    cep = Column(String)
    estado = Column(String)
    cidade = Column(String)
    bairro = Column(String)
    rua = Column(String)
    numero_casa = Column(String)
    data_cadastro = Column(DateTime)

    def __init__(self, cpf, nome, numero, email, data_nascimento, cep,
                 estado, cidade, bairro, rua, numero_casa,
                 data_cadastro) -> None:
        self.cpf = cpf
        self.nome = nome
        self.numero = numero
        self.email = email
        self.data_nascimento = data_nascimento
        self.cep = cep
        self.estado = estado
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero_casa = numero_casa
        self.data_cadastro = data_cadastro


Base.metadata.create_all(bind=engine)
