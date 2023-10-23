from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Define API routes and views
router = DefaultRouter()
router.register(r'pokemons', views.PokemonViewSet)

# Define routes for function-based views
urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.ListPokemon.as_view(), name='list_pokemon'),
    path('search/<int:pokemon_id>/', views.SearchPokemon.as_view(), name='search_pokemon'),
    path('add_skill/<int:pokemon_id>/', views.AddSkill.as_view(), name='add_skill'),
]