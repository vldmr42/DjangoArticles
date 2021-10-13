from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient


# Create your views here.
# CRUD -> Create Retrieve Update & Delete

@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse('recipes:hx-detail', kwargs={'id': id})
    context = {
        'hx-url': hx_url
    }
    return render(request, 'recipes/detail.html', context)


@login_required
def recipe_detail_hx_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse('Not Found')
    context = {
        'object': obj
    }
    return render(request, 'recipes/partials/detail.html', context)


@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list': qs
    }
    return render(request, 'recipes/list.html', context)


@login_required
def recipe_create_view(request, id=None):
    form = RecipeForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'recipes/create-update.html', context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    RecipeIngredientFormset = modelformset_factory(
        RecipeIngredient,
        form=RecipeIngredientForm,
        extra=0
    )
    qs = obj.recipeingredient_set.all()
    formset = RecipeIngredientFormset(request.POST or None,
                                      queryset=qs)
    context = {
        'form': form,
        'formset': formset,
        'object': obj,
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, 'recipes/partials/forms.html', context)
    return render(request, 'recipes/create-update.html', context)
