# sistema_ti.py

from datetime import datetime
from models import criar_sessao, Chamado, Tecnico, IP, Ativo

sessao = criar_sessao()

def cadastrar_tecnico():
    nome = input("Nome do técnico: ").strip()
    email = input("E-mail: ").strip()
    novo = Tecnico(nome=nome, email=email)
    sessao.add(novo)
    sessao.commit()
    print("Técnico cadastrado.")


def abrir_chamado():
    categoria = input("Categoria (Rede, Wi-Fi, Impressora etc.): ").strip()
    prioridade = input("Prioridade (Alta / Média / Baixa): ").strip()
    descricao = input("Descreva o problema: ").strip()

    novo = Chamado(categoria=categoria, prioridade=prioridade, descricao=descricao)
    sessao.add(novo)
    sessao.commit()
    print(f"Chamado criado. Código: {novo.id}")


def mostrar_chamados():
    lista = sessao.query(Chamado).all()
    if not lista:
        print("Nenhum chamado encontrado.")
        return
    print("\n--- Chamados ---")
    for c in lista:
        print(f"[{c.id}] {c.categoria} | {c.status} | Prioridade: {c.prioridade}")


def atualizar_status():
    mostrar_chamados()
    try:
        codigo = int(input("\nInforme o ID do chamado: "))
    except ValueError:
        print("ID inválido.")
        return

    novo_status = input("Novo status (Aberto / Em atendimento / Fechado): ").strip()
    chamado = sessao.get(Chamado, codigo)

    if chamado:
        chamado.status = novo_status
        if novo_status.lower() == "fechado":
            chamado.data_fechamento = datetime.now()
        sessao.commit()
        print("Status atualizado.")
    else:
        print("Chamado não encontrado.")


def cadastrar_ip():
    endereco = input("Endereço IP: ").strip()
    mac = input("Endereço MAC (opcional): ").strip() or None
    reservado = input("Reservar este IP? (s/n): ").strip().lower() == "s"
    status = "Ocupado" if reservado else "Disponível"

    novo = IP(endereco=endereco, mac=mac, reservado=reservado, status=status)
    sessao.add(novo)
    sessao.commit()
    print("Endereço IP cadastrado.")


def listar_ips():
    lista = sessao.query(IP).all()
    if not lista:
        print("Nenhum IP cadastrado.")
        return
    print("\n--- Endereços IP ---")
    for ip in lista:
        print(f"[{ip.id}] {ip.endereco} - {ip.status}")


def cadastrar_ativo():
    nome = input("Nome do ativo: ").strip()
    tipo = input("Tipo (Computador, Notebook, Roteador etc.): ").strip()
    listar_ips()

    try:
        ip_id = int(input("Informe o ID do IP a associar: "))
    except ValueError:
        print("ID inválido.")
        return

    ativo = Ativo(nome=nome, tipo=tipo, ip_id=ip_id)
    sessao.add(ativo)
    sessao.commit()
    print("Ativo registrado.")


def menu():
    while True:
        print("""
1 - Cadastrar técnico
2 - Abrir chamado
3 - Ver chamados
4 - Alterar status
5 - Cadastrar IP
6 - Registrar ativo
0 - Sair
""")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tecnico()
        elif opcao == "2":
            abrir_chamado()
        elif opcao == "3":
            mostrar_chamados()
        elif opcao == "4":
            atualizar_status()
        elif opcao == "5":
            cadastrar_ip()
        elif opcao == "6":
            cadastrar_ativo()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo.")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()
