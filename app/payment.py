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
                    "description": service.description or service.name,
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
        
        try:
            # Debug: imprimir dados enviados para o Mercado Pago
            print(f"Enviando dados para o Mercado Pago: {json.dumps(preference_data, indent=2)}")
            
            # Criar a preferência
            preference_response = self.sdk.preference().create(preference_data)
            
            # Debug: imprimir resposta do Mercado Pago
            print(f"Resposta do Mercado Pago: {json.dumps(preference_response, indent=2, default=str)}")
            
            # Verificar se a resposta foi bem-sucedida e contém os dados esperados
            if preference_response.get("status") == 201 and "response" in preference_response:
                preference = preference_response["response"]
                
                # Verificar se o campo 'id' existe
                if "id" not in preference:
                    print(f"ERRO: Campo 'id' não encontrado na resposta: {json.dumps(preference, indent=2, default=str)}")
                    # Criar um objeto de resposta de erro
                    return {
                        "id": "error",
                        "init_point": "#",
                        "error_message": "A resposta do Mercado Pago não contém o ID da preferência",
                        "status": "error"
                    }
                
                print(f"Preferência criada com sucesso. ID: {preference.get('id')}")
                return preference
            else:
                # Se houver erro na resposta
                error_message = preference_response.get('message', 'Erro desconhecido')
                print(f"Erro na resposta do Mercado Pago: {error_message}")
                print(f"Resposta completa: {json.dumps(preference_response, indent=2, default=str)}")
                
                return {
                    "id": "error",
                    "init_point": "#",
                    "error_message": f"Falha ao criar preferência de pagamento: {error_message}",
                    "status": "error"
                }
        except Exception as e:
            # Tratar exceções
            import traceback
            print(f"Exceção ao criar preferência: {str(e)}")
            print(traceback.format_exc())
            return {
                "id": "error",
                "init_point": "#",
                "error_message": f"Erro ao processar pagamento: {str(e)}",
                "status": "error"
            }
    
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
        
        try:
            payment_response = self.sdk.payment().create(payment_data)
            # Verificar se a resposta foi bem-sucedida
            if payment_response["status"] == 201:
                payment = payment_response["response"]
                return payment
            else:
                # Se houver erro na resposta
                print(f"Erro na resposta do Mercado Pago: {payment_response}")
                return {
                    "id": "error",
                    "status": "error",
                    "error_message": "Falha ao gerar QR Code PIX",
                    "point_of_interaction": None
                }
        except Exception as e:
            # Tratar exceções
            print(f"Exceção ao gerar PIX: {str(e)}")
            return {
                "id": "error",
                "status": "error",
                "error_message": str(e),
                "point_of_interaction": None
            }
