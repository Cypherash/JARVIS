import discord
key_features ={
    'temp': "Temperature",
    "feels_like": "Feels Like",
    "temp_min": "Minimum temperature",
    "temp_max": "Maximum temperature",
    "humidity": "Humidity"


}


def parse_data(data):
    data = data["main"]
    del data["pressure"]
    return data


def weather_message(data, location):
    location = location.title()
    message = discord.Embed(
        title=f"{location} Weather:",
        description=f" here is the weather forecast for {location}",
        color=0xFF6500
    )
    for key in data:
        message.add_field(
            name=key_features[key],
            value=str(data[key]),
            inline=False
        )
    return message


def weather_error_message(location):
    location=location.title()
    return discord.Embed(
        title="ERROR",
        description=f"Error retrieving weather data for {location}",
        color=0xFF0000
    )