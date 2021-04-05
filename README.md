# article_django

これはDjangoで作成した簡易的なblogサイトです。  
一般的なブログのように記事を閲覧、ログインすることで記事を作成し投稿することができます。

## セットアップ方法
gitとdocker-composeを用いてこのサイトをセットアップします。  
まず、gitを用いて  
```git clone aiueo```  
コードをダウンロードします。次に、docker-composeを用いて  
```docker-compose up -d```  
コンテナを立ち上げます。最後に静的ファイルを集めるために以下を実行します。  
```docker-compose exec app bash -c 'python manage.py collectstatic'```  
以下のURLでサイトにアクセスできます。  
http://127.0.0.1:8123/article/index/  
