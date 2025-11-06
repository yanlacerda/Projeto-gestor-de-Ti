# models.py

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

    chamados = relationship("Chamado", back_populates="tecnico")

    def __repr__(self):
        return f"Técnico: {self.nome}"


class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True)
    categoria = Column(String(100), nullable=False)
    prioridade = Column(String(50), nullable=False)
    status = Column(String(50), default="Aberto")
    descricao = Column(String(255))
    data_abertura = Column(DateTime, default=datetime.now)
    data_fechamento = Column(DateTime)

    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"))
    tecnico = relationship("Tecnico", back_populates="chamados")

    def __repr__(self):
        return f"Chamado {self.id} - {self.categoria} ({self.status})"


class IP(Base):
    __tablename__ = "enderecos_ip"

    id = Column(Integer, primary_key=True)
    endereco = Column(String(15), nullable=False, unique=True)
    mac = Column(String(17))
    reservado = Column(Boolean, default=False)
    status = Column(String(20), default="Disponível")

    def __repr__(self):
        return f"IP {self.endereco} - {self.status}"


class Ativo(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(String(50))
    ip_id = Column(Integer, ForeignKey("enderecos_ip.id"))
    ip = relationship("IP")

    def __repr__(self):
        return f"Ativo: {self.nome} ({self.tipo})"


def criar_engine(url_banco="sqlite:///suporte_ti.db"):
    return create_engine(url_banco, echo=False, future=True)


def criar_sessao(url_banco="sqlite:///suporte_ti.db"):
    engine = criar_engine(url_banco)
    Base.metadata.create_all(engine)
    Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return Sessao()
