# 1. 👏 소개
- 프로젝트명 : **U-NFT**
  - 'U-NFT'는 블록체인은 없는 NFT를 모방한 플랫폼 서비스 입니다.

<br>

# 2. ⏱︎ 개발기간
- 2022.11.22 ~ 2022.11.27

<br>

# 3. 🦕 역할분담

- ## 🖥 Frontend
  - 팀원 전체

- ## ⚙ Backend 
  - ### **유저 파트 : 박수인, 정현주**
    - 로그인 / 회원가입 - 현주님
    - 비밀번호 찾기 메일링 - 현주님, 수인님
    - 비밀번호찾기 / 비밀번호 재설정 - 수인님

  - ### **작품 파트 : 이동영, 이현지**
    - 유화제작 딥러닝
    - UFT 생성

  - ### **거래 내역 파트 : 최해민**

<br>

# 4. 🌌 시작하기

1. 패키지 설치
    - `pip install -r requirements.txt`

2. NST 패키지 설치
    - `cd install; pip install .; cd ..`

3. Media 디렉토리 생성
    a. unft 폴더 안에 `base`, `style`, `result`, `result_pass` 디렉토리 생성

4. secrets.json 파일 생성
   - google email app 비밀번호 확인 후 아래와 같이 내용을 추가합니다.
    ```json
    {
        "SECRET_KEY": "본인의 google email SECRET_KEY",
        "SECRET_EMAIL":"본인의 google email SECRET_EMAIL",
        "SECRET_PASSWORD":"본인의 google email SECRET_PASSWORD"
    }
    ```

## 5. 📂 기능 명세서

![](https://velog.velcdn.com/images/haeminchoi2/post/ab3ee637-da94-4373-94b6-50b06623513f/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/f2d34296-e500-410b-9d04-fec508ccc48b/image.png)![](https://velog.velcdn.com/images/haeminchoi2/post/dbcb6980-4fdf-4d68-9e26-e6ec733ad444/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/75658bcc-2a03-41ef-901d-941c1ac401dd/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/7681c93c-892b-4d21-9cd9-16496cf351d8/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/48ae4aee-828f-4931-ade5-dc5cc4e90ecc/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/6cb6cd81-af7e-4264-80f3-6713d8a20011/image.png)


<br>

## 6. 📗 DB설계

![](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/e5b9baed-ebba-46c3-893b-5b23ae9de5e0/USD%E1%84%90%E1%85%B5%E1%86%B7_%E1%84%8B%E1%85%B2%E1%84%92%E1%85%AA%E1%84%8C%E1%85%A6%E1%84%8C%E1%85%A1%E1%86%A8%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3_-_U-NFT_%283%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221128%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221128T011931Z&X-Amz-Expires=86400&X-Amz-Signature=903da40f8a29c41aa65b6b3d27ba0aa87cfe39912526e1dfd36fb3835e6fe804&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22%255BUSD%25E1%2584%2590%25E1%2585%25B5%25E1%2586%25B7%255D%2520%25E1%2584%258B%25E1%2585%25B2%25E1%2584%2592%25E1%2585%25AA%25E1%2584%258C%25E1%2585%25A6%25E1%2584%258C%25E1%2585%25A1%25E1%2586%25A8%25E1%2584%2591%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25A9%25E1%2584%258C%25E1%2585%25A6%25E1%2586%25A8%25E1%2584%2590%25E1%2585%25B3%2520-%2520U-NFT%2520%283%29.png%22&x-id=GetObject)

## 7. 📕 API명세서

![](https://velog.velcdn.com/images/haeminchoi2/post/4ebae5a1-c855-4a9d-bf7e-2fd9dc5af13f/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/bf3e0119-a678-4d7f-a842-cfe86d86886e/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/96afd32e-3ec9-45c8-aa97-a8b2b4ac394a/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/5354f862-5223-4b14-bd47-641d62adf705/image.png)
![](https://velog.velcdn.com/images/haeminchoi2/post/2a534f8d-482b-4ef0-baae-b9f0c70043cd/image.png)

## 8. 🍺 이렇게 문제 해결했어요.
### <a href="https://github.com/sparta-USD/Na-dle/wiki/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85">상세보기 이동!</a>
