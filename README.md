# Project 07_관계형 데이터베이스 설계

## 1. 프로젝트 소개

- 진행 일시: 2021.04.02 (금)
- 프로젝트 내용
  - 커뮤니티 서비스 의 회원관련 기능 개발을 위한 단계
  - 모델간의 관계 설정 후 데이터의 생성/조회/수정/삭제 할 수 있는 기능을 완성

- **역할 분담**: 페어인 김영주님과 기능별로 `navigator` / `driver` 역할 번갈아가며 담당
- **진행 상황**: 마감 기한 내 모든 문제 해결 완료!



## 2. 결과 사진



## 3. 문제 해결 과정

### a. 필수 기능 구현

>  수업시간에 배운 내용이라서 어렵지 않게 구현할 수 있었다.

#### 1. 좋아요 기능

1. `models.py`: User-Review를 M:N관계로 설정한다. 이 때 기존의 1:N 관계(유저가 리뷰 작성)와의 매니저가 겹치는 것을 방지하기 위해 `related_name` 옵션을 준다.

   ```python
   class Review(models.Model):
       user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
       like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
       ...
   ```

2. `urls.py` : `path('<int:review_pk>/like/', views.like, name='like')`

3. `views.py - like`

   - 요청을 보낸 유저가 '해당 리뷰를 좋아요 한 유저 목록'에 존재하면 그 목록에서 제거한다. (좋아요 취소)
   - 존재하지 않으면 그 목록에 추가한다. (좋아요)

4. templates

   - `index.html` : 좋아요 개수를 게시글마다 보여준다.
   - `detail.html` : 좋아요를 누르지 않은 상태는 투명 하트  / 누른 상태는 빨간 하트로 구별한다. 또한 좋아요를 누른 사람 수를 보여준다.

   

#### 2. 팔로우 기능

1. `models.py`: User-User를 M:N 관계로 설정한다. 이 때 `symmetrical=False` 로 설정하여 자동 맞팔로우가 되지 않게 한다.

   ```python
   class User(AbstractUser):
       followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
   ```

2. `urls.py` : `path('<int:user_pk>/follow/', views.follow, name='follow')`

3. `views.py - follow`

   - 요청한 유저(myself)와 팔로우를 하고자 하는 유저(other)가 다를 때만 함수를 실행한다.
   - other의 followers에 myself의 pk가 존재하면 그 목록에서 제거한다. (팔로우 취소)
   - 존재하지 않으면 그 목록에 추가한다. (팔로우)

4. `profile.html`

   - 자기 자신의 프로필 페이지에서는 팔로우/팔로우 취소 버튼이 보이지 않는다.
   - 팔로우를 한 상태에서는 팔로우 취소, 그렇지 않은 상태에서는 팔로우 버튼이 보인다.



### b. 추가 기능 구현

#### 1. profile page

- 내 프로필은 '내 프로필', 다른 회원의 프로필은 '[회원이름]님의 프로필'로 보인다.
- 팔로우, 팔로우 취소 버튼 외에 팔로우, 팔로잉 회원 수 / 작성한 글 목록 / 좋아요한 글 목록이 보인다.
- 네비게이션 바에 있던 '회원정보수정', '회원탈퇴' 버튼을 내 프로필 페이지 내부로 이동했다.

#### 2. Social login

> 소셜 로그인 중 가장 쉽다고 한 google 을 도전해보았지만... 쉽지 않았다.

1. https://django-allauth.readthedocs.io/en/latest/installation.html 문서를 참고하여 기초 환경을 세팅한다.

2. https://console.developers.google.com/ 에서 프로젝트를 생성한 후 받은 Client ID 와 Secret key를 사용하여 admin 페이지 - 소셜 계정 - 소셜 어플리케이션에 추가한다.
3. 이 때 google 계정으로 로그인을 하면 바로 빈 profile 페이지로 이동하는 문제가 생겼다. 이를 해결하기 위해 `settings.py` 에서 `LOGIN_REDIRECT_URL = 'community:index'` 를 추가하여 로그인 후 redirect 하는 url을 메인 페이지로 설정하였다.



#### 3. Pagination

> 소셜 로그인을 힘들게 성공한 후에 봐서 그런지 쉬워 보였는데 오히려 더 어려웠다. 😂

1. `community/views.py` 에 `Paginator`를 import 한다.
2. `Paginator` 관련 개념을 이해해보았다.
   - Paginator(objects, n): 받은 객체들 중 n개를 한 페이지에 보여주게 한다.
   - get_page(n): n번 페이지를 가져온다.
   - has_next(): 다음 페이지의 유무를 boolean 값으로 리턴한다.
   - has_previous(): 이전 페이지의 유무를 boolean 값으로 리턴한다.
   - num_pages(): 총 페이지 수
