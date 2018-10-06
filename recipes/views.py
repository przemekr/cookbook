# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def index(request):
    tags = Tag.objects.all()
    query =  request.GET.get('q', '')
    tag =  request.GET.get('t', '')
    if tag:
        tag = get_object_or_404(Tag, name=tag)
        recipes = tag.recipes.all()
    else:
        recipes = Recipe.objects.filter(title__contains=query)

    recipes_with_img = [
            (get_thumb_url(recipe.picture_set.first()), recipe)
            for recipe in recipes
            ]


    template = loader.get_template('recipes/index.html')
    context = {
        'recipes': recipes_with_img,
        'tags': tags,
    }
    return HttpResponse(template.render(context, request))

def detail(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    pictures = recipe.picture_set.all()
    gallery = [(i[0], get_small_url(i[1]), i[1].upload.url) for i in enumerate(pictures)]
    tags = recipe.tag_set.all()
    return render(request, 'recipes/detail.html',
            {
                'recipe': recipe,
                'gallery': gallery,
                'tags': tags,
                'gallery_size': len(gallery),
            })

def contact(request):
    return render(request, 'recipes/contact.html', { })

def about(request):
    return render(request, 'recipes/contact.html', { })
