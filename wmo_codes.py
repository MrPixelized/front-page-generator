# https: //gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c
# https: //openweathermap.org/weather-conditions
wmo_codes = {
  0: {
    "day": {
      "description": "sunny",
      "owm_image_url": "http://openweathermap.org/img/wn/01d@4x.png",
      "owm_image_description": "clear-sky-day"
    },
    "night": {
      "description": "clear",
      "owm_image_url": "http://openweathermap.org/img/wn/01n@4x.png",
      "owm_image_description": "clear-sky-night"
    }
  },
  1: {
    "day": {
      "description": "mainly sunny",
      "owm_image_url": "http://openweathermap.org/img/wn/01d@4x.png",
      "owm_image_description": "clear-sky-day"
    },
    "night": {
      "description": "mainly clear",
      "owm_image_url": "http://openweathermap.org/img/wn/01n@4x.png",
      "owm_image_description": "clear-sky-night"
    }
  },
  2: {
    "day": {
      "description": "partly cloudy",
      "owm_image_url": "http://openweathermap.org/img/wn/02d@4x.png",
      "owm_image_description": "few-clouds-day"
    },
    "night": {
      "description": "partly cloudy",
      "owm_image_url": "http://openweathermap.org/img/wn/02n@4x.png",
      "owm_image_description": "few-clouds-night"
    }
  },
  3: {
    "day": {
      "description": "cloudy",
      "owm_image_url": "http://openweathermap.org/img/wn/03d@4x.png",
      "owm_image_description": "scattered-clouds-day"
    },
    "night": {
      "description": "cloudy",
      "owm_image_url": "http://openweathermap.org/img/wn/03n@4x.png",
      "owm_image_description": "scattered-clouds-night"
    }
  },
  45: {
    "day": {
      "description": "foggy",
      "owm_image_url": "http://openweathermap.org/img/wn/50d@4x.png",
      "owm_image_description": "mist-day"
    },
    "night": {
      "description": "foggy",
      "owm_image_url": "http://openweathermap.org/img/wn/50n@4x.png",
      "owm_image_description": "mist-night"
    }
  },
  48: {
    "day": {
      "description": "rime fog",
      "owm_image_url": "http://openweathermap.org/img/wn/50d@4x.png",
      "owm_image_description": "mist-day"
    },
    "night": {
      "description": "rime fog",
      "owm_image_url": "http://openweathermap.org/img/wn/50n@4x.png",
      "owm_image_description": "mist-night"
    }
  },
  51: {
    "day": {
      "description": "light drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "light drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  53: {
    "day": {
      "description": "drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  55: {
    "day": {
      "description": "heavy drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "heavy drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  56: {
    "day": {
      "description": "light freezing drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "light freezing drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  57: {
    "day": {
      "description": "freezing drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "freezing drizzle",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  61: {
    "day": {
      "description": "light rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10d@4x.png",
      "owm_image_description": "rain-day"
    },
    "night": {
      "description": "light rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10n@4x.png",
      "owm_image_description": "rain-night"
    }
  },
  63: {
    "day": {
      "description": "rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10d@4x.png",
      "owm_image_description": "rain-day"
    },
    "night": {
      "description": "rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10n@4x.png",
      "owm_image_description": "rain-night"
    }
  },
  65: {
    "day": {
      "description": "heavy rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10d@4x.png",
      "owm_image_description": "rain-day"
    },
    "night": {
      "description": "heavy rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10n@4x.png",
      "owm_image_description": "rain-night"
    }
  },
  66: {
    "day": {
      "description": "light freezing rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10d@4x.png",
      "owm_image_description": "rain-day"
    },
    "night": {
      "description": "light freezing rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10n@4x.png",
      "owm_image_description": "rain-night"
    }
  },
  67: {
    "day": {
      "description": "freezing rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10d@4x.png",
      "owm_image_description": "rain-day"
    },
    "night": {
      "description": "freezing rain",
      "owm_image_url": "http://openweathermap.org/img/wn/10n@4x.png",
      "owm_image_description": "rain-night"
    }
  },
  71: {
    "day": {
      "description": "light snow",
      "owm_image_url": "http://openweathermap.org/img/wn/13d@4x.png",
      "owm_image_description": "snow-day"
    },
    "night": {
      "description": "light snow",
      "owm_image_url": "http://openweathermap.org/img/wn/13n@4x.png",
      "owm_image_description": "snow-night"
    }
  },
  73: {
    "day": {
      "description": "snow",
      "owm_image_url": "http://openweathermap.org/img/wn/13d@4x.png",
      "owm_image_description": "snow-day"
    },
    "night": {
      "description": "snow",
      "owm_image_url": "http://openweathermap.org/img/wn/13n@4x.png",
      "owm_image_description": "snow-night"
    }
  },
  75: {
    "day": {
      "description": "heavy snow",
      "owm_image_url": "http://openweathermap.org/img/wn/13d@4x.png",
      "owm_image_description": "snow-day"
    },
    "night": {
      "description": "heavy snow",
      "owm_image_url": "http://openweathermap.org/img/wn/13n@4x.png",
      "owm_image_description": "snow-night"
    }
  },
  77: {
    "day": {
      "description": "snow grains",
      "owm_image_url": "http://openweathermap.org/img/wn/13d@4x.png",
      "owm_image_description": "snow-day"
    },
    "night": {
      "description": "snow grains",
      "owm_image_url": "http://openweathermap.org/img/wn/13n@4x.png",
      "owm_image_description": "snow-night"
    }
  },
  80: {
    "day": {
      "description": "light showers",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "light showers",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  81: {
    "day": {
      "description": "showers",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "showers",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  82: {
    "day": {
      "description": "heavy showers",
      "owm_image_url": "http://openweathermap.org/img/wn/09d@4x.png",
      "owm_image_description": "shower-rain-day"
    },
    "night": {
      "description": "heavy showers",
      "owm_image_url": "http://openweathermap.org/img/wn/09n@4x.png",
      "owm_image_description": "shower-rain-night"
    }
  },
  85: {
    "day": {
      "description": "light snow showers",
      "owm_image_url": "http://openweathermap.org/img/wn/13d@4x.png",
      "owm_image_description": "snow-day"
    },
    "night": {
      "description": "light snow showers",
      "owm_image_url": "http://openweathermap.org/img/wn/13n@4x.png",
      "owm_image_description": "snow-night"
    }
  },
  86: {
    "day": {
      "description": "snow showers",
      "owm_image_url": "http://openweathermap.org/img/wn/13d@4x.png",
      "owm_image_description": "snow-day"
    },
    "night": {
      "description": "snow showers",
      "owm_image_url": "http://openweathermap.org/img/wn/13n@4x.png",
      "owm_image_description": "snow-night"
    }
  },
  95: {
    "day": {
      "description": "thunderstorm",
      "owm_image_url": "http://openweathermap.org/img/wn/11d@4x.png",
      "owm_image_description": "thunderstorm-day"
    },
    "night": {
      "description": "thunderstorm",
      "owm_image_url": "http://openweathermap.org/img/wn/11n@4x.png",
      "owm_image_description": "thunderstorm-night"
    }
  },
  96: {
    "day": {
      "description": "light thunderstorms with hail",
      "owm_image_url": "http://openweathermap.org/img/wn/11d@4x.png",
      "owm_image_description": "thunderstorm-day"
    },
    "night": {
      "description": "light thunderstorms with hail",
      "owm_image_url": "http://openweathermap.org/img/wn/11n@4x.png",
      "owm_image_description": "thunderstorm-night"
    }
  },
  99: {
    "day": {
      "description": "thunderstorm with hail",
      "owm_image_url": "http://openweathermap.org/img/wn/11d@4x.png",
      "owm_image_description": "thunderstorm-day"
    },
    "night": {
      "description": "thunderstorm with hail",
      "owm_image_url": "http://openweathermap.org/img/wn/11n@4x.png",
      "owm_image_description": "thunderstorm-night"
    }
  }
}
