import python_weather

import asyncio
import os
import datetime

class weatherClass():

    async def main(self) -> None:

        # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
        async with python_weather.Client (unit=python_weather.METRIC) as client:


            # Fetch a weather forecast from a city.
            weather = await client.get('Bournemouth')

            # Fetch the temperature for today.
            return weather.temperature

    # Fetch weather forecast for upcoming days.
    def runEvent(self):
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        temperature =asyncio.run(self.main())
        answer =  str(temperature) + ' degrees'

        return answer

if __name__ == '__main__':

  # See https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details.
    print(weatherClass().runEvent())