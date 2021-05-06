# Ecobee Temperature Monitor
This project utilizes the Ecobee API to poll data from an Ecobee remote temperature sensor. It is currently configured to extract temperature sensor data and outdoor ambient temperature (from the local weather report), though it can easily be expanded to include more data (such as data from from other sensors or the Ecobee thermostat).

# Use Cases/Motivation
The primary motivation for this project was to monitor the temperature in my beer cellar. I have an extensive beer collection and was experimenting with using a natural root cellar as a temperature-stable environment. I had an extra Ecobee temperature sensor lying around, so as a quick and easy way to determine the viability of the root cellar, I tapped the Ecobee API to monitor temperature inside the cellar as well as outdoor ambient temperature based on the local weather report.

Data was imported to a Google Sheets for visualization:

![chart](https://user-images.githubusercontent.com/10524839/117350412-608f5900-ae61-11eb-83dd-1fe9605e7bf2.png)
<img width="147" alt="Screen Shot 2021-05-06 at 11 52 25 AM" src="https://user-images.githubusercontent.com/10524839/117350587-96344200-ae61-11eb-84bd-4f840af662e2.png">

As seen above, the temperature remains relatively constant as the ambient temperature fluctuates throughout the day. Due to the temperate climate where I live, the natural root cellar actually remains relatively cool throughout the whole year, never exceeding 75 degF even when the ambient temperature spikes to the mid-90s for a few days during the summer. However, in the spirit of tinkering, I eventually migrated my beer cellar over to a temperature controlled chest freezer and am monitoring temperatures with a Raspberry Pi and remote dashboard, as documented in [here](https://github.com/alexgui/temp-humidity-monitor-cloud4rpi).

# Getting Started
To use this code:
1. Download the repo: ```git pull https://github.com/alexgui/temp-monitor-ecobee.git```
2. Set up your Ecobee: https://www.ecobee.com/home/developer/api/examples/index.shtml
3. Authenticate your app: https://www.ecobee.com/home/developer/api/examples/ex1.shtml
4. Copy your Ecobee Access Token, API Key, and Refresh Token into their respective .txt files
5. Open a Terminal, navigate to the repository, and execute the code:
  
    ```python3 ecobeerequest.py```
    
6. Data will be written to ```data.txt```, which you can then import to any major spreadsheet tool as a comma dilineated file... or build your own custom parsing tools!
