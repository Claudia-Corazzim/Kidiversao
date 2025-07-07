"""
Script para aplicar as otimizações de performance
- Adicionar índices para service_id e payment_status na tabela booking
- Adicionar cascade delete nas relações
"""

from app import create_app, db
from sqlalchemy import text

def apply_optimizations():
    app = create_app()
    
    with app.app_context():
        # Aplicar manualmente os índices via SQL
        print("Aplicando otimizações de performance...")
        
        # Verificar se os índices já existem
        result = db.session.execute(text("SELECT indexname FROM pg_indexes WHERE tablename = 'booking' AND indexname = 'ix_booking_service_id'")).fetchone()
        if not result:
            print("Criando índice em booking.service_id...")
            db.session.execute(text("CREATE INDEX ix_booking_service_id ON booking (service_id)"))
        
        result = db.session.execute(text("SELECT indexname FROM pg_indexes WHERE tablename = 'booking' AND indexname = 'ix_booking_payment_status'")).fetchone()
        if not result:
            print("Criando índice em booking.payment_status...")
            db.session.execute(text("CREATE INDEX ix_booking_payment_status ON booking (payment_status)"))
        
        # Commit para salvar as alterações
        db.session.commit()
        print("Otimizações aplicadas com sucesso!")

if __name__ == "__main__":
    apply_optimizations()
    print("Script concluído.")
