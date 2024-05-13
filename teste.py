import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cadastros_informacoes'
)

if conexao.is_connected():
    print("Conectado ao MySQL!")

cursor = conexao.cursor()
verificacao = False
while not verificacao:
    switch = str(input(" \n1 - CREATE TABLE..."
                        "\n2 - UPDATE TABLE..."
                        "\n3 - ATUALIZAR......"
                        "\n4 - DELETE TABLE..."
                        "\n0 - SAIR...........\n" 
                    ))

    match switch:
        case "2":
            verificacao = False
            while not verificacao:
                
                email = input("\nINFORME SEU NOME....")
                nome  = input("\nINFORME SEU EMAIL...")
                senha = input("\nINFORME SUA SENHA...")
                
                if nome and senha and email:
                    confirmado = True
                    
                    create = 'INSERT INTO usuarios (email, nome, senha, confirmado) VALUES (%s, %s, %s, %s)'
                    valores = (nome, email, senha, confirmado)
                    
                    cursor.execute(create, valores)
                    conexao.commit()  # confirma a operação no banco de dados
                    print("\nSUCESSO NO CADASTRAMENTO!")
                    
                    stop = input("\nDESEJA SAIR? 'S' PARA SIM E 'N' PARA NÃO...").upper()
                    if stop == 'S':
                        verificacao = True
                    
                    else:
                        verificacao = False
                
                else:
                    stop = input("\nDESEJA SAIR? 'S' PARA SIM E 'N' PARA NÃO...").upper()
                    if stop == 'S':
                        verificacao = True
                    
                    else:
                        verificacao = False
                        print("\nPREENCHA TODOS OS CAMPOS...")
                        
    
                    
        case "3":
            comando = 'SELECT * FROM usuarios;'
            cursor.execute(comando)
            resultado = cursor.fetchall()
            print(resultado)
            stop = input("\nDESEJA SAIR? 'S' PARA SIM E 'N' PARA NÃO...").upper()
            if stop == 'S':
                verificacao = True
            else:
                verificacao = False
        
        case "1":
            campo = input("\nDESEJA ATULIZAR QUAL CAMPO?...")
            atualizar = input("\nQUAL O VALOR DO CAMPO?...")
            valor = input("\nDESEJA ATUALIZAR QUAL VALOR?...")
            valor_novo = input("\nINFORME O NOVO VALOR...")
            comando = f'UPDATE usuarios SET {campo} = "{atualizar}" WHERE {valor} = "{valor_novo}"'
            cursor.execute(comando)
            conexao.commit()
            
        case "4":
            campo = input("\nQUAL CAMPO DESEJA UTILIZAR O 'DELETE'...")
            condition = input("\nQUAL A CONDIÇÃO QUE DESEJA DELETAR?...")
            comando = f'DELETE FROM usuarios WHERE {campo} = {condition}'
        case"0":
            verificacao = True

    
cursor.close()
conexao.close()
print("Conexão fechada.")
