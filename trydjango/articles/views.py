from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
from articles.models import Article
from .forms import ArticleForm


def article_search_view(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query=query)
    context = {
        'object_list': qs
    }
    return render(request, 'articles/search.html',
                  context=context)


@login_required
def article_create_view(request, id: int = None):
    form = ArticleForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm()
        return redirect(article_object.get_absolute_url())

    return render(request, 'articles/create.html', context=context)


def article_detail_view(request, slug: int = None):
    article_obj = None
    if id is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExists:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
    context = {
        'object': article_obj,
    }

    return render(request, 'articles/detail.html', context=context)
