# CVE-2022-22978: Spring Security Authorization Bypass
## 요약

- Spring Security 프레임워크는 Spring 기반 애플리케이션에서 인증 및 권한 부여 기능을 제공하는 보안 프레임워크이다.
- Spring Security 5.5.6, 5.6.3 및 그 이전 버전에서 정규표현식을 이용하여 권한을 부여하는 기능인 `RegexRequestMatcher`를 사용할 때 요청 URL에 개행 문자가 포함되어 있으면 권한 우회가 발생할 수 있다.
- 공격자는 `%0a`, `%0d` 등 인코딩된 개행문자를 사용하여 관리자 페이지(`/admin`) 접근 권한을 우회할 수 있다.

## 환경 구성 및 실행

- `docker compose up -d` 을 실행하여 테스트 환경을 준비하였다.
- `http://localhost:8080/admin` 을 실행하여 관리자페이지에 대한 엑세스가 차단되어 있는지 확인한다.
- `http://localhost:8080/admin/%0atest` 을 실행하여 관리자 페이지에 접근한다.

![image](https://github.com/user-attachments/assets/47f67420-c311-44b9-9302-e082ea46ae5d)
![image](https://github.com/user-attachments/assets/ba19ba01-0f51-4b93-99bc-d3855b7a7097)
취약한 환경을 구성하였다.

## 결과

![image](https://github.com/user-attachments/assets/e71e2111-ffd3-476f-b15a-03e2743dbd0a)

관리자 페이지에 대한 접근이 차단되어 있다.

![image](https://github.com/user-attachments/assets/192ed347-7328-4810-9e74-3b621cc72986)
![image](https://github.com/user-attachments/assets/92873e36-c5ca-43f9-b1b3-36fc79968d97)

`%0d`는 '\r'을, `%0a`는 '\n'을 나타내는 개행문자이다. `%0d`, `%0a`를 사용하여 요청을 보내면 접근권한을 우회할 수 있다.

## 정리

`%0a`, `%0d` 등의 개행문자가 URL에 포함되어 있으면, `RegexRequestMatcher`에서 요청 경로를 필터링할 때 개행문자에 대한 처리가 누락되어 권한을 우회할 수 있게 된다. 공격자는 권한 우회를 통해 관리자 페이지에 접근하고 그곳에서 중요 정보를 탈취할 수 있기 때문에 주의가 필요하다.


깃허브 주소: https://github.com/he-ewo/CVE-2022-22978.git
