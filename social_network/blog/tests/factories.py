import factory
from django.utils.text import slugify
from faker import Faker

from social_network.blog.models import Post
from social_network.users.tests.factories import BaseUserFactory


class PostFactory(factory.django.DjangoModelFactory):
    content = Faker().paragraph(nb_sentences=2)
    auther = factory.SubFactory(BaseUserFactory)

    @factory.lazy_attribute
    def title(self):
        title = Faker().unique.sentence(nb_words=10, variable_nb_words=False)
        title += str(self.uid)
        return title

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)

    class Params:
        uid = Faker().random_number(digits=3)

    class Meta:
        model = Post
