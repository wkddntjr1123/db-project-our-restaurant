# 우리들의 맛집 : 전주시 그룹별 맛집 공유 서비스
## 2021 학부 데이터베이스 프로젝트

## 기술스택 : EC2, Nginx, SQLite, Django
![ezgif-3-04354c5e1c](https://user-images.githubusercontent.com/64186072/169265051-3c749ecc-8209-42cd-a4d6-a9114ba5a14a.gif)



### 시스템 구조도
![image](https://user-images.githubusercontent.com/64186072/169104340-ff03d4a3-9cae-49d0-8170-4fe01d0fc114.png)

### DB 구조
![image](https://user-images.githubusercontent.com/64186072/169104668-67af007b-3e5a-4e7b-ab6a-a16d6979abc4.png)

1. 사용자 그룹별로 전주시 내의 음식점들에 대한 솔직한 리뷰를 공유하는 서비스
2. 각 사용자들은 그룹을 만들 수 있고 해당 그룹의 관리자가 된다
3. 그룹의 관리자는 다른 사용자들을 초대할 수 있다
4. 각 그룹의 관리자들이 멤버를 초대하는 구조이기 때문에 그룹 리뷰만 모아본다면 허위 리뷰를 쓰는 사용자들을 사전에 걸러낼 수 있다.
5. Kakao 지도 API를 이용하여 전주시 내의 모든 음식점을 보여줌
6. 원하는 메뉴나 음식점 이름 등을 입력하여 필터링 가능
7. 해당 음식점 마커를 클릭 시 모든 사용자의 리뷰, 그룹원들이 작성한 리뷰를 모아서 볼 수 
