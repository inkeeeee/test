from django.contrib.auth.models import User
from news.models import *
from news.resources import *

us1 = User.objects.create_user('us1')
us2 = User.objects.create_user('us2')

au1 = Author.objects.create(user=us1)
au2 = Author.objects.create(user=us2)

sport = Category.objects.create(name='Sport')
music = Category.objects.create(name='Music')
weather = Category.objects.create(name='Weather')
games = Category.objects.create(name='Games')

art1 = Post.objects.create(author=au1, kind=article)
art2 = Post.objects.create(author=au1, kind=article)
news1 = Post.objects.create(author=au2, kind=news)

art1.category.add(sport, games)
art2.category.add(weather)
news1.category.add(music)

comm1 = Comment.objects.create(post=art1, user=us1)
comm2 = Comment.objects.create(post=art1, user=us1)
comm3 = Comment.objects.create(post=art2, user=us1)
comm4 = Comment.objects.create(post=news1, user=us2)

comm4.like()
comm4.like()
art1.like()
art1.like()
news1.like()
art1.dislike()
art2.like()
comm1.like()
comm1.like()
comm1.dislike()
comm1.like()
comm1.like()
comm1.like()
comm1.like()

for author in Author.objects.all():
    author.update_rating()

best_author = Author.objects.all().order_by('rating')[0]
print(best_author.user.username)

best_art = Post.objects.filter(kind=article).order_by('rating')[0]
print(best_art.time_in, best_art.author.user.username, best_art.rating, best_art.title, best_art.preview(), sep='\n')

for comm in Comment.objects.filter(post=best_art.pk):
    print(comm.time_in, comm.user.username, comm.rating, comm.text)




