![Alt text](./app/static/RGPTBanner.png "RedactedGPT Banner")



# PII, PHI, IP scrubber for ChatGPT

## Watch demo here: https://youtu.be/ldUYTdizbVg

<hr>


## How to run it:

Add your API Key to the _.env_ inside the _app_ folder

## From the main folder run the commands:


_docker-compose build_

(include the _--no-cache_ at the end of the command if needed)

_docker-compose up_

(include the _--force-recreate_ at the end of the command if needed)



Open a browser on _0.0.0.0:8000_



<hr>

### References:


I'm using the API call from this tutorial: #https://www.twilio.com/blog/integrate-chatgpt-api-python

I obtained the PII remover function from a ChatGPT prompt!


### Future updates:


- Build a separate module for the PII removal that import the functions into the flask App, that way we can add more regex more easily.
- Improve the page to be responsive.


### Feel free to make improvements and send merge request if you do.

