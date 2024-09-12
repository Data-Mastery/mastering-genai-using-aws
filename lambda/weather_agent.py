
import json
from urllib import request, parse

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    param_dict = {param['name'].lower(): param['value'] for param in parameters}
    location = param_dict.get('location')
    
    if function == "get_weather":
        api_key = 'XXXXXXXXXXXXX' #put your API key here
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric'
        }
        url = f"{base_url}?{parse.urlencode(params)}"
        
        try:
            with request.urlopen(url) as response:
                weather_data = json.loads(response.read().decode('utf-8'))
        
            weather_description = weather_data['weather'][0]['description']
            weather_message = f"The current weather conditions in {location} are {weather_description}."
        except Exception as e:
            weather_message = f"An error occurred while fetching the weather data: {str(e)}"
            
        responseBody = {
            "TEXT": {
                "body": weather_message
            }
        }
    else:
        responseBody = {
            "TEXT": {
                "body": "The function {} was called successfully!".format(function)
            }
        }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }

    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response
