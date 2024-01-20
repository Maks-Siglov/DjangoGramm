from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, QuerySet, Model

from post.utils import q_search
from post.models import Post, Like
from users.models import User


def get_posts(query: str | None, order_by: str | None) -> QuerySet[Post]:
    if query:
        posts = q_search(query)
    else:
        posts = Post.objects.all()

    if order_by and posts:
        _order_by_post(posts, order_by)

    return posts


def get_users_post(
        user: User, query: str | None, order_by: str | None
) -> QuerySet[Post]:
    if query:
        posts = q_search(query)
    else:
        posts = Post.objects.filter(owner=user)

    if order_by and posts:
        _order_by_post(posts, order_by)

    return posts


def get_following_posts(
        user: User, query: str | None, order_by: str | None
) -> QuerySet[Post]:
    following_id_list = list(
        user.profile.following.all().values_list("following_id", flat=True)
    )
    following_users = User.objects.filter(
        id__in=following_id_list
    ).all()

    if query:
        posts = q_search(query)
    else:
        posts = Post.objects.filter(owner__in=following_users)

    if order_by and posts:
        _order_by_post(posts, order_by)

    return posts


def _order_by_post(
        posts: QuerySet[Post], order_by: str | None
) -> QuerySet[Post]:
    if order_by != "default" and order_by != "likes":
        posts = posts.order_by(order_by)
    elif order_by == "likes":
        posts = Post.objects.annotate(like_count=Count("likes")).order_by(
            "-like_count"
        )

    return posts


def get_like(instance: Model, user: User) -> tuple[Like, Like, bool]:
    content_type = ContentType.objects.get_for_model(instance.__class__)

    dislike = Like.objects.filter(
        value=False,
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    ).first()

    like, like_created = Like.objects.get_or_create(
        value=True,
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    )

    return dislike, like, like_created


def get_dislike(instance: Model, user: User) -> tuple[Like, Like, bool]:
    content_type = ContentType.objects.get_for_model(instance.__class__)

    like = Like.objects.filter(
        value=True,
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    ).first()

    dislike, dislike_created = Like.objects.get_or_create(
        value=False,
        owner=user,
        content_type=content_type,
        object_id=instance.id,
    )
    return like, dislike, dislike_created