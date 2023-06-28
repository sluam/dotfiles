import argparse
import os

import requests
from requests.adapters import HTTPAdapter

ICON_SUNNY = "  Clear"
ICON_CLOUDY = "  Cloudy"
ICON_RAINY = "  Rainy"
ICON_STORM = " Storm"
ICON_SNOW = "  Snow"
ICON_FOG = "  Fog"
ICON_DRIZZLE = "  Drizzle"
ICON_MISC = " "

URL = "https://api.openweathermap.org/data/2.5/weather"
# Get your API KEY here https://openweathermap.org/api,
# and set an environment variable for OPENWEATHER_API_KEY with your API KEY.
API_KEY = os.environ.get("OPENWEATHER_API_KEY",
                         "970606528befaa317698cc75083db8b2")
HEADER = {"User-agent": "Mozilla/5.0"}


def get_city() -> str:
    try:
        r = requests.get("https://ipapi.co/json", headers=HEADER)
        return r.json()["city"]
    except requests.exceptions.ConnectionError:
        print("E: couldn't get city name")
        return "london"


def unit_suffix(unit: str) -> str:
    match unit:
        case "metric":
            unit = "ºC"
        case "imperial":
            unit = "ºF"
        case _:
            unit = "K"

    return unit


def get_icon(weather: str) -> str:

    if "Snow" in weather:
        icon = ICON_SNOW
    elif "Rain" in weather:
        icon = ICON_RAINY
    elif "Drizzle" in weather:
        icon = ICON_DRIZZLE
    elif "Cloud" in weather:
        icon = ICON_CLOUDY
    elif "Clear" in weather:
        icon = ICON_SUNNY
    elif "Fog" in weather:
        icon = ICON_FOG
    elif "Thunderstorm" in weather:
        icon = ICON_STORM
    else:
        icon = ICON_MISC
    return icon


def get_weather(city: str, lang: str, unit: str, api_key: str) -> dict[str, str] | None:
    try:
        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=5))
        r = s.get(
            f"{URL}?q={city}&lang={lang}&units={unit}&appid={api_key}",
            headers=HEADER,
            timeout=10,
        )
        data = r.json()
        temp = data["main"]["temp"]
        icon_desc = data["weather"][0]["main"]
        unit = unit_suffix(unit)
        icon = get_icon(icon_desc)

        return {

            "icon": icon,
            "temp": f"{int(temp)}{unit}"
        }

    except requests.exceptions.ConnectionError:
        print("E: failed to establish connection with the API")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display information about the weather.",
    )
    parser.add_argument(
        "-c",
        metavar="CITY",
        dest="city",
        type=str,
        nargs="+",
        help="city name",
    )
    parser.add_argument(
        "-l",
        metavar="LANG",
        dest="lang",
        type=str,
        nargs=1,
        help="language (en, es, fr, ja, pt, pt_br, ru, zh_cn)",
    )
    parser.add_argument(
        "-u",
        metavar="metric/imperial",
        choices=("metric", "imperial"),
        dest="unit",
        type=str,
        nargs=1,
        help="unit of temperature (default: kelvin)",
    )
    parser.add_argument(
        "-a",
        metavar="API_KEY",
        dest="api_key",
        nargs=1,
        help="API Key",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="verbose mode",
    )

    args = parser.parse_args()

    api_key = args.api_key[0] if args.api_key else API_KEY
    city = args.city[0] if args.city else get_city()
    lang = args.lang[0] if args.lang else "en"
    unit = args.unit[0] if args.unit else "standard"

    weather = get_weather(city, lang, unit, api_key)
    if weather:
        icon, temp = weather.values()
        if args.verbose:
            print(icon, temp)
        else:
            print(icon, temp)


if __name__ == "__main__":
    main()
