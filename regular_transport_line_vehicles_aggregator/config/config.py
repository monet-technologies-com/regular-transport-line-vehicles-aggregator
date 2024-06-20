import os


# 環境設定の辞書
config = {
    'dev': {
        'referer': 'https://dev-monet-life-admin.monet-technologies.co.jp',
        'apiContractUrl': 'https://dev-monet-life-contract-api.monet-technologies.co.jp/',
        'apiFleetUrl': 'https://dev-monet-life-fleet-api.monet-technologies.co.jp/'
    },
    'alpha-dev': {
        'referer': '',
        'apiContractUrl': 'https://dev-alpha-monet-life-contract-api.monet-technologies.co.jp/',
        'apiFleetUrl': 'https://dev-alpha-monet-life-fleet-api.monet-technologies.co.jp/'
    },
    'stg': {
        'referer': 'https://stg-monet-life-admin.monet-technologies.co.jp/',
        'apiContractUrl': 'https://stg-monet-life-contract-api.monet-technologies.co.jp/',
        'apiFleetUrl': 'https://stg-monet-life-fleet-api.monet-technologies.co.jp/'
    },
    'alpha-stg': {
        'referer': 'https://stg-alpha-monet-life-admin.monet-technologies.co.jp/',
        'apiContractUrl': 'https://stg-alpha-monet-life-contract-api.monet-technologies.co.jp/',
        'apiFleetUrl': 'https://stg-alpha-monet-life-fleet-api.monet-technologies.co.jp/'
    },
    'trial': {
        'referer': 'https://trial-monet-life-admin.monet-technologies.co.jp',
        'apiContractUrl': 'https://trial-monet-life-contract-api.monet-technologies.co.jp/',
        'apiFleetUrl': 'https://trial-monet-life-fleet-api.monet-technologies.co.jp/'
    },
    'prod': {
        'referer': 'https://monet-life-admin.monet-technologies.co.jp',
        'apiContractUrl': 'https://monet-life-contract-api.monet-technologies.co.jp/',
        'apiFleetUrl': 'https://monet-life-fleet-api.monet-technologies.co.jp/'
    }
}

# 環境変数を取得
ENV = os.environ.get('ENV', '')

# jwtトークンを取得
TOKEN = os.environ.get('TOKEN', '')

# 環境設定を取得
env_config = config.get(ENV)

# 環境設定が見つからない場合はエラーを発生
if not env_config:
    raise ValueError(f'Invalid environment: {ENV}')

# slack webhook url
slack_webhook = 'https://hooks.slack.com/services/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'

# HTTPヘッダーを設定
mlp_api_header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TOKEN}',
    'User-Agent': 'MonetMoveTool',
    'Referer': env_config['referer']
}
