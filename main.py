import customtkinter as ctk
import tkinter
import re
from datetime import date, datetime
from pycep import Cep
from sqlalchemy import create_engine, delete, desc
from sqlalchemy.orm import Session
from models import Pessoa
from validate_docbr import CPF


caminho = "sqlite:///banco.db"
engine = create_engine(caminho)

app = ctk.CTk()
app.geometry("1300x650")
app.title("Cadastro")
app.iconbitmap("fav.ico")
ctk.set_appearance_mode("light")

tela_cadastro = ctk.CTkFrame(master=app)
tela_listar = ctk.CTkScrollableFrame(master=app)
tela_menu = ctk.CTkFrame(master=app)
tela_confirmacao = ctk.CTkFrame(master=app)


def calcular_idade(data: date) -> str:
    data_atual = date.today()
    ano = data_atual.year - data.year
    mes = data_atual.month - data.month
    dia = data_atual.day - data.day
    if mes >= 0 and dia >= 0:
        return ano
    else:
        return ano-1


def formatar_numero_celular(numero_celular: str) -> str:
    lista_numero_celular = list(numero_celular)
    tamanho = len(lista_numero_celular)
    if tamanho == 10:
        lista_numero_celular.insert(0, "(")
        lista_numero_celular.insert(3, ")")
        lista_numero_celular.insert(4, " ")
        lista_numero_celular.insert(5, " ")
        lista_numero_celular.insert(10, "-")
    else:
        lista_numero_celular.insert(0, "(")
        lista_numero_celular.insert(3, ")")
        lista_numero_celular.insert(4, " ")
        lista_numero_celular.insert(10, "-")

    numero_celular_formatado = ""
    return numero_celular_formatado.join(lista_numero_celular)


def formatar_cpf(cpf: str) -> str:
    lista_cpf = list(cpf)
    lista_cpf.insert(3, ".")
    lista_cpf.insert(7, ".")
    lista_cpf.insert(11, "-")
    cpf_formatado = ""
    return cpf_formatado.join(lista_cpf)


def formatar_cep(cep: str) -> str:
    lista_cep = list(cep)
    lista_cep.insert(5, "-")
    cep_formatado = ""
    return cep_formatado.join(lista_cep)


def formatar_string(string: str) -> str:
    string = string.strip().title()
    lista_string: list[str] = string.split(" ")
    while "" in lista_string:
        lista_string.remove("")

    string = " "
    return string.join(lista_string)


def verificar_cep(
    input_cep, input_estado, input_cidade, input_bairro, input_rua
) -> None:
    if input_cep.cget("border_color") == "green":
        pass
    else:
        tamanho_cep = len(input_cep.get().strip())
        if tamanho_cep < 8 or tamanho_cep > 8:
            input_cep.configure(border_color="red")
        else:
            cep = Cep(input_cep.get())
            if cep.city is None or cep.district is None:
                input_cep.configure(border_color="red")
            else:
                input_cep.configure(border_color="green")
                input_estado.delete(0, len(input_estado.get()))
                input_estado.insert(0, cep.state)
                input_estado.configure(border_color="green")

                input_cidade.delete(0, len(input_cidade.get()))
                input_cidade.insert(0, cep.city)
                input_cidade.configure(border_color="green")

                input_bairro.delete(0, len(input_bairro.get()))
                input_bairro.insert(0, cep.district)
                input_bairro.configure(border_color="green")

                input_rua.delete(0, len(input_bairro.get()))
                input_rua.insert(0, cep.street)
                input_rua.configure(border_color="green")


