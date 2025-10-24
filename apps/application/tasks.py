from celery import shared_task
import logging
import re
from django.conf import settings

import requests

from apps.application.bitrix import Bitrix24
from .models import Customer, Manufacturer, TemporaryContact
logger = logging.getLogger(__name__)




@shared_task(name="send_manufacturer_to_bitrix")
def send_manufacturer_to_bitrix(application_id):
    application = Manufacturer.objects.get(id=application_id)

    
    contact_fields = {
        "UF_CRM_FULL_NAME": application.full_name,
        "UF_CRM_TELEGRAM_ID": application.user.telegram_id,
    }

    product_segments = list(application.product_segment.values_list("title", flat=True))
    
    deal_fields = {
        "CATEGORY_ID": 0,
        "TITLE": 'Заполнение CRM-формы "Test"',
        "UF_CRM_FULL_NAME": application.full_name,
        "UF_CRM_COMPANY_NAME": application.company_name,
        "UF_CRM_MARKET_EXPERIENCE": application.market_experience,
        "UF_CRM_POSITION": application.position,
        "UF_CRM_MIN_ORDER_QUANTITY": application.min_order_quantity,
        "UF_CRM_PRODUCT_SEGMENT": product_segments,
        "UF_CRM_COMMERCIAL_OFFER_TEXT": application.commercial_offer_text,
        "UF_CRM_PRODUCTION_ADDRESS": application.production_address,
        "UF_CRM_OFFICE_ADDRESS": application.office_address,
        "UF_CRM_WEBSITE": application.website,
        "UF_CRM_HAS_QUALITY_CONTROL": application.has_quality_control,
        "UF_CRM_HAS_CRM": application.has_crm,
        "UF_CRM_HAS_ERP": application.has_erp,
        "UF_CRM_HAS_GEMINI_GERBER": application.has_gemini_gerber,
        "UF_CRM_EMPLOYEE_COUNT": application.employee_count,
        "UF_CRM_OWNS_BUILDING": application.owns_building,
        "UF_CRM_HAS_POWER_ISSUES": application.has_power_issues,
        "UF_CRM_HAS_CREDIT_LOAD": application.has_credit_load,
        "UF_CRM_ORGANIZATION_STRUCTURE": application.organization_structure,
        "UF_CRM_EQUIPMENT_INFO": application.equipment_info,
  
    }


    try:
        bitrix = Bitrix24()
        normalized_phone = "+" + re.sub(r"\D", "", application.phone)
        # temporary_contact = TemporaryContact.objects.filter(phone_number=normalized_phone).last()
        temporary_contact, created = TemporaryContact.objects.get_or_create(phone_number=normalized_phone)
        contact_id = None
        if temporary_contact and temporary_contact.contact_id:
            try:
                result = bitrix.update_contact(temporary_contact.contact_id, contact_fields)
                try:
                    if result.status_code == 400:
                        res = bitrix.add_contact(contact_fields)
                        contact_id = res["result"]
                        temporary_contact.contact_id = contact_id
                        deal_fields["CONTACT_ID"] = contact_id
                        temporary_contact.save()
                        res = bitrix.update_deal(temporary_contact.deal_id, deal_fields)
                        try:
                            if res.status_code == 400:
                                contact_id = temporary_contact.contact_id

                                deal_fields["CONTACT_ID"] = contact_id
                                res = bitrix.add_deal(deal_fields)
                                deal_id = res.get("result")

                                temporary_contact.deal_id = deal_id
                                temporary_contact.save()
                                pass
                        except:
                            pass
                        
                except:
                    pass
                contact_id = temporary_contact.contact_id
            except Exception as e:
                
                print(e)
            if temporary_contact.deal_id:
                try:
                    res = bitrix.update_deal(temporary_contact.deal_id, deal_fields)
                    try:
                        if res.status_code == 400:
                            contact_id = temporary_contact.contact_id

                            deal_fields["CONTACT_ID"] = contact_id
                            res = bitrix.add_deal(deal_fields)
                            deal_id = res.get("result")

                            temporary_contact.deal_id = deal_id
                            temporary_contact.save()
                            pass
                    except:
                        pass
                except Exception as e:
                    print(f"shu yerdan : {e}")
            #TemporaryContact.objects.filter(phone_number=normalized_phone).delete()
        if not contact_id:
            try:
                res = bitrix.add_contact(contact_fields)
                contact_id = res["result"]

                deal_fields["CONTACT_ID"] = contact_id
                res = bitrix.add_deal(deal_fields)
                deal_id = res.get("result")

                temporary_contact.contact_id = contact_id
                temporary_contact.deal_id = deal_id
                temporary_contact.save()
                
                
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    


