# SheetLog
## Python Logging with Google Sheet.


## Install
1. Clone this repo  
    `git clone https://www.github.com/tobyclh/sheetLog`
2. Install  
    `python setup.py install`

## Why do you want this
Logging into your AWS instance to check training loss? That's so 2018. JK.  
Yet I am not aware of any good free loggin solution that allows:
*  hosted logging
*  free unlimited event logging*
*  Good log filtering / manipulation

If you are willing to pay for it, one of [these services](https://www.fullstackpython.com/logging.html) would probably make a better option.

\*Google Sheet API is free for 100 API calls per key in every 100 seconds, that's why we only push logs to sheet at an interval. But other than that its free.
## How to use
Continue reading? Guess you are as broke as me, and that's alright ;)
1. Get a google account  
    oh well...
2. Install this repo (scroll up)
3. [Setup your crediential following the gspread tutorial](https://gspread.readthedocs.io/en/latest/oauth2.html)  

Now you are done preparing for it, let's test it out.  
```
from SheetLog import SheetLog
import logging
sheetlog = SheetLog('path to your crediential.json', name='name of the file', email='your email address')
logger = logging.getLogger('name your logger')
logger.addHandler(sheetlog.handler)

#then you can start logging as usual
logger.warn('Dont say I didnt warn you')
logger.info('Here is some suprising info for ya')
logger.error('Critical error')
```

You will receive an email in your mail box, open it and enjoy your log.