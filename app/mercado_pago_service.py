"""
Serviço de integração com o Mercado Pago
"""
import mercadopago
import json
from datetime import datetime
from flask import current_app, url_for, request

class MercadoPagoService:
    """
    Serviço para integração com a API do Mercado Pago
    """
    
    @staticmethod
    def _get_sdk():
        """Retorna uma instância do SDK do Mercado Pago"""
        # Obtém o token diretamente do arquivo de configuração para evitar problemas de contexto
        from app.payment_config import MERCADO_PAGO_ACCESS_TOKEN
        
        # Print para debug
        print(f"Inicializando SDK do Mercado Pago com token: {MERCADO_PAGO_ACCESS_TOKEN[:10]}...")
        
        # Configurar o SDK com timeout maior para evitar falhas por tempo limite
        sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)
        
        # Definir configurações adicionais para evitar timeout
        sdk.requests_opts.update({'timeout': 30.0})  # Aumentar timeout para 30 segundos
        
        return sdk
    
    @staticmethod
    def teste_conexao():
        """Testar conexão com o Mercado Pago"""
        try:
            sdk = MercadoPagoService._get_sdk()
            # Tenta obter informações básicas para verificar a conexão
            response = sdk.payment().get_payment_methods()
            
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
    
    @staticmethod
    def gerar_link_pagamento(booking, service):
        """
        Gera um link de pagamento para o Mercado Pago baseado na reserva
        
        Args:
            booking: objeto Booking com os detalhes da reserva
            service: objeto Service com os detalhes do serviço
            
        Returns:
            dict: Resposta do Mercado Pago contendo init_point e outras informações
        """
        # Usa a configuração centralizada de tokens do Mercado Pago
        sdk = MercadoPagoService._get_sdk()
        
        # Define a URL de retorno usando url_for para garantir URLs corretas
        # Usa o host atual da requisição para URLs dinâmicas
        if hasattr(request, 'host_url'):
            host_url = request.host_url.rstrip('/')
        else:
            # Fallback para localhost se não estiver em um contexto de requisição
            host_url = "http://localhost:5000"
        
        # Verificar se o valor total está definido
        total_amount = float(booking.total_amount if booking.total_amount and booking.total_amount > 0 else service.price)
        if total_amount <= 0:
            print(f"AVISO: Valor total inválido ({total_amount}). Usando preço do serviço ({service.price}).")
            total_amount = float(service.price)
        
        payment_data = {
            "items": [
                {
                    "id": str(booking.id),
                    "title": f"Serviço: {service.name}",
                    "description": f"Agendamento para {booking.event_date.strftime('%d/%m/%Y')}",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": total_amount
                }
            ],
            "payer": {
                "email": booking.user.email,
                "name": booking.user.username,
            },
            "back_urls": {
                "success": f"{host_url}{url_for('main.payment_success', booking_id=booking.id)}",
                "failure": f"{host_url}{url_for('main.payment_failure', booking_id=booking.id)}",
                "pending": f"{host_url}{url_for('main.payment_pending', booking_id=booking.id)}"
            },
            "auto_return": "approved",
            "external_reference": str(booking.id),
            "notification_url": f"{host_url}{url_for('main.payment_webhook')}",
            "payment_methods": {
                "excluded_payment_types": [],
                "installments": 12  # Permitir parcelamento em até 12x
            },
            "statement_descriptor": "Kidiversao"
        }
        
        try:
            # Debug: imprimir dados enviados para o Mercado Pago
            print(f"Enviando dados para o Mercado Pago: {json.dumps(payment_data, indent=2, default=str)}")
            
            # Cria a preferência de pagamento - com retry para caso de falha
            MAX_RETRIES = 2
            retry_count = 0
            result = None
            
            while retry_count <= MAX_RETRIES:
                try:
                    print(f"Tentativa {retry_count + 1} de criar preferência...")
                    # Configura um timeout maior para a requisição
                    result = sdk.preference().create(payment_data)
                    # Se chegou aqui, deu certo
                    break
                except Exception as retry_error:
                    retry_count += 1
                    print(f"Erro na tentativa {retry_count}: {str(retry_error)}")
                    if retry_count <= MAX_RETRIES:
                        print(f"Aguardando 2 segundos antes de tentar novamente...")
                        import time
                        time.sleep(2)
                    else:
                        # Repassar o erro para ser tratado no bloco catch externo
                        raise
            
            # Debug: imprimir resposta completa do Mercado Pago
            print(f"Resposta completa do Mercado Pago: {json.dumps(result, indent=2, default=str)}")
            
            # Verificar se a resposta foi bem-sucedida
            if result and result.get("status") == 201 and "response" in result:
                print(f"Preferência criada com sucesso. ID: {result['response'].get('id')}")
                return result["response"]
            else:
                # Se houver erro na resposta, extrair mais detalhes
                error_message = result.get('message', 'Erro desconhecido') if result else "Nenhuma resposta recebida"
                error_status = result.get('status', 'Desconhecido') if result else "Sem status"
                error_detail = ""
                
                # Tentar extrair mais detalhes
                if result and 'cause' in result:
                    try:
                        if isinstance(result['cause'], list) and len(result['cause']) > 0:
                            error_detail = " - Causas: " + json.dumps(result['cause'])
                        elif isinstance(result['cause'], dict):
                            error_detail = " - Detalhes: " + json.dumps(result['cause'])
                        else:
                            error_detail = " - Info: " + str(result['cause'])
                    except:
                        error_detail = " - Não foi possível obter detalhes adicionais"
                
                print(f"ERRO ao criar preferência: Status={error_status}, Mensagem={error_message}{error_detail}")
                
                return {
                    "id": "error",
                    "init_point": "#",
                    "error_message": f"Erro ao criar preferência: {error_message}{error_detail}",
                    "status": "error"
                }
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            error_message = str(e)
            
            # Verificar tipos específicos de erros comuns
            if "ConnectionError" in error_message or "timeout" in error_message.lower():
                friendly_message = "Erro de conexão com o Mercado Pago. Verifique sua conexão com a internet."
            elif "401" in error_message:
                friendly_message = "Credenciais inválidas para o Mercado Pago. Verifique o token de acesso."
            elif "400" in error_message:
                friendly_message = "Requisição inválida para o Mercado Pago. Verifique os dados enviados."
            elif "500" in error_message:
                friendly_message = "Erro interno do servidor do Mercado Pago. Tente novamente mais tarde."
            else:
                friendly_message = "Erro ao processar o pagamento. Tente novamente em alguns instantes."
            
            print(f"ERRO ao criar preferência de pagamento: {error_message}")
            print(error_trace)
            
            # Se a exceção tiver uma resposta, tente extrair mais detalhes
            details = ""
            if hasattr(e, 'response') and e.response:
                try:
                    response_text = e.response.text
                    print(f"Resposta de erro do Mercado Pago: {response_text}")
                    response_json = json.loads(response_text)
                    if 'message' in response_json:
                        details = f" - {response_json['message']}"
                except:
                    pass
            
            # Criar objeto de erro padronizado
            error_response = {
                "id": "error",
                "init_point": "#",
                "error_message": f"{friendly_message}{details}",
                "status": "error"
            }
            
            print(f"Retornando resposta de erro: {json.dumps(error_response, indent=2)}")
            return error_response
    
    @staticmethod
    def gerar_qrcode_pix(booking, service):
        """
        Gerar QR Code PIX para pagamento
        
        Args:
            booking: Objeto do modelo Booking
            service: Objeto do modelo Service
        
        Returns:
            dict: Informações do pagamento PIX criado
        """
        sdk = MercadoPagoService._get_sdk()
        
        # Obter a URL base para callbacks
        host_url = request.host_url.rstrip('/')
            
        # Configurar notificação webhook
        notification_url = f"{host_url}{url_for('main.payment_webhook')}"
        
        # Configurar dados do pagamento
        payment_data = {
            "transaction_amount": float(booking.total_amount or service.price),
            "description": f"Serviço: {service.name} - Data: {booking.event_date.strftime('%d/%m/%Y')}",
            "payment_method_id": "pix",
            "payer": {
                "email": booking.user.email,
                "first_name": booking.user.username,
                "last_name": "",
            },
            "notification_url": notification_url,
            "external_reference": str(booking.id)
        }
        
        try:
            # Debug: imprimir dados enviados para o Mercado Pago
            print(f"Enviando dados para o Mercado Pago (PIX): {json.dumps(payment_data, indent=2, default=str)}")
            
            # Criar o pagamento
            payment_response = sdk.payment().create(payment_data)
            
            # Debug: imprimir resposta do Mercado Pago
            print(f"Resposta do Mercado Pago (PIX): {json.dumps(payment_response, indent=2, default=str)}")
            
            # Verificar se a resposta foi bem-sucedida e contém os dados esperados
            if payment_response.get("status") == 201 and "response" in payment_response:
                payment = payment_response["response"]
                
                # Verificar se os campos necessários existem
                if "id" not in payment or "point_of_interaction" not in payment:
                    print(f"ERRO: Campos necessários não encontrados na resposta: {json.dumps(payment, indent=2, default=str)}")
                    return {
                        "id": "error",
                        "status": "error",
                        "error_message": "A resposta do Mercado Pago não contém os dados necessários para PIX"
                    }
                
                print(f"Pagamento PIX criado com sucesso. ID: {payment.get('id')}")
                return payment
            else:
                # Se houver erro na resposta
                error_message = payment_response.get('message', 'Erro desconhecido')
                print(f"ERRO ao criar pagamento PIX: {error_message}")
                
                return {
                    "id": "error",
                    "status": "error",
                    "error_message": f"Erro ao criar pagamento PIX: {error_message}"
                }
                
        except Exception as e:
            import traceback
            print(f"ERRO ao criar pagamento PIX: {str(e)}")
            print(traceback.format_exc())
            
            return {
                "id": "error",
                "status": "error",
                "error_message": f"Erro ao criar pagamento PIX: {str(e)}"
            }
    
    @staticmethod
    def verificar_pagamento(payment_id):
        """
        Verificar status de um pagamento específico
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
            
        Returns:
            dict: Informações atualizadas do pagamento
        """
        sdk = MercadoPagoService._get_sdk()
        
        try:
            # Obter informações do pagamento
            payment_response = sdk.payment().get(payment_id)
            
            # Verificar se a resposta foi bem-sucedida
            if payment_response.get("status") == 200 and "response" in payment_response:
                payment = payment_response["response"]
                return payment
            else:
                # Se houver erro na resposta
                error_message = payment_response.get('message', 'Erro desconhecido')
                print(f"ERRO ao verificar pagamento {payment_id}: {error_message}")
                return None
                
        except Exception as e:
            print(f"ERRO ao verificar pagamento {payment_id}: {str(e)}")
            return None
            
    @staticmethod
    def processar_webhook(data):
        """
        Processar informações recebidas via webhook do Mercado Pago
        
        Args:
            data: Dados recebidos no webhook
            
        Returns:
            dict: Informações processadas do pagamento
        """
        try:
            # Verificar se é uma notificação de pagamento
            if 'action' in data and data['action'] == 'payment.updated':
                # Obter o ID do pagamento
                payment_id = data.get('data', {}).get('id')
                
                if payment_id:
                    # Verificar o status do pagamento
                    payment = MercadoPagoService.verificar_pagamento(payment_id)
                    return payment
            
            return None
                
        except Exception as e:
            print(f"ERRO ao processar webhook: {str(e)}")
            return None
        
    @staticmethod
    def criar_preferencia_com_contexto(booking, nome_item, descricao_item, preco_item, base_url):
        """
        Gera uma preferência de pagamento baseada no contexto (serviço ou pacote)
        
        Args:
            booking: objeto Booking com os detalhes da reserva
            nome_item: Nome do item a ser pago (serviço ou pacote)
            descricao_item: Descrição do item
            preco_item: Preço do item
            base_url: URL base para redirecionamentos
            
        Returns:
            dict: Resposta do Mercado Pago contendo init_point e outras informações
        """
        # Usa a configuração centralizada de tokens do Mercado Pago
        sdk = MercadoPagoService._get_sdk()
        
        # Verificar se o valor total está definido
        total_amount = float(preco_item)
        if total_amount <= 0:
            print(f"AVISO: Valor total inválido ({total_amount}). Usando valor padrão (100).")
            total_amount = 100.0
        
        payment_data = {
            "items": [
                {
                    "id": str(booking.id),
                    "title": nome_item,
                    "description": f"{descricao_item} - Agendamento para {booking.event_date.strftime('%d/%m/%Y')}",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": total_amount
                }
            ],
            "payer": {
                "email": booking.user.email,
                "name": booking.user.username,
            },
            "back_urls": {
                "success": f"{base_url}{url_for('main.payment_success', booking_id=booking.id)}",
                "failure": f"{base_url}{url_for('main.payment_failure', booking_id=booking.id)}",
                "pending": f"{base_url}{url_for('main.payment_pending', booking_id=booking.id)}"
            },
            "auto_return": "approved",
            "external_reference": str(booking.id),
            "notification_url": f"{base_url}{url_for('main.payment_webhook')}",
            "payment_methods": {
                "excluded_payment_types": [],
                "installments": 12  # Permitir parcelamento em até 12x
            },
            "statement_descriptor": "Kidiversao"
        }
        
        try:
            # Debug: imprimir dados enviados para o Mercado Pago
            print(f"Enviando dados para o Mercado Pago: {json.dumps(payment_data, indent=2, default=str)}")
            
            # Cria a preferência de pagamento - com retry para caso de falha
            MAX_RETRIES = 2
            retry_count = 0
            result = None
            
            while retry_count <= MAX_RETRIES:
                try:
                    print(f"Tentativa {retry_count + 1} de criar preferência...")
                    # Configura um timeout maior para a requisição
                    result = sdk.preference().create(payment_data)
                    # Se chegou aqui, deu certo
                    break
                except Exception as retry_error:
                    retry_count += 1
                    print(f"Erro na tentativa {retry_count}: {str(retry_error)}")
                    if retry_count <= MAX_RETRIES:
                        print(f"Aguardando 2 segundos antes de tentar novamente...")
                        import time
                        time.sleep(2)
                    else:
                        # Repassar o erro para ser tratado no bloco catch externo
                        raise
            
            # Debug: imprimir resposta completa do Mercado Pago
            print(f"Resposta completa do Mercado Pago: {json.dumps(result, indent=2, default=str)}")
            
            # Verificar se a resposta foi bem-sucedida
            if result and result.get("status") == 201 and "response" in result:
                print(f"Preferência criada com sucesso. ID: {result['response'].get('id')}")
                return result["response"]
            else:
                # Se houver erro na resposta, extrair mais detalhes
                error_message = result.get('message', 'Erro desconhecido') if result else "Nenhuma resposta recebida"
                error_status = result.get('status', 'Desconhecido') if result else "Sem status"
                error_detail = ""
                
                # Tentar extrair mais detalhes
                if result and 'cause' in result:
                    try:
                        if isinstance(result['cause'], list) and len(result['cause']) > 0:
                            error_detail = " - Causas: " + json.dumps(result['cause'])
                        elif isinstance(result['cause'], dict):
                            error_detail = " - Detalhes: " + json.dumps(result['cause'])
                        else:
                            error_detail = " - Info: " + str(result['cause'])
                    except:
                        error_detail = " - Não foi possível obter detalhes adicionais"
                
                print(f"ERRO ao criar preferência: Status={error_status}, Mensagem={error_message}{error_detail}")
                
                return {
                    "id": "error",
                    "init_point": "#",
                    "error_message": f"Erro ao criar preferência: {error_message}{error_detail}",
                    "status": "error"
                }
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            error_message = str(e)
            
            # Verificar tipos específicos de erros comuns
            if "ConnectionError" in error_message or "timeout" in error_message.lower():
                friendly_message = "Erro de conexão com o Mercado Pago. Verifique sua conexão com a internet."
            elif "401" in error_message:
                friendly_message = "Credenciais inválidas para o Mercado Pago. Verifique o token de acesso."
            elif "400" in error_message:
                friendly_message = "Requisição inválida para o Mercado Pago. Verifique os dados enviados."
            elif "500" in error_message:
                friendly_message = "Erro interno do servidor do Mercado Pago. Tente novamente mais tarde."
            else:
                friendly_message = "Erro ao processar o pagamento. Tente novamente em alguns instantes."
            
            print(f"ERRO ao criar preferência de pagamento: {error_message}")
            print(error_trace)
            
            return {
                "id": "error",
                "init_point": "#",
                "error_message": friendly_message,
                "status": "error",
                "technical_details": error_message
            }
