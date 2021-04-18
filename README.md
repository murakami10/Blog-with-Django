# Blog-with-Django

これはDjangoで作成した社内やグループ内で使える簡易的なblogサイトです。  
一般的なブログのように記事を閲覧でき、ログインすることで記事を作成し投稿することができます。

<img width="1427" alt="top" src="https://user-images.githubusercontent.com/53958213/113576870-4b08f280-965b-11eb-8520-cec43296e6bb.png">

# セットアップ方法

gitとdocker-composeを用いてこのサイトをセットアップします。  
まず、gitを用いてコードをダウンロードします。
~~~
git clone https://github.com/murakami10/Blog-with-Django.git
~~~  
次に、ダウンロードしたコードの中でdocker-composeを用いてコンテナを立ち上げます。
~~~
cd Blog-with-Django
docker-compose up -d
~~~  
最後に静的ファイルを集めるために以下を実行します。  
~~~
docker-compose exec app bash -c 'python manage.py collectstatic'
~~~  
以下のURLでサイトにアクセスできます。  
http://127.0.0.1:8123/article/index/  

ログインするためのユーザー情報は以下になります。  
* email: root@root.com  
* password: aiueoaiueo

# 使用技術
- Python 3.8
- Django 3.1
- MySQL 5.7
- Nginx
- Docker/Docker-compose
- uWSGI 2.0.17
- django-mdeditor 0.1.18
- black 19.10b0
- markdown 3.3.4
- django-bootstrap-datepicker-plus 3.0.5

# 機能一覧

- 記事閲覧機能
- カテゴリー、タグ選択機能
- ログイン機能
- 記事投稿機能
- カテゴリとタグ追加機能
- 記事の削除機能
- 投稿記事編集機能
- ページネーション機能 
- ユーザ名,メールアドレス,パスワード変更機能
- ユーザの作成機能