def confirmar(
    input_cpf,
    input_nome,
    input_numero,
    input_email,
    input_data_nascimento,
    input_cep,
    input_estado,
    input_cidade,
    input_bairro,
    input_rua,
    input_numero_casa,
    botao_confirmar,
    tela_menu,
    tela_cadastro,
    tela_confirmacao,
    tela_listar
) -> None:

    with Session(engine) as session:
        q = session.query(Pessoa).where(
            Pessoa.cpf == input_cpf.get().strip()
            ).all()
        verificar_cpf = CPF()
        if q != []:
            input_cpf.configure(border_color="red",
                                placeholder_text="CPF já cadastrado")
            input_cpf.delete(0, len(input_cpf.get()))
            print("ERRO")
        elif verificar_cpf.validate(input_cpf.get().strip()):
            input_cpf.configure(border_color="green",
                                placeholder_text="")
            cpf: str = input_cpf.get().strip()
        else:
            input_cpf.configure(border_color="red",
                                placeholder_text="CPF inválido")
            input_cpf.delete(0, len(input_cpf.get()))

    if len(input_nome.get().strip()) >= 2:
        input_nome.configure(border_color="green")
        nome: str = formatar_string(input_nome.get())
    else:
        input_nome.configure(border_color="red")

    tamanho_numero = len(input_numero.get().strip().replace(" ", ""))
    numero_str: str = input_numero.get().strip().replace(" ", "")
    if tamanho_numero == 10 or tamanho_numero == 11 and numero_str.isalnum():
        input_numero.configure(border_color="green")
        numero: str = input_numero.get().strip().replace(" ", "")
    else:
        input_numero.configure(border_color="red")

    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
    verificacao_email = re.match(email_pattern, input_email.get().strip())
    if verificacao_email is None:
        input_email.configure(border_color="red")
    else:
        input_email.configure(border_color="green")
        email: str = input_email.get()
    tamanho_nascimento = len(
        input_data_nascimento.get().strip().replace(" ", "")
        )
    if tamanho_nascimento == 8:
        input_data = input_data_nascimento.get()
        try:
            data: date = date(
                        day=int(f"{input_data[0]+input_data[1]}"),
                        month=int(f"{input_data[2]+input_data[3]}"),
                        year=int(f"{input_data[4]+input_data[5]+input_data[6] +
                                    input_data[7]}")
                        )
            data_atual: date = date.today()
            if data > data_atual:
                input_data_nascimento.configure(border_color="red")
            else:
                input_data_nascimento.configure(border_color="green")
        except ValueError:
            input_data_nascimento.configure(border_color="red")
    else:
        input_data_nascimento.configure(border_color="red")
    if input_cep.cget("border_color") == "green":
        cep: str = input_cep.get().strip()

    tamanho_cep = len(input_cep.get().strip())
    if tamanho_cep < 8 or tamanho_cep > 8:
        input_cep.configure(border_color="red")

    if input_estado.get().strip().upper() in [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', "DF", 'ES', 'GO', 'MA', 'MT', 'MS',
        'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
        'SP', 'SE', 'TO'
    ]:
        input_estado.configure(border_color="green")
        estado: str = input_estado.get().strip().upper()
    else:
        input_estado.configure(border_color="red")

    if len(input_cidade.get().strip()) > 2:
        input_cidade.configure(border_color="green")
        cidade = formatar_string(input_cidade.get())
    else:
        input_cidade.configure(border_color="red")

    if len(input_bairro.get().strip()) > 0:
        input_bairro.configure(border_color="green")
        bairro = formatar_string(input_bairro.get())
    else:
        input_bairro.configure(border_color="red")

    if len(input_rua.get().strip()) > 0:
        input_rua.configure(border_color="green")
        rua = formatar_string(input_rua.get())
    else:
        input_rua.configure(border_color="red")

    if len(input_numero_casa.get().strip()) > 0:
        input_numero_casa.configure(border_color="green")
        numero_casa = input_numero_casa.get().upper()
    else:
        input_numero_casa.configure(border_color="red")

    if (
        input_cpf.cget("border_color") == "green" and
        input_nome.cget("border_color") == "green" and
        input_numero.cget("border_color") == "green" and
        input_email.cget("border_color") == "green" and
        input_data_nascimento.cget("border_color") == "green" and
        input_cep.cget("border_color") == "green" and
        input_estado.cget("border_color") == "green" and
        input_cidade.cget("border_color") == "green" and
        input_bairro.cget("border_color") == "green" and
        input_rua.cget("border_color") == "green" and
        input_numero_casa.cget("border_color") == "green"
    ):
        pessoa = Pessoa(
            cpf=cpf,
            nome=nome,
            numero=numero,
            email=email,
            data_nascimento=data,
            cep=cep,
            estado=estado,
            cidade=cidade,
            bairro=bairro,
            rua=rua,
            numero_casa=numero_casa,
            data_cadastro=datetime.today()
        )
        with Session(engine) as session:
            session.add(pessoa)
            session.commit()
        confirmacao(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar
        )

    botao_confirmar.focus_set()


