# from celery import shared_task
# from django.utils import timezone

# @shared_task
# def process_scheduled_posts():
#     current_time = timezone.now()
#     scheduled_posts = Post.objects.filter(scheduled_datetime__lte=current_time)
#     for post in scheduled_posts:
#         # Code to post the scheduled post goes here
#         post.delete()  # Optionally, delete the post after posting
