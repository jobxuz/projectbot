import hashlib
import hmac
import json
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from apps.application.models import Payment, Manufacturer, BotUser

class PaymentService:
    """To'lov xizmati asosiy klassi"""
    
    @staticmethod
    def create_payment(payment):
        """To'lov yaratish"""
        if payment.payment_method == 'click':
            return ClickPaymentService.create_payment(payment)
        elif payment.payment_method == 'payme':
            return PaymePaymentService.create_payment(payment)
        elif payment.payment_method in ['visa', 'mastercard']:
            return VisaPaymentService.create_payment(payment)
        else:
            raise ValueError(f"Noto'g'ri to'lov usuli: {payment.payment_method}")
    
    @staticmethod
    def process_webhook(payment, data, provider):
        """Webhook ma'lumotlarini qayta ishlash"""
        if provider == 'click':
            return ClickPaymentService.process_webhook(payment, data)
        elif provider == 'payme':
            return PaymePaymentService.process_webhook(payment, data)
        elif provider == 'visa':
            return VisaPaymentService.process_webhook(payment, data)
        else:
            raise ValueError(f"Noto'g'ri provayder: {provider}")

class ClickPaymentService:
    """Click to'lov xizmati"""
    
    @staticmethod
    def create_payment(payment):
        """Click to'lov yaratish"""
        from django.conf import settings
        
        # Click API kalitlari
        click_service_id = getattr(settings, 'CLICK_SERVICE_ID', '')
        click_secret_key = getattr(settings, 'CLICK_SECRET_KEY', '')
        
        # To'lov ma'lumotlari
        amount = int(payment.amount * 100)  # Tiyinlarda
        merchant_trans_id = str(payment.id)
        
        # Imzo yaratish
        sign_string = f"{click_service_id}{merchant_trans_id}{amount}{click_secret_key}"
        sign = hashlib.md5(sign_string.encode()).hexdigest()
        
        # Click API ga yuborish
        payment_data = {
            'service_id': click_service_id,
            'merchant_trans_id': merchant_trans_id,
            'amount': amount,
            'currency': '860',  # UZS
            'sign_time': int(timezone.now().timestamp()),
            'sign_string': sign_string,
            'sign': sign
        }
        
        # Click to'lov havolasini yaratish
        payment_url = f"https://my.click.uz/services/pay?service_id={click_service_id}&merchant_trans_id={merchant_trans_id}&amount={amount}&currency=860&sign={sign}"
        
        return {
            'payment_url': payment_url,
            'transaction_id': merchant_trans_id,
            'payment_data': payment_data
        }
    
    @staticmethod
    def process_webhook(payment, data):
        """Click webhook qayta ishlash"""
        from django.conf import settings
        
        click_secret_key = getattr(settings, 'CLICK_SECRET_KEY', '')
        
        # Imzoni tekshirish
        sign_string = f"{data['click_trans_id']}{data['service_id']}{data['merchant_trans_id']}{data['amount']}{data['action']}{data['sign_time']}{click_secret_key}"
        expected_sign = hashlib.md5(sign_string.encode()).hexdigest()
        
        if data['sign'] != expected_sign:
            raise ValueError("Noto'g'ri imzo")
        
        # To'lov holatini yangilash
        if data['action'] == '1':  # To'lov muvaffaqiyatli
            payment.status = 'completed'
            payment.transaction_id = data['click_trans_id']
            payment.completed_at = timezone.now()
            payment.payment_data = data
            payment.save()
            
            # To'lov turiga qarab amal qilish
            PaymentService._process_payment_success(payment)
        
        return True

class PaymePaymentService:
    """Payme to'lov xizmati"""
    
    @staticmethod
    def create_payment(payment):
        """Payme to'lov yaratish"""
        from django.conf import settings
        
        payme_merchant_id = getattr(settings, 'PAYME_MERCHANT_ID', '')
        payme_secret_key = getattr(settings, 'PAYME_SECRET_KEY', '')
        
        # To'lov ma'lumotlari
        amount = int(payment.amount * 100)  # Tiyinlarda
        merchant_trans_id = str(payment.id)
        
        # Payme API ga yuborish
        payment_data = {
            'merchant_id': payme_merchant_id,
            'amount': amount,
            'currency': '860',  # UZS
            'merchant_trans_id': merchant_trans_id,
            'description': f"To'lov #{payment.id}",
            'return_url': f"{settings.BASE_URL}/payment/success/{payment.id}/",
            'cancel_url': f"{settings.BASE_URL}/payment/cancel/{payment.id}/"
        }
        
        # Payme to'lov havolasini yaratish
        payment_url = f"https://checkout.paycom.uz/{payme_merchant_id}?amount={amount}&currency=860&merchant_trans_id={merchant_trans_id}"
        
        return {
            'payment_url': payment_url,
            'transaction_id': merchant_trans_id,
            'payment_data': payment_data
        }
    
    @staticmethod
    def process_webhook(payment, data):
        """Payme webhook qayta ishlash"""
        # Payme webhook logikasi
        if data.get('status') == 'success':
            payment.status = 'completed'
            payment.transaction_id = data.get('transaction_id')
            payment.completed_at = timezone.now()
            payment.payment_data = data
            payment.save()
            
            PaymentService._process_payment_success(payment)
        
        return True

