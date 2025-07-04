import os
from app.payment_config import MERCADO_PAGO_PUBLIC_KEY, MERCADO_PAGO_ACCESS_TOKEN

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://admin:admin@localhost/kidiversao_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações do Mercado Pago
    MERCADO_PAGO_PUBLIC_KEY = MERCADO_PAGO_PUBLIC_KEY
    MERCADO_PAGO_ACCESS_TOKEN = MERCADO_PAGO_ACCESS_TOKEN

