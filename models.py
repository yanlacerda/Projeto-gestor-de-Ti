# models.py
# Projeto: Sistema de Gestão de TI

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ======= BASE DO BANCO =======
Base = declarative_base()

# ======= TABELAS PRINCIPAIS =======

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

    chamados = relationship("Chamado", back_populates="tecnico")

    def __repr__(self):
        return f"<Técnico {self.nome}>"


class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True)
    categoria = Column(String(100), nullable=False)   # Exemplo: Rede, Wi-Fi, Impressora
    prioridade = Column(String(50), nullable=False)   # Alta / Média / Baixa
    status = Column(String(50), default="Aberto")     # Aberto / Em andamento / Fechado
    descricao = Column(String(255))
    data_abertura = Column(DateTime, default=datetime.now)
    data_fechamento = Column(DateTime, nullable=True)

    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"))
    tecnico = relationship("Tecnico", back_populates="chamados")

    def __repr__(self):
        return f"<Chamado #{self.id} - {self.categoria} ({self.status})>"


class IP(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True)
    endereco = Column(String(15), nullable=False, unique=True)
    mac = Column(String(17))
    reservado = Column(Boolean, default=False)
    status = Column(String(20), default="Livre")  # Livre / Alocado

    def __repr__(self):
        return f"<IP {self.endereco} - {self.status}>"


class Ativo(Base):
    __tablename__ = "ativos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(String(50))  # Exemplo: Switch, Notebook, Roteador
    ip_id = Column(Integer, ForeignKey("ips.id"))
    ip = relationship("IP")

    def __repr__(self):
        return f"<Ativo {self.nome} ({self.tipo})>"


# ======= CONEXÃO COM O BANCO =======

def criar_engine(database_url="sqlite:///gestao_ti.db"):
    """Cria o objeto Engine do SQLAlchemy."""
    return create_engine(database_url, echo=False, future=True)


def criar_sessao(database_url="sqlite:///gestao_ti.db"):
    """Cria as tabelas (se não existirem) e retorna uma sessão."""
    engine = criar_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return Session()
