import factory
from django.utils.text import slugify
from faker import Faker

from social_network.blog.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    title = Faker().unique.sentence(nb_words=10, variable_nb_words=False)
    content = Faker().paragraph(nb_sentences=2)
    auther = None

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)

    class Params:
        uid = Faker().random_number(digits=3)

    class Meta:
        model = Post
