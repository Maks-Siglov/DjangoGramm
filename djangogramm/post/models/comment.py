from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Comment(models.Model):
    id = models.AutoField(primary_key=True)

    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="comments"
    )

    owner = models.ForeignKey(
        "my_auth.User", on_delete=models.CASCADE, related_name="comments"
    )

    likes = GenericRelation("post.Like", related_name="liked_comments")
