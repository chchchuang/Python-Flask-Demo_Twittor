# Python Flask Demo - Twittor

>* 這是一個用Python Flask、JavaScript (AJAX, Fetch)、Bootstrap 、MySQL、Docker架設並部署在 AWS 的社交網站

## Demo 網址

* https://twittor.link/
* 可以使用 (帳號: **root**/ 密碼: **root**) 或自行註冊帳號進行登入
* 未來不定期下線 

## Architecture Diagram 架構圖

![Twittor_Architecture](https://user-images.githubusercontent.com/111694502/230896354-4f0d9306-14bb-45d2-a423-4ed863124208.jpg)

## Prerequisites 使用環境
* 前端: 
  * HTML
  * [Bootstrap](https://getbootstrap.com/)
  * JavaScript (AJAX, Fetch)
* 後端: 
  * [Python Flask](https://flask.palletsprojects.com/en/2.2.x/)
    * form
    * login
    * mail
    * sqlalchemy
    * migrate
    * moment
    * share
  * 第三方登入: [Facebook for Developers](https://developers.facebook.com/?locale=zh_TW) Facebook Login API
* 雲端部署: 
  * [Amazon Web Services](https://aws.amazon.com/tw/)(AWS) EC2
  * [Docker](https://www.docker.com/) (Docker-Compose)
  * [NGINX](https://www.nginx.com/)
  * [Certbot (Let's encrype)](https://certbot.eff.org/)
* 資料庫: 
  * [MySQL](https://www.mysql.com/)
  * [SQLite](https://www.sqlite.org/index.html) (local開發時使用)

## Usage example 使用範例

### login

> 1. 使用 Twittor 帳號登入系統
> 2. 支持第三方 Facebook 帳號登入
<img width="1440" alt="Twittor-login page" src="https://user-images.githubusercontent.com/111694502/230837030-0fff7fd2-fe89-4848-90c1-a8906b136b0c.png">
<img width="1440" alt="Twittor-FB login page" src="https://user-images.githubusercontent.com/111694502/230837280-658af4f6-0fee-4310-b191-99228c1a6082.png">


### register

> 註冊 Twittor 帳號且需進行 email 驗證
<img width="1440" alt="Twittor-register page" src="https://user-images.githubusercontent.com/111694502/230837618-07c37458-7ab4-4566-8d37-163ca4a08b1d.png">
<img width="1129" alt="Twittor-activate email" src="https://user-images.githubusercontent.com/111694502/230837803-17535712-fa46-41cf-ab64-dfdb03e1841c.png">


### reset password

> 忘記密碼時, 進行 email 驗證後可以重設密碼
<img width="1440" alt="Twittor-reset password" src="https://user-images.githubusercontent.com/111694502/230837975-53061cf2-d362-4914-9af1-ba4369c3c6a0.png">
<img width="1128" alt="Twittor-reset email" src="https://user-images.githubusercontent.com/111694502/230838010-8870cf98-2bad-4559-aaea-1a1a8809593f.png">


### user profile/ (un)follow

> 1. 在 user 頁面可以編輯個人介紹
> 2. 支持 follow/unfollow 其他用戶發文的推文
<img width="1440" alt="Twittor-user page" src="https://user-images.githubusercontent.com/111694502/230838146-19b59be9-0abc-4787-8fe5-cf524c66923c.png">
<img width="1440" alt="Twittor-follow:unfollow" src="https://user-images.githubusercontent.com/111694502/230838186-311d9c35-47de-446f-a8d5-40015a0fa132.png">


### tweet

> 1. 在 tweet 頁面可以進行推文
> 2. 支持修改及刪除自己的推文, 修改後會註明已編輯[Edited]
> 3. 推文時間根據用戶本地時間顯示
<img width="1440" alt="Twittor-tweet page" src="https://user-images.githubusercontent.com/111694502/230838894-0c517fbb-04af-4a69-8c95-3370ae44fb3a.png">


### explore

> 1. 查看其他貼文(包含未 follow 用戶)
> 2. 支持按讚功能且顯示按讚數, 並可以分享到外部網站
> 3. 貼文分頁載入(pagination), 減少卡頓可能
<img width="1440" alt="Twittor-explore page" src="https://user-images.githubusercontent.com/111694502/230851393-46630dd2-0de7-4669-81ec-657dd1eb7ed7.png">


## Authors 關於作者
* Author: **chchchuang**  
* Update: 2023-04-10  
* Contact: chchchuang@gmail.com

## Reference 參考資料
* 參考[repo](https://github.com/xiaopeng163/twittor)架構進行修改及新功能開發
