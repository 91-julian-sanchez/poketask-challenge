from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Define API routes and views
router = DefaultRouter()
router.register(r'pokemons', views.PokemonViewSet, basename='pokemon')

# Define routes for function-based views

urlpatterns = [
    path('', include(router.urls)),
    path('pokemons/<int:id>/add_skill/', views.AddSkill.as_view(), name='add_skill'),
]