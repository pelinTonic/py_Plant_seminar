import requests
import bs4 as bs
def get_current_temperature():
    """Dohvaća temperaturu s interneta

    Returns:
        Temperature: temperetura
    """
    try:
        URL = "https://goweather.herokuapp.com/weather/Zagreb"
        response = requests.get(URL)
        web_data = response.json()
        temperature = web_data["temperature"]
        return f"{temperature}"
    except:
        try:
            URL = "https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.98&hourly=is_day&current_weather=true&forecast_days=1&timezone=Europe%2FBerlin"
            response = requests.get(URL)
            web_data = response.json()
            temperature = web_data["temperature"]
            return f"{temperature}"
        except:
            try:
                URL = "https://vrijeme.hr/hrvatska_n.xml"
                response = requests.get(URL)
                web_data = bs.BeautifulSoup(response.text, "xml")
                for city in web_data.find_all("Grad"):
                    city_name_all = city.find("GradIDE").text
                    if city_name_all == "Zagreb":
                        temperature = city_name_all.find("Temp")
                        return temperature
                    else:
                        continue

            except:
                return "23°C"