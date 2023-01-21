import json
import re
import pandas as pd


responses = [] # array of all the responses
requests= [] # array of all the request
result = [] # array of all the merged responses and requests

# Array of the total Team Emissions
emissionTotal = [{
    'Username': 'Team Total',
    'Address': '',
    'Total Red Meat Emission': 0,
    'Total Grains Emission': 0,
    'Total Dairy Emission': 0,
    'Total Cellphone Emission': 0,
    'Total TV Emission': 0,
    'Total Computer Emission': 0,
    'Total Car Emission': 0,
    'Total Walking Emission': 0,
    'Total Food CO2 Emission': 0,
    'Total Public Transport Emission': 0,
    'Total Electronic CO2 Emission': 0,
    'Total Transportation CO2 Emission': 0,
    'Total Team Emission': 0,
    'Total Team New Year Predicted Emissions': 0
}
]

"""
Calculates the emission of a given action based on the giving value (amount or hour) and the CO2 per (hour or kg)
Param:
    type: A String that signifies the type of emission activity
    value: A Float that siginifies the amount or hour of the giving activity
Return: The calculated emission for the given activity and value
"""
def calcEmission(type, value):
    emission = {
        'Public Transport': 4.3,
        'Car': 6.5,
        'Walking': 0.0,
        'Red Meat': 8.0,
        'Dairy': 6.3,
        'Grains': 3.7,
        'Cellphone': 3.6,
        'Computer': 4.2,
        'TV': 6.8
    }

    carbonEmmission = value*emission[type]

    return carbonEmmission


