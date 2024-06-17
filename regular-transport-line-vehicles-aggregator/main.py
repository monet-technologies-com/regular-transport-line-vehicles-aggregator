import datetime
import json

from enums import ServiceCatalogs
from api.contract import Contract
from api.fleet import Fleet
from api.external_api import Slack


NON_COUNT_LIST = [1, 180]  # 集計対象外の契約ID


def main():
    regular_transport_line_contract_ids = get_regular_transport_line_contract_ids()

    # 集計対象外の契約IDを除外
    regular_transport_line_contract_ids = [regular_transport_line_contract_id
                                           for regular_transport_line_contract_id in regular_transport_line_contract_ids
                                           if regular_transport_line_contract_id not in NON_COUNT_LIST]

    monthly_vehicle_assignment_plans = get_monthly_vehicle_assignment_plans(contract_ids=regular_transport_line_contract_ids)
    monthly_assignmented_vehicles = count_monthly_assignmented_vehicles(vehicle_assignment_plans=monthly_vehicle_assignment_plans)

    # slackに送るメッセージを整形
    message_header = f'{datetime.datetime.now().strftime("%Y-%m-%d")} 時点で定時便サービスで使用されている車両台数は下記になります。\n'
    message = json.dumps(monthly_assignmented_vehicles, indent=4, ensure_ascii=False)

    message = message_header + "```" + message + "```"
    _ = Slack.send_slack_message(message=message)

    return


def get_regular_transport_line_contract_ids():
    """
    運行中のサービスカタログ定時便方向が含まれている契約IDを取得する関数

    Returns:
    list: contract_ids
    """
    services = Contract.get_services()
    dt_now = str(datetime.datetime.now())
    regular_transport_line_contract_ids = []

    # 運行中かつ定時便サービスに紐づく契約idを取得
    for service in services['services']:
        if service['deleted_at'] is None:  # 削除されていないサービス
            if service['end_datetime'] is None or service['end_datetime'] > dt_now:  # サービス終了日を迎えていないサービス
                if service['service_catalog']['id'] == ServiceCatalogs.RegularTransportLine.value:  # 定時便サービス
                    regular_transport_line_contract_ids.append(service['contract_id'])

    # 定時便は1契約1サービスだが念の為ユニークを取る
    regular_transport_line_contract_ids = list(set(regular_transport_line_contract_ids))
    return regular_transport_line_contract_ids


def get_monthly_vehicle_assignment_plans(contract_ids: list):
    """
    月毎の契約に紐づく車両割り当てを返却する関数

    Returns:
    dict: {
        'xxxx/yy車両割当計画': {contract_id1: vehicle_assignment_plan_id1, contract_id2: vehicle_assignment_plan_id2},
        'xxxx/zz車両割当計画': {contract_id3: vehicle_assignment_plan_id3, contract_id4: vehicle_assignment_plan_id4}
        }
    """
    monthly_vehicle_assignment_plans = {}

    # 契約idに紐づく運行割り当てを取得
    for contract_id in contract_ids:
        vehicle_assignment_plans = Fleet.get_vehicle_assignment_plans_bulk(contract_id=contract_id)  # 契約idに紐づく車両割当計画を取得

        # レスポンスの形に整形
        for vehicle_assignment_plan in vehicle_assignment_plans['vehicle_assignment_plans']:
            if monthly_vehicle_assignment_plans.get(vehicle_assignment_plan['name']):
                monthly_vehicle_assignment_plans[vehicle_assignment_plan['name']][vehicle_assignment_plan['contract_id']] = vehicle_assignment_plan['id']
            else:
                monthly_vehicle_assignment_plans[vehicle_assignment_plan['name']] = {vehicle_assignment_plan['contract_id']: vehicle_assignment_plan['id']}

    return monthly_vehicle_assignment_plans


def count_monthly_assignmented_vehicles(vehicle_assignment_plans: dict):
    """
    月毎の車両割り当てされた車両数を計算する関数

    Returns:
    dict: {
        'xxxx/yy車両割当計画': {
            subtotal: {contract_name: number_of_vehicle, contract_name: number_of_vehicle},  # 契約ごとの小計
            total: xxx  # 合計
            }
        }
    """
    # 契約IDから契約表示名に変換するため契約を取得
    contracts = Contract.get_contracts()
    contract_id_name_idx = {}
    for contract in contracts['contracts']:
        contract_id_name_idx[contract['id']] = contract['display_name']

    # 月の車両割り当て台数を集計
    monthly_assignmented_vehicles = {}
    for name, vehicle_assignment_plans in vehicle_assignment_plans.items():
        for contract_id, vehicle_assignment_plan_id in vehicle_assignment_plans.items():
            contract_name = contract_id_name_idx[contract_id]
            # 車両ごとの割り当て計画を取得
            vehicle_assignments = Fleet.get_vehicle_assignment_plans(contract_id=contract_id,
                                                                     vehicle_assignment_plans_id=vehicle_assignment_plan_id)
            for vehicle_assignment in vehicle_assignments['vehicles']:
                if vehicle_assignment.get('vehicle_assignments'):  # "vehicle_assignments" という項目があれば車両稼働しているとみなす
                    if monthly_assignmented_vehicles.get(name):
                        if monthly_assignmented_vehicles[name]['subtotal'].get(contract_name):
                            monthly_assignmented_vehicles[name]['subtotal'][contract_name] += 1
                            monthly_assignmented_vehicles[name]['total'] += 1
                        else:
                            monthly_assignmented_vehicles[name]['subtotal'][contract_name] = 1
                            monthly_assignmented_vehicles[name]['total'] += 1
                    else:
                        monthly_assignmented_vehicles[name] = {
                            'subtotal': {},
                            'total': 0
                        }
                        monthly_assignmented_vehicles[name]['subtotal'][contract_name] = 1
                        monthly_assignmented_vehicles[name]['total'] += 1

    return monthly_assignmented_vehicles


if __name__ == "__main__":
    main()
