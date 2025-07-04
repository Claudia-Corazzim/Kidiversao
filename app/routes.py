from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Service, Package, Booking

bp = Blueprint('main', __name__)

# Rota inicial: lista serviços
@bp.route('/')
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)

# Listar todos os serviços (API JSON)
@bp.route('/services')
def list_services():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services])

# Criar um novo serviço
@bp.route('/service/create', methods=['GET', 'POST'])
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
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    db.session.delete(service)
    db.session.commit()
    flash('Serviço excluído com sucesso!', 'success')
    return redirect(url_for('main.index'))

# Listar pacotes
@bp.route('/packages')
def list_packages():
    packages = Package.query.all()
    return render_template('packages.html', packages=packages)

# Criar pacote
@bp.route('/package/create', methods=['GET', 'POST'])
def create_package():
    if request.method == 'POST':
        name = request.form['name']
        descricao = request.form.get('description', '')
        
        # Se o usuário estiver logado, associa o pacote ao usuário atual
        user_id = None
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            user_id = current_user.id
        
        new_package = Package(name=name, descricao=descricao, user_id=user_id)
        db.session.add(new_package)
        db.session.commit()
        flash('Pacote criado com sucesso!', 'success')
        return redirect(url_for('main.list_packages'))
    return render_template('create_package.html')

# Editar pacote
@bp.route('/package/edit/<int:package_id>', methods=['GET', 'POST'])
def edit_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    if request.method == 'POST':
        package.name = request.form['name']
        package.descricao = request.form.get('description', '')
        
        db.session.commit()
        flash('Pacote atualizado com sucesso!', 'success')
        return redirect(url_for('main.list_packages'))
    
    return render_template('edit_package.html', package=package)

# Excluir pacote
@bp.route('/package/delete/<int:package_id>', methods=['POST'])
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    db.session.delete(package)
    db.session.commit()
    flash('Pacote excluído com sucesso!', 'success')
    return redirect(url_for('main.list_packages'))

# Listar agendamentos
@bp.route('/bookings')
def list_bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)

# Criar agendamento
@bp.route('/booking/create', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'POST':
        user_id = request.form['user_id']
        package_id = request.form['package_id']
        date = request.form['date']  # Exemplo: '2025-07-10'

        new_booking = Booking(user_id=user_id, package_id=package_id, date=date)
        db.session.add(new_booking)
        db.session.commit()
        flash('Agendamento realizado com sucesso!')
        return redirect(url_for('main.list_bookings'))
    services = Service.query.all()
    packages = Package.query.all()
    return render_template('create_booking.html', services=services, packages=packages)

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
        booking = Booking(user_id=current_user.id, service_id=service.id, event_date=event_date)
        db.session.add(booking)
        db.session.commit()
        flash('Serviço reservado!', 'success')
        return redirect(url_for('main.index'))
    return render_template('book_service.html', service=service)

# Rotas de autenticação
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Implementação pendente
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Implementação pendente
    return render_template('register.html')

@bp.route('/logout')
def logout():
    # Implementação pendente
    flash('Você foi desconectado.')
    return redirect(url_for('main.index'))
