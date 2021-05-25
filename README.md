# CarNotify

CarNotify is a simple script that is used to track cars on https://olx.ba website and inform about price changes on email.
You don't need any database for it, it saves data in file that commits itself on each run.

## Modification

This project doesn't have any license and I don't take any responsibility on the way it is used. I don't have to be credited, you can do whatever you like with it. With that said, here is the way to use it and modify it for your own needs.

1. Fork the project
2. Clone your fork
3. Add following secrets to your project:
  - USER_EMAIL - current email that you use for GitHub (needed for self commit)
  - EMAIL_PWD - password for this email
  - USER_USERNAME - current username that you use for GitHub

  - SENDING_EMAIL - Email address from which email will be sent
  - SENDING_EMAIL_PASSWORD - Password for this email
      If you are using gmail as a sending email make sure to disable all security :D 
      (If you are ready to do this, you need to [enable less secure apps](https://myaccount.google.com/lesssecureapps) and [remove reCaptcha](https://accounts.google.com/b/0/DisplayUnlockCaptcha))
  - RECEIVING_EMAIL - Email address to which you want to receive email

4. Change url in ```scraper.py``` to whatever your search criteria is
5. You might want to change text of words in ```get_email_body()``` method in ```helper_methods.py```, but you don't have to. (You will just get updates which will indicate that it is update about cars, even though it might not be.)
6. Uncomment and change cron expression in ```scrape.yml``` to accomodate your needs. I usually use [this website](https://crontab.guru/) to get cron expression for my needs

Don't forget that you have 1000 minutes of free execution time monthly on GitHub, so don't overdo it.