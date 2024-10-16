import json
from util import *
from dateutil.parser import isoparse
from typing import Optional, Generator
from datetime import datetime
from dataclasses import dataclass
from location import Location


@dataclass
class TransitStop:
    location: Location
    time: datetime
    platform: Optional[str] = None

    def __str__(self):
        return f"{self.location} on platform {self.platform} at {self.time}"

    @classmethod
    def from_ns_stop(cls, stop: dict):
        if "plannedDepartureDateTime" in stop:
            time = stop["plannedDepartureDateTime"]
            platform = stop["plannedDepartureTrack"]
        else:
            time = stop["plannedArrivalDateTime"]
            platform = stop["plannedArrivalTrack"]

        time = isoparse(time)

        return cls(
            location=Location.from_ns_location(stop),
            time=time,
            platform=platform,
        )


@dataclass
class TransitLeg:
    start: TransitStop
    end: TransitStop
    """ Value from 0-1 indicating the punctuality percentage for this leg """
    punctuality: Optional[float] = None
    transport_type: Optional[str] = None
    operator: Optional[str] = None

    def __str__(self):
        return (
            f"{self.start}  -- {self.transport_type} ({self.operator}) -->  {self.end}" +
            f" ({self.punctuality * 100}% punctual)" if self.punctuality is not None else ""
        )

    @classmethod
    def from_ns_leg(cls, leg: dict):
        return cls(
            start=TransitStop.from_ns_stop(leg["stops"][0]),
            end=TransitStop.from_ns_stop(leg["stops"][-1]),
            punctuality=(leg["punctuality"] / 100) if "punctuality" in leg else None,
            transport_type=leg["product"]["longCategoryName"],
            operator=leg["product"]["operatorName"],
        )


@dataclass
class TransitRoute:
    start_time: datetime
    end_time: datetime
    start_location: Location
    end_location: Location
    legs: list[TransitLeg]

    def __str__(self):
        return (
            f"Journey from {self.start_location} at {self.start_time} to {self.end_location} at {self.end_time}\n\n" +
            "\n".join(map(str, self.legs))
        )


    @classmethod
    def from_ns_query(cls, arrive_at: datetime, station_from: str, station_to: str) -> Generator:# -> Generator[TransitRoute]:
        data = json_from_url(
            "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips",
             fromStation=station_from,
             toStation=station_to,
             dateTime=str(arrive_at),
             lang="nl",
             product="OVCHIPKAART_ENKELE_REIS",
             travelClass=2,
             searchForArrival="true",
             firstMileModality="PUBLIC_TRANSPORT",
             lastMileModality="PUBLIC_TRANSPORT",
             headers={
                  "Authority": "gateway.apiportal.ns.nl",
                  "Accept": "application/json, text/plain, */*",
                  "Accept-Language": "en-US,en;q=0.5",
                  "Dnt": "1",
                  "Ocp-Apim-Subscription-Key": "1ea3dd385baf4127a20cb8fb38af634d",
                  "Origin": "https://www.ns.nl",
                  "Sec-Ch-Ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
                  "Sec-Ch-Ua-Mobile": "?0",
                  "Sec-Ch-Ua-Platform": '"Linux"',
                  "Sec-Fetch-Dest": "empty",
                  "Sec-Fetch-Mode": "cors",
                  "Sec-Fetch-Site": "same-site",
                  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.7.3 Chrome/118.0.5993.220 Safari/537.36",
                  "X-Caller-Version": "rio-frontends-20241016.16",
         })

        for trip_data in data["trips"]:
            legs = list(map(TransitLeg.from_ns_leg, trip_data["legs"]))
            start_leg = min(legs, key=lambda leg: leg.start.time)
            end_leg = max(legs, key=lambda leg: leg.end.time)

            yield TransitRoute(
                start_time=start_leg.start.time,
                start_location=start_leg.start.location,
                end_time=end_leg.end.time,
                end_location=end_leg.end.location,
                legs=legs,
            )


if __name__ == "__main__":
    tomorrow = datetime.now() + timedelta(days=1)
    arrive_at = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

    for route in TransitRoute.from_ns_query(arrive_at, "Almere Centrum", "Geldermalsen"):
        dbg(route)
        print("----\n")
