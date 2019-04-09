# cloud-hamster
Cloud Hamster is a simple tool to create rolling backups on Google Drive account. It compresses selected directory into
one zip file and send it to Google Drive.

##Disclaimer
I do not guarantee any correctness of the solution. You are using it at your own risk.

##Installing and usage

1. Fetch the repository or download zip file
2. Prepare virtualenv for the application in the app directory:
```buildoutcfg
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

```

3. Create project and client_id and client_secret in [Google Could Console](https://console.developers.google.com/apis/dashboard)
I can't just put my credentials to the repo :)_
4. `examples` directory contains a file `example.app.json`. Copy into app root and fill client_id and client_secret.
_A name of the file is random. It will be passed as argument when the app will run_
5. There is also `example.config.json`. The only thing you need to set is backup_directory which is a folder being backed up.
6. You need to authorize the app to use your Google Drive account. Run:
```
python3 autorize_google_drive.py {config_filename.json} {app_filename.json}

config_filename.json - file created in step 5.
app_filename.json - file created in step 4.
```
7. The app will ask you to copy url into the browser, go through authorization flow and paste received key.
8. Now the app is ready. Check it running:
```
python3 simple_backup.py {config_filename.json} {app_filename.json}

```

## Rolling backup
After 10 backups are created, on next upload the oldest one will be removed. Currently it is not possible to configure
this behaviour.

## Further development

The application is not finished. It misses a few critical things:
* error handling - it is very poor now
* recovering backup - not implemented at all
* configuration of rolling backup
* credentials refreshing - this might not work
