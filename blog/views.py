from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
from django.contrib import messages
from django.http import HttpResponse

def update_equipment(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    # Your logic to update the equipment
    return HttpResponse("Equipment updated successfully!")
def post_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    context = {
        "characters": characters,
        "equipements": equipements,
    }
    return render(request, 'blog/character_list.html', context)

 
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    lieu = character.lieu

    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)

        if form.is_valid():
            nouveau_lieu = get_object_or_404(Equipement, id_equip=form.cleaned_data['lieu'].id_equip)

            if nouveau_lieu.id_equip == "Les Quatre Pôles - Restaurant pour animaux aquatiques" and character.etat == "Affamé":
                ancien_lieu.disponibilite = "Libre"
                ancien_lieu.save()
                character.etat = "Fatigué"
                character.lieu = nouveau_lieu

            elif nouveau_lieu.disponibilite == "Libre":
                if (nouveau_lieu.id_equip == "Eau calme en coin tranquille" and character.etat == "Fatigué") or \
                   (nouveau_lieu.id_equip == "Les Grandes Casquades" and character.etat == "Joueur") or \
                   (nouveau_lieu.id_equip == "salle de méditation" and character.etat == "Curieux"):
                    ancien_lieu.disponibilite = "Libre"
                    nouveau_lieu.disponibilite = "Occupé"
                    character.etat = "Joueur" if nouveau_lieu.id_equip == "Eau calme en coin tranquille" else \
                                     "Fatigué" if nouveau_lieu.id_equip == "Les Grandes Casquades" else \
                                     "Affamé"
                    character.lieu = nouveau_lieu

                else:
                    messages.error(request, "Le changement n'est pas autorisé car l'état du personnage ne correspond pas.")
                    return redirect('character_detail', id_character=id_character)

            else:
                messages.error(request, "Le changement n'est pas autorisé car le lieu n'est pas libre.")
                return redirect('character_detail', id_character=id_character)

            ancien_lieu.save()
            nouveau_lieu.save()
            character.save()
            return redirect('character_detail', id_character=id_character)

    else:
        form = MoveForm(instance=character)
        return render(request, 'blog/character_detail.html', {'character': character, 'lieu': lieu, 'form': form})


