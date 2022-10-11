# 環境に依存しない定数を定義してください
import os

# Cloud Runの実行時に指定します
# 本番: onesdata-prod
# stg: onesdata-stg
# デフォルト: onesdata-stg
PROJECT_ID = os.getenv('PROJECT_ID', 'onesdata-stg')