# read data
with open('original.txt', 'r') as f:
    # Used to check if the data is a request or response
    isRes = False 
    isReq = False
    
    # Sets where the end of the file is
    f.seek(0,2)
    eof = f.tell()
    f.seek(0,0)
    nextLine = True 

    data = f.readline()
    
    # Used to store the data that is read
    retrivedData = {}

    # Loops through the file to get all the data and appends them to their respective array
    while nextLine:

        # Checks if the line is empty
        if len(data.strip()) == 0:
            if isReq:
                requests.append(retrivedData)
            else:
                responses.append(retrivedData)

            # Resets the value to ensure that the next data set is properly checked
            isReq = False
            isRes = False

            # Clears the retrived data so new data can be put in
            retrivedData = {}

        # Checks if we have reached the end of the file
        if f.tell() == eof:
            nextLine = False
        
        # Checks if the set of data is a Request
        if "Request" in data:
            isReq = True
            isRes = False
            # read next line
            data = f.readline()

        # Checks if the set of data is a Response 
        elif "Response" in data:
            isReq = False
            isRes = True
            # read next line
            data = f.readline()

        # store in keyvalue pairs  
        if isReq:
            key = data.split(":", 1)[0]
            value = data.split(":", 1)[1].strip()
            retrivedData[key] = value

        elif isRes:
            key = data.split(":", 1)[0]
            value = data.split(":", 1)[1].strip()
            retrivedData[key] = value

        data = f.readline()

    # Loops through the requests and responses to merge the correct data together and filter unneeded data
    for req in requests:

        data = {
            
        }

        # Loops through the responses to find the response that matches the requests
        for res in responses:
            if req['Controller'] == res['Controller'] and res['Endpoint'].split('(OWL)')[1].strip() == req['Endpoint'].strip():

                # Transportation Emissions
                car = calcEmission('Car', float(re.split(r'hours|hour', res['Car'], flags=re.IGNORECASE)[0]))
                walking = calcEmission('Walking', float(re.split(r'hours|hour', res['Walking'], flags=re.IGNORECASE)[0]))
                publicTransport = calcEmission('Public Transport', float(re.split(r'hours|hour',res['Public Transport'], flags=re.IGNORECASE)[0]))
                totalTransportEmissions = car + walking + publicTransport
                
                # Food Emissions
                redMeat = calcEmission('Red Meat', float(re.split(r'pounds|pound', req['Red Meat'], flags=re.IGNORECASE)[0]) / 2.205)
                grains = calcEmission('Grains', float(re.split(r'pounds|pound', req['Grains'], flags=re.IGNORECASE)[0]) / 2.205)
                dairy = calcEmission('Dairy', float(re.split(r'pounds|pound', req['Dairy'], flags=re.IGNORECASE)[0]) / 2.205)
                totalFoodEmissions = redMeat + grains + dairy

                # Electronics Emissions
                cellphone = calcEmission('Cellphone', float(re.split(r'hours|hour', req['Cellphone'], flags=re.IGNORECASE)[0]))
                tv = calcEmission('TV', float(re.split(r'hours|hour', req['TV'], flags=re.IGNORECASE)[0]))
                computer = calcEmission('Computer', float(re.split(r'hours|hour', req['Computer'], flags=re.IGNORECASE)[0]))
                totalElectronicsEmissions = cellphone + tv + computer

                totalEmissions = totalTransportEmissions + totalFoodEmissions + totalElectronicsEmissions

                newYearEmissions = totalEmissions * (1 - float(req['New Year Resolution'].split('%')[0]) / 100)
                
                # Adds the filter and merged data to the result array
                data['Username'] = res['Username']
                data['Address'] = req['Address']
                data['Red Meat'] = calcEmission('Red Meat', float(re.split(r'pounds|pound', req['Red Meat'], flags=re.IGNORECASE)[0]) / 2.205)
                data['Grains'] = calcEmission('Grains', float(re.split(r'pounds|pound', req['Grains'], flags=re.IGNORECASE)[0]) / 2.205)
                data['Dairy'] = calcEmission('Dairy', float(re.split(r'pounds|pound', req['Dairy'], flags=re.IGNORECASE)[0]) / 2.205)
                data['Cellphone'] = calcEmission('Cellphone', float(re.split(r'hours|hour', req['Cellphone'], flags=re.IGNORECASE)[0]))
                data['TV'] = calcEmission('TV', float(re.split(r'hours|hour', req['TV'], flags=re.IGNORECASE)[0]))
                data['Computer'] = calcEmission('Computer', float(re.split(r'hours|hour', req['Computer'], flags=re.IGNORECASE)[0]))
                data['Car'] = calcEmission('Car', float(re.split(r'hours|hour', res['Car'], flags=re.IGNORECASE)[0]))
                data['Walking'] = calcEmission('Walking', float(re.split(r'hours|hour', res['Walking'], flags=re.IGNORECASE)[0]))
                data['Public Transport'] = calcEmission('Public Transport', float(re.split(r'hours|hour',res['Public Transport'], flags=re.IGNORECASE)[0]))
                data['Food CO2 Emissions'] = totalFoodEmissions       
                data['Electronic CO2 Emissions'] = totalElectronicsEmissions
                data['Transportation CO2 Emissions'] = totalTransportEmissions
                data['Total CO2 Emissions'] = totalEmissions
                data['New Year Predicted Emissions'] = newYearEmissions

                result.append(data)

                # Adds to the total emission of the team
                emissionTotal[0]['Total Red Meat Emission'] += redMeat
                emissionTotal[0]['Total Grains Emission'] += grains
                emissionTotal[0]['Total Dairy Emission'] += dairy
                emissionTotal[0]['Total Cellphone Emission'] += cellphone
                emissionTotal[0]['Total TV Emission'] += tv
                emissionTotal[0]['Total Computer Emission'] += computer
                emissionTotal[0]['Total Car Emission'] += car
                emissionTotal[0]['Total Walking Emission'] += walking
                emissionTotal[0]['Total Public Transport Emission'] += publicTransport
                emissionTotal[0]['Total Food CO2 Emission'] += totalFoodEmissions
                emissionTotal[0]['Total Electronic CO2 Emission'] += totalElectronicsEmissions
                emissionTotal[0]['Total Transportation CO2 Emission'] += totalTransportEmissions
                emissionTotal[0]['Total Team Emission'] += totalEmissions
                emissionTotal[0]['Total Team New Year Predicted Emissions'] += newYearEmissions
                break

    # Saves the JSON as a JSON File
    open('carbon.json', 'w').write(json.dumps(result, indent=4))
    open('emissionTotal.json', 'w').write(json.dumps(emissionTotal, indent=4))
    
    # Converts the JSON File to a xlsx file
    pd.read_json('carbon.json').to_excel('WEC 2023-result.xlsx', index=False)
