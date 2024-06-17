import requests

from config import config


class Fleet:
    fleet_base_url = config.env_config.get('apiFleetUrl')

    @classmethod
    def get_vehicle_assignment_plans(self, contract_id: str, vehicle_assignment_plans_id: str):
        path = f'api/v2/vehicle/assignment/plans/{vehicle_assignment_plans_id}'
        params = {
            'contract_id': contract_id
        }

        url = self.fleet_base_url + path
        res = requests.get(headers=config.mlp_api_header, url=url, params=params)

        return res.json()

    @classmethod
    def get_vehicle_assignment_plans_bulk(self, contract_id: str):
        path = 'api/v2/vehicle/assignment/plans'
        params = {
            'contract_id': contract_id
        }

        url = self.fleet_base_url + path
        res = requests.get(headers=config.mlp_api_header, url=url, params=params)

        return res.json()
