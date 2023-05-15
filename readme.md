# 概要

- local: http://0.0.0.0:8000/
- admin: http://0.0.0.0:8000/admin/



# 初期コマンド

## Django
```
docker-compose run --rm web django-admin startproject projectCfg .

docker-compose run --rm web python manage.py startapp accounts

docker-compose run --rm web python manage.py makemigrations accounts

docker-compose run --rm web python manage.py migrate

docker-compose run --rm web python manage.py createsuperuser
```

# Serializerのまとめ

Serializerはやり取りされる出たのシリアライズ，デシリアライズを行う
ModelSerializer：
Modelクラスで定義しているフィールドをJSON文字列と変換するシリアライザとして利用する
listSerializer：
複数のModelリソースを利用する
Serializer：
Modelを利用せず自分で定義した形でJSON文字列と変換するシリアライザとして利用する
一言で表すと、データの入出力を扱い、モデルでの橋渡しをするクラスのことです。

シリアライズ（入力）：複雑な入力値をモデルに合わせてバリデーションしてレコードに伝える
デシリアライズ（出力）：Model（レコード）を適切な形式にフォーマットしてpythonで扱えるようにする
これらの役割を担っています。DjangoにおけるFormと同じような位置付けのようです

# Account機能
* ユーザー情報を返したい
  * ユーザのリストを返す
* ユーザ登録機能
* JWTAuth
* プロフィール機能
  * CRUD
* チャンネル機能
  * CRUD


# Viewのまとめ
[【備忘録】Django Rest Framework のViewについて](https://qiita.com/asami___t/items/f9b11a5f5d24a0bc5802)

restframeworkのViewはいくつかのクラスを継承する

- View Set
  - もっともスタンダードなやつ
  - `rest_framework.viewsets.ModelViewSet`を継承
  - 最も簡易的にCRUDを作れる
- function view
  - メソッド型のビューを作る
  - `from rest_framework.decorators.api_view`を使う
  - `def <function name>:`
  - `@api_view`のとデコーダを使用する
  - post get put patch delete全てのメソッドに対応
  - 自分でメソッドを限定して行う
- Class based Views
  - `rest_framework.views.APIView`を継承
  - HTTPメソッドごとにメソッドを作成できる
  - put,get,post等の処理は自分で書く必要がある
  - get,post,put等のメソッドがそのまま処理をしてくれる
  - また，モデルとは一切関係ない処理を作るときは基本これ
    - 値を入れたら，計算結果が帰ってくる
    - スクレイピングした結果を返す
  - その他モデルに対して処理をするときも，自作可能
- Generic Views
  - restframework御用達，お作法そのままならこれ
  - `rest_framework.generics`を継承する
  - いろいろ種類があり，上記よりも簡略化した書き方をすることが可能

---

# API一覧
## AccountAPI

```
/auth/	rest_framework.routers.APIRootView	accounts:api-root
/auth/\.<format>/	rest_framework.routers.APIRootView	accounts:api-root
/auth/account/jwt/create/	rest_framework_simplejwt.views.TokenObtainPairView	jwt-create
/auth/account/jwt/refresh/	rest_framework_simplejwt.views.TokenRefreshView	jwt-refresh
/auth/account/jwt/verify/	rest_framework_simplejwt.views.TokenVerifyView	jwt-verify
/auth/signup/	accounts.views.RegisterView	accounts:registration
/auth/user/myprofile/	accounts.views.MyUserInfoView	accounts:myprofile
/auth/user/profile/	accounts.views.ProfileViewSet	accounts:userprofile-list
/auth/user/profile/<pk>/	accounts.views.ProfileViewSet	accounts:userprofile-detail
/auth/user/profile/<pk>\.<format>/	accounts.views.ProfileViewSet	accounts:userprofile-detail
/auth/user/profile\.<format>/	accounts.views.ProfileViewSet	accounts:userprofile-list
/media/<path>	django.views.static.serve	
```
---

# APIテスト


- `curl -X POST -H "Content-Type: application/json" -d '{"email":"","password":""}' http://0.0.0.0:8000/auth/signup/`
- `curl -X POST -H "Content-Type: application/json" -d '{"email":"","password":""}' http://0.0.0.0:8000/auth/signup/`
- `curl -X POST -H "Content-Type: application/json" -d '{"email":"","password":""}' http://0.0.0.0:8000/auth/account/jwt/create/`
- `curl -X POST -H "Content-Type: application/json" -d '{"refresh":"xxxxxx"}' http://0.0.0.0:8000/auth/account/jwt/refresh/`
- `curl -X POST -H "Content-Type: application/json" -d '{"token":"xxxxxx"}' http://0.0.0.0:8000/auth/account/jwt/verify/`
- `curl -X POST -H "Content-Type: application/json" -H 'Authorization: JWT xxxxxxxxxxxxxxxxx' -d '{"nickname":"","account_id":"","bio":""}' http://0.0.0.0:8000/auth/user/profile/`
- `curl -X GET -H "Content-Type: application/json" -H 'Authorization: JWT xxxxxxxxxxxxxxxxx' http://0.0.0.0:8000/auth/admin/secret/accounts/`
- `curl -X GET -H "Content-Type: application/json" -H 'Authorization: JWT xxxxxxxxxxxxxxxxx' http://0.0.0.0:8000/auth/account/myuser`

# 開発でDB周りで詰まったとき

- `docker compose down` コンテナを削除
- `docker volume ls` ボリュームを確認
- `docker volume rm <xxxxx>` 該当ボリュームを削除
- コンテナを作り直す