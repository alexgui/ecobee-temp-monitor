import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from shutil import copyfile
import os


def get_tokens():
    # Read from text file
    f = open("ecobee_api_key.txt", "r")
    API_KEY = f.read()
    f = open("ecobee_access_token.txt", "r")
    ACCESS_TOKEN = f.read()
    f = open("ecobee_refresh_token.txt", "r")
    REFRESH_TOKEN = f.read()

    return API_KEY, ACCESS_TOKEN, REFRESH_TOKEN


def refresh_and_get_tokens():
    API_KEY, ACCESS_TOKEN, REFRESH_TOKEN = get_tokens()

    # refresh
    url = "https://api.ecobee.com/token"
    payload = {
        "grant_type": "refresh_token",
        "code": REFRESH_TOKEN,
        "client_id": API_KEY,
    }
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print("Something went wrong when trying to refresh access")
    else:
        f = open("ecobee_access_token.txt", "w")
        ACCESS_TOKEN = response.json()["access_token"]
        f.write(ACCESS_TOKEN)
        f.close()
        f = open("ecobee_refresh_token.txt", "w")
        f.write(response.json()["refresh_token"])
        f.close()

    return API_KEY, ACCESS_TOKEN, REFRESH_TOKEN


def get_thermostat_data(ACCESS_TOKEN):
    # get temperature
    url = "https://api.ecobee.com/1/thermostat"
    header = {"Content-Type": "text/json", "Authorization": "Bearer " + ACCESS_TOKEN}
    payload = {
        "json": '{"selection":{"selectionType":"registered","selectionMatch":"","includeRuntime":"true","includeSensors":"true","includeWeather":"true"}}'
    }
    response = requests.get(url, params=payload, headers=header)

    return response


def get_temperature():
    now = datetime.datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")

    API_KEY, ACCESS_TOKEN, REFRESH_TOKEN = refresh_and_get_tokens()
    response = get_thermostat_data(ACCESS_TOKEN)

    if response.status_code != 200:
        print("Something went wrong when trying to get thermostat data")
    else:
        r_json = response.json()
        r_json_thermostatList = r_json["thermostatList"][0]
        r_json_remoteSensors = r_json_thermostatList["remoteSensors"]
        r_json_weather = r_json_thermostatList['weather']

        sensorName = "Cellar"
        sensorFound = False
        for sensor in r_json_remoteSensors:
            if sensor["name"] == sensorName:
                sensorFound = True

                for capability in sensor["capability"]:
                    if capability["type"] == "temperature":
                        temp = capability["value"]
                        tempString = f"{temp[0:temp.__len__() - 1]}.{temp.__len__()}"
                        print(f"{now_formatted} - Sensor temp: {tempString} degF")
                        break
                break

        if not sensorFound:
            print(f"{sensorName} sensor not found!")

        # Get forecast data; [0] is the most accurate
        r_json_forecast = r_json_weather['forecasts'][0]
        temp_forecast = r_json_forecast['temperature'].__str__()
        tempString_forecast = f"{temp_forecast[0:temp_forecast.__len__() - 1]}.{temp_forecast.__len__()}"
    try:
        tempStringFloat = float(tempString)
    except:
        tempStringFloat = -1

    try:
        tempStringFloat_forecast = float(tempString_forecast)
    except:
        tempStringFloat_forecast = -1

    return tempString, tempStringFloat, now, tempString_forecast, tempStringFloat_forecast


def main():
    now = datetime.datetime.now()
    if os.path.exists('data.txt'):
        copyfile('data.txt',f'archive/data_backup_{now}.txt')
        os.remove('data.txt')

    # Execute once
    tempString, tempFloat, time, tempString_forecast, tempFloat_forecast = get_temperature()
    f = open('data.txt', 'a')
    f.write(f'{time},{tempString},{tempString_forecast}\n')
    f.close()

    # Start scheduler
    scheduler = BlockingScheduler()

    @scheduler.scheduled_job('interval',seconds=900)
    def my_job():
       tempString, tempFloat, time, tempString_forecast, tempFloat_forecast = get_temperature()
       f = open('data.txt','a')
       f.write(f'{time},{tempString},{tempString_forecast}\n')
       f.close()

    scheduler.start()
    # get_temperature()


if __name__ == "__main__":
    main()
