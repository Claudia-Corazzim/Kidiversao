"""
Rotas de pagamento para Kidiversão
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Booking, Service
from app.payment import PaymentManager
from datetime import datetime

# Estas rotas serão adicionadas ao arquivo routes.py existente
# Adicione este conteúdo ao final do arquivo routes.py

@bp.route('/payment/<int:booking_id>', methods=['GET'])
@login_required
def payment(booking_id):
    """Iniciar processo de pagamento"""
    booking = Booking.query.get_or_404(booking_id)
    service = Service.query.get_or_404(booking.service_id)
    
    # Verificar se o booking pertence ao usuário atual
    if booking.user_id != current_user.id:
        flash('Você não tem permissão para acessar este recurso.', 'error')
        return redirect(url_for('main.index'))
    
    # Inicializar gerenciador de pagamentos
    payment_manager = PaymentManager()
    
    # Definir base_url
    if request.headers.get('X-Forwarded-Proto'):
        base_url = request.headers.get('X-Forwarded-Proto') + '://' + request.headers.get('Host', '')
    else:
        base_url = request.scheme + '://' + request.headers.get('Host', '')
    
    # Criar preferência de pagamento
    preference = payment_manager.create_preference(booking, service, base_url)
    
    # Salvar ID da preferência
    booking.payment_preference_id = preference["id"]
    booking.total_amount = service.price
    db.session.commit()
    
    # Renderizar página de pagamento
    return render_template('payment.html', 
                          booking=booking, 
                          service=service, 
                          preference=preference, 
                          public_key=current_app.config.get('MERCADO_PAGO_PUBLIC_KEY'))

@bp.route('/payment/pix/<int:booking_id>', methods=['GET'])
@login_required
def payment_pix(booking_id):
    """Gerar QR Code PIX para pagamento"""
    booking = Booking.query.get_or_404(booking_id)
    service = Service.query.get_or_404(booking.service_id)
    
    # Verificar se o booking pertence ao usuário atual
    if booking.user_id != current_user.id:
        flash('Você não tem permissão para acessar este recurso.', 'error')
        return redirect(url_for('main.index'))
    
    # Inicializar gerenciador de pagamentos
    payment_manager = PaymentManager()
    
    # Gerar QR code PIX
    payment = payment_manager.generate_pix_qrcode(booking, service)
    
    # Salvar informações do pagamento
    booking.payment_id = payment["id"]
    booking.payment_method = "pix"
    booking.payment_status = payment["status"]
    db.session.commit()
    
    # Renderizar página com QR code PIX
    return render_template('payment_pix.html', 
                          booking=booking, 
                          service=service, 
                          payment=payment)

@bp.route('/payment/success/<int:booking_id>')
@login_required
def payment_success(booking_id):
    """Callback para pagamento aprovado"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Atualizar status do pagamento
    payment_id = request.args.get('payment_id')
    if payment_id:
        booking.payment_id = payment_id
        booking.payment_status = 'approved'
        booking.payment_date = datetime.utcnow()
        booking.status = 'Confirmed'
        db.session.commit()
    
    flash('Pagamento aprovado com sucesso!', 'success')
    return render_template('payment_success.html', booking=booking)

@bp.route('/payment/failure/<int:booking_id>')
@login_required
def payment_failure(booking_id):
    """Callback para pagamento recusado"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Atualizar status do pagamento
    payment_id = request.args.get('payment_id')
    if payment_id:
        booking.payment_id = payment_id
        booking.payment_status = 'rejected'
        booking.payment_date = datetime.utcnow()
        db.session.commit()
    
    flash('Houve um problema com o seu pagamento.', 'error')
    return render_template('payment_failure.html', booking=booking)

@bp.route('/payment/pending/<int:booking_id>')
@login_required
def payment_pending(booking_id):
    """Callback para pagamento pendente"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Atualizar status do pagamento
    payment_id = request.args.get('payment_id')
    if payment_id:
        booking.payment_id = payment_id
        booking.payment_status = 'pending'
        booking.payment_date = datetime.utcnow()
        db.session.commit()
    
    flash('Seu pagamento está em processamento.', 'info')
    return render_template('payment_pending.html', booking=booking)

@bp.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    """Webhook para receber notificações de pagamento do Mercado Pago"""
    payload = request.json
    
    if payload.get('type') == 'payment' and payload.get('data', {}).get('id'):
        payment_id = payload['data']['id']
        
        # Inicializar gerenciador de pagamentos
        payment_manager = PaymentManager()
        
        # Obter status do pagamento
        payment = payment_manager.get_payment_status(payment_id)
        
        # Obter ID da reserva a partir da referência externa
        external_reference = payment.get('external_reference')
        if external_reference:
            booking = Booking.query.get(int(external_reference))
            if booking:
                # Atualizar status do pagamento
                booking.payment_id = payment_id
                booking.payment_status = payment.get('status')
                booking.payment_method = payment.get('payment_method_id')
                booking.payment_date = datetime.utcnow()
                
                # Se pagamento aprovado, confirmar reserva
                if payment.get('status') == 'approved':
                    booking.status = 'Confirmed'
                
                db.session.commit()
    
    return jsonify({'status': 'ok'})
