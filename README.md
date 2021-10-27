
<p align="center" width="100%">
    <img width="50%" src="https://github.com/eduardopenedo/google_classroom_downloader/blob/main/docs/images/kissclipart-google-classroom-icon-clipart-google-classroom-edu-9a98222156330de7.png?raw=true"> 
</p>

<h1 align="center">
    Google Classroom Downloader
</h1>

<p align="center" style="font-size:1.4rem">
    A script to make downloading files of Google Classroom more easy
</p>

<p align="center" style="font-size:1.4rem">
    <a href="https://pyup.io/repos/github/eduardopenedo/google_classroom_downloader/">
        <img src="https://pyup.io/repos/github/eduardopenedo/google_classroom_downloader/shield.svg">
    </a>
        <a href="https://pyup.io/repos/github/eduardopenedo/google_classroom_downloader/">
        <img src="https://pyup.io/repos/github/eduardopenedo/google_classroom_downloader/python-3-shield.svg">
    </a>
</p>

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Install

* Clone or download the zip of the project

* This project use [Python 3+](https://www.python.org/downloads/), install it if you dont have it on your machine.

* Install project dependencies
```
pip install -r requirements.txt
```

* Credentials.json
    * Make a [new project in Google Cloud Plataform](https://developers.google.com/workspace/guides/create-project)

    * Enable Google Drive and Google Classroom Api at the new project created

    * In the tab "Api and Services" make a new OAuth 2.0 Credential and download the json file

    * In the tab OAuth Login Screen, click in the button "Publish App"

    * Rename the json downloaded to "credentials.json" and place into the root folder of the project


## Usage

To get all stuffs just open a command line in the root folder of the project and execute the command above, it will download all classes and activities of the courses you're at

```
python main.py
```

## Contributing

Feel free to dive in! [Open an issue](https://github.com/eduardopenedo/google_classroom_downloader/issues/new) or submit PRs.


## License
This project was made with GPL license.
