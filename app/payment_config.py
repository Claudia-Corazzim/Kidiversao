"""
Configurações para integração com o Mercado Pago
"""

# Credenciais do Mercado Pago (substitua por suas credenciais reais quando for para produção)
# Estas são credenciais de teste atualizadas, você deve obter suas próprias no Dashboard do Mercado Pago
MERCADO_PAGO_PUBLIC_KEY = "TEST-743dd07f-5fbd-42ac-9bd8-e38e3eba5d21"
MERCADO_PAGO_ACCESS_TOKEN = "TEST-7399425281055906-052511-18f902b7d20e483d5e69a8da114a3ab3-1607370319"

# Para testar, você também pode usar estas credenciais alternativas caso as acima não funcionem
# MERCADO_PAGO_PUBLIC_KEY = "TEST-bb6c3a5d-662c-4b7d-b15c-94e8f482d732"
# MERCADO_PAGO_ACCESS_TOKEN = "TEST-2145556447344029-110222-2d6b1511f8607afd33e8e945b656e9e7-1461559219"

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
