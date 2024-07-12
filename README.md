**THIS IS A SAMPLE SOURCE CODE FOR AN ONLINE SHOPPING SITE DEVELOPED USING PYTHON　※ IT CAN BE USE JAPANESE ONLY SRY :(**

## **【日本語】**
ご覧いただきありがとうございます。
このリポジトリは、Pythonを使用して開発されたオンライン通販サイトのソースコードとインストーラーを提供します。
このアプリケーションは、ユーザーが商品を閲覧、検索、カートに追加、注文、レビューを投稿できる機能を備えています。
管理者は、商品の管理、注文の処理、ユーザーの管理などを行うことができます。

## **実装環境**
- OS: Windows 11
- Python: 3.12.1
- 必要なパッケージ
  - Flask==2.1.0
  - Flask-SQLAlchemy==2.5.1
  - Flask-Migrate==3.1.0
  - Flask-Login==0.5.0
  - Flask-WTF==0.15.1
  - Werkzeug==2.0.3
  - SQLAlchemy==1.4.32
  - WTForms==2.3.3
    
## **ファイル構成**
- app/: アプリケーションのメインディレクトリ
  - templates/: HTMLテンプレートファイル
  - static/: 静的ファイル（CSS、画像など）
  - models.py: データベースモデルの定義
  - forms.py: フォームの定義
  - routes.py: ルーティングとビューの定義
  - __init__.py: アプリケーションの初期化
- migrations/: データベースマイグレーションファイル
- config.py: アプリケーション設定ファイル
- requirements.txt: 必要なPythonパッケージのリスト
- run.py: アプリケーションのエントリーポイント
- setup.bat: セットアップと起動用のバッチファイル
- Shopping-Setup.exe: アプリケーションのインストーラー

## **導入方法**
1. Shopping-Setup.exeをダブルクリックしてインストーラーを起動します。
2. インストール先のディレクトリを選択し、インストールを進めます。
3. インストールが完了したら、デスクトップまたはスタートメニューからアプリケーションを起動します。

## **起動方法**
1. デスクトップまたはスタートメニューにあるShoppingアイコンをダブルクリックします。
2. アプリケーションが起動し、自動的に仮想環境の作成、依存関係のインストール、データベースのセットアップが行われます。
3. セットアップが完了すると、Webブラウザが開き、通販サイトのトップページが表示されます。
4. ユーザー登録またはログインを行い、商品の閲覧、検索、カートへの追加、注文、レビューの投稿などの機能を利用できます。
5. 管理者アカウントでログインすると、管理者用の機能（商品管理、注文管理、ユーザー管理など）にアクセスできます。(ID:admin, Password:admin)

<img src="https://emojix.s3.ap-northeast-1.amazonaws.com/g3/svg/26a0.svg" width="20" hight="20"> **上記の例で起動しない場合は以下の方法でお試しください。** <img src="https://emojix.s3.ap-northeast-1.amazonaws.com/g3/svg/26a0.svg" width="20" hight="20">
1. コマンドプロンプトから仮想環境を立ち上げます。
```
python -m venv [仮想環境名]
[仮想環境名]\scripts\activate
```
2. 必要なPythonライブラリをインストールします。
```
pip install -r requirements.txt
```
3. データベースの初期化をします。
```
flask db init
```
4. データベースのマイグレーションをします。
```
flask db migrate
```
5. アプリケーションを起動します。
```
flask run
```


## **その他のリソース**
- [Flask公式ドキュメント](https://flask.palletsprojects.com/en/3.0.x/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/en/20/)
- [Flask-SQLAlchemy公式ドキュメント](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- [Flask-Migrate公式ドキュメント](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-Login公式ドキュメント](https://flask-login.readthedocs.io/en/latest/)
- [Flask-WTF公式ドキュメント](https://flask-wtf.readthedocs.io/en/1.2.x/)

## **【English】**
Thank you for visiting.
This repository provides the source code and installer for an online shopping site developed using Python.
The application provides the ability for users to browse, search, add products to cart, place orders, and post reviews.
Administrators can manage products, process orders, and manage users.

## **ENV**
- OS: Windows 11
- Python: 3.12.1
- Required packages
  - Flask==2.1.0
  - Flask-SQLAlchemy==2.5.1
  - Flask-Migrate==3.1.0
  - Flask-Login==0.5.0
  - Flask-WTF==0.15.1
  - Werkzeug==2.0.3
  - SQLAlchemy==1.4.32
  - WTForms==2.3.3

## **File Structure**
- app/: Main application directory
  - templates/: HTML template files
  - static/: Static files (CSS, images, etc.)
  - models.py: Database model definitions
  - forms.py: Form definitions
  - routes.py: Routing and view definitions
  - __init__.py: Application initialization
- migrations/: Database migration files
- config.py: Application configuration file
- requirements.txt: List of required Python packages
- run.py: Application entry point
- setup.bat: Setup and launch batch file
- Shopping-Setup.exe: Application installer

## **Installation Guide**
1. Double-click on Shopping-Setup.exe to launch the installer.
2. Select the installation directory and proceed with the installation.
3. Once the installation is complete, launch the application from the desktop or start menu.

## **Starting Method**
1. Double-click on the Shopping icon on the desktop or in the start menu.
2. The application will start and automatically create a virtual environment, install dependencies, and set up the database.
3. Once the setup is complete, a web browser will open, and the top page of the shopping site will be displayed.
4. Register as a user or log in to access features such as browsing products, searching, adding to cart, placing orders, and posting reviews.
5. Logging in with an administrator account will grant access to admin features (product management, order management, user management, etc.).


## **作成者 Developer**

- 作成者: xM1guel
- GitHub: https://github.com/xM1guel
- Zenn: https://zenn.dev/miguel
