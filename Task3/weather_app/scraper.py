from bs4 import BeautifulSoup
import requests

def get_weather(city, state, country):
    print("Entering get_weather")
    try:
        query = f'{city} {state} {country} weather'.replace(' ', "+")
        url = f'https://www.google.com/search?q={query}'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        fahrenheit = soup.find("span", id="wob_tm").text
        celsius = soup.find("span", id="wob_ttm").text
        precipitation = soup.find("span", id="wob_pp").text
        humidity = soup.find("span", id="wob_hm").text
        wind_speed_mph = soup.find("span", id="wob_ws").text
        wind_speed_kmph  = soup.find("span", id="wob_tws").text
        time_updated = soup.find("div", id="wob_dts").text

        return {
            "fahrenheit": f"{fahrenheit}°F",
            "celsius": f"{celsius}°C",
            "precipitation": f"{precipitation}",
            "humidity": f"{humidity}",
            "wind_speed_mph": f"{wind_speed_mph}",
            "wind_speed_kmph": f"{wind_speed_kmph}",
            "last_updated": f"{time_updated}",
        }
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        response.close()