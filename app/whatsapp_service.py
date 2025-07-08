"""
Serviço de WhatsApp para envio de notificações
"""
from flask import current_app
import requests
import json

class WhatsAppService:
    """
    Classe para envio de mensagens via WhatsApp
    """
    
    @staticmethod
    def enviar_confirmacao_pagamento(booking, service):
        """
        Envia mensagem de WhatsApp confirmando o pagamento
        
        Args:
            booking: Objeto Booking com informações da reserva
            service: Objeto Service com informações do serviço
            
        Returns:
            bool: True se a mensagem foi enviada com sucesso, False caso contrário
        """
        try:
            # Verificar se o usuário tem número de telefone
            if not hasattr(booking.user, 'phone') or not booking.user.phone:
                print("Usuário não possui número de telefone cadastrado para WhatsApp")
                return False
                
            # Formatar mensagem
            mensagem = f"""
*Pagamento Confirmado - Kidiversão*

Olá {booking.user.username},

Seu pagamento para o serviço *{service.name}* foi confirmado com sucesso!

*Detalhes:*
- Número do pedido: #{booking.id}
- Valor: R$ {booking.total_amount or service.price}
- Data do evento: {booking.event_date.strftime('%d/%m/%Y')}
- Status do pagamento: {booking.payment_status}

Agradecemos sua preferência!
Equipe Kidiversão
            """
            
            # Simulação de envio (em ambiente real, integrar com API de WhatsApp)
            print(f"[SIMULAÇÃO] Mensagem WhatsApp enviada para: {booking.user.phone}")
            print(f"Conteúdo: {mensagem[:100]}...")
            
            # Exemplo de implementação real (comentada para testes)
            """
            url = current_app.config.get('WHATSAPP_API_URL')
            headers = {
                'Authorization': f"Bearer {current_app.config.get('WHATSAPP_API_TOKEN')}",
                'Content-Type': 'application/json'
            }
            
            payload = {
                'phone': booking.user.phone,
                'message': mensagem
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            return response.status_code == 200
            """
            
            return True
            
        except Exception as e:
            print(f"ERRO ao enviar mensagem de WhatsApp: {str(e)}")
            return False
    
    @staticmethod
    def enviar_confirmacao_agendamento(booking, service):
        """
        Envia mensagem de WhatsApp confirmando o agendamento
        
        Args:
            booking: Objeto Booking com informações da reserva
            service: Objeto Service com informações do serviço
            
        Returns:
            bool: True se a mensagem foi enviada com sucesso, False caso contrário
        """
        try:
            # Verificar se o usuário tem número de telefone
            if not hasattr(booking.user, 'phone') or not booking.user.phone:
                print("Usuário não possui número de telefone cadastrado para WhatsApp")
                return False
                
            # Formatar mensagem
            mensagem = f"""
*Agendamento Confirmado - Kidiversão*

Olá {booking.user.username},

Seu agendamento para o serviço *{service.name}* foi registrado com sucesso!

*Detalhes:*
- Número do pedido: #{booking.id}
- Valor: R$ {booking.total_amount or service.price}
- Data do evento: {booking.event_date.strftime('%d/%m/%Y')}
- Status do pagamento: {booking.payment_status}

Para efetuar o pagamento, acesse: {current_app.config.get('HOST_URL', 'http://localhost:5000')}/payment/{booking.id}

Agradecemos sua preferência!
Equipe Kidiversão
            """
            
            # Simulação de envio (em ambiente real, integrar com API de WhatsApp)
            print(f"[SIMULAÇÃO] Mensagem WhatsApp de agendamento enviada para: {booking.user.phone}")
            print(f"Conteúdo: {mensagem[:100]}...")
            
            # Exemplo de implementação real (comentada para testes)
            """
            url = current_app.config.get('WHATSAPP_API_URL')
            headers = {
                'Authorization': f"Bearer {current_app.config.get('WHATSAPP_API_TOKEN')}",
                'Content-Type': 'application/json'
            }
            
            payload = {
                'phone': booking.user.phone,
                'message': mensagem
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            return response.status_code == 200
            """
            
            return True
            
        except Exception as e:
            print(f"ERRO ao enviar mensagem de WhatsApp para agendamento: {str(e)}")
            return False