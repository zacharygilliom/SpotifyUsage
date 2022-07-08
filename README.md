##SpotifyUsage

##### I have always wondered what how my music listening tastes changed during the week and over the day.  So I decided to build an application to visualize my music preferences.

<br>

##### The entire application is written in python using the spotify public API.  The API only allows a user to pull the 50 most recent played songs, so there are two scripts run on a cron job to:
	1. Pull the most recently played songs every hour
	2. Pull the audio features about the songs once a day
##### The two scripts update a PostgreSQL database running in a Docker container on my local machine. THe frontend is built using the Plotly/Dash framework which allows us to build the web frontend entirely in python.
