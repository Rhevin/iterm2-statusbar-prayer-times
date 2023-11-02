import iterm2
import requests
from datetime import datetime

# Modify the endpoint and parameters
PRAYER_TIMES_ENDPOINT = "http://www.islamicfinder.us/index.php/api/prayer_times"
PRAYER_TIMES_PARAMS = {"country": "LT", "zipcode": "", "time_format": "0"}


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description="Prayer Time",
        detailed_description="Upcoming Prayer Time",
        exemplar="🕌Loading",
        update_cadence=900,
        identifier="rhev.iterm-components.prayer-time",
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def prayer_time_coroutine(knobs):
        try:
            # Fetch prayer times data using a form POST request
            response = requests.post(
                PRAYER_TIMES_ENDPOINT, data=PRAYER_TIMES_PARAMS, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            # Extract the upcoming prayer time based on the current time
            prayer_times = data.get("results", {})
            current_time = datetime.now().strftime("%H:%M")

            upcoming_prayer_time = "N/A"
            for prayer, time in prayer_times.items():
                if time > current_time:
                    upcoming_prayer_time = f"{prayer}: {time}"
                    break

            return f"󱠧 {upcoming_prayer_time}"
        except Exception as e:
            print(e)
            return "󱠧 N/A"

    await component.async_register(connection, prayer_time_coroutine, timeout=15)


iterm2.run_forever(main)
