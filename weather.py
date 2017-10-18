import pyowm

def weather(place):
	owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')
	observation = owm.weather_at_place(place)
	w = observation.get_weather()
	complete_temp = w.get_temperature('celsius') 
	for i in complete_temp:
		if(i=="temp"):
			return complete_temp[i]

print(weather("South America"))