def confirmacao(
    tela_menu,
    tela_cadastro,
    tela_confirmacao,
    tela_listar
) -> None:
    tela_cadastro.forget()

    tela_confirmacao = ctk.CTkFrame(
        master=app,
        fg_color="green",
        width=300,
        height=100
        )
    tela_confirmacao.place(relx=0.5, rely=0.5, anchor="center")

    texto_confirmacao = ctk.CTkLabel(
        master=tela_confirmacao,
        text="CADASTRO REALIZADO",
        text_color="white",
        font=("", 20, "bold")
    )
    texto_confirmacao.place(relx=0.5, rely=0.5, anchor="center")
    tela_confirmacao.after(
        3000,
        lambda: menu(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar
        )
    )


def cadastrar(tela_menu, tela_cadastro, tela_confirmacao, tela_listar) -> None:
    tela_menu.place_forget()
    tela_cadastro = ctk.CTkFrame(master=app)
    tela_cadastro.pack(fill="both", expand=True)
    frame_auxiliar_1 = ctk.CTkFrame(
        master=tela_cadastro,
        fg_color="transparent",
        bg_color="transparent"
    )
    frame_auxiliar_1.place(relx=0.5, rely=0.5, anchor="center")

    frame_auxiliar_2 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        fg_color="gray",
        corner_radius=10
    )
    frame_auxiliar_2.pack(ipadx=10, ipady=10)

    texto_cadastro = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Cadastro",
        font=("", 25, "bold"),
        width=400
    )
    texto_cadastro.grid(row=0, column=0, columnspan=3, pady=5)

    tamanho_input = 250

    texto_cpf = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" CPF"
        )
    texto_cpf.grid(row=1, column=0, padx=5, pady=0, sticky="w")
    input_cpf = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
    )
    input_cpf.grid(row=2, column=0, padx=5, pady=0)

    texto_nome = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Nome Completo"
        )
    texto_nome.grid(row=1, column=1, padx=5, pady=0, sticky="w")
    input_nome = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
    )
    input_nome.grid(row=2, column=1, padx=5, pady=0)

    texto_numero = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Número de celular"
        )
    texto_numero.grid(row=1, column=2, padx=5, pady=0, sticky="w")
    input_numero = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20,
        placeholder_text="DDD+Número"
    )
    input_numero.grid(row=2, column=2, padx=5, pady=0)

    email_texto = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Email"
        )
    email_texto.grid(row=3, column=0, padx=5, pady=0, sticky="w")
    input_email = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
        )
    input_email.grid(row=4, column=0, padx=5, pady=0)

    data_nascimento = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Data de Nascimento"
        )
    data_nascimento.grid(row=3, column=1, padx=5, pady=0, sticky="w")
    input_data_nascimento = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20,
        placeholder_text="01012001"
    )
    input_data_nascimento.grid(row=4, column=1, padx=5, pady=0)

    texto_cep = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" CEP"
        )
    texto_cep.grid(row=3, column=2, padx=5, pady=0, sticky="w")
    input_cep = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
        )
    input_cep.grid(row=4, column=2, padx=5, pady=0)

    botao_verificar_cep = ctk.CTkButton(
        master=frame_auxiliar_2,
        text="⟳",
        width=1,
        corner_radius=20,
        command=lambda: verificar_cep(
            input_cep, input_estado, input_cidade, input_bairro, input_rua
        ),
    )
    botao_verificar_cep.grid(row=4, column=3)

    texto_estado = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Estado"
        )
    texto_estado.grid(row=5, column=0, padx=5, pady=0, sticky="w")
    input_estado = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20,
        placeholder_text="Sigla \"RJ\""
        )
    input_estado.grid(row=6, column=0, padx=5, pady=0)

    texto_cidade = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Cidade"
        )
    texto_cidade.grid(row=5, column=1, padx=5, pady=0, sticky="w")
    input_cidade = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
        )
    input_cidade.grid(row=6, column=1, padx=5, pady=0)

    texto_bairro = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Bairro"
        )
    texto_bairro.grid(row=5, column=2, padx=5, pady=0, sticky="w")
    input_bairro = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
        )
    input_bairro.grid(row=6, column=2, padx=5, pady=0)

    texto_rua = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Rua"
        )
    texto_rua.grid(row=7, column=0, padx=5, pady=0, sticky="w")
    input_rua = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
        )
    input_rua.grid(row=8, column=0, padx=5, pady=0)

    texto_numero_casa = ctk.CTkLabel(
        master=frame_auxiliar_2,
        text=" Número Casa"
        )
    texto_numero_casa.grid(row=7, column=1, padx=5, pady=0, sticky="w")
    input_numero_casa = ctk.CTkEntry(
        master=frame_auxiliar_2,
        width=tamanho_input,
        corner_radius=20
        )
    input_numero_casa.grid(row=8, column=1, padx=5, pady=0)

    botao_confirmar = ctk.CTkButton(
        master=frame_auxiliar_2,
        text="Confirmar",
        command=lambda: confirmar(
            input_cpf,
            input_nome,
            input_numero,
            input_email,
            input_data_nascimento,
            input_cep,
            input_estado,
            input_cidade,
            input_bairro,
            input_rua,
            input_numero_casa,
            botao_confirmar,
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar
        ),
        width=tamanho_input,
        corner_radius=20
    )
    botao_confirmar.grid(row=8, column=2, padx=2.5, pady=2.5)

    botao_voltar = ctk.CTkButton(
        master=frame_auxiliar_2,
        text="Voltar",
        command=lambda: menu(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar),
        width=tamanho_input,
        corner_radius=20
    )
    botao_voltar.grid(row=9, column=0, columnspan=3, padx=5, pady=10)