3. 원래 하려고 했던 디자인은 페이지 숫자를 3개씩 보여준 다음, 이전/다음 버튼을 누르면 그 전/다음 페이지 숫자 3개가 나오게 하는 것이었다. (ex. 1-2-3 이 있고 다음 버튼 누르면 4-5-6이 나옴) 
4. 하지만 이렇게 하기에는 너무 복잡해보여서 이전/다음 버튼을 누를 때 해당 페이지 바로 전/후 페이지가 나오도록 구현했다.



#### 4. new-badge

> 이것 역시 쉽지 않았다... 하지만 해냈다! 🏆

1. 처음엔 html에서 `{% if 현재시간 - review.create_at < 특정시간 %}` 형태로 구현하려고 했는데 DTL에서는 뺄셈을 하지 못해서 실패했다. 그래서 view에서 해결하는 것으로 접근 방향을 바꿨다.
2. datetime 모듈을 이용하여 받아온 현재시간(current)과 모든 리뷰들의 생성시각을 비교하고자 했다. `paginator.get_page(page)` 를 할당한 `reviews`를 for문으로 돌면서 created_at 필드에 접근하려 했는데, 일반 쿼리셋과 타입이 달라서 그런지 current와 계산이 되지 않았다.
3. 파이썬의 날짜/시간 관련 함수를 찾다가 `timedelta`라는 함수를 발견하여 현재 시간의 10분 전인 `ten_minutes_before` 변수를 생성했다.
4. 또한 ORM에서 시간을 비교할 수 있다는 점을 발견하여 모든 리뷰 객체 중 생성 날짜가 현재 날짜와 같고 + 생성 시각이 `ten_minutes_before` 보다 큰(즉, 생성된 지 10분 미만인) 리뷰만을 필터링하여 `new_reviews`에 받아 context에 넘겼다.
5. html에서 해당 리뷰가 new_reviews에 있으면 'new' 뱃지를 보여주도록 구현했다.



- Pagination 과 new-badge 기능을 구현한 community/index 함수

```python
@require_safe
def index(request):
    reviews_all = Review.objects.order_by('-pk')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(reviews_all, 10)
    reviews = paginator.get_page(page)
    current = datetime.today()
    ten_minutes_before = current - timedelta(minutes=10)
    new_reviews = Review.objects.filter(created_at__date=current, created_at__time__gt=ten_minutes_before.time())
    context = {
        'reviews': reviews,
        'ten_minutes_before': ten_minutes_before,
        'new_reviews': new_reviews,
    }
    return render(request, 'community/index.html', context)
```



#### 5. 기타

- google font 사이트에서 가져온 영문/한글 폰트를 적용했다. 이 때 static을 활용해서 font에 해당하는 css style 파일을 따로 저장해두었다.
- table 태그를 활용하여 index페이지의 영화 리뷰, profile페이지의 작성 글 목록/좋아요 글 목록을 표 형태로 구현하여 보다 깔끔하게 만들었다.



## 4. 후기

💡 **총평**: 지난 프로젝트에 이어서 시작한거라 저번만큼 막막하진 않았지만, 새로운 기능을 추가하는게 매우 어려웠어서 프로젝트 진행 시간은 비슷하게 걸렸다. (하루종일...😂)  그래도 기존에 배운 것 외에 다양한 기능을 구현해냈고, 그 과정에서 더욱 성장한 것 같아 뿌듯하다. 또 프로젝트 중간에 다른 친구들이 와서 구경하기도 하고, 반대로 다른 친구들의 프로젝트를 볼 수 있어서 좋았다. 우리가 생각하지 못한 기능들, 또는 생각'만' 했던 기능들을 구현한 것을 본 게 새로운 자극이 되었다. 함께 하루종일 고생한 영주님께도 감사의 말씀을...!



💡 **프로젝트를 하며 새로 배운 것**

1. 소셜 로그인, 페이지네이션 등 다양한 기능
2. DTL 에서는 연산을 하지 못 한다는 점
3. ORM에서 시간/날짜 비교도 할 수 있다는 점 



🙂 **잘한 점**

- 여러 난관에 부딪혔음에도 불구하고 포기하지 않고 기능 구현을 해낸 점 (new...💫)



🙁 **아쉬운 점**

- 시간 문제로평점을 별모양으로 나타내기, 글/댓글 삭제 시 모달 등 자잘한 기능들을 구현해내지 못한 점... 다음 프로젝트에는 꼭 해봐야지💪