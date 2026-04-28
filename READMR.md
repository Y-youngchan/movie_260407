# FilmAtique
<p align="center">
    <img src="https://github.com/user-attachments/assets/97365aa8-2c7b-40fb-bb1b-2b6f6afda022">
</p>
<br><br>

## 목차
- [개요](#개요)
- [주요 기능](#주요기능)
- [화면 구현](#화면-구현실행화면)
- [보고서](#보고서)
- [넣고 싶은 기능](#넣고-싶은-기능)
- [소감](#느낀점)
<br><br>

## 개요
### 목표
- 사용자가 실제 영화관처럼 편리하게 예매할 수 있는 서비스를 구현하면서, 실무 수준의 웹 개발 역량을 키우기 위한 프로젝트이다.
<br>

### 개발 기간
- 2026.04.06 ~ 2026.04.29(약 3주간)
<br>

### 팀원 소개
- 강민식 : 팀장 및 구상, DB, 프론트엔드, 백엔드
- 김동환 : DB, 프론트엔드, 백엔드
- 유영찬 : DB, 프론트엔드, 백엔드
- 조예연 : DB, 프론트엔드, 백엔드
<br>

### 개발 환경
<div align=left> 
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
  <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> 
  <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
  <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
  <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
</div>
<br><br>

## 주요기능
### 로그인/회원가입
- 일반 회원가입 및 로그인 기능을 제공하며, 사용자 인증을 통해 개인화된 서비스를 이용할 수 있다.
- 입력된 비밀번호는 암호화되어 저장되어 보안을 강화하였다.
<br>

### 예매
- 사용자는 원하는 영화를 선택하고 상영 시간 및 좌석을 선택하여 예매할 수 있다.
- 직관적인 UI를 통해 빠르고 편리한 예매 경험을 제공한다.
<br>

### 결제
- 선택한 예매 내역을 기반으로 결제를 진행할 수 있으며, 결제 완료 시 예매 정보가 저장된다.
- 실제 결제 프로세스를 고려하여 사용자 흐름을 구현하였다.
<br>

### 관리자(공지사항 등록 및 삭제)
- 관리자는 공지사항을 등록, 수정, 삭제할 수 있어 사용자에게 중요한 정보를 전달할 수 있다.
- 관리자 페이지를 통해 효율적인 서비스 운영이 가능하다.
<br><br>

## 화면 구현(실행화면)
### 메인페이지
![메인페이지](https://github.com/user-attachments/assets/db24dbff-6da6-4a89-919b-c4a593d9e36d)
* 메인 화면에서는 현재 상영 중인 영화 목록을 확인할 수 있다.
* 영화 포스터를 클릭하면 해당 영화의 상세 페이지로 이동한다.
<br>

### 로그인/회원가입
![로그인/회원가입](https://github.com/user-attachments/assets/2ad52a21-25d5-4d62-aa8d-4c4100b9357d)
* 상단 메뉴에서 `로그인` 버튼을 클릭하면 로그인 화면으로 이동한다.
* `회원가입`을 통해 새로운 계정을 생성할 수 있으며, 입력한 정보로 로그인할 수 있다.
<br>

### 예매 및 결제
![예매및결제](https://github.com/user-attachments/assets/3bd7f79c-5be6-4ace-bdc5-e077898b2ec0)
* 원하는 영화를 선택한 후 상영 시간과 좌석을 선택한다.
* 선택이 완료되면 예매 정보를 확인한 뒤 결제 화면으로 이동한다.
* 결제가 완료되면 예매가 정상적으로 처리된다.
<br>

### 상품 결제
![상품결제](https://github.com/user-attachments/assets/0883ae9f-6c8d-4bc5-9049-5e02e8c946a2)
* 상품 상세 페이지에서 `구매` 버튼을 클릭하면 결제 페이지로 이동한다.
* 결제 진행 후 완료 메시지를 통해 정상 처리 여부를 확인할 수 있다.
<br>

### 마이페이지
![마이페이지](https://github.com/user-attachments/assets/26e92469-dd7d-45a7-bcd6-1165ba79a0b0)
* 마이페이지에서는 사용자의 예매 내역을 확인할 수 있다.
* 이전에 결제한 내역과 관련 정보를 조회할 수 있다.
<br>

### 공지사항
![공지사항](https://github.com/user-attachments/assets/70ea8dcc-3da2-4b40-9f71-3fed1d9d3943)
* 공지사항 페이지에서는 서비스 관련 안내사항을 확인할 수 있다.
* 항목을 클릭하면 상세 내용을 확인할 수 있다.
<br>

### 관리자페이지
![관리자페이지](https://github.com/user-attachments/assets/130ae0b2-b3da-424a-8348-1b48f9eee2cd)
* 관리자 계정으로 접속 시 관리자 페이지에 접근할 수 있다.
* 기본 배너 변경 및 재고를 통해 상품의 품절 및 구매를 확인할 수 있다.
* 공지사항을 등록하거나 삭제하는 기능을 수행할 수 있다.
<br><br>

## 보고서
<br><br>

## 넣고 싶은 기능
- 장바구니
- 리뷰
- 성인인증
- API를 이용한 결제 취소
- 상영시간 재설정
<br><br>

## 느낀점
- 강민식 : 이번 프로젝트를 진행하면서 초반에 진행 방향을 잘못 잡아 큰 어려움이 있었지만 그럼에도 팀원들의 노력으로 방향을 다시 잡고 무리 없이 진행을 했다. 그리고 작업 중에 예매가 가능한 시스템을 구현하는 데 있어서 어려움은 있었지만 흥미를 느낄 수 있었고 초반에 방향을 잘 잡고 진행을 했다면 성인인증이나 여러 시스템을 추가하지 못한 부분이 아쉬웠다.
<br>

- 김동환 : 초기에는 하드코딩으로 기능 흐름을 먼저 구현하면서 전체 서비스 구조를 빠르게 이해할 수 있었고, 이후 DB 연동 과정에서 데이터 설계의 중요성을 체감했다. 또, 특히 회원정보와 결제 데이터를 다루면서 데이터 무결성과 보안 처리의 필요성을 직접 경험할 수 있었다.
<br>

- 유영찬 : 요즘 AI 기술의 발전으로 인해 정말 많은 정보와 다양한 도움을 받았다. 또, 아이디어 정리, 코드에 발생한 오류 문제 해결 과정에서 AI를 활용하니 시간 효율이 높아졌고, 이전보다 더 빠르고 원하는 기획에 맞게 프로젝트를 진행할 수 있었다.
<br>

- 조예연 : 프로젝트를 끝내면서 데이터베이스가 얼마나 중요한지, 그리고 내가 얼마나 부족한지 깨달았다. ChatGPT에 너무 의존한 것 같아 나중에 꼭 내 자신을 점검해야겠다는 필요성을 느꼈다. 마지막으로, 내가 직접 데이터베이스를 만든다는 점이 매우 신기하게 느껴졌다.