from util import *


@dataclass
class Location:
    latitude: float
    longitude: float
    timezone: str
    name: str

    def __str__(self):
        return f"{self.name} ({self.latitude},{self.longitude})"

    @classmethod
    def fetch(cls, location: str | None = None): # -> Location:
        # If no location specified, fetch it using IP
        if location == None:
            data = json_from_url("https://ipinfo.io")
            return Location(*data["loc"].split(","),
                            timezone=data["timezone"],
                            name=f"{data['city']}, {data['region']}, {data['country']}")

        # Maybe the location is already a lat, lon[, name] pair/triple
        try:
            lat, lon, timezone, *location = location.split(",")
            location = ",".join(location)
            return Location(float(lat), float(lon), timezone=timezone, name=location)
        except (ValueError, TypeError):
            pass

        # Otherwise, look the location up using a geocoding API
        data = json_from_url("https://geocoding-api.open-meteo.com/v1/search",
                             name=location, count=1)
        data = data["results"][0]

        return cls(
            data["latitude"],
            data["longitude"],
            timezone=data["timezone"],
            name=f"{data['name']}, {data['admin1']}, {data['country_code']}"
        )
