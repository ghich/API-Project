# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:45 2017

@author: NKaldor
"""
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import urlopen

#Get user location
def get_location( ):
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    #debug
    #print(r.text)
    city=j['city']
    state=j['region_code']
    print(state)
    print(city)
    return state, city

#Get API request
def call_api(state, city):
    response = requests.get('http://api.wunderground.com/api/b9a08daa3d694346/geolookup/conditions/forecast/q/'+state+'/'+city+'.json')
    parsed_json = json.loads(response.text)
    location = parsed_json['location']['city']
    temp_f = parsed_json['current_observation']['temp_f']
    print ("Current temperature in " + location + " is: " + str(temp_f))
    response.close()
    return parsed_json

def put_in_database(parsed_json):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Wunderground").sheet1
    
    #The geolocation we're using isn't the most accurate
    sheet.update_cell(1,1, "General location: ")
    sheet.update_cell(1,2, parsed_json['location']['city']+", "+ parsed_json['location']['state'])
    
    #Using a for loop to overwrite the data each time instead of adding new rows
    row = ["Current weather:", parsed_json['current_observation']['weather'], "Temperature", parsed_json['current_observation']['temp_f'], "Feels like: ", parsed_json['current_observation']['feelslike_f']]
    for i in range (6):
        print(row[i])
        sheet.update_cell(2,i+1, row[i])
        i += 1
        
    #debug
    #print(parsed_json['forecast']['simpleforecast']['forecastday'][2]['date']['weekday'])

    sheet.update_cell(4,1, "Forecast")
    index = 2
    for k in range(3):
        j = 0
        forecast_row = {"Day: ": parsed_json['forecast']['simpleforecast']['forecastday'][k]['date']['weekday'],
                        "High: ": parsed_json['forecast']['simpleforecast']['forecastday'][k]['high']['fahrenheit'], 
                        "Low: ": parsed_json['forecast']['simpleforecast']['forecastday'][k]['low']['fahrenheit'],
                        "Conditions: ":  parsed_json['forecast']['simpleforecast']['forecastday'][k]['conditions']}
        for key,val in forecast_row.items():
            sheet.update_cell(index+3,j+1, key)
            sheet.update_cell(index+3,j+2, val)
            print (key, val)
            j+= 2
        index += 1

state, city = get_location()
json_data = call_api(state, city)
put_in_database(json_data)