crescente = False


def listar(
    tela_menu,
    tela_cadastro,
    tela_confirmacao,
    tela_listar,
    ordem="nome"
) -> None:
    tela_listar.pack_forget()
    tela_menu.place_forget()
    tela_listar = ctk.CTkScrollableFrame(master=app)
    tela_listar.pack(padx=5, pady=5, fill="both", expand=True)

    dicio_ordem = {
        "nome": False,
        "email": False,
        "data_nascimento": False,
        "estado": False,
        "cidade": False,
        "data_cadastro": False
    }
    simbolo_cheio = " "
    simbolo_crescente = "↑"
    simbolo_decrescente = "↓"
    dicio_texto = {
        "nome": simbolo_cheio,
        "email": simbolo_cheio,
        "data_nascimento": simbolo_cheio,
        "estado": simbolo_cheio,
        "cidade": simbolo_cheio,
        "data_cadastro": simbolo_cheio
    }
    global crescente
    crescente = not crescente

    match ordem:
        case "nome":
            if dicio_ordem.get("nome") is False:
                for i in dicio_ordem:
                    dicio_ordem.update({i: False})
                    dicio_texto.update({i: simbolo_cheio})
                dicio_ordem.update({"nome": True})
                if crescente:
                    dicio_texto.update({"nome": simbolo_crescente})
                else:
                    dicio_texto.update({"nome": simbolo_decrescente})

        case "email":
            if dicio_ordem.get("email") is False:
                for i in dicio_ordem:
                    dicio_ordem.update({i: False})
                    dicio_texto.update({i: simbolo_cheio})
                dicio_ordem.update({"email": True})
                if crescente:
                    dicio_texto.update({"email": simbolo_crescente})
                else:
                    dicio_texto.update({"email": simbolo_decrescente})

        case "data_nascimento":
            if dicio_ordem.get("data_nascimento") is False:
                for i in dicio_ordem:
                    dicio_ordem.update({i: False})
                    dicio_texto.update({i: simbolo_cheio})
                dicio_ordem.update({"data_nascimento": True})
                if crescente:
                    dicio_texto.update({"data_nascimento": simbolo_crescente})
                else:
                    dicio_texto.update(
                        {"data_nascimento": simbolo_decrescente}
                        )

        case "estado":
            if dicio_ordem.get("estado") is False:
                for i in dicio_ordem:
                    dicio_ordem.update({i: False})
                    dicio_texto.update({i: simbolo_cheio})
                dicio_ordem.update({"estado": True})
                if crescente:
                    dicio_texto.update({"estado": simbolo_crescente})
                else:
                    dicio_texto.update({"estado": simbolo_decrescente})

        case "cidade":
            if dicio_ordem.get("cidade") is False:
                for i in dicio_ordem:
                    dicio_ordem.update({i: False})
                    dicio_texto.update({i: simbolo_cheio})
                dicio_ordem.update({"cidade": True})
                if crescente:
                    dicio_texto.update({"cidade": simbolo_crescente})
                else:
                    dicio_texto.update({"cidade": simbolo_decrescente})

        case "data_cadastro":
            if dicio_ordem.get("data_cadastro") is False:
                for i in dicio_ordem:
                    dicio_ordem.update({i: False})
                    dicio_texto.update({i: simbolo_cheio})
                dicio_ordem.update({"data_cadastro": True})
                if crescente:
                    dicio_texto.update({"data_cadastro": simbolo_crescente})
                else:
                    dicio_texto.update({"data_cadastro": simbolo_decrescente})

    ipadx_frame = 10
    padx_texto = 0
    ipady_frame = 2

    with Session(engine) as session:
        lista_pessoas = session.query(Pessoa).all()
        quantidade_pessoas = len(lista_pessoas)

    frame_auxiliar_1 = ctk.CTkScrollableFrame(
        master=tela_listar,
        orientation="horizontal",
        height=39*quantidade_pessoas
        )
    frame_auxiliar_1.pack(padx=0, pady=0, fill="both", expand=True)

    if quantidade_pessoas == 0:
        frame_auxiliar_1.pack_forget()

    cor_colunas = "#808080"

    frame_auxiliar_1_0 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_0.grid(
        row=0,
        column=0,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_1 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_1.grid(
        row=0,
        column=1,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_2 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_2.grid(
        row=0,
        column=2,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_3 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_3.grid(
        row=0,
        column=3,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_4 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_4.grid(
        row=0,
        column=4,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_5 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_5.grid(
        row=0,
        column=5,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_6 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_6.grid(
        row=0,
        column=6,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_7 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_7.grid(
        row=0,
        column=7,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )
    frame_auxiliar_1_8 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_8.grid(
        row=0,
        column=8,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_9 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_9.grid(
        row=0,
        column=9,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_10 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_10.grid(
        row=0,
        column=10,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_11 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_11.grid(
        row=0,
        column=11,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    frame_auxiliar_1_12 = ctk.CTkFrame(
        master=frame_auxiliar_1,
        border_color="black",
        fg_color=cor_colunas,
        border_width=2,
        corner_radius=0
        )
    frame_auxiliar_1_12.grid(
        row=0,
        column=12,
        ipadx=ipadx_frame,
        ipady=ipady_frame
        )

    with Session(engine) as session:
        if crescente:
            lista_pessoas = session.query(Pessoa).order_by(ordem).all()
        else:
            lista_pessoas = session.query(Pessoa).order_by(desc(ordem)).all()

    nome_maior = ""
    for i in lista_pessoas:
        if len(i.nome) > len(nome_maior):
            nome_maior = i.nome

    cidade_maior = ""
    for i in lista_pessoas:
        if len(i.cidade) > len(cidade_maior):
            cidade_maior = i.cidade

    bairro_maior = ""
    for i in lista_pessoas:
        if len(i.bairro) > len(bairro_maior):
            bairro_maior = i.bairro

    rua_maior = ""
    for i in lista_pessoas:
        if len(i.rua) > len(rua_maior):
            rua_maior = i.rua

    email_maior = ""
    for i in lista_pessoas:
        if len(i.email) > len(email_maior):
            email_maior = i.email

    multiplicador_tamanho = 8

    texto_nome = ctk.CTkButton(
        master=frame_auxiliar_1_0,
        text=f"Nome {dicio_texto.get("nome")}",
        text_color="black",
        fg_color="transparent",
        font=("", 14, "bold"),
        width=len(nome_maior)*multiplicador_tamanho,
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="nome"
        )
    )
    texto_nome.pack(padx=padx_texto, pady=2)

    texto_cpf = ctk.CTkLabel(
        master=frame_auxiliar_1_1,
        text_color="black",
        text="CPF",
        font=("", 14, "bold"),
        width=100
    )
    texto_cpf.pack(padx=padx_texto, pady=2)

    texto_numero = ctk.CTkLabel(
        master=frame_auxiliar_1_2,
        text_color="black",
        text="Número de celular",
        font=("", 14, "bold"),
        width=130
    )
    texto_numero.pack(padx=padx_texto, pady=2)

    texto_email = ctk.CTkButton(
        master=frame_auxiliar_1_3,
        text=f"Email {dicio_texto.get("email")}",
        text_color="black",
        fg_color="transparent",
        font=("", 14, "bold"),
        width=len(email_maior)*multiplicador_tamanho,
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="email"
        )
    )
    texto_email.pack(padx=padx_texto, pady=2)

    texto_data_nascimento = ctk.CTkButton(
        master=frame_auxiliar_1_4,
        text=f"Data de Nascimento {dicio_texto.get("data_nascimento")}",
        text_color="black",
        fg_color="transparent",
        font=("", 14, "bold"),
        width=170,
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="data_nascimento"
        )
    )
    texto_data_nascimento.pack(padx=padx_texto, pady=2)

    texto_idade = ctk.CTkButton(
        master=frame_auxiliar_1_5,
        text=f"Idade {dicio_texto.get("data_nascimento")}",
        text_color="black",
        fg_color="transparent",
        font=("", 14, "bold"),
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="data_nascimento"
        ),
        width=70
    )
    texto_idade.pack(padx=padx_texto, pady=2)

    texto_cep = ctk.CTkLabel(
        master=frame_auxiliar_1_6,
        text_color="black",
        text="CEP",
        font=("", 14, "bold"),
        width=80
    )
    texto_cep.pack(padx=padx_texto, pady=2)

    texto_estado = ctk.CTkButton(
        master=frame_auxiliar_1_7,
        text=f"Estado {dicio_texto.get("estado")}",
        text_color="black",
        fg_color="transparent",
        font=("", 14, "bold"),
        width=70,
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="estado"
        )
    )
    texto_estado.pack(padx=padx_texto, pady=2)

    texto_cidade = ctk.CTkButton(
        master=frame_auxiliar_1_8,
        text=f"Cidade {dicio_texto.get("cidade")}",
        text_color="black",
        fg_color="transparent",
        font=("", 14, "bold"),
        width=len(cidade_maior)*multiplicador_tamanho,
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="cidade"
        )
    )
    texto_cidade.pack(padx=padx_texto, pady=2)

    texto_bairro = ctk.CTkLabel(
        master=frame_auxiliar_1_9,
        text_color="black",
        text="Bairro",
        font=("", 14, "bold"),
        width=len(bairro_maior)*multiplicador_tamanho
    )
    texto_bairro.pack(padx=padx_texto, pady=2)

    texto_rua = ctk.CTkLabel(
        master=frame_auxiliar_1_10,
        text_color="black",
        text="Rua",
        font=("", 14, "bold"),
        width=len(rua_maior)*multiplicador_tamanho,
    )
    texto_rua.pack(padx=padx_texto, pady=2)

    texto_numero_casa = ctk.CTkLabel(
        master=frame_auxiliar_1_11,
        text_color="black",
        text="Número da Casa",
        font=("", 14, "bold"),
        width=120
    )
    texto_numero_casa.pack(padx=padx_texto, pady=2)

    texto_data_cadastro = ctk.CTkButton(
        master=frame_auxiliar_1_12,
        text=f"Data Cadastro {dicio_texto.get("data_cadastro")}",
        fg_color="transparent",
        bg_color="transparent",
        text_color="black",
        font=("", 14, "bold"),
        hover=False,
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar,
            ordem="data_cadastro"
        ),
        width=130
    )
    texto_data_cadastro.pack(padx=padx_texto, pady=2)

    class BotaoDelete(ctk.CTkButton):
        def __init__(
            self,
            master,
            width=140,
            height=28,
            corner_radius=None,
            border_width=None,
            border_spacing=2,
            bg_color="transparent",
            fg_color=None,
            hover_color=None,
            border_color=None,
            text_color=None,
            text_color_disabled=None,
            background_corner_colors=None,
            round_width_to_even_numbers=True,
            round_height_to_even_numbers=True,
            text="CTkButton",
            font=None,
            textvariable=None,
            image=None,
            state="normal",
            hover=True,
            command=False,
            compound="left",
            anchor="center",
            cpf="",
            nome="",
            **kwargs
        ):
            super().__init__(
                master, width,
                height,
                corner_radius,
                border_width,
                border_spacing,
                bg_color,
                fg_color,
                hover_color,
                border_color,
                text_color,
                text_color_disabled,
                background_corner_colors,
                round_width_to_even_numbers,
                round_height_to_even_numbers,
                text,
                font,
                textvariable,
                image,
                state,
                hover,
                command,
                compound,
                anchor,
                **kwargs
            )
            self.cpf = cpf
            self.nome = nome

        def _clicked(self, event=None):
            if self._state != tkinter.DISABLED:
                self._on_leave()
                self._click_animation_running = True
                self.after(100, self._click_animation)
            if self._command:
                popup_delete = ctk.CTkInputDialog(
                    text=f"CPF: {formatar_cpf(self.cpf)}\n" +
                    f"NOME: {self.nome}\n" +
                    "Digite SIM para deletar",
                    title="DELETAR"
                )
                popup_delete.after(
                    200, lambda: popup_delete.iconbitmap("alerta.ico"))
                popup_delete.pack_propagate()
                if popup_delete.get_input() == "SIM":
                    stmt = delete(Pessoa).where(Pessoa.cpf == self.cpf)
                    with Session(engine) as session:
                        session.execute(stmt)
                        session.commit()

                    listar(
                        tela_menu,
                        tela_cadastro,
                        tela_confirmacao,
                        tela_listar
                    )

    linha = 1
    for i in lista_pessoas:
        if linha % 2 == 0:
            cor_linhas = "#999999"
        else:
            cor_linhas = "#b0b0b0"

        frame_auxiliar_2_0 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
        )
        frame_auxiliar_2_0.grid(
            row=linha,
            column=0,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_1 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_1.grid(
            row=linha,
            column=1,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_2 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_2.grid(
            row=linha,
            column=2,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_3 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_3.grid(
            row=linha,
            column=3,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_4 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_4.grid(
            row=linha,
            column=4,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_5 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_5.grid(
            row=linha,
            column=5,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_6 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_6.grid(
            row=linha,
            column=6,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_7 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_7.grid(
            row=linha,
            column=7,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_8 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_8.grid(
            row=linha,
            column=8,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_9 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_9.grid(
            row=linha,
            column=9,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_10 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_10.grid(
            row=linha,
            column=10,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_11 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_11.grid(
            row=linha,
            column=11,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_12 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color=cor_linhas,
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_12.grid(
            row=linha,
            column=12,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )

        frame_auxiliar_2_13 = ctk.CTkFrame(
            master=frame_auxiliar_1,
            border_color="black",
            fg_color="red",
            border_width=2,
            corner_radius=0
            )
        frame_auxiliar_2_13.grid(
            row=linha,
            column=13,
            ipadx=ipadx_frame,
            ipady=ipady_frame
            )
        # continuar aqui
        output_nome = ctk.CTkEntry(
            master=frame_auxiliar_2_0,
            text_color="black",
            width=len(nome_maior)*multiplicador_tamanho,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_nome.pack(padx=padx_texto, pady=3)
        output_nome.insert(0, i.nome)
        output_nome.configure(state="readonly")

        output_cpf = ctk.CTkEntry(
            master=frame_auxiliar_2_1,
            width=100,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_cpf.pack(padx=padx_texto, pady=3)
        output_cpf.insert(0, formatar_cpf(i.cpf))
        output_cpf.configure(state="readonly")

        output_numero = ctk.CTkEntry(
            master=frame_auxiliar_2_2,
            width=130,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_numero.pack(padx=padx_texto, pady=3)
        output_numero.insert(0, formatar_numero_celular(i.numero))
        output_numero.configure(state="readonly")

        output_email = ctk.CTkEntry(
            master=frame_auxiliar_2_3,
            width=len(email_maior)*multiplicador_tamanho,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_email.pack(padx=padx_texto, pady=3)
        output_email.insert(0, i.email)
        output_email.configure(state="readonly")

        output_data_nascimento = ctk.CTkEntry(
            master=frame_auxiliar_2_4,
            width=170,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_data_nascimento.pack(padx=padx_texto, pady=3)
        output_data_nascimento.insert(0, date.strftime(
            i.data_nascimento, "%d/%m/%Y"))
        output_data_nascimento.configure(state="readonly")

        output_idade = ctk.CTkEntry(
            master=frame_auxiliar_2_5,
            width=70,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_idade.pack(padx=padx_texto, pady=3)
        output_idade.insert(0, calcular_idade(i.data_nascimento))
        output_idade.configure(state="readonly")

        output_cep = ctk.CTkEntry(
            master=frame_auxiliar_2_6,
            width=80,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_cep.pack(padx=padx_texto, pady=3)
        output_cep.insert(0, formatar_cep(i.cep))
        output_cep.configure(state="readonly")

        output_estado = ctk.CTkEntry(
            master=frame_auxiliar_2_7,
            width=70,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_estado.pack(padx=padx_texto, pady=3)
        output_estado.insert(0, i.estado)
        output_estado.configure(state="readonly")

        output_cidade = ctk.CTkEntry(
            master=frame_auxiliar_2_8,
            width=len(cidade_maior)*multiplicador_tamanho,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_cidade.pack(padx=padx_texto, pady=3)
        output_cidade.insert(0, i.cidade)
        output_cidade.configure(state="readonly")

        output_bairro = ctk.CTkEntry(
            master=frame_auxiliar_2_9,
            width=len(bairro_maior)*multiplicador_tamanho,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_bairro.pack(padx=padx_texto, pady=3)
        output_bairro.insert(0, i.bairro)
        output_bairro.configure(state="readonly")

        output_rua = ctk.CTkEntry(
            master=frame_auxiliar_2_10,
            width=len(rua_maior)*multiplicador_tamanho,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_rua.pack(padx=padx_texto, pady=3)
        output_rua.insert(0, i.rua)
        output_rua.configure(state="readonly")

        output_numero_casa = ctk.CTkEntry(
            master=frame_auxiliar_2_11,
            width=120,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_numero_casa.pack(padx=padx_texto, pady=3)
        output_numero_casa.insert(0, i.numero_casa)
        output_numero_casa.configure(state="readonly")

        output_data_cadastro = ctk.CTkEntry(
            master=frame_auxiliar_2_12,
            width=130,
            height=26,
            fg_color="transparent",
            border_width=0
        )
        output_data_cadastro.pack(padx=padx_texto, pady=3)
        output_data_cadastro.insert(0, datetime.strftime(
            i.data_cadastro, "%d/%m/%Y %H:%M:%S"))
        output_data_cadastro.configure(state="readonly")

        botao_deletar = BotaoDelete(
            master=frame_auxiliar_2_13,
            text="x",
            fg_color="red",
            width=25,
            height=28,
            cpf=i.cpf,
            nome=i.nome,
            command=True,
            compound="right",
            hover=False
        )
        botao_deletar.pack(padx=padx_texto, pady=2, anchor="s")

        linha += 1

    texto_total = ctk.CTkLabel(
        master=tela_listar,
        text=f"Total: {quantidade_pessoas} pessoas cadastradas",
        font=("", 12, "bold")
    )
    texto_total.pack()

    botao_voltar = ctk.CTkButton(
        master=tela_listar,
        text="Voltar",
        command=lambda: menu(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar
            ))
    botao_voltar.pack()


def menu(
    tela_menu,
    tela_cadastro,
    tela_confirmacao,
    tela_listar: ctk.CTkScrollableFrame
) -> None:
    tela_cadastro.forget()
    tela_listar.pack_forget()
    tela_confirmacao.place_forget()

    tela_menu = ctk.CTkFrame(master=app, fg_color="transparent")
    tela_menu.place(relx=0.5, rely=0.5, anchor="center")

    frame_auxiliar = ctk.CTkFrame(master=tela_menu, corner_radius=20)
    frame_auxiliar.pack(ipadx=2.5, ipady=2.5)

    texto_menu = ctk.CTkLabel(
        master=frame_auxiliar,
        text="Menu Principal",
        font=("", 20, "bold"),
        width=200,
        height=40,
    )
    texto_menu.pack(padx=5, pady=4)

    botao_cadastro = ctk.CTkButton(
        master=frame_auxiliar,
        text="Cadastrar",
        command=lambda: cadastrar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar),
        width=200,
        corner_radius=20,
    )
    botao_cadastro.pack(padx=5, pady=4)

    botao_listar = ctk.CTkButton(
        master=frame_auxiliar,
        text="Listar",
        command=lambda: listar(
            tela_menu,
            tela_cadastro,
            tela_confirmacao,
            tela_listar
            ),
        width=200,
        corner_radius=20,
    )
    botao_listar.pack(padx=5, pady=4)

    botao_sair = ctk.CTkButton(
        master=frame_auxiliar,
        text="Sair",
        command=lambda: exit(),
        width=200,
        corner_radius=20,
    )
    botao_sair.pack(padx=5, pady=4)


if __name__ == "__main__":
    menu(tela_menu, tela_cadastro, tela_confirmacao, tela_listar)
    app.mainloop()
