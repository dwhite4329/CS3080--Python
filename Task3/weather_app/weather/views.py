from django.shortcuts import render
from scraper import get_weather 

# Create your views here.

def weather(request, city, state, country):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        weather_data = get_weather(city, state, country)

        if weather_data:
            context = {
                "city": city,
                "state": state,
                "country": country,
                "weather": weather_data,
                "first_name": first_name,
                "last_name": last_name,
            }
        else:
            context = {
                "city": city,
                "state": state,
                "country": country,
                "error": "Unable to get weather data.",
                "first_name": first_name,
                "last_name": last_name, 
            }

    return render(request, 'weather.html', context=context)