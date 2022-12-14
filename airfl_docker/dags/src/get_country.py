import requests, os, json
from datetime import datetime

url = "https://meteostat.p.rapidapi.com/stations/hourly"

querystring = {"station":"10637","start":"2021-01-01","end":"2021-01-01","tz":"Europe/Berlin"}

headers = {
	"X-RapidAPI-Key": "0e9f756b16msh32a91efae8630bbp1191eejsn29ba2947aeaf",
	"X-RapidAPI-Host": "meteostat.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

if response.status_code == 200:
	#get data
	json_data = response.json()
	filename = str( datetime.now().date()) + ".json" 
	tot_name = os.path.join( os.path.dirname( __file__ ), 'data', filename )
	print( tot_name )

	with open( tot_name, "w" ) as outputfile:
		json.dump( json_data, outputfile )

else:
	print( response.status_code)
	print( "Error in API call")