"""
Serviço de Email para envio de notificações
"""
from flask import render_template, current_app
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    """
    Classe para envio de emails de notificação
    """
    
    @staticmethod
    def enviar_confirmacao_pagamento(booking, service):
        """
        Envia email de confirmação de pagamento
        
        Args:
            booking: Objeto Booking com informações da reserva
            service: Objeto Service com informações do serviço
            
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrário
        """
        try:
            # Configurações do email
            sender_email = current_app.config.get('EMAIL_SENDER', 'noreply@kidiversao.com.br')
            receiver_email = booking.user.email
            subject = f"Confirmação de Pagamento - Kidiversão - Pedido #{booking.id}"
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = receiver_email
            
            # Renderizar o template HTML com as informações da reserva
            html = render_template('emails/payment_confirmation.html', 
                                  booking=booking, 
                                  service=service)
            
            # Anexar parte HTML
            part = MIMEText(html, 'html')
            msg.attach(part)
            
            # Enviar email (simulado, adicionar código real de envio em produção)
            print(f"[SIMULAÇÃO] Email de confirmação enviado para {receiver_email}")
            print(f"Assunto: {subject}")
            print(f"Conteúdo: {html[:100]}...")
            
            # Implementação real (comentada para testes)
            """
            with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.sendmail(sender_email, receiver_email, msg.as_string())
            """
            
            return True
            
        except Exception as e:
            print(f"ERRO ao enviar email de confirmação: {str(e)}")
            return False
    
    @staticmethod
    def enviar_confirmacao_agendamento(booking, service):
        """
        Envia email de confirmação de agendamento
        
        Args:
            booking: Objeto Booking com informações da reserva
            service: Objeto Service com informações do serviço
            
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrário
        """
        try:
            # Configurações do email
            sender_email = current_app.config.get('EMAIL_SENDER', 'noreply@kidiversao.com.br')
            receiver_email = booking.user.email
            subject = f"Confirmação de Agendamento - Kidiversão - Pedido #{booking.id}"
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = receiver_email
            
            # Renderizar o template HTML com as informações da reserva
            html = render_template('emails/booking_confirmation.html', 
                                  booking=booking, 
                                  service=service)
            
            # Anexar parte HTML
            part = MIMEText(html, 'html')
            msg.attach(part)
            
            # Enviar email (simulado, adicionar código real de envio em produção)
            print(f"[SIMULAÇÃO] Email de confirmação de agendamento enviado para {receiver_email}")
            print(f"Assunto: {subject}")
            print(f"Conteúdo: {html[:100]}...")
            
            # Implementação real (comentada para testes)
            """
            with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.sendmail(sender_email, receiver_email, msg.as_string())
            """
            
            return True
            
        except Exception as e:
            print(f"ERRO ao enviar email de confirmação de agendamento: {str(e)}")
            return False