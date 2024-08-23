import json
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models, limesurvey

def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("survey")
        else:
            error_message = 'incorrect password or username.'
            context = {'error_message' : error_message}
            return render(request,"login.html", context)
    else:
        return render(request, "login.html")

def logoutview(request):
    logout(request)
    request.session.flush()
    return redirect("login")

def surveyview(request):
    if not request.user.is_authenticated:
        return redirect("login")
    items = models.Item.objects.all()
    print(items)
    if request.method == 'POST':
        user = request.user
        play_chess = request.POST.get('chess')
        elo_rating = request.POST.get('elo')
        play_chess_daily = request.POST.get('daily')
        participate_in_tournament = request.POST.get('tournament')
        experience = request.POST.get('problems')
        
        preference = []
        
        for item in items:
            preference.append(request.POST.get(f'{item.item_name}'))
        
        new_item_name = request.POST.get('new-item')
        print(user)
        print(play_chess)
        print(elo_rating)
        print(play_chess_daily)
        print(participate_in_tournament)
        print(experience)
        print(preference)
        print(new_item_name)
        if "Chess Pieces" in new_item_name:
            new_item = models.Item.objects.create(user=request.user, item_name = new_item_name)
        else:
            context = {'error_message': 'Did not enter Suggestion for Chess Pieces correctly.'}
            return render(request, "survey.html", context)
        allitems = models.Item.objects.all()
        context = {'items':allitems}
        return render(request, "survey.html", context)
    else:
        context = {'items':items}
        return render(request, "survey.html", context)

def get_latest_suggestion(request):
    new_suggestion = str(limesurvey.get_latest_suggestion())
    print(new_suggestion)
    new_item, created = models.Item.objects.get_or_create(item_name=new_suggestion)
    item_set = models.Item.objects.all().distinct()
    item_list = [
        item['item_name'] 
        for item in item_set.values('item_name') 
        if item['item_name'] and item['item_name'] != 'None'
    ]
    print(item_list)
    context = {'suggestions': item_list}
    return JsonResponse(context)

suggestion_rating_dict = {} #to store the solution and rating as key value pairs
@csrf_exempt
def post_suggestion_ratings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_value = data.get("solution")
            selected_rating = data.get("rating")
            suggestion_rating_dict[f"{selected_value}"] = selected_rating
            print(f" {selected_value} : {selected_rating} ")
            response_data = {
                "message": "Rating received successfully!",
            }
            print(suggestion_rating_dict) #temporarily stored in a dictionary - should be saved to Db
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
