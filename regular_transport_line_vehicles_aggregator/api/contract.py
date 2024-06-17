import requests

from config import config


class Contract:
    contract_base_url = config.env_config.get('apiContractUrl')

    @classmethod
    def get_contracts(self):
        path = 'api/v2/contracts'
        url = self.contract_base_url + path
        res = requests.get(headers=config.mlp_api_header, url=url)

        return res.json()

    @classmethod
    def get_services(self, contract_id: str = ''):
        path = 'api/v2/services'
        url = self.contract_base_url + path
        params = {}
        if contract_id:
            params['contract_id'] = contract_id
        res = requests.get(headers=config.mlp_api_header, params=params, url=url)

        return res.json()
