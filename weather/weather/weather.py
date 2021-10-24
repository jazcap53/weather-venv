# weather.py
# Andrew Jarcho
# 5/2021

"""Get weather for two U.S. cities; store weather data in AWS S3 bucket"""
import json
import logging
import os

import boto3
from botocore.exceptions import ClientError
from opencage.geocoder import OpenCageGeocode
import requests

try:
    from prepare import (setup_logging, do_parse_args, get_location_list,
                         create_bucket, log_python_executable)
    from utils import get_bucket_name
    from tomorrow_api_codes import WEATHER_CODES, PRECIP_CODES
except ModuleNotFoundError:
    from weather.prepare import (setup_logging, do_parse_args,
                                 get_location_list, create_bucket,
                                 log_python_executable)
    from weather.utils import get_bucket_name
    from weather.tomorrow_api_codes import WEATHER_CODES, PRECIP_CODES


def get_geocode(city, state):
    """Return latitude and longitude of a U.S. city and state"""
    geocoder = OpenCageGeocode(os.environ['GEOCODER_KEY'])
    query = f'{city}, {state}, USA'
    results = geocoder.geocode(query)
    lat = str(results[0]['geometry']['lat'])
    lng = str(results[0]['geometry']['lng'])
    return lat, lng


def build_request(geocode):
    """Get the endpoint and payload format for a geocoded U.S. city"""
    endpoint = 'https://api.tomorrow.io/v4/timelines'
    payload = {'location': f'{geocode[0]},{geocode[1]}',
               'fields': ["precipitationIntensity",
                          "precipitationType",
                          "windSpeed",
                          "windGust",
                          "windDirection",
                          "temperature",
                          "temperatureApparent",
                          "cloudCover",
                          "cloudBase",
                          "cloudCeiling",
                          "weatherCode"],
               'timesteps': ['current'],
               'units': 'imperial',
               'apikey': f'{os.environ["TOMORROW_KEY"]}',
               'timezone': 'America/Detroit'}
    return endpoint, payload


def get_weather_data(request_data):
    """Use requests module to retrieve weather data"""
    endpoint, payload = request_data
    request = requests.get(endpoint, params=payload)
    response_dict = get_response_dict(request)
    return response_dict


def get_response_dict(response):
    """Convert API's JSON response to a Python dict"""
    if not response:
        raise ValueError('Empty Response')
    response_dict = response.json()['data']['timelines'][0]['intervals'][0]
    return response_dict


def format_data(w_data, loc, gcode):
    """Parse and format data for a single location and time"""
    ret_dict = {'time': w_data['startTime'],
                'city': loc.city,
                'state': loc.state,
                'lat': gcode[0],
                'lng': gcode[1]}
    for item in w_data['values'].items():
        if item[0] == 'weatherCode':
            ret_dict['weatherType'] = WEATHER_CODES.get(item[1], 'Unknown')
        elif item[0] == 'precipitationType':
            ret_dict['precipitationType'] = PRECIP_CODES.get(item[1],
                                                             'None or Unknown')
        else:
            ret_dict[item[0]] = item[1]
    return ret_dict


def write_day_file(weather_now):
    """Write data for both cities for one day/time to local file as JSON"""
    file_name = f"{weather_now[0]['time']}.json"
    with open(file_name, "w") as outfile:
        try:
            json.dump(weather_now, outfile)
        except Exception as err:
            logging.error(err)
            raise
        return file_name


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as err:
        logging.error(err)
        return False
    return True


def get_output_contents(location_list):
    """Return a list of dict-formatted locations"""
    list_of_dicts = []
    for location in location_list:
        geocode = get_geocode(*location)
        request = build_request(geocode)
        weather_data = get_weather_data(request)
        tmp_dict = format_data(weather_data, location, geocode)
        list_of_dicts.append(tmp_dict)
    return list_of_dicts


def delete_local_file(new_file_name):
    """Delete the local copy of the weather data"""
    os.remove(new_file_name)


def main() -> list[dict]:
    """Driver for this script"""
    setup_logging()
    args = do_parse_args()
    log_python_executable(args)
    location_list = get_location_list(args)
    if not location_list:
        return []
    bucket_name = create_bucket(get_bucket_name(args))
    if not bucket_name:
        return []
    list_of_dicts = get_output_contents(location_list)
    new_file_name = write_day_file(list_of_dicts)
    upload_file(new_file_name, bucket_name)
    delete_local_file(new_file_name)

    return list_of_dicts


if __name__ == '__main__':
    for itm in main():
        print(itm)
        print()
