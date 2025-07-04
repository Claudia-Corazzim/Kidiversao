"""
Script para criar um usuário de teste para o sistema Kidiversão
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Verifica se já existe um usuário admin
    admin = User.query.filter_by(email='admin@kidiversao.com').first()
    
    if not admin:
        # Cria um usuário administrador
        admin = User(
            username='admin',
            email='admin@kidiversao.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Cria um usuário comum
        user = User(
            username='usuario',
            email='usuario@teste.com',
            is_admin=False
        )
        user.set_password('senha123')
        db.session.add(user)
        
        db.session.commit()
        print("Usuários criados com sucesso!")
        print("Admin: admin@kidiversao.com / Senha: admin123")
        print("Usuário: usuario@teste.com / Senha: senha123")
    else:
        print("Usuários já existem no banco de dados!")
