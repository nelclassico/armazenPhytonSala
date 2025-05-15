# Importa os módulos necessários do Flask
from flask import Flask, request, render_template, redirect, url_for, session, flash

import os

# Importa a classe Usuario e funções do models
from models import Usuario, get_db_connection, init_db
from functools import wraps

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configura uma chave secreta para a sessão (obrigatória para segurança)
app.secret_key = "chavealeatoria_muitosegura"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:        
            flash('Você precisa estar logado para acessar esta página', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



# Rota para a página inicial
@app.route('/')
def index():
   return render_template('index.html')

# Rota para login, aceita métodos GET (mostrar formulário) e POST (processar login)
@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        return redirect(url_for('index')) 
    
    # Se o método for POST, processa a tentativa de login
    if request.method == 'POST':
        # Obtém o username e senha do formulário
        username = request.form['username']
        senha = request.form['senha']

        # Tenta autenticar o usuário usando a classe Usuario
        user = Usuario.autenticar(username, senha)

        # Se a autenticação for bem-sucedida
        if user:
            # Armazena o username e função na sessão
            session['username'] = user.username
            session['funcao'] = user.funcao

            #mensagem de sucesso
            flash(f'Bem vindo, {user.nome}!', 'success')
            # Redireciona para a página inicial
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos!', 'error')
    
    # Se o método for GET, exibe o formulário de login
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    # Remove o username e função da sessão
    session.pop('username', None)
    session.pop('funcao', None)
    # Redireciona para a página inicial
    return redirect(url_for('index'))

# Rota para listar usuários (apenas para administradores)
@app.route('/usuarios')
def listar_usuarios():
    # Verifica se o usuário está logado e é administrador
    if 'username' in session and session['funcao'] == 'admin':
        # Obtém uma conexão com o banco de dados
        conn = get_db_connection()
        # Executa uma consulta para buscar todos os usuários
        usuarios = conn.execute('SELECT id_usuario, username, funcao, nome FROM usuarios').fetchall()
        # Fecha a conexão com o banco de dados
        conn.close()
        # Monta uma tabela HTML com os usuários
        html = '<h1>Usuários</h1><table border="1"><tr><th>ID</th><th>Username</th><th>Função</th><th>Nome</th></tr>'
        for usuario in usuarios:
            html += f'<tr><td>{usuario["id_usuario"]}</td><td>{usuario["username"]}</td><td>{usuario["funcao"]}</td><td>{usuario["nome"]}</td></tr>'
        html += '</table>'
        return html
    else:
        # Retorna mensagem de acesso negado para não administradores
        return 'Acesso negado. Você precisa ser um administrador para ver esta página. <a href="/login">Fazer login</a>'

# Inicia o servidor Flask em modo debug, acessível em todas as interfaces na porta 5001
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

    # Inicializa o banco de dados antes de executar a aplicação
init_db()