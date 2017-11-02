# API-Project
API Exercise

Here's where I'm at so far:

This gets the general location based on the IP address that runs the code, fetches the current weather, and outputs a forecast for the current day, the next day, and the day after. I like to start simple and build onto it.

Process:
1. I played around with the Weather Underground API and used GetPostMan to quickly analyse the JSON that's received so that I can figure out what I'd want to put into a database.

I've spent time on the documentation of what's available through the API located here: https://www.wunderground.com/weather/api/d/docs

2. I decided it'd be fun to grab geolocation data, so I read about how to do that in Python. I like to understand what the code -does-, so I end up taking a little bit longer reading examples/ideas. I'd rather not be surprised by executing code. I opted to use this:
```
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
```
Which grabs location based on IP. It's not the most accurate, but it's reasonable.

3. I followed the tutorial to learn how to input information in Google Sheets. I wanted to be able to have it working before I build on that knowledge. Once that was set up, I went to their documentation and read more about it: http://gspread.readthedocs.io/en/latest/#main-interface

As I went, I would write code in Spyder/Anaconda so that I could continually test it when I'd add more functionality. If I broke it, I'd fix it.

One of the challenges was working with JSON and Python simply because of the lack of experience with it. Once I understood that multiple JSON values can be treated as an array, and got advice that a Python dictionary works well with them, it was significantly easier.

I can grab a list of resources I referred to if that's helpful.
