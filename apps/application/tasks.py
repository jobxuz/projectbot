from celery import shared_task
import logging
import re

from apps.application.bitrix import Bitrix24
from .models import Manufacturer, TemporaryContact
logger = logging.getLogger(__name__)



@shared_task
def notify_manufacturer_created(manufacturer_id):
    manufacturer = Manufacturer.objects.get(id=manufacturer_id)
    print(f"Yangi Manufacturer yaratildi: {manufacturer.company_name}")
    return f"{manufacturer.company_name} created"





# @shared_task(name="send_manufacturer_to_bitrix")
# def send_manufacturer_to_bitrix(application_id):
#     application = Manufacturer.objects.get(id=application_id)
#     # user = application.user.id

    
#     contact_fields = {
#         "NAME": application.full_name if application.full_name else "Unknown",
#         "LAST_NAME": application.user.last_name if application.user.last_name else " ",
#         "SECOND_NAME": application.user.middle_name if application.user.middle_name else "",
#         "BIRTHDATE": application.birth_date.strftime("%Y-%m-%d") if application.birth_date else "",
#         "PHONE": [{"VALUE": application.user.phone, "VALUE_TYPE": "OTHER"}],
#     }
    
#     deal_fields = {
#         "CATEGORY_ID": 0,
#         "TITLE": 'Заполнение CRM-формы "Test"',
#         "UF_CRM_1740758931": application.full_name,
        
        
#     }


#     try:
#         bitrix = Bitrix24()
#         normalized_phone = "+" + re.sub(r"\D", "", application.user.phone)
#         # temporary_contact = TemporaryContact.objects.filter(phone_number=normalized_phone).last()
#         temporary_contact, created = TemporaryContact.objects.get_or_create(phone_number=phone_number)
#         contact_id = None
#         if temporary_contact and temporary_contact.contact_id:
#             try:
#                 result = bitrix.update_contact(temporary_contact.contact_id, contact_fields)
#                 try:
#                     if result.status_code == 400:
#                         res = bitrix.add_contact(contact_fields)
#                         contact_id = res["result"]
#                         temporary_contact.contact_id = contact_id
#                         deal_fields["CONTACT_ID"] = contact_id
#                         temporary_contact.save()
#                         res = bitrix.update_deal(temporary_contact.deal_id, deal_fields)
#                         try:
#                             if res.status_code == 400:
#                                 contact_id = temporary_contact.contact_id

#                                 deal_fields["CONTACT_ID"] = contact_id
#                                 res = bitrix.add_deal(deal_fields)
#                                 deal_id = res.get("result")

#                                 temporary_contact.deal_id = deal_id
#                                 temporary_contact.save()
#                                 pass
#                         except:
#                             pass
                        
#                 except:
#                     pass
#                 contact_id = temporary_contact.contact_id
#             except Exception as e:
                
#                 print(e)
#             if temporary_contact.deal_id:
#                 try:
#                     res = bitrix.update_deal(temporary_contact.deal_id, deal_fields)
#                     try:
#                         if res.status_code == 400:
#                             contact_id = temporary_contact.contact_id

#                             deal_fields["CONTACT_ID"] = contact_id
#                             res = bitrix.add_deal(deal_fields)
#                             deal_id = res.get("result")

#                             temporary_contact.deal_id = deal_id
#                             temporary_contact.save()
#                             pass
#                     except:
#                         pass
#                 except Exception as e:
#                     print(f"shu yerdan : {e}")
#             #TemporaryContact.objects.filter(phone_number=normalized_phone).delete()
#         if not contact_id:
#             try:
#                 res = bitrix.add_contact(contact_fields)
#                 contact_id = res["result"]

#                 deal_fields["CONTACT_ID"] = contact_id
#                 res = bitrix.add_deal(deal_fields)
#                 deal_id = res.get("result")

#                 temporary_contact.contact_id = contact_id
#                 temporary_contact.deal_id = deal_id
#                 temporary_contact.save()
                
                
#             except Exception as e:
#                 print(e)
#     except Exception as e:
#         print(e)
    


# @shared_task(name="send_phone_number_to_bitrix")
# def send_phone_number_to_bitrix():
#     bitrix = Bitrix24()

#     try:
#         contact_payload = {
#             "PHONE": [{"VALUE": f"{phone_number}", "VALUE_TYPE": "MOBILE"}],
#             "UF_CRM_1741801752": phone_number,
#             "UF_CRM_1743018186": password,
#         }

#         # TemporaryContact ni olish yoki yaratish
#         temporary_contact, created = TemporaryContact.objects.get_or_create(phone_number=phone_number)

#         # Agar mavjud bo‘lsa va contact_id bo‘lsa → update
#         if temporary_contact.contact_id:
#             contact_id = temporary_contact.contact_id
#             bitrix.update_contact(contact_id, contact_payload)

#             deals = bitrix.get("crm.deal.list", {
#                 "filter": {"CONTACT_ID": contact_id},
#                 "select": ["ID"]
#             })

#             deal_payload = {
#                 "CONTACT_ID": contact_id,
#                 "CATEGORY_ID": 0,
#                 "STAGE_ID": "NEW",
#                 "UF_CRM_1743018186": password,
#             }

#             if deals:
#                 deal_id = deals[0]["ID"]
#                 bitrix.update_deal(deal_id, deal_payload)
#                 temporary_contact.deal_id = deal_id
#             else:
#                 deal_res = bitrix.add_deal(deal_payload)
#                 deal_id = deal_res.get("result")
#                 temporary_contact.deal_id = deal_id

#             temporary_contact.save()

#         # Agar TemporaryContact yangidan yaratilgan yoki contact_id bo‘lmasa
#         else:
#             contact_res = bitrix.add_contact(contact_payload)
#             contact_id = contact_res.get("result")

#             if not contact_id:
#                 return  # Bitrix contact yaratmadi → taskdan chiqamiz

#             deal_payload = {
#                 "CONTACT_ID": contact_id,
#                 "CATEGORY_ID": 0,
#                 "STAGE_ID": "NEW",
#                 "UF_CRM_1743018186": password,
#             }

#             deal_res = bitrix.add_deal(deal_payload)
#             deal_id = deal_res.get("result")

#             temporary_contact.contact_id = contact_id
#             temporary_contact.deal_id = deal_id
#             temporary_contact.save()

#     except Exception as e:
#         logger.exception("Bitrixga jo'natishda xatolik:")
