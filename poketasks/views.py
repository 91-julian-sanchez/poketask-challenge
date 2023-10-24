from .models import Pokemon
from rest_framework import viewsets
from .models import Pokemon
from .serializers import PokemonSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# API endpoint to add a skill to a specific Pokemon
class AddSkill(APIView):
    """
    API endpoint to add a skill to a specific Pokemon.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        """
        POST request to add a skill to a specific Pokemon by ID.
        """
        print(request)
        pokemon = Pokemon.objects.filter(id=id).first()
        if not pokemon:
            return Response({"message": "Pokemon not found"}, status=status.HTTP_404_NOT_FOUND)

        new_skill = request.data.get('new_skill', '')
        pokemon.skills += ", " + new_skill
        pokemon.save()
        serializer = PokemonSerializer(pokemon)  
        return Response({"message": "Skill added successfully", "data":serializer.data})

# ViewSet for managing Pokemon data
class PokemonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Pokemon data.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def create(self, request):
        """
        Create a new Pokemon or return an error if a Pokemon with the same ID already exists.
        """
        try:
            id = request.data.get('id')
            existing_pokemon = Pokemon.objects.filter(id=id).first()
            if existing_pokemon:
                print("The Pokemon already exists")
                return Response(
                    data={
                        "error": "DUP_ENTRY",
                        "message": "A Pokemon with the same ID already exists",
                        "existing_pokemon": {
                            "name": existing_pokemon.name,
                            "id": existing_pokemon.id,
                            "skills": existing_pokemon.skills
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # Log any unexpected errors and return an internal server error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
