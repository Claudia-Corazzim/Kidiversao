from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models import Service, Package, Booking, User, PackageItem
from app.contact import ContactManager
from datetime import datetime
import json

bp = Blueprint('main', __name__)

# Rota inicial: lista serviços
@bp.route('/')
def index():
    services = Service.query.all()
    # Se o usuário não estiver logado, mostra apenas a página com mensagem
    return render_template('index.html', services=services)

# Listar todos os serviços (API JSON)
@bp.route('/services')
@login_required
def list_services():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services])

# Criar um novo serviço
@bp.route('/service/create', methods=['GET', 'POST'])
@login_required
def create_service():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price = request.form.get('price', 0)
        image_url = request.form.get('image_url', '')

        new_service = Service(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_service)
        db.session.commit()
        flash('Serviço criado com sucesso!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_service.html')

# Editar serviço
@bp.route('/service/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form.get('description', '')
        service.price = request.form.get('price', 0)
        service.image_url = request.form.get('image_url', '')
        
        db.session.commit()
        flash('Serviço atualizado com sucesso!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit_service.html', service=service)

# Excluir serviço
@bp.route('/service/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    try:
        # Verificação rápida de reservas confirmadas associadas a este serviço
        bookings_count = Booking.query.filter_by(
            service_id=service_id, 
            status='Confirmado'
        ).count()
        
        # Se houver reservas confirmadas, não permitir exclusão
        if bookings_count > 0:
            flash(f'Não é possível excluir este serviço porque existem {bookings_count} reservas confirmadas associadas a ele.', 'error')
            return redirect(url_for('main.index'))
        
        # Verificar se o serviço está em algum pacote
        package_items_count = PackageItem.query.filter_by(service_id=service_id).count()
        if package_items_count > 0:
            flash(f'Não é possível excluir este serviço porque ele está incluído em {package_items_count} pacotes. Remova-o dos pacotes primeiro.', 'error')
            return redirect(url_for('main.index'))
        
        # Com a configuração cascade='all, delete-orphan' no modelo,
        # a exclusão do serviço irá automaticamente excluir todas as reservas
        db.session.delete(service)
        db.session.commit()
        
        flash('Serviço excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        # Log simplificado para não sobrecarregar o console
        import traceback
        print(f"Erro ao excluir serviço {service_id}: {str(e)}")
        flash(f'Erro ao excluir serviço: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

# Listar pacotes
@bp.route('/packages')
@login_required
def list_packages():
    packages = Package.query.all()
    return render_template('packages.html', packages=packages)

# Criar pacote
@bp.route('/package/create', methods=['GET', 'POST'])
@login_required
def create_package():
    if request.method == 'POST':
        name = request.form['name']
        descricao = request.form.get('description', '')
        user_id = current_user.id
        
        new_package = Package(name=name, descricao=descricao, user_id=user_id)
        db.session.add(new_package)
        db.session.commit()
        
        flash('Pacote criado com sucesso! Agora adicione serviços ao pacote.', 'success')
        return redirect(url_for('main.package_items', package_id=new_package.id))
    return render_template('create_package.html')

# Editar pacote
@bp.route('/package/edit/<int:package_id>', methods=['GET', 'POST'])
@login_required
def edit_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    # Obter serviços disponíveis para adicionar ao pacote
    services = Service.query.all()
    
    # Obter itens existentes no pacote
    package_items = PackageItem.query.filter_by(package_id=package_id).all()
    
    if request.method == 'POST':
        package.name = request.form['name']
        package.descricao = request.form.get('description', '')
        
        # Atualizar o preço total baseado nos itens (opcional)
        if not package.total_price or package.total_price == 0:
            total = 0
            for item in package_items:
                service = Service.query.get(item.service_id)
                if service:
                    total += float(service.price) * item.quantity
            package.total_price = total
        
        db.session.commit()
        flash('Pacote atualizado com sucesso!', 'success')
        return redirect(url_for('main.package_items', package_id=package_id))
    
    return render_template('edit_package.html', package=package, services=services, package_items=package_items)

# Excluir pacote
@bp.route('/package/delete/<int:package_id>', methods=['POST'])
@login_required
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    db.session.delete(package)
    db.session.commit()
    flash('Pacote excluído com sucesso!', 'success')
    return redirect(url_for('main.list_packages'))

# Listar agendamentos
@bp.route('/bookings')
@login_required
def list_bookings():
    # Se for admin, mostra todos os agendamentos
    if current_user.is_admin:
        bookings = Booking.query.order_by(Booking.event_date.desc()).all()
    else:
        # Se for usuário comum, mostra apenas seus agendamentos
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.event_date.desc()).all()
    
    return render_template('bookings.html', bookings=bookings)

# Criar agendamento
@bp.route('/booking/create', methods=['GET', 'POST'])
@login_required
def create_booking():
    if request.method == 'POST':
        user_id = request.form['user_id']
        booking_type = request.form.get('booking_type', 'service')
        date = request.form['date']  # Exemplo: '2025-07-10'

        # Criar booking baseado no tipo (serviço ou pacote)
        if booking_type == 'service':
            service_id = request.form['service_id']
            service = Service.query.get_or_404(service_id)
            
            new_booking = Booking(
                user_id=user_id,
                service_id=service_id,
                package_id=None,  # Explicitamente definido como None para agendamentos de serviço
                event_date=date,
                status='Pending',
                total_amount=service.price
            )
            
        else:  # package
            package_id = request.form['package_id']
            package = Package.query.get_or_404(package_id)
            
            # Verificamos se o pacote tem algum serviço associado
            package_items = PackageItem.query.filter_by(package_id=package_id).all()
            
            if package_items:
                # Se tem serviço associado, usamos o primeiro
                service_id = package_items[0].service_id
            else:
                # Se não tem serviço associado, verificamos se existe algum serviço no sistema
                default_service = Service.query.first()
                
                if default_service:
                    service_id = default_service.id
                    # Adicionamos esse serviço ao pacote para futuras referências
                    new_package_item = PackageItem(
                        package_id=package_id,
                        service_id=service_id,
                        quantity=1
                    )
                    db.session.add(new_package_item)
                    
                    # Atualizar o preço total do pacote se necessário
                    if not package.total_price or package.total_price == 0:
                        package.total_price = float(default_service.price)
                    
                    db.session.commit()
                    flash('Um serviço padrão foi adicionado ao pacote automaticamente.', 'info')
                else:
                    # Se não houver nenhum serviço no sistema
                    flash('Não há serviços disponíveis no sistema. Por favor, crie serviços primeiro.', 'error')
                    return redirect(url_for('main.create_booking'))
            
            new_booking = Booking(
                user_id=user_id,
                service_id=service_id,
                package_id=package_id,  # Guardamos a referência ao pacote
                event_date=date,
                status='Pending',
                total_amount=package.total_price or 0
            )
        
        db.session.add(new_booking)
        db.session.commit()
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('main.list_bookings'))
    
    # Pegar a data de hoje para definir a data mínima no formulário
    today = datetime.now().strftime('%Y-%m-%d')
    packages = Package.query.all()
    services = Service.query.all()
    return render_template('create_booking.html', packages=packages, services=services, today=today)

@bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Acesso negado.')
        return redirect(url_for('main.index'))
    services = Service.query.all()
    bookings = Booking.query.all()
    return render_template('admin_dashboard.html', services=services, bookings=bookings)

@bp.route('/book/<int:service_id>', methods=['GET', 'POST'])
@login_required
def book_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        event_date = request.form['event_date']
        booking = Booking(
            user_id=current_user.id, 
            service_id=service.id, 
            package_id=None,  # Explicitamente definido como None para agendamentos de serviço
            event_date=event_date,
            status='Pendente',
            total_amount=service.price
        )
        db.session.add(booking)
        db.session.commit()
        flash('Serviço reservado! Prossiga para o pagamento.', 'success')
        return redirect(url_for('main.payment', booking_id=booking.id))
    return render_template('book_service.html', service=service, now=datetime.now())

# Rotas de autenticação
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        # Verifica se o usuário existe e a senha está correta
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Login realizado com sucesso!', 'success')
            
            # Verifica se há um parâmetro 'next' na URL (redirecionamento após login)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Email ou senha incorretos', 'error')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Se o usuário já estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Verifica se as senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return render_template('register.html')
        
        # Verifica se a senha tem pelo menos 6 caracteres
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres', 'error')
            return render_template('register.html')
        
        # Verifica se o email já está cadastrado
        if User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado', 'error')
            return render_template('register.html')
        
        # Verifica se o nome de usuário já está cadastrado
        if User.query.filter_by(username=username).first():
            flash('Este nome de usuário já está em uso', 'error')
            return render_template('register.html')
        
        # Cria um novo usuário
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('main.index'))

# ============ ROTAS DE RESERVA ============

@bp.route('/booking/<int:booking_id>', methods=['GET'])
@login_required
def booking_details(booking_id):
    """Visualizar detalhes da reserva"""
    booking = Booking.query.get_or_404(booking_id)
    service = Service.query.get_or_404(booking.service_id)
    
    # Verificar se o booking pertence ao usuário atual
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar este recurso.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('booking_details.html', booking=booking, service=service)

# Cancelar agendamento
@bp.route('/booking/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Verificar se o booking pertence ao usuário atual ou se é admin
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para cancelar este agendamento.', 'error')
        return redirect(url_for('main.list_bookings'))
    
    # Verificar status de pagamento - não permitir cancelar se já pago
    if booking.payment_status == 'Aprovado':
        flash('Não é possível cancelar um agendamento já pago. Entre em contato com o suporte.', 'error')
        return redirect(url_for('main.list_bookings'))
    
    try:
        # Log antes da exclusão
        print(f"Tentando excluir o agendamento {booking_id}...")
        
        # Excluir o booking (sem logs excessivos)
        db.session.delete(booking)
        db.session.commit()
        
        print(f"Agendamento {booking_id} excluído com sucesso!")
        flash('Agendamento cancelado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        # Log detalhado do erro
        import traceback
        print(f"ERRO ao cancelar agendamento {booking_id}: {str(e)}")
        print(traceback.format_exc())
        flash(f'Erro ao cancelar agendamento: {str(e)}', 'error')
    
    return redirect(url_for('main.list_bookings'))

# Página de contato
@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Página de contato com informações da empresa e formulário de mensagem"""
    if request.method == 'POST':
        # Processar o formulário de contato
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        message = request.form.get('message')
        
        # Validação básica
        if not name or not email or not message:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
            return render_template('contact.html')
        
        # Processar a mensagem usando ContactManager
        success, msg = ContactManager.save_message(name, email, phone, message)
        
        if success:
            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('main.contact'))
        else:
            flash(msg, 'error')
            
    return render_template('contact.html')

# Gerenciar itens de um pacote
@bp.route('/package/<int:package_id>/items', methods=['GET', 'POST'])
@login_required
def package_items(package_id):
    package = Package.query.get_or_404(package_id)
    services = Service.query.all()
    
    # Obter itens existentes no pacote
    package_items = PackageItem.query.filter_by(package_id=package_id).all()
    
    if request.method == 'POST':
        # Adicionar novo item ao pacote
        service_id = request.form.get('service_id')
        quantity = int(request.form.get('quantity', 1))
        
        if service_id:
            # Verificar se o serviço já está no pacote
            existing_item = PackageItem.query.filter_by(
                package_id=package_id, 
                service_id=service_id
            ).first()
            
            if existing_item:
                # Atualizar quantidade se já existir
                existing_item.quantity = quantity
                flash('Quantidade do serviço atualizada no pacote.', 'success')
            else:
                # Adicionar novo item
                new_item = PackageItem(
                    package_id=package_id,
                    service_id=service_id,
                    quantity=quantity
                )
                db.session.add(new_item)
                flash('Serviço adicionado ao pacote com sucesso!', 'success')
            
            # Atualizar preço total do pacote
            service = Service.query.get(service_id)
            if service:
                # Inicializar o preço total se for nulo
                if not package.total_price:
                    package.total_price = 0
                
                # Recalcular preço total somando todos os itens
                total = 0
                
                # Adicionar os itens existentes ao total (exceto o que acabamos de adicionar)
                for item in package_items:
                    item_service = Service.query.get(item.service_id)
                    if item_service:
                        total += float(item_service.price) * item.quantity
                
                # Adicionar o novo item ao preço (ou sua atualização)
                if existing_item:
                    # Se atualizamos um item existente, ele já está incluído na soma acima
                    pass
                else:
                    # Se é um novo item, adicionar ao total
                    total += float(service.price) * quantity
                
                package.total_price = total
            
            db.session.commit()
        
        return redirect(url_for('main.package_items', package_id=package_id))
    
    return render_template('package_items.html', 
                          package=package, 
                          services=services, 
                          package_items=package_items)

# Remover item de um pacote
@bp.route('/package/<int:package_id>/remove_item/<int:item_id>', methods=['POST'])
@login_required
def remove_package_item(package_id, item_id):
    package = Package.query.get_or_404(package_id)
    item = PackageItem.query.get_or_404(item_id)
    
    # Verificar se o item pertence ao pacote
    if item.package_id != package_id:
        flash('Item não pertence a este pacote.', 'error')
        return redirect(url_for('main.package_items', package_id=package_id))
    
    # Verificar se é o último item do pacote
    remaining_items = PackageItem.query.filter_by(package_id=package_id).count()
    if remaining_items <= 1:
        flash('Atenção: este é o último serviço do pacote. Se você remover, não será possível agendar este pacote até que adicione pelo menos um serviço.', 'warning')
    
    # Recalcular o preço do pacote
    service = Service.query.get(item.service_id)
    if service and package.total_price:
        package.total_price = float(package.total_price) - (float(service.price) * item.quantity)
        if package.total_price < 0:
            package.total_price = 0
    
    # Remover o item
    db.session.delete(item)
    db.session.commit()
    
    flash('Item removido do pacote com sucesso!', 'success')
    return redirect(url_for('main.package_items', package_id=package_id))

# ============ ROTAS DE PAGAMENTO (Estrutura básica) ============

@bp.route('/payment/<int:booking_id>', methods=['GET'])
@login_required
def payment(booking_id):
    """Página de pagamento (estrutura básica para futura integração)"""
    booking = Booking.query.get_or_404(booking_id)
    service = Service.query.get_or_404(booking.service_id)
    
    # Verificar se o booking pertence ao usuário atual
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar este recurso.', 'error')
        return redirect(url_for('main.index'))
    
    # Atualizar o status do agendamento para aguardando pagamento
    booking.status = 'Aguardando Pagamento'
    booking.payment_status = 'Pendente'
    db.session.commit()
    
    # Em uma implementação futura, aqui seria integrada a plataforma de pagamento escolhida
    
    return render_template('payment.html', booking=booking, service=service)

@bp.route('/payment/success/<int:booking_id>', methods=['GET'])
@login_required
def payment_success(booking_id):
    """Callback para pagamento bem-sucedido"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verificar se o booking pertence ao usuário atual
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar este recurso.', 'error')
        return redirect(url_for('main.index'))
    
    # Atualizar status do pagamento
    booking.status = 'Confirmado'
    booking.payment_status = 'Aprovado'
    booking.payment_date = datetime.utcnow()
    db.session.commit()
    
    flash('Pagamento realizado com sucesso!', 'success')
    return redirect(url_for('main.booking_details', booking_id=booking.id))

@bp.route('/payment/cancel/<int:booking_id>', methods=['GET'])
@login_required
def payment_cancel(booking_id):
    """Cancelamento de pagamento"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verificar se o booking pertence ao usuário atual
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar este recurso.', 'error')
        return redirect(url_for('main.index'))
    
    # Atualizar status do pagamento
    booking.payment_status = 'Cancelado'
    db.session.commit()
    
    flash('Pagamento cancelado.', 'info')
    return redirect(url_for('main.list_bookings'))
