from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import LostItem, FoundItem
from .forms import LostItemForm, FoundItemForm, MatchItemForm
from .utils import segment_image, match_image_text, get_coordinates, calculate_distance, match_locations
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import LostItem, FoundItem
from .forms import LostItemForm, FoundItemForm
from .utils import get_coordinates
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def lost_item_page(request):
    """Render the page where users submit lost items with auto/manual location."""
    if request.method == "POST":
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)

            if form.cleaned_data["use_gps"]:
                lost_item.latitude = request.POST.get("latitude")
                lost_item.longitude = request.POST.get("longitude")
            else:
                lat, lng = get_coordinates(form.cleaned_data["location"]) or (None, None)
                lost_item.latitude = lat
                lost_item.longitude = lng

            image = request.FILES["image"]
            image_path = default_storage.save(f"lost_items/{image.name}", ContentFile(image.read()))
            lost_item.image = image_path
            lost_item.save()

            return JsonResponse({"message": "Lost item submitted", "item_id": lost_item.id})
    else:
        form = LostItemForm()
    return render(request, "lost_item_form.html", {"form": form})

def found_item_page(request):
    """Render the page where users submit found items with auto/manual location."""
    if request.method == "POST":
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)

            if form.cleaned_data["use_gps"]:
                found_item.latitude = request.POST.get("latitude")
                found_item.longitude = request.POST.get("longitude")
            else:
                lat, lng = get_coordinates(form.cleaned_data["location"]) or (None, None)
                found_item.latitude = lat
                found_item.longitude = lng

            image = request.FILES["image"]
            image_path = default_storage.save(f"found_items/{image.name}", ContentFile(image.read()))
            found_item.image = image_path
            found_item.save()

            return JsonResponse({"message": "Found item submitted", "item_id": found_item.id})
    else:
        form = FoundItemForm()
    return render(request, "items/found_item_form.html", {"form": form})


def match_item_page(request):
    """Render the page where users can enter a lost item ID to find matches."""
    if request.method == "POST":
        form = MatchItemForm(request.POST)
        if form.is_valid():
            lost_item_id = form.cleaned_data["lost_item_id"]
            return redirect("match_results", lost_item_id=lost_item_id)
    else:
        form = MatchItemForm()
    return render(request, "match_item_form.html", {"form": form})


def match_results_page(request, lost_item_id):
    """Find matches for a given lost item ID and display results."""
    lost_item = get_object_or_404(LostItem, id=lost_item_id)
    found_items = FoundItem.objects.all()

    matches = []
    for found_item in found_items:
        score = match_image_text(found_item.image.path, lost_item.description)
        location_score = match_locations(lost_item.location, found_item.location)
        distance = calculate_distance((lost_item.latitude, lost_item.longitude), (found_item.latitude, found_item.longitude))

        if score > 0.5 or location_score > 0.6 or distance < 5:  # Flexible threshold
            matches.append({
                "found_item_id": found_item.id,
                "found_image": found_item.image.url,
                "score": score,
                "distance_km": distance
            })

    return render(request, "match_results.html", {"lost_item": lost_item, "matches": matches})
