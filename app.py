# app.py
# Projeto: Sistema de Gestão de TI

from datetime import datetime
from models import criar_sessao, Chamado, Tecnico, IP, Ativo

# Cria sessão com o banco de dados
session = criar_sessao()

# ====== CADASTROS ======

def novo_tecnico():
    nome = input("Nome do técnico: ").strip()
    email = input("E-mail: ").strip()
    tecnico = Tecnico(nome=nome, email=email)
    session.add(tecnico)
    session.commit()
    print("✅ Técnico cadastrado com sucesso!")


def novo_chamado():
    categoria = input("Categoria (Rede, Wi-Fi, Impressora...): ").strip()
    prioridade = input("Prioridade (Alta / Média / Baixa): ").strip()
    descricao = input("Descrição do problema: ").strip()

    chamado = Chamado(
        categoria=categoria,
        prioridade=prioridade,
        descricao=descricao
    )
    session.add(chamado)
    session.commit()
    print(f"📋 Chamado registrado com sucesso! ID: {chamado.id}")


def listar_chamados():
    chamados = session.query(Chamado).all()
    if not chamados:
        print("Nenhum chamado encontrado.")
        return
    print("\n=== LISTA DE CHAMADOS ===")
    for c in chamados:
        print(f"[{c.id}] {c.categoria} | {c.status} | Prioridade: {c.prioridade}")


def alterar_status():
    listar_chamados()
    try:
        chamado_id = int(input("\nDigite o ID do chamado: "))
    except ValueError:
        print("ID inválido.")
        return

    novo_status = input("Novo status (Aberto / Em atendimento / Fechado): ").strip()
    chamado = session.get(Chamado, chamado_id)

    if chamado:
        chamado.status = novo_status
        if novo_status.lower() == "fechado":
            chamado.data_fechamento = datetime.now()
        session.commit()
        print("✅ Status atualizado com sucesso!")
    else:
        print("❌ Chamado não encontrado.")


def novo_ip():
    endereco = input("Endereço IP: ").strip()
    mac = input("Endereço MAC (opcional): ").strip() or None
    reservado = input("Reservado? (s/n): ").strip().lower() == "s"
    status = "Alocado" if reservado else "Livre"

    ip = IP(endereco=endereco, mac=mac, reservado=reservado, status=status)
    session.add(ip)
    session.commit()
    print("💾 IP cadastrado com sucesso!")


def listar_ips():
    ips = session.query(IP).all()
    if not ips:
        print("Nenhum IP cadastrado.")
        return
    print("\n=== LISTA DE ENDEREÇOS IP ===")
    for i in ips:
        print(f"[{i.id}] {i.endereco} - {i.status}")


def novo_ativo():
    nome = input("Nome do ativo: ").strip()
    tipo = input("Tipo (Computador, Notebook, Roteador, etc.): ").strip()
    listar_ips()

    try:
        ip_id = int(input("ID do IP a vincular: "))
    except ValueError:
        print("ID inválido.")
        return

    ativo = Ativo(nome=nome, tipo=tipo, ip_id=ip_id)
    session.add(ativo)
    session.commit()
    print("💻 Ativo cadastrado com sucesso!")


# ====== MENU PRINCIPAL ======

def menu_principal():
    while True:
        print("""
==============================
     SISTEMA DE GESTÃO DE TI
==============================
1 - Cadastrar Técnico
2 - Abrir Chamado
3 - Listar Chamados
4 - Atualizar Status
5 - Cadastrar IP
6 - Cadastrar Ativo
0 - Sair
""")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            novo_tecnico()
        elif opcao == "2":
            novo_chamado()
        elif opcao == "3":
            listar_chamados()
        elif opcao == "4":
            alterar_status()
        elif opcao == "5":
            novo_ip()
        elif opcao == "6":
            novo_ativo()
        elif opcao == "0":
            print("Encerrando o sistema... Até logo!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
