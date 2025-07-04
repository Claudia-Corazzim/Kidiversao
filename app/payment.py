"""
Módulo para gerenciar pagamentos com Mercado Pago e PIX
"""
import mercadopago
import json
from datetime import datetime
from flask import current_app, url_for, request
from app.payment_config import MERCADO_PAGO_ACCESS_TOKEN, MERCADO_PAGO_BACK_URL

class PaymentManager:
    """Gerenciador de pagamentos"""
    
    def __init__(self):
        self.sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
    
    def create_preference(self, booking, service, base_url):
        """Criar uma preferência de pagamento no Mercado Pago"""
        # Configurar URLs de retorno
        back_urls = {
            "success": f"{base_url}{url_for('main.payment_success', booking_id=booking.id)}",
            "failure": f"{base_url}{url_for('main.payment_failure', booking_id=booking.id)}",
            "pending": f"{base_url}{url_for('main.payment_pending', booking_id=booking.id)}"
        }
        
        # Configurar dados da preferência
        preference_data = {
            "items": [
                {
                    "title": service.name,
                    "description": service.description,
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": float(service.price)
                }
            ],
            "payer": {
                "email": booking.user.email
            },
            "back_urls": back_urls,
            "auto_return": "approved",
            "external_reference": str(booking.id),
            "payment_methods": {
                "excluded_payment_types": [],
                "installments": 1
            },
            "statement_descriptor": "Kidiversao"
        }
        
        # Criar a preferência
        preference_response = self.sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        return preference
    
    def get_payment_status(self, payment_id):
        """Obter o status de um pagamento"""
        payment_response = self.sdk.payment().get(payment_id)
        payment = payment_response["response"]
        
        return payment
    
    def generate_pix_qrcode(self, booking, service):
        """Gerar QR code PIX"""
        payment_data = {
            "transaction_amount": float(service.price),
            "description": f"Kidiversao - {service.name}",
            "payment_method_id": "pix",
            "payer": {
                "email": booking.user.email,
                "first_name": booking.user.username,
                "last_name": "",
                "identification": {
                    "type": "CPF",
                    "number": "12345678909"  # Exemplo, em produção use um CPF real
                }
            }
        }
        
        payment_response = self.sdk.payment().create(payment_data)
        payment = payment_response["response"]
        
        return payment
