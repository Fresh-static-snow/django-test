from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from . import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse

@login_required
def favorites(request):
    user = request.user
    favorite_recipes = user.favorite_recipes.all()
    context = {
        'user': user,
        'favorite_recipes': favorite_recipes
    }
    return render(request, 'recipes/favorites.html', context)

@login_required
def add_to_favorites(request, pk):
    recipe = get_object_or_404(models.Recipe, pk=pk)
    user = request.user
    if recipe.favorited_by.filter(id=user.id).exists():
        recipe.favorited_by.remove(user)
        response_data = {'message': 'Recipe removed from favorites.'}
    else:
        recipe.favorited_by.add(user)
        response_data = {'message': 'Recipe added to favorites.'}
    return JsonResponse(response_data)


def add_review(request, pk):
    recipe = models.Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        author = request.POST.get('author')
        description = request.POST.get('description')
        review = models.Review.objects.create(recipe=recipe, author=author, description=description)
        # You can add any additional logic or validation here
        return redirect('recipes-detail', pk=pk)

class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return models.Recipe.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(author__username__icontains=query)
            )
        return models.Recipe.objects.all()
# Create your views here.
def home(request):
  recipes = models.Recipe.objects.all()
  context = {
    'recipes': recipes
  }
  return render(request, 'recipes/home.html', context)

def about(request):
  return render(request, 'recipes/about.html', {'title': 'about page'})


class RecipeDetailView(DetailView):
    model = models.Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        return context

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = models.Recipe
  success_url = reverse_lazy('recipes-home')

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
  model = models.Recipe
  fields = ['title', 'description']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = models.Recipe
  fields = ['title', 'description']

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)