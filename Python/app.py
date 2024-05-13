import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurações do email
EMAIL_USUARIO = 'seu_email@gmail.com'  # Substitua pelo seu email
EMAIL_SENHA = 'sua_senha'  # Substitua pela sua senha

# Configurações do banco de dados MySQL
DB_HOST = 'localhost'  # Substitua pelo host do seu banco de dados
DB_USUARIO = 'root'  # Substitua pelo seu usuário do banco de dados
DB_SENHA = 'root'  # Substitua pela sua senha do banco de dados
DB_NOME = 'nome_do_banco'  # Substitua pelo nome do seu banco de dados

# Função para conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USUARIO,
        password=DB_SENHA,
        database=DB_NOME
    )

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = EMAIL_USUARIO
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USUARIO, EMAIL_SENHA)
        server.sendmail(EMAIL_USUARIO, destinatario, msg.as_string())

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(os.urandom(16), method='pbkdf2:sha256')

        try:
            db = conectar_db()
            cursor = db.cursor()
            
            # Verificar se o email já existe
            cursor.execute("SELECT 1 FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                return "Este email já está cadastrado."
            
            # Inserir novo usuário
            sql = "INSERT INTO usuarios (nome, email, senha, confirmado) VALUES (%s, %s, %s, %s)"
            val = (nome, email, senha, False)
            cursor.execute(sql, val)
            db.commit()

            # Gerar token de confirmação 
            token = os.urandom(16).hex()

            # Enviar email de confirmação
            link_confirmacao = url_for('confirmar', token=token, _external=True)
            enviar_email(email, 'Confirme seu Email', f'Clique aqui para confirmar: {link_confirmacao}')

            return 'Verifique seu email para confirmar sua conta.'

        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return "Ocorreu um erro. Tente novamente mais tarde."

        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    else:
        return render_template('registro.html')

@app.route('/confirmar/<token>')
def confirmar(token):
    try:
        db = conectar_db()
        cursor = db.cursor()

        # Encontrar o usuário com o token
        cursor.execute("SELECT id FROM usuarios WHERE confirmado = 0 AND token = %s", (token,))
        usuario = cursor.fetchone()

        if usuario:
            # Confirmar o usuário
            usuario_id = usuario[0]
            cursor.execute("UPDATE usuarios SET confirmado = 1, token = NULL WHERE id = %s", (usuario_id,))
            db.commit()
            return "Sua conta foi confirmada com sucesso!"
        else:
            return "Token inválido ou conta já confirmada."

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return "Ocorreu um erro. Tente novamente mais tarde."

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == '__main__':
    app.run(debug=True)