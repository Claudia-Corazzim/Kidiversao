# Kidiversão - Sistema de Gerenciamento de Festas Infantis

Desenvolvimento de um software com framework web que utiliza banco de dados, inclui script web (Javascript), nuvem, acessibilidade, controle de versões e testes.

## 📋 Descrição

O Kidiversão é um sistema web para gerenciamento de serviços e pacotes para festas infantis. A plataforma permite que prestadores de serviços cadastrem seus produtos e serviços, enquanto clientes podem visualizar, reservar e contratar estes serviços.

## 🚀 Funcionalidades

- **Gerenciamento de Serviços**: Cadastro, edição, visualização e exclusão de serviços para festas.
- **Gerenciamento de Pacotes**: Criação de pacotes personalizados combinando diferentes serviços.
- **Sistema de Reservas**: Clientes podem fazer reservas de serviços e pacotes.
- **Pagamentos Online**: Estrutura preparada para integração com gateways de pagamento.
- **Autenticação de Usuários**: Sistema de registro e login para clientes e prestadores.
- **Interface Responsiva**: Design adaptável a diferentes dispositivos usando Bootstrap.
- **Flash Messages**: Feedback visual para operações realizadas no sistema.
- **Acessibilidade**: Implementações seguindo diretrizes WCAG para garantir inclusão digital.

## 🎯 Requisitos Atendidos

- ✅ **Framework Web**: Flask (Python)
- ✅ **Banco de Dados**: PostgreSQL com SQLAlchemy
- ✅ **JavaScript**: Interatividade e validação de formulários
- ✅ **Nuvem**: Deploy na plataforma Render
- ✅ **API**: Preparado para integração com APIs de pagamento
- ✅ **Acessibilidade**: WCAG 2.1 AA compliance
- ✅ **Controle de Versões**: Git/GitHub
- ✅ **Testes**: Testes automatizados com Pytest

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3 com Flask
- **Banco de Dados**: PostgreSQL com SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Autenticação**: Flask-Login
- **Migrações de Banco**: Flask-Migrate com Alembic
- **Pagamentos**: Estrutura preparada para integração com gateways de pagamento
- **Controle de Versão**: Git e GitHub
- **Acessibilidade**: ARIA, elementos semânticos HTML5

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

## ♿ Acessibilidade

O Kidiversão foi desenvolvido com foco em acessibilidade digital, seguindo as diretrizes WCAG (Web Content Accessibility Guidelines) para garantir uma experiência inclusiva:

- **Estrutura Semântica**: Uso correto de elementos HTML5 semânticos (header, nav, main, section, etc.)
- **Atributos ARIA**: Implementação de atributos ARIA para melhorar a navegação por leitores de tela
- **Contraste de Cores**: Cores com contraste adequado para facilitar a leitura por pessoas com deficiência visual
- **Navegação por Teclado**: Possibilidade de navegar por todas as funcionalidades usando apenas o teclado
- **Textos Alternativos**: Imagens com descrições adequadas através do atributo alt
- **Mensagens de Feedback**: Notificações claras e acessíveis para todas as ações realizadas no sistema
- **Formulários Acessíveis**: Labels associados corretamente a campos de formulário e mensagens de erro descritivas
- **Responsividade**: Design adaptável a diferentes dispositivos e configurações de tela
- **Linguagem Simples**: Textos claros e diretos para facilitar a compreensão

Estas implementações seguem as recomendações do WCAG 2.1 níveis A e AA, tornando o sistema acessível para pessoas com diversas necessidades e habilidades.

## 🌐 Deploy em Nuvem

O projeto está hospedado na plataforma Render:
- **URL**: [https://kidiversao.onrender.com](https://kidiversao.onrender.com)
- **Banco de Dados**: PostgreSQL em nuvem gerenciado pelo Render

### Configuração para Deploy:

1. **Arquivos de Configuração**:
   - `requirements.txt` - Dependências do projeto
   - `Procfile` - Configuração do servidor web (Gunicorn)
   - `render.yaml` - Configuração automática do Render

2. **Variáveis de Ambiente**:
   - `FLASK_ENV=production`
   - `SECRET_KEY` (gerado automaticamente)
   - `DATABASE_URL` (configurado pelo Render)

## 💸 Pagamentos

O sistema Kidiversão está preparado para integração com diversos gateways de pagamento:

- **Estrutura de Dados**: Modelo de banco de dados com campos preparados para registrar transações
- **Fluxo de Pagamento**: Rotas implementadas para lidar com o processo de pagamento
- **Templates**: Interface de usuário pronta para exibir opções de pagamento
- **Callbacks**: Sistema preparado para receber notificações de status de pagamento
- **Flexibilidade**: Facilmente adaptável para diversos gateways como Mercado Pago, PayPal, Stripe, etc.

Para integrar seu gateway de pagamento preferido:
1. Adicione a biblioteca da API do gateway ao arquivo `requirements.txt`
2. Crie um módulo com os métodos de comunicação com a API do gateway
3. Atualize as rotas de pagamento para usar os métodos do seu módulo
4. Configure os callbacks para receber notificações de pagamento

## 🧪 Testes Automatizados

O projeto inclui testes automatizados usando Pytest:

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Executar testes
pytest
```

### Tipos de Testes Implementados:
- **Testes de Unidade**: Validação de modelos e funções individuais
- **Testes de Integração**: Verificação de fluxos completos da aplicação
- **Testes de Rotas**: Validação de endpoints HTTP

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.