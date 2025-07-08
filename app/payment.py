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
        self._test_connection()
        
    def _test_connection(self):
        """Testar conexão com o Mercado Pago"""
        try:
            # Tenta obter informações básicas para verificar a conexão
            response = self.sdk.payment().get_payment_methods()
            
            if response.get("status") != 200:
                print(f"AVISO: Conexão com Mercado Pago não está funcionando corretamente. Resposta: {response}")
                print(f"Detalhes da resposta: {json.dumps(response, indent=2, default=str)}")
                return False
            else:
                print("Conexão com Mercado Pago estabelecida com sucesso.")
                print(f"Método(s) de pagamento disponíveis: {len(response.get('response', []))}")
                return True
                
        except Exception as e:
            import traceback
            print(f"ERRO ao testar conexão com Mercado Pago: {str(e)}")
            print(traceback.format_exc())
            return False
    
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
                error_detail = preference_response.get('error', '')
                error_cause = ''
                
                # Tentar extrair causas mais detalhadas do erro
                if 'cause' in preference_response:
                    if isinstance(preference_response['cause'], list) and len(preference_response['cause']) > 0:
                        error_cause = json.dumps(preference_response['cause'])
                    elif isinstance(preference_response['cause'], dict):
                        error_cause = json.dumps(preference_response['cause'])
                    else:
                        error_cause = str(preference_response['cause'])
                
                print(f"Erro na resposta do Mercado Pago: {error_message}")
                print(f"Detalhes do erro: {error_detail}")
                print(f"Causa do erro: {error_cause}")
                print(f"Resposta completa: {json.dumps(preference_response, indent=2, default=str)}")
                
                error_msg = f"Falha ao criar preferência de pagamento: {error_message}"
                if error_detail:
                    error_msg += f" - {error_detail}"
                if error_cause:
                    error_msg += f" (Causa: {error_cause})"
                
                return {
                    "id": "error",
                    "init_point": "#",
                    "error_message": error_msg,
                    "status": "error"
                }
        except Exception as e:
            # Tratar exceções
            import traceback
            print(f"Exceção ao criar preferência: {str(e)}")
            print(traceback.format_exc())
            
            # Verificar se é um erro de conexão ou API
            error_message = str(e)
            detailed_error = error_message
            
            # Tentar extrair mais detalhes da exceção
            if hasattr(e, 'response') and e.response:
                try:
                    response_text = e.response.text
                    print(f"Texto da resposta de erro: {response_text}")
                    response_json = json.loads(response_text)
                    if 'message' in response_json:
                        detailed_error = response_json['message']
                    if 'error' in response_json:
                        detailed_error += f" - {response_json['error']}"
                except:
                    pass
            
            if "ConnectionError" in error_message or "timeout" in error_message.lower():
                error_message = "Falha de conexão com o Mercado Pago. Verifique sua conexão com a internet."
            elif "401" in error_message:
                error_message = "Credenciais inválidas para o Mercado Pago. Verifique o token de acesso."
            elif "400" in error_message:
                error_message = "Requisição inválida para o Mercado Pago. Verifique os dados enviados."
            elif "500" in error_message:
                error_message = "Erro interno do servidor do Mercado Pago. Tente novamente mais tarde."
            
            # Adicionar detalhes do erro original para depuração
            error_message += f" | Detalhes técnicos: {detailed_error}"
            
            return {
                "id": "error",
                "init_point": "#",
                "error_message": f"Erro ao processar pagamento: {error_message}",
                "status": "error"
            }
    
    def get_payment_status(self, payment_id):
        """Obter o status de um pagamento"""
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            # Debug: imprimir resposta do Mercado Pago
            print(f"Resposta do status de pagamento: {json.dumps(payment_response, indent=2, default=str)}")
            
            if payment_response.get("status") == 200 and "response" in payment_response:
                payment = payment_response["response"]
                return payment
            else:
                print(f"Erro ao obter status do pagamento: {payment_response}")
                return {
                    "status": "error",
                    "message": "Falha ao obter status do pagamento"
                }
        except Exception as e:
            print(f"Exceção ao obter status do pagamento: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }
    
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
            # Debug: imprimir dados enviados para o Mercado Pago
            print(f"Enviando dados PIX para o Mercado Pago: {json.dumps(payment_data, indent=2)}")
            
            payment_response = self.sdk.payment().create(payment_data)
            
            # Debug: imprimir resposta do Mercado Pago
            print(f"Resposta PIX do Mercado Pago: {json.dumps(payment_response, indent=2, default=str)}")
            
            # Verificar se a resposta foi bem-sucedida
            if payment_response.get("status") == 201 and "response" in payment_response:
                payment = payment_response["response"]
                
                # Verificar se o campo 'id' existe
                if "id" not in payment:
                    print(f"ERRO: Campo 'id' não encontrado na resposta PIX: {json.dumps(payment, indent=2, default=str)}")
                    # Criar um objeto de resposta de erro
                    return {
                        "id": "error",
                        "status": "error",
                        "error_message": "A resposta do Mercado Pago não contém o ID do pagamento PIX",
                        "point_of_interaction": None
                    }
                
                # Verificar se o campo point_of_interaction existe
                if "point_of_interaction" not in payment:
                    print(f"ERRO: Campo 'point_of_interaction' não encontrado na resposta PIX: {json.dumps(payment, indent=2, default=str)}")
                    return {
                        "id": payment.get("id", "error"),
                        "status": payment.get("status", "error"),
                        "error_message": "A resposta do Mercado Pago não contém os dados do QR Code PIX",
                        "point_of_interaction": None
                    }
                
                print(f"PIX gerado com sucesso. ID: {payment.get('id')}")
                return payment
            else:
                # Se houver erro na resposta
                error_message = payment_response.get('message', 'Erro desconhecido')
                print(f"Erro na resposta PIX do Mercado Pago: {error_message}")
                print(f"Resposta completa: {json.dumps(payment_response, indent=2, default=str)}")
                
                return {
                    "id": "error",
                    "status": "error",
                    "error_message": f"Falha ao gerar QR Code PIX: {error_message}",
                    "point_of_interaction": None
                }
        except Exception as e:
            # Tratar exceções
            import traceback
            print(f"Exceção ao gerar PIX: {str(e)}")
            print(traceback.format_exc())
            return {
                "id": "error",
                "status": "error",
                "error_message": str(e),
                "point_of_interaction": None
            }
    
    def create_preference_with_context(self, booking, item_name, item_description, item_price, base_url):
        """
        Criar uma preferência de pagamento no Mercado Pago com contexto personalizado
        
        Args:
            booking: objeto Booking
            item_name: Nome do item (serviço ou pacote)
            item_description: Descrição do item
            item_price: Preço do item
            base_url: URL base para redirecionamentos
            
        Returns:
            dict: Resposta do Mercado Pago contendo init_point e outras informações
        """
        from app.mercado_pago_service import MercadoPagoService
        
        # Usar o novo método do serviço que aceita parâmetros de contexto
        return MercadoPagoService.criar_preferencia_com_contexto(
            booking, 
            item_name, 
            item_description, 
            item_price, 
            base_url
        )
