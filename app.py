from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

# Cria a instância do aplicativo Flask
app = Flask(__name__)
# Configura o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)

# Define a classe do modelo de dados para o banco de dados
class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    # A senha é salva como um hash SHA-256 para segurança
    password_hash = db.Column(db.String(256), nullable=False)
    
    def __repr__(self):
        return f'<Credential {self.site}>'

# Cria o banco de dados e a tabela se eles não existirem
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtém os dados do formulário
        site = request.form['site']
        username = request.form['username']
        raw_password = request.form['password']
        
        # Cria um hash SHA-256 da senha antes de salvá-la
        hashed_password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        
        # Cria um novo objeto Credential e adiciona ao banco de dados
        new_credential = Credential(site=site, username=username, password_hash=hashed_password)
        db.session.add(new_credential)
        db.session.commit()
        
        # Redireciona para a página inicial para mostrar a lista atualizada
        return redirect(url_for('index'))
    
    # Busca todas as credenciais do banco de dados para exibir
    credentials = Credential.query.all()
    return render_template('index.html', credentials=credentials)

if __name__ == '__main__':
    # Obtém a porta do ambiente ou usa 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=port, debug=True)
