"""
Configurações para integração com o Mercado Pago
"""

# Credenciais do Mercado Pago - Versão atualizada Julho 2025
# Utilizando tokens de produção (sandbox) em vez de tokens de teste
MERCADO_PAGO_PUBLIC_KEY = "APP_USR-7eb0138a-189f-4bec-87d1-c0504ead5626"
MERCADO_PAGO_ACCESS_TOKEN = "APP_USR-7399425281055906-070523-39a8c55f3963e558822e050f8485b138-1607370319"

# Configurações de usuários de teste
TEST_USERS = {
    "vendedor": {
        "user_id": "TESTUSER1133005777",
        "password": "UMdozFQDUU"
    },
    "comprador": {
        "user_id": "TETE7163752", 
        "password": "M4E7MoJX7g"
    }
}

# Credenciais anteriores (manter como backup)
# MERCADO_PAGO_PUBLIC_KEY = "TEST-743dd07f-5fbd-42ac-9bd8-e38e3eba5d21"
# MERCADO_PAGO_ACCESS_TOKEN = "TEST-7399425281055906-052511-18f902b7d20e483d5e69a8da114a3ab3-1607370319"

# Configurações gerais
MERCADO_PAGO_BACK_URL = {
    "success": "/payment/success",
    "failure": "/payment/failure",
    "pending": "/payment/pending"
}

# Mensagens
PAYMENT_MESSAGES = {
    "success": "Pagamento processado com sucesso!",
    "pending": "Pagamento em processamento.",
    "failure": "Houve um problema com o pagamento."
}
