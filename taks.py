import redis
import os

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def generate_task_id():
    return r.incr("task_id")

def add_task(description):
    task_id = generate_task_id()
    r.hset(f"task:{task_id}", mapping={
        "id": task_id,
        "descricao": description,
        "checked": 0
    })
    print(f"Tarefa '{description}' adicionada com ID: {task_id}")

def edit_task(task_id, description):
    if r.exists(f"task:{task_id}"):
        r.hset(f"task:{task_id}", "descricao", description)
        print(f"Tarefa com ID: {task_id} atualizada!")
    else:
        print("Tarefa não encontrada.")

def delete_task(task_id):
    if r.exists(f"task:{task_id}"):
        r.delete(f"task:{task_id}")
        print(f"Tarefa com ID: {task_id} excluída!")
    else:
        print("Tarefa não encontrada.")

def complete_task(task_id):
    if r.exists(f"task:{task_id}"):
        r.hset(f"task:{task_id}", "checked", 1)
        print(f"Tarefa com ID: {task_id} marcada como concluída!")
    else:
        print("Tarefa não encontrada.")

def list_tasks(filter="all"):
    keys = r.keys("task:*")
    for key in keys:
        if r.exists(key):
            task = r.hgetall(key)
            if filter == "all" or (filter == "completed" and task[b"checked"] == b"1") or (filter == "pending" and task[b"checked"] == b"0"):
                status = "Concluída" if task[b"checked"] == b"1" else "Pendente"
                print(f"\n-----------------------------\nID: {task[b'id'].decode()}\nStatus: {status}\nDescrição: {task[b'descricao'].decode()}")
            else:
                print(f"Não existe tarefas para listar")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        print("\nMenu:")
        print("1. Adicionar Tarefa")
        print("2. Editar Tarefa")
        print("3. Excluir Tarefa")
        print("4. Marcar como Concluída")
        print("5. Listar Todas as Tarefas")
        print("6. Listar Tarefas Concluídas")
        print("7. Listar Tarefas Pendentes")
        print("8. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            description = input("Informe a descrição da tarefa: ")
            add_task(description)
        elif choice == "2":
            task_id = input("Informe o ID da tarefa: ")
            description = input("Informe a nova descrição: ")
            edit_task(task_id, description)
        elif choice == "3":
            task_id = input("Informe o ID da tarefa: ")
            delete_task(task_id)
        elif choice == "4":
            task_id = input("Informe o ID da tarefa: ")
            complete_task(task_id)
        elif choice == "5":
            list_tasks("all")
        elif choice == "6":
            list_tasks("completed")
        elif choice == "7":
            list_tasks("pending")
        elif choice == "8":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
