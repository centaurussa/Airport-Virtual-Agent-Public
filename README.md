


<p align="center">
   <img src="http://ue.edu.krd/wp-content/uploads/2017/06/Top-logo-02.png"/>
</p>
<br>
<p align="center">
	Project: Airport Virtual Agent
	<br>
	By: Yousif Adnan
	<br>
	Supervisor: Mariwan Mahmood
</p>
<hr/>

#### <p align="center"> Airport virtual agent used to act as a host for passengers in the airport, where passengers can check for flights, arrivals, lost and founded bags, hotels and room bookings, ordering a taxi or a driver, browsing the internet and etc. </p>
<br>

<p align="center">
   <img src="https://raw.githubusercontent.com/centaurussa/Airport-Virtual-Agent-Public/master/docs/animations/10.png"/>
</p>
<p align="center" style="font-size:5px;"><i>[Aneesh Ravi, Sound wave,
	https://lottiefiles.com/10158-wave-animation]</i></p>
<br>
&nbsp;

# Requirements

The following dependencies should be installed to run and power the virtual agent up.
### Python(>=3.6):
	
	  - PortAudio
	  - PyAudio     
      - Selenium
      - Pillow
      - Requests
      - SpeechRecognition
      - screeninfo
      - gTTS
      - Google
      - BeautifulSoup4
      - PyMySQL
      - Pydub
	  - Pyttsx3     # From centaurussa's repository
 ### Windows:
      - ffmpeg      # Should be added to the environment variable PATH
 ### Linux:
      - libttspico-utils
| :warning: ATTENTION |
|:---------------------------|
| If you had a problem installing or importing PortAudio or PyAudio, please check the following comment [here](https://github.com/ContinuumIO/anaconda-issues/issues/4139#issuecomment-433710003)  |
<p><br></p>

# To be Configured

### 1- /docs/settings.txt

### 2- /docs/database.json

### 3- /docs/smtp_server.json
<p><br></p>

# Launching the Virtual Agent
1) Navigating to project's working directory with the CMD/Terminal
2) a) Launching with animations, execute: `python run.py`

   b) Launching without animations, execute: `python agent.py`

<p><br></p>

# Error Checking
1) Navigating to project's working directory with the CMD/Terminal
2) Execute: `python error_checker.py`


<p><br><br></p>

| :warning: ATTENTION |
|:---------------------------|
| 1) Website files can be found in `/docs/airport website`.
| 2) MySQL database can be imported and found in `/docs/database design`.
| 3) If you don't want to host the website or you don't want to use a database, you can set `smtp_server_enabled` and/or `database_enabled` to `0` in `/docs/settings.txt`.