class VisaPaymentService:
    """Visa/Mastercard to'lov xizmati"""
    
    @staticmethod
    def create_payment(payment):
        """Visa to'lov yaratish"""
        from django.conf import settings
        
        # Visa API kalitlari (misol uchun)
        visa_merchant_id = getattr(settings, 'VISA_MERCHANT_ID', '')
        visa_secret_key = getattr(settings, 'VISA_SECRET_KEY', '')
        
        # To'lov ma'lumotlari
        amount = payment.amount
        currency = payment.currency
        merchant_trans_id = str(payment.id)
        
        # Visa to'lov havolasini yaratish (misol)
        payment_url = f"https://secure.visa.com/payment?merchant_id={visa_merchant_id}&amount={amount}&currency={currency}&transaction_id={merchant_trans_id}"
        
        return {
            'payment_url': payment_url,
            'transaction_id': merchant_trans_id,
            'payment_data': {
                'merchant_id': visa_merchant_id,
                'amount': amount,
                'currency': currency,
                'merchant_trans_id': merchant_trans_id
            }
        }
    
    @staticmethod
    def process_webhook(payment, data):
        """Visa webhook qayta ishlash"""
        # Visa webhook logikasi
        if data.get('status') == 'approved':
            payment.status = 'completed'
            payment.transaction_id = data.get('transaction_id')
            payment.completed_at = timezone.now()
            payment.payment_data = data
            payment.save()
            
            PaymentService._process_payment_success(payment)
        
        return True

class PaymentService:
    """To'lov xizmati asosiy klassi"""
    
    @staticmethod
    def _process_payment_success(payment):
        """To'lov muvaffaqiyatli bo'lganda amal qilish"""
        if payment.payment_type == 'subscription':
            # Zavod obunasini faollashtirish
            manufacturer = payment.user.manufacturer
            if manufacturer:
                manufacturer.subscription_expires = timezone.now() + timedelta(days=180)  # 6 oy
                manufacturer.status = 'paid'
                manufacturer.save()
        
        elif payment.payment_type == 'catalog_access':
            # Katalog kirish huquqini berish
            pass
        
        elif payment.payment_type == 'verification':
            # Zavodni tekshirish
            manufacturer = payment.user.manufacturer
            if manufacturer:
                manufacturer.status = 'verified'
                manufacturer.verification_date = timezone.now()
                manufacturer.save()
        
        # Bildirishnoma yuborish
        from apps.application.tasks import send_payment_notification
        send_payment_notification.delay(payment.id)

# To'lov xizmatlarini yaratish
def create_payment(payment):
    return PaymentService.create_payment(payment)

def create_subscription_payment(bot_user):
    """Zavod obuna uchun to'lov"""
    payment = Payment.objects.create(
        user=bot_user,
        payment_type='subscription',
        amount=Decimal('200.00'),
        currency='USD',
        payment_method='click'
    )
    
    return ClickPaymentService.create_payment(payment)

def create_catalog_access_payment(bot_user):
    """Katalog kirish uchun to'lov"""
    payment = Payment.objects.create(
        user=bot_user,
        payment_type='catalog_access',
        amount=Decimal('30.00'),
        currency='USD',
        payment_method='click'
    )
    
    return ClickPaymentService.create_payment(payment)

# Webhook qayta ishlash
def process_click_webhook(payment, data):
    return ClickPaymentService.process_webhook(payment, data)

def process_payme_webhook(payment, data):
    return PaymePaymentService.process_webhook(payment, data)

def process_visa_webhook(payment, data):
    return VisaPaymentService.process_webhook(payment, data)