@shared_task(name="send_customer_to_bitrix")
def send_customer_to_bitrix(application_id):
    application = Customer.objects.get(id=application_id)

    
    contact_fields = {
        "UF_CRM_FULL_NAME": application.full_name,
        "UF_CRM_TELEGRAM_ID": application.user.telegram_id,
    }
    
    deal_fields = {
        "CATEGORY_ID": 0,
        "TITLE": 'Заполнение CRM-формы "Test"',
        "UF_CRM_FULL_NAME": application.full_name,
        "UF_CRM_COMPANY_NAME": application.company_name,
        "UF_CRM_POSITION": application.position,
        "UF_CRM_WEBSITE": application.website,
        "UF_CRM_LEGAL_ADDRESS": application.legal_address,
        "UF_CRM_MARKETPLACE_BRANDS": application.marketplace_brand,
        "UF_CRM_SEGMENT": ", ".join(application.segment.values_list("title", flat=True)),
        "UF_CRM_PAYMENT_TERMS": application.payment_terms,
  
    }


    try:
        bitrix = Bitrix24()
        normalized_phone = "+" + re.sub(r"\D", "", application.phone)
        # temporary_contact = TemporaryContact.objects.filter(phone_number=normalized_phone).last()
        temporary_contact, created = TemporaryContact.objects.get_or_create(phone_number=normalized_phone)
        contact_id = None
        if temporary_contact and temporary_contact.contact_id:
            try:
                result = bitrix.update_contact(temporary_contact.contact_id, contact_fields)
                try:
                    if result.status_code == 400:
                        res = bitrix.add_contact(contact_fields)
                        contact_id = res["result"]
                        temporary_contact.contact_id = contact_id
                        deal_fields["CONTACT_ID"] = contact_id
                        temporary_contact.save()
                        res = bitrix.update_deal(temporary_contact.deal_id, deal_fields)
                        try:
                            if res.status_code == 400:
                                contact_id = temporary_contact.contact_id

                                deal_fields["CONTACT_ID"] = contact_id
                                res = bitrix.add_deal(deal_fields)
                                deal_id = res.get("result")

                                temporary_contact.deal_id = deal_id
                                temporary_contact.save()
                                pass
                        except:
                            pass
                        
                except:
                    pass
                contact_id = temporary_contact.contact_id
            except Exception as e:
                
                print(e)
            if temporary_contact.deal_id:
                try:
                    res = bitrix.update_deal(temporary_contact.deal_id, deal_fields)
                    try:
                        if res.status_code == 400:
                            contact_id = temporary_contact.contact_id

                            deal_fields["CONTACT_ID"] = contact_id
                            res = bitrix.add_deal(deal_fields)
                            deal_id = res.get("result")

                            temporary_contact.deal_id = deal_id
                            temporary_contact.save()
                            pass
                    except:
                        pass
                except Exception as e:
                    print(f"shu yerdan : {e}")
            #TemporaryContact.objects.filter(phone_number=normalized_phone).delete()
        if not contact_id:
            try:
                res = bitrix.add_contact(contact_fields)
                contact_id = res["result"]

                deal_fields["CONTACT_ID"] = contact_id
                res = bitrix.add_deal(deal_fields)
                deal_id = res.get("result")

                temporary_contact.contact_id = contact_id
                temporary_contact.deal_id = deal_id
                temporary_contact.save()
                
                
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    



@shared_task(bind=True, max_retries=3)
def send_status_change_message_task(self, manufacturer_id, new_status, is_created=False):
   
    try:
        manufacturer = Manufacturer.objects.select_related('user').get(id=manufacturer_id)
        telegram_id = manufacturer.user.telegram_id
        if not telegram_id:
            return
        
        if is_created:
            message = (
                f"📩 Уважаемый(ая) {manufacturer.full_name}!\n\n"
                f"Ваша заявка от компании <b>{manufacturer.company_name}</b> успешно принята. "
                f"Наши менеджеры скоро её рассмотрят и свяжутся с вами. 🤝\n\n"
                f"📋 Статус заявки: <b>В процессе</b>"
            )

        elif new_status == Manufacturer.StatusChoices.APPROVED:
            message = (
                f"🎉 Поздравляем, {manufacturer.full_name}!\n\n"
                f"Ваша компания <b>{manufacturer.company_name}</b> успешно прошла проверку и "
                f"добавлена в список <b>надёжных производителей</b>.\n\n"
                f"📋 Статус заявки: <b>Одобрено</b>\n"
                f"Спасибо за доверие и желаем дальнейших успехов! 🚀"
            )

        elif new_status == Manufacturer.StatusChoices.PAID:
            message = (
                f"💰 Уважаемый(ая) {manufacturer.full_name}, мы получили оплату от вашей компании <b>{manufacturer.company_name}</b>.\n\n"
                f"Ваш платёж успешно подтверждён, и доступ к дополнительным возможностям активирован! ✅\n\n"
                f"📋 Статус заявки: <b>Оплачено</b>\n"
                f"Благодарим за сотрудничество и желаем процветания вашему бизнесу! 🌟"
            )

        elif new_status == Manufacturer.StatusChoices.CANCELED:
            message = (
                f"⚠️ Уважаемый(ая) {manufacturer.full_name}, к сожалению, в вашей заявке были обнаружены некоторые неточности.\n\n"
                f"Пожалуйста, проверьте введённые данные и отправьте заявку повторно.\n\n"
                f"📋 Статус заявки: <b>Отменено</b>\n"
                f"Если у вас возникли вопросы, наша команда поддержки всегда готова помочь 🤝"
            )

        else:
            return

        token = settings.BOT_TOKEN  
        if not token:
            raise ValueError("BOT_TOKEN не найден в настройках. Проверьте .env файл.")

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={
            "chat_id": telegram_id,
            "text": message,
            "parse_mode": "HTML"
        })

    except Exception as exc:
        self.retry(exc=exc, countdown=10)