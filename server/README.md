# 概要
EL Streamによる永続化に失敗したリクエストをリクエストログからリカバリーする機能です

- Cloud Schedulerから1日1回 Cloud Runにリクエストが飛びます
- Cloud Runではaid毎にリカバリー処理が行われます
- 実行日の3日前のリクエストデータに対してリカバリー処理を行います
  - pubsubが最大24時間データを保持している可能性があるので、重複を避けるために2日前のデータを対象とします
  - 冪等な処理なので何度処理しても問題ありませんが、実行コストが高いので基本1日分のみを対象として実行します
- 対象日付を大きくするとBigQueryのscan量が大きくなるので注意してください
  - 1アプリ1日分実行するするのに約2~4GBのscanが走る目安としてください

# deploy
- imageの作成 & artifact registryへのpush
- cloudrunの起動

## to stg

```sh
 export PROJECT=onesdata-stg
 cd PROJECT/server
 gcloud config set project $PROJECT
 gcloud auth configure-docker asia-northeast1-docker.pkg.dev
 docker build -t asia-northeast1-docker.pkg.dev/onesdata-stg/form-docker/form:latest .
 docker push asia-northeast1-docker.pkg.dev/onesdata-stg/form-docker/form:latest 
```

## to prod

```sh
 export PROJECT=onesdata-prod
 cd PROJECT/recovery
 gcloud config set project $PROJECT
 gcloud auth configure-docker asia-northeast1-docker.pkg.dev
 docker build -t asia-northeast1-docker.pkg.dev/onesdata-prod/recovery-docker/recovery:latest .
 docker push asia-northeast1-docker.pkg.dev/onesdata-prod/recovery-docker/recovery:latest 
```

## cloudrunの起動

- コンソールからぽちぽちで起動
- 起動イメージを artifact_registry から指定
- ポートは80にする
- ingress: 全てのトラフィックを許可
- サービスアカウント: default
- 認証: 認証が必要
- 環境変数
  - (本番)PROJECT_ID: onesdata-prod
  - (stg)PROJECT_ID: onesdata-stg

## cloud schedulerの設定
- 名前: el-stream-recovery-with-request-logs
- region: asia-northeast1
- 頻度: 0 1 * * *(JST)
- target: http(GET)
- URL: https://recovery-yzucdfg5vq-an.a.run.app/recovery
- 認証: OIDC(default SA)
- 試行期限: 30m


# ローカル環境(pipenv)での動作確認

```sh
cd PROJECT/recovery
pipenv shell
export FLASK_APP=main
flask run
```

# ローカル環境(docker)での動作確認

```sh
cd PROJECT/recovery

# imageない場合
docker build -t recovery:local .

# コンテナ起動
docker run --name app -it recovery:local /bin/bash
```

# lintチェック
```
cd PROJECT/recovery

# flake8
flake8

# mypy
mypy .
```

# Cloud Schedulerの設定
- 名前は任意
- region: asia-northeast1
- 頻度: 10 0 * * * (JST)
- HTTP GET: `${cloudrunのURL}/recovery`
- AUTH: OIDC
- Service Account: xxx
- 試行期限: 30m
- その他デフォルト値

# エラー時の対応

### 全てのaidに対してリカバリーを実行したい場合
```
`${cloudrunのURL}/recovery?execute_dt=20220910&sub_days=0`
```

### execute_dtから3日分の全てのaidに対してリカバリーを実行したい場合
```
`${cloudrunのURL}/recovery?execute_dt=20220910&sub_days=0&execute_days=3`
```

### 7日前の特定のaidに対してリカバリーを実行したい場合
```
`${cloudrunのURL}/recovery?aid=10&execute_dt=20220910&sub_days=0`
```