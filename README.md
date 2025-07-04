# Kidiversão - Sistema de Gerenciamento de Festas Infantis
Desenvolvimento de um software com framrwork web que utilize banco de dados inclua script web (Javascript), nuvem, uso de API, acessibilidade, controle de versões e testes.

Desenvolvimento de um sistema web com framework Flask que utiliza banco de dados PostgreSQL, JavaScript, autenticação de usuários, e interfaces responsivas com Bootstrap.

## 📋 Descrição

O Kidiversão é um sistema web para gerenciamento de serviços e pacotes para festas infantis. A plataforma permite que prestadores de serviços cadastrem seus produtos e serviços, enquanto clientes podem visualizar, reservar e contratar estes serviços.

## 🚀 Funcionalidades

- **Gerenciamento de Serviços**: Cadastro, edição, visualização e exclusão de serviços para festas.
- **Gerenciamento de Pacotes**: Criação de pacotes personalizados combinando diferentes serviços.
- **Sistema de Reservas**: Clientes podem fazer reservas de serviços e pacotes.
- **Pagamentos Online**: Integração com Mercado Pago para pagamentos via cartão, boleto e PIX.
- **Autenticação de Usuários**: Sistema de registro e login para clientes e prestadores.
- **Interface Responsiva**: Design adaptável a diferentes dispositivos usando Bootstrap.
- **Flash Messages**: Feedback visual para operações realizadas no sistema.
- **Acessibilidade**: Implementações seguindo diretrizes WCAG para garantir inclusão digital.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3 com Flask
- **Banco de Dados**: PostgreSQL com SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Autenticação**: Flask-Login
- **Migrações de Banco**: Flask-Migrate com Alembic
- **Pagamentos**: API Mercado Pago (cartão, boleto e PIX)
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

4. Configure as credenciais do Mercado Pago:
   - Crie uma conta no [Mercado Pago](https://www.mercadopago.com.br/)
   - Obtenha suas credenciais de teste no [Painel de Desenvolvedores](https://www.mercadopago.com.br/developers)
   - Atualize as credenciais no arquivo `app/payment_config.py`

5. Configure o banco de dados:
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

## 💸 API de Pagamentos

O Kidiversão integra a API do Mercado Pago para oferecer diversas opções de pagamento:

- **Checkout Pro**: Interface completa de pagamento do Mercado Pago
- **Pagamento via PIX**: Geração de QR Code para pagamento instantâneo
- **Webhook**: Recebimento de notificações de pagamento em tempo real
- **Callbacks**: URLs para redirecionamento após o pagamento (sucesso/falha/pendente)

A integração com o Mercado Pago permite:

1. **Criação de Preferências**: Configuração dos detalhes do pagamento
2. **Checkout Transparente**: Experiência de pagamento sem sair do site
3. **Geração de QR Code PIX**: Pagamento instantâneo usando PIX
4. **Consulta de Status**: Verificação do status de pagamentos
5. **Notificações em Tempo Real**: Webhook para atualizações automáticas

Para testar pagamentos no ambiente de desenvolvimento, utilize os [cartões de teste](https://www.mercadopago.com.br/developers/pt/docs/checkout-api/test-integration) fornecidos pelo Mercado Pago.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.