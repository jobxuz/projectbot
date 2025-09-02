import requests
import itertools


class Bitrix24:

    def __init__(self):
        domain = "b24-v50vg5.bitrix24.ru"
        token = "63h82dwr6zmy8xus"
        self.base_url = f"https://{domain}/rest/1/{token}/"


    def _request(self, method = "GET", payload = None, headers = None, params = None,  bitrix_method = None):
        headers = headers or {}

        url = self.base_url + bitrix_method

        response = requests.request(method, url, json=payload, headers=headers, params=params)


        if response.ok:
            return response.json()
        else:
            return response

    def request(self, method, params, start=0):
        url = self.base_url + method + f"?start={start}"
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(res)

    def prepare_params(self, params, prev=""):
        ret = ""
        if isinstance(params, dict):
            for key, value in params.items():
                if isinstance(value, dict):
                    if prev:
                        key = "{0}[{1}]".format(prev, key)
                    ret += self.prepare_params(value, key)
                elif (isinstance(value, list) or isinstance(value, tuple)) and len(value) > 0:
                    for offset, val in enumerate(value):
                        if isinstance(val, dict):
                            ret += self.prepare_params(
                                val, "{0}[{1}][{2}]".format(prev, key, offset)
                            )
                        else:
                            if prev:
                                ret += "{0}[{1}][{2}]={3}&".format(prev, key, offset, val)
                            else:
                                ret += "{0}[{1}]={2}&".format(key, offset, val)
                else:
                    if prev:
                        ret += "{0}[{1}]={2}&".format(prev, key, value)
                    else:
                        ret += "{0}={1}&".format(key, value)
        return ret


    def get(self, method, params={}, start=0):
        start = start if start else 0
        params_flat = self.prepare_params(params)
        res = self.request(method, params_flat, start)
        if "next" in res and not start:
            items = []
            for s in range(res["total"] // 50):
                item = self.get(method, params, (s + 1) * 50)
                items.append(item)
            result = list(itertools.chain(*items))
            return res["result"] + result
        return res["result"]


    def add_contact(self, contact_data):
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "fields": contact_data
        }

        return self._request("POST", payload, headers, bitrix_method="crm.contact.add")


    def update_contact(self, contact_id, contact_data):
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "id": contact_id,
            "fields": contact_data
        }

        return self._request("POST", payload, headers, bitrix_method="crm.contact.update")


    def add_deal(self, deal_data):
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "fields": deal_data
        }

        return self._request("POST", payload, headers, bitrix_method="crm.deal.add")
    
    def update_deal(self, deal_id, deal_data):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "id": deal_id, 
            "fields": deal_data
        }
        return self._request("POST", payload, headers, bitrix_method="crm.deal.update")

