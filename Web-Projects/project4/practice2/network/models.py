from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # https://velog.io/@jiffydev/Django-11.-ManyToManyField-2
    # 먼저 여기서 "self"를 하게되면 User 테이블을 하나 더 만드는것(중간). 이러면 위에 포스트를 봐도 알지만 임의로 다른 Follow 테이블을 안만들어도 되기때문.
    # symmetrical, 대칭된다는 뜻이다. 예를 들어 인스타그램에서 A가 B를 팔로우하면 자동으로 B도 A를 팔로우하게 된다는 말이다.
    # 그런 관계가 필요한 경우라면 그냥 True로 냅둬도 되겠지만, 위와 같은 인스타그램에서는 그런 상황이 발생하면 안 될 것이다.
    # 그렇기 때문에 M2M필드를 생성할 때 symmetrical=False를 인자로 주어서 한 쪽이 팔로우를 하더라도 상호 팔로우가 되지 않도록 해야 한다.
    following = models.ManyToManyField("self", blank=True, related_name='followers', symmetrical=False)

class Post(models.Model):
    # 여기서 ForeignKey사용 이유. There is one author with many posts.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return f"{self.author} posted {self.content}"

    def likes(self):
        """Returns total number of likes on post"""
        return self.liked_by.all().count()

    class Meta:
        # Orders posts by most recent first, by default
        ordering = ['-created_at']

# ForeignKey와 ManyToManyField를 설명
# ForeignKey는 예를 들면 하나의 Post가 있으면 그 포스트에 여러개의 Comments가 달릴수 있음.
# ManyToManyField는 예를 들면
# https://ssungkang.tistory.com/entry/Django-%EA%B4%80%EA%B3%84%EB%A5%BC-%ED%91%9C%ED%98%84%ED%95%98%EB%8A%94-%EB%AA%A8%EB%8D%B8-%ED%95%84%EB%93%9C-ForeignKeyOneToOneFieldManyToManyField
# https://cs50.harvard.edu/web/2020/notes/4/#many-to-many-relationships -글자 검색으로 Many to Many 검색