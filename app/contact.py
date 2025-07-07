"""
Módulo para gerenciar mensagens de contato
"""

class ContactManager:
    """Gerencia mensagens enviadas pelo formulário de contato"""
    
    @staticmethod
    def save_message(name, email, phone, message):
        """
        Salva a mensagem no sistema e simula envio de email
        No ambiente de produção, substituir por implementação real de envio de email
        """
        try:
            # Simulação de log da mensagem
            print(f"Nova mensagem de contato recebida:")
            print(f"Nome: {name}")
            print(f"Email: {email}")
            print(f"Telefone: {phone}")
            print(f"Mensagem: {message}")
            print("-" * 50)
            
            # Aqui poderia haver integração com serviço de email como:
            # - SendGrid
            # - Mailgun
            # - SMTP direto
            # - Salvamento em banco de dados
            
            return True, "Mensagem enviada com sucesso!"
        except Exception as e:
            print(f"Erro ao processar mensagem de contato: {str(e)}")
            return False, f"Erro ao enviar mensagem: {str(e)}"
