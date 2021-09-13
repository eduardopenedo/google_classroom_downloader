
<span style="font-size:8rem;display:block" align="center">👨‍🏫</span>
<p align="center" style="font-size:2rem">
    Google Classroom Downloader
</p>
<p align="center" style="font-size:1.4rem">
    A script to make downloading files of Google Classroom more easy
</p>

<div align="center">
    <img src="https://img.shields.io/pypi/v/pip?label=pip">
    <img src="https://img.shields.io/static/v1?label=google-api-python-client&message=2.20.0&color=green">
    <img src="https://img.shields.io/static/v1?label=google-auth-oauthlib2&message=0.4.6&color=green">
</div>
<br/>


## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Install

* This project use [Python 3+](https://www.python.org/downloads/), go check them out if you don't have them locally installed.

* The project need some demependencies too, to install all of then just place the command bellow in your favourite terminal
```
pip install -r requirements.txt
```

* Now we need "login" to your Google account, to make this just follow the steps above

    1. Clone or download the zip of the project

    2. Make a [new project in Google Cloud Plataform](https://developers.google.com/workspace/guides/create-project)

    3. Enable Google Drive and Google Classroom Api at the new project created

    4. In the tab "Api and Services" make a new OAuth 2.0 Credential and download the json file

    5. Rename the json downloaded to "credentials.json" and place into the root folder of the project


## Usage

To get all stufs of your courses just open a command line in the root folder of the project and execute the command above, it will download all classes and activities of the courses you're at
```
python main.py
```

## Contributing

Feel free to dive in! [Open an issue](https://github.com/RichardLitt/standard-readme/issues/new) or submit PRs.


## License
This project was made with ... license.