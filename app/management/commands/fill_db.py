import os
import random
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User
from faker import Faker
from app.models import Question, Comment, Tag, Likes, LikesComment, Profile



fake = Faker()


AVATAR_PATH = 'avatars/'

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Data fill ratio')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        users = []
        profiles = []
        for i in range(ratio):
            username = fake.user_name() + str(i)
            email = fake.email()
            user = User(username=username, email=email)
            users.append(user)


        User.objects.bulk_create(users)

        users = User.objects.all()[:ratio]


        for user in users:
            first_letter = user.username[0].lower()
            avatar_filename = f"{first_letter}.jpg"
            avatar_path = os.path.join(AVATAR_PATH, avatar_filename)
            profile = Profile(user=user, avatar=avatar_path, bio=fake.paragraph())
            profiles.append(profile)

        Profile.objects.bulk_create(profiles)


        tags = []
        for i in range(ratio):
            try:
                tag_name = fake.word() + str(i)
                tags.append(Tag(name=tag_name))
            except IntegrityError:
                pass

        Tag.objects.bulk_create(tags)
        tags = Tag.objects.all()[:ratio]


        questions = []
        for i in range(ratio * 10):
            question = Question(
                title=fake.sentence(),
                text=fake.paragraph(),
                user=random.choice(users)
            )
            questions.append(question)


        Question.objects.bulk_create(questions)

        questions = Question.objects.all()[:ratio * 10]

        # Добавляем теги к вопросам

        for question in questions:
            question.tags.add(*random.sample(list(tags), k=min(3, len(tags))))


        comments = []
        for question in questions:
            for _ in range(100):
                comment = Comment(
                    text_comment=fake.sentence(),
                    question=question,
                    user=random.choice(users)
                )
                comments.append(comment)
            if len(comments) >= ratio:
                Comment.objects.bulk_create(comments)
                comments = []

        Comment.objects.bulk_create(comments)
        comments = Comment.objects.all()[:ratio * 10 * 100]


        question_likes = []
        unique_question_likes = set(Likes.objects.values_list('user_id', 'pos_id'))
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            like_key = (user.id, question.id)

            if like_key not in unique_question_likes:
                question_like = Likes(
                    user=user,
                    pos=question,
                    is_like=random.choice([True, False])
                )
                question_likes.append(question_like)
                unique_question_likes.add(like_key)
            if len(question_likes) >= ratio:
                Likes.objects.bulk_create(question_likes)
                question_likes = []

        Likes.objects.bulk_create(question_likes)


        comment_likes = []
        unique_comment_likes = set(LikesComment.objects.values_list('user_id', 'comment_id'))
        for _ in range(ratio * 200):
            user = random.choice(users)
            comment = random.choice(comments)
            like_key = (user.id, comment.id)

            if like_key not in unique_comment_likes:
                comment_like = LikesComment(
                    user=user,
                    comment=comment,
                    is_like=random.choice([True, False])
                )
                comment_likes.append(comment_like)
                unique_comment_likes.add(like_key)
            if len(comment_likes) >= ratio:
                LikesComment.objects.bulk_create(comment_likes)
                comment_likes = []

        LikesComment.objects.bulk_create(comment_likes)


        self.stdout.write(self.style.SUCCESS('Database filled with test data!'))
