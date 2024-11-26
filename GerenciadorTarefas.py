from datetime import datetime
from uuid import uuid4
from tkinter import *
from tkinter import messagebox, simpledialog, PhotoImage
from PIL import Image

imagem_natal = None


class Task:
    # Classe com todos os atributos e metodos referentes as tarefas
    def __init__(self, task_id, task_name, prazo, data_criacao=None, status="Pendente"):
        self.task_id = task_id
        self.task_name = task_name
        self.deadline = prazo
        self.status = status
        self.data_criacao = (
            str(datetime.now().strftime("%d/%m/%Y"))
            if data_criacao == None
            else data_criacao
        )

    def detalhes(self):
        return f"ID: {self.task_id}\nNome: {self.task_name}\nPrazo: {self.deadline}\nStatus: {self.status}\nTarefa criada em {self.data_criacao}"

    def detalhes2(self):
        return f"Nome: {self.task_name}   Status: {self.status}"


class TaskManager:
    # Classe com todos os atributos e metodos referentes ao gerenciador de tarefas
    def __init__(self, master: Tk):
        # Cria a interface gráfica para o usuário
        self.master = master
        self.master.geometry("600x400")
        self.master.minsize(600, 400)
        self.master.maxsize(700, 500)
        self.master.title("Task Manager")
        self.lista_tarefas = []
        self.atributos_dict = {"titulo": "task_name", "prazo": "deadline"}
        # Try Except para caso haja algum erro de leitura
        try:
            with open("Tasks.csv", "r") as arquivo:
                tarefas = arquivo.readlines()

            for tarefa in tarefas:
                valores = tarefa.strip().split(",")
                if len(valores) == 5:
                    id, nome, prazo, data_criacao, status = valores
                    task = Task(id, nome, prazo, data_criacao, status)
                    self.lista_tarefas.append(task)
        except Exception as e:
            messagebox.showerror(
                "Erro de Leitura", f"Ocorreu um erro ao ler o arquivo: {e}"
            )
        self.criar_interface()

    def data_valida(self, data):
        try:
            # Faz o split e transforma em números
            dia, mes, ano = map(int, data.split("/"))

            # Cria um objeto de data para a data fornecida
            data_fornecida = datetime(ano, mes, dia).date()

            # Obtém a data atual
            data_atual = datetime.now().date()

            # Compara se a data fornecida é menor que a data atual
            if data_fornecida < data_atual:
                return False

            # Mês ou ano inválido (só considera do ano 1 em diante), retorna False
            if mes < 1 or mes > 12 or ano <= 0:
                return False

            # Verifica qual o último dia do mês
            if mes in (1, 3, 5, 7, 8, 10, 12):
                ultimo_dia = 31
            elif mes == 2:
                # Verifica se é ano bissexto
                if (ano % 4 == 0) and (ano % 100 != 0 or ano % 400 == 0):
                    ultimo_dia = 29
                else:
                    ultimo_dia = 28
            else:
                ultimo_dia = 30

            # Verifica se o dia é válido
            if dia < 1 or dia > ultimo_dia:
                return False

            return True
        except ValueError:
            # Se ocorrer um erro ao converter para int, a data é inválida
            return False

    def criar_interface(self):
        def reproduzir_gif():
            # Função para reproduzir um GIF em uma nova janela
            janela_gif = Toplevel(self.master)
            janela_gif.title("FELIZ NATAL!!!")

            caminho = "leader.gif"
            gif = Image.open(caminho)
            frames = [
                PhotoImage(file=caminho, format=f"gif -index {i}")
                for i in range(gif.n_frames)
            ]

            label_gif = Label(janela_gif)
            label_gif.pack()

            def update_frame(count=0):
                novo_frame = frames[count]
                label_gif.configure(image=novo_frame)
                count += 1
                if count == gif.n_frames:
                    count = 0
                janela_gif.after(50, lambda: update_frame(count))

            update_frame()

        def sair():
            # Adiciona os botões sim, não e confirmar
            radio_nao.pack()
            radio_sim.pack()
            btn_confirmar.pack()

        def confirmar_saida():
            # Fecha a janela do tkinter caso var seja 1
            if var.get() == 1:
                self.master.destroy()
            else:
                # Caso o var seja igual a 0(não) ele apaga os botões sim, não e confirmar
                radio_nao.forget()
                radio_sim.forget()
                btn_confirmar.forget()

        def ajuda():
            # Exibe uma mensagem que guia uma pessoa a usar o gerenciador de tarefas
            mensagem = """Bem-vindo ao Task Manager!\n\nEste é um aplicativo simples para gerenciar suas tarefas. Aqui estão algumas dicas úteis:\n\n1. Adicionar Tarefa: Clique em "Adicionar Tarefa" para inserir uma nova tarefa. Você será solicitado a fornecer o nome e o prazo.\n\n2. Marcar como Concluída: Selecione uma tarefa na lista e clique em "Marcar como Concluída" para indicar que a tarefa foi concluída.\n\n3. Editar Tarefa: Escolha uma tarefa na lista, clique em "Editar Tarefa" e selecione se deseja editar o nome ou a data da tarefa.\n\n4. Deletar Tarefa: Selecione uma tarefa na lista e clique em "Deletar Tarefa" para remover a tarefa.\n\n5. Detalhes da Tarefa: Clique duas vezes em uma tarefa na lista para ver todos os detalhes.\n\n6. Sair: Ao clicar em "Sair", você será perguntado se deseja sair. Escolha "sim" para fechar o aplicativo.\n\nEspero que essas dicas facilitem o uso do Task Manager. Boa organização!"""

            messagebox.showinfo("Ajuda", mensagem)

        def deletar_tarefa():
            # Deleta uma tarefa atráves do index que se encontra a tarefa selecionada
            selected_index = self.lista_box.curselection()
            if selected_index:
                # Cria um pop up que pergunta se o usuário deseja realmente deletar a tarefa
                resposta = messagebox.askquestion(
                    "Confirmar",
                    f"Tem certeza que deseja deletar a tarefa {self.lista_tarefas[selected_index[0]].task_name}?",
                    icon="warning",
                )
                if resposta == "yes":
                    self.lista_tarefas.pop(selected_index[0])
                    self.atualizar_arquivo()
                    self.atualizar_tkinter()
                    messagebox.showinfo(
                        "Deletada",
                        f"A tarefa foi deletada com sucesso!",
                    )
                else:
                    messagebox.showinfo(
                        "Aviso",
                        f"A tarefa {self.lista_tarefas[selected_index[0]].task_name} não foi deletada",
                    )

        def adicionar_tarefa():
            # Adiciona uma tarefa, com input do usuário
            nome = simpledialog.askstring(
                "Adicionar Tarefa", "Digite o nome da tarefa:", parent=self.master
            )
            # Verifica se o nome foi digitado
            if nome and nome.strip():
                for task in self.lista_tarefas:
                    if task.task_name == nome:
                        messagebox.showerror("Error", "Ja tem uma tarefa com esse nome")
                        return
                prazo = simpledialog.askstring(
                    "Adicionar Tarefa",
                    "Digite o prazo da tarefa (dd/mm/yyyy):",
                    parent=self.master,
                )
                # Verifica se o prazo é de uma data valida(maior que a do dia de hoje ou igual o dia de hoje)
                if self.data_valida(prazo):
                    task = Task(str(uuid4()), nome, prazo)
                    self.lista_tarefas.append(task)
                    self.atualizar_arquivo()
                    self.atualizar_tkinter()
                    messagebox.showinfo(
                        "Adicionada", "Sua tarefa foi adicionada com sucesso!"
                    )
                else:
                    messagebox.showerror("Error", "Data inválida")
            else:
                messagebox.showerror("Error", "Nome inválido")

        def marcar_concluido():
            # Caso a tarefa esteja pendente, troca o status para concluida
            selected_index = self.lista_box.curselection()
            if selected_index:
                selected_task = self.lista_tarefas[selected_index[0]]
                if selected_task.status == "Pendente":
                    selected_task.status = "Concluida"
                    self.atualizar_arquivo()
                    self.atualizar_tkinter()
                    message = "Parabéns você concluiu sua tarefa"
                    if self.data_valida(selected_task.deadline) == False:
                        message = "Você concluiu a tarefa, porém a data de conclusão já expirou"
                    messagebox.showinfo(
                        "Concluída", message
                    )
                else:
                    resposta = messagebox.askquestion(
                        "Confirmar",
                        f"Tem certeza que deseja deixar pendente a tarefa {self.lista_tarefas[selected_index[0]].task_name}?",
                        icon="warning",
                    )
                    if resposta == 'yes' and self.data_valida(selected_task.deadline):
                        selected_task.status = "Pendente"
                        self.atualizar_arquivo()
                        self.atualizar_tkinter()
                        messagebox.showinfo('Tarefa pendente novamente', 'Atenção, sua tarefa está pendente novamente, terá que conclui-la de novo')
                    elif resposta == 'no':
                        pass
                    else:
                        messagebox.showerror('Data expirada', 'A data de conlusão da sua tarefa já expirou.')

        def editar_nome(tarefa):
            # Pergunta ao usuário qual novo nome que ele deseja
            nome = simpledialog.askstring(
                "Novo nome", "Digite um novo nome para a tarefa: ", parent=self.master
            )
            # Verifica se o usuário digitou um nome ou deixou em branco
            if nome is not None and nome.strip():
                for i in self.lista_tarefas:
                    if i.task_name == nome:
                        messagebox.showerror("Error", "Já tem uma tarefa com esse nome")
                        return
                tarefa.task_name = nome
                self.atualizar_arquivo()
                self.atualizar_tkinter()
                messagebox.showinfo("Edição", "Sua tarefa foi editada com êxito")
                # Feche a janela Toplevel após a edição
                self.janela_edicao.destroy()
            else:
                self.janela_edicao.destroy()
                messagebox.showerror("Nome", "Nenhum nome foi digitado")

        def editar_data(tarefa):
            # Pergunta ao usuário para qual data deseja alterar
            data = simpledialog.askstring(
                "Nova Data", "Digite uma nova data(dd/mm/aaaa): ", parent=self.master
            )
            # Verifica se a data é válida
            if self.data_valida(data):
                tarefa.deadline = data
                self.atualizar_arquivo()
                self.atualizar_tkinter()
                messagebox.showinfo("Edição", "Sua tarefa foi editada com êxito")
                # Feche a janela Toplevel após a edição
                self.janela_edicao.destroy()
            else:
                self.janela_edicao.destroy()
                messagebox.showerror("Error", "Data inválida")

        def abrir_janela_edicao(tarefa):
            # Cria uma única janela Toplevel
            self.janela_edicao = Toplevel()
            self.janela_edicao.geometry("300x200")
            self.janela_edicao.title("Edição Tarefa")
            Label(self.janela_edicao, text="Escolha uma opção para editar: ").pack(
                pady=10
            )

            # Cria dois botões para selecionar oque deseja editar e chama a função respectiva dependendo do botão que foi clicado
            btn_nome = Button(
                self.janela_edicao, text="Nome", command=lambda: editar_nome(tarefa)
            )
            btn_nome.pack(pady=20, padx=10)

            btn_data = Button(
                self.janela_edicao, text="Data", command=lambda: editar_data(tarefa)
            )
            btn_data.pack(pady=20, padx=40)

        def editar_tarefa():
            # Edita o nome ou a data da tarefa, dependendo da escolha do usuário
            selected_index = self.lista_box.curselection()
            if selected_index:
                edicao = self.lista_tarefas[selected_index[0]]
                if edicao.status == "Concluida":
                    messagebox.showerror("Error", "Tarefa já concluída")
                    return

                # Chama a função para abrir a janela de edição
                abrir_janela_edicao(edicao)

        # Cria um frame a esquerda na qual ficam os botões do codigo
        botoes = Frame(self.master, bg="#C89F9C")
        botoes.pack(side="left", fill="y")

        # Cria os botões e da comando a eles
        btn_adicionar = Button(
            botoes,
            text="Adicionar Tarefa",
            command=adicionar_tarefa,
            bg="#EEE2DF",
            font=("Arial", 10),
        )
        btn_concluir = Button(
            botoes,
            text="Marcar como Concluída",
            command=marcar_concluido,
            bg="#EEE2DF",
            font=("Arial", 10),
        )
        btn_editar = Button(
            botoes,
            text="Editar Tarefa",
            command=editar_tarefa,
            bg="#EEE2DF",
            font=("Arial", 10),
        )
        btn_deletar = Button(
            botoes,
            text="Deletar Tarefa",
            command=deletar_tarefa,
            bg="#EEE2DF",
            font=("Arial", 10),
        )
        btn_ajuda = Button(
            botoes, text="Ajuda", command=ajuda, bg="#EEE2DF", font=("Arial", 10)
        )
        btn_sair = Button(
            botoes, text="Sair", command=sair, bg="#EEE2DF", font=("Arial", 10)
        )
        btn_confirmar = Button(
            botoes,
            text="Confirmar",
            command=confirmar_saida,
            bg="#C89F9C",
            font=("Arial", 10),
        )
        btn_natal = Button(
            botoes,
            text="Feliz Natal!!!",
            command=reproduzir_gif,
            bg="#EEE2DF",
            font=("Arial", 10),
        )

        # Cria dois radiobuttons e atribui um valor para cada
        var = IntVar()
        radio_sim = Radiobutton(botoes, text="sim", variable=var, value=1, bg="#C89F9C")
        radio_nao = Radiobutton(botoes, text="não", variable=var, value=0, bg="#C89F9C")

        # Adicona os botões
        btn_adicionar.pack(fill="both")
        btn_concluir.pack(fill="both")
        btn_editar.pack(fill="both")
        btn_deletar.pack(fill="both")
        btn_ajuda.pack(fill="both")
        btn_sair.pack(fill="both")
        btn_natal.pack(fill="both")

        # Cria uma lista que armazena as tarefas
        self.lista_box = Listbox(
            self.master, selectmode=SINGLE, height=50, font=("sans", 10), bg="#EED7C5"
        )
        self.lista_box.pack(side="right", fill="both", expand=True)
        self.scrollbar = Scrollbar(
            self.master, orient=VERTICAL, command=self.lista_box.yview
        )
        self.lista_box.config(yscrollcommand=self.scrollbar.set)
        lista = self.exibirTarefas()
        for i in lista:
            self.lista_box.insert(END, i)
        # Define o comando para exibir as informações da tarefa clicada
        self.lista_box.bind("<Double-1>", self.exibir_tarefa)
        self.lista_box.pack(side=LEFT, fill="both")
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def exibir_tarefa(self, event):
        # Ao clicar duas vezes numa tarefa, abre uma aba com mais detalhamento sobre a tarefa que foi clicada
        selected_index = self.lista_box.curselection()
        if selected_index:
            selected_task = self.lista_tarefas[selected_index[0]]
            detalhes = selected_task.detalhes()
            messagebox.showinfo("Detalhes da Tarefa", detalhes)

    def exibirTarefas(self):
        # Percorre lista das tarefas e armazena os detalhes de cada tarefa em uma lista
        lista = []
        for i in self.lista_tarefas:
            lista.append(i.detalhes2())
        return lista

    def atualizar_tkinter(self):
        # Atualiza a interface do tkinter após alterar ou criar uma tarefa
        self.lista_box.delete(0, END)
        for i in self.lista_tarefas:
            self.lista_box.insert(END, i.detalhes2())

    def atualizar_arquivo(self):
        # Atualiza os arquivos ao fazer alguma alteração nas tarefas ou em criar uma
        with open("Tasks.csv", "w") as arquivo:
            for task in self.lista_tarefas:
                arquivo.write(
                    f"\n{task.task_id},{task.task_name},{task.deadline},{task.data_criacao},{task.status}"
                )


# Inicia o mainloop
if __name__ == "__main__":
    master = Tk()
    app = TaskManager(master)
    mainloop()
