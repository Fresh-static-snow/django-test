from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name="recipes-home"),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name="recipes-detail"),
    path('recipe/<int:pk>/add-review', views.add_review, name="add-review"),
    path('recipe/create', views.RecipeCreateView.as_view(), name="recipes-create"),
    path('recipe/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipes-update"),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),
    path('about/', views.about, name="recipes-about"),
    path('recipe/favorites/', views.favorites, name="favorites"),
    path('recipe/<int:pk>/add-to-favorites/', views.add_to_favorites, name="add-to-favorites"),
]
