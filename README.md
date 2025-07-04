# Kidiversão - Sistema de Gerenciamento de Festas Infantis

Desenvolvimento de um sistema web com framework Flask que utiliza banco de dados PostgreSQL, JavaScript, autenticação de usuários, e interfaces responsivas com Bootstrap.

## 📋 Descrição

O Kidiversão é um sistema web para gerenciamento de serviços e pacotes para festas infantis. A plataforma permite que prestadores de serviços cadastrem seus produtos e serviços, enquanto clientes podem visualizar, reservar e contratar estes serviços.

## 🚀 Funcionalidades

- **Gerenciamento de Serviços**: Cadastro, edição, visualização e exclusão de serviços para festas.
- **Gerenciamento de Pacotes**: Criação de pacotes personalizados combinando diferentes serviços.
- **Sistema de Reservas**: Clientes podem fazer reservas de serviços e pacotes.
- **Autenticação de Usuários**: Sistema de registro e login para clientes e prestadores.
- **Interface Responsiva**: Design adaptável a diferentes dispositivos usando Bootstrap.
- **Flash Messages**: Feedback visual para operações realizadas no sistema.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3 com Flask
- **Banco de Dados**: PostgreSQL com SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Autenticação**: Flask-Login
- **Migrações de Banco**: Flask-Migrate com Alembic
- **Controle de Versão**: Git e GitHub

## 📦 Estrutura do Projeto

```
kidiversao/
│
├── app/                    # Pacote principal da aplicação
│   ├── __init__.py         # Inicialização da aplicação Flask
│   ├── models.py           # Modelos de dados (ORM)
│   ├── routes.py           # Rotas e controladores
│   ├── static/             # Arquivos estáticos (CSS, JS)
│   └── templates/          # Templates HTML
│
├── migrations/             # Migrações do banco de dados
├── config.py               # Configurações da aplicação
├── create_test_users.py    # Script para criar usuários de teste
├── requirements.txt        # Dependências do projeto
└── run.py                  # Script para executar o servidor
```

## 🔧 Instalação e Execução

1. Clone o repositório:
   ```
   git clone https://github.com/Claudia-Corazzim/Kidiversao.git
   cd kidiversao
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o banco de dados:
   ```
   flask db upgrade
   ```

5. Crie usuários de teste (opcional):
   ```
   python create_test_users.py
   ```

6. Execute a aplicação:
   ```
   python run.py
   ```

7. Acesse no navegador:
   ```
   http://localhost:5000
   ```

## 👥 Usuários de Teste

- **Administrador**:
  - Email: admin@kidiversao.com
  - Senha: admin123

- **Usuário comum**:
  - Email: usuario@teste.com
  - Senha: senha123

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.