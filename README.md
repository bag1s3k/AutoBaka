<p align="center">
  <img src="docs/autobaka_baner.png" alt="AutoBaka Banner" style="width:100%;"/>
</p>

# AutoBaka App

**AutoBaka** is a simple script that calculates your average grades from Bakaláři.

## How it started
Our school blocked access to our grade averages, so I came with an idea. After doing some research, I found two options: Selenium or BeautifulSoup. Thanks the responsive layout of the Baka page, I chose Selenium.



## Table of Contents

- [AutoBaka App](#autobaka-app)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
    - [Functions](#functions)
    - [Variants](#variants)
    - [Structure](#structure)
  - [Getting started](#getting-started)
  - [Installation](#installation)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Run main script](#run-main-script)
      - [Procedure with WINDOWS 11](#procedure-with-windows-11)
  - [Examples](#examples)
  - [Features](#features)
  - [Contributing](#contributing)
  - [Known Issues](#known-issues)
  - [FAQ](#faq)
  - [License](#license)
  - [Authors](#authors)
  - [Changelog](#changelog)
  - [Planned](#planned)


## About the Project

The user enters their login credentials to Bakaláři system. The app uses Selenium to log into the Bakaláři website and fetches your data to your PC

### Functions

1. Calculating grades

    > Ideal for students whose school has hidden the average and who just don’t want to calculate them manually.

[//]: # (2. Calculating absense)
[//]: # ()
[//]: # (    > It quickly shows you how many lessons you will miss, and gives your absence percentage — without using Bakaláři system. )
[//]: # (    > ⚠️ **Note:** Be cautious - some lessons may be replaced, cancelled, or rescheduled. The data is based on your current timetable.)

### Variants

| Variant    | Stable | Version |
|------------|--------|--------|
| Windows 11 |   ✅   | ✅   | 1.2.0 |

[//]: # (| Android | ❌ | ❌ | ❌ | ❌ | 0 |)
[//]: # (| Website | ❌ | ❌ | ❌ | ❌ | 0 |)
- single script

[//]: # (- UI desktop &#40;windows/linux/macOS&#41; Maybe!)

[//]: # (- CLI &#40;windows/linux/macOS&#41; Maybe!)

[//]: # (- Mobile &#40;android/IOS&#41; Maybe!)

[//]: # (- Website <https://autobaka.cz> Maybe!)

### Structure

```
autobaka
 ┣ config
 ┃ ┣ .env
 ┃ ┣ config.ini
 ┣ docs
 ┃ ┣ autobaka_baner.png
 ┃ ┗ screenshot_chronological.png
 ┣ internal
 ┃ ┣ core
 ┃ ┃ ┗ page_model.py
 ┃ ┣ filesystem
 ┃ ┃ ┣ env_utils.py
 ┃ ┃ ┣ export.py
 ┃ ┃ ┣ ini_loader.py
 ┃ ┃ ┗ paths_constants.py
 ┃ ┗ utils
 ┃ ┃ ┣ arg_parser.py
 ┃ ┃ ┣ decorators.py
 ┃ ┃ ┣ logging_setup.py
 ┃ ┃ ┗ selenium_setup.py
 ┣ output
 ┃ ┣ marks.json
 ┃ ┣ project_log.log
 ┃ ┣ raw_absence.json
 ┃ ┣ raw_marks.json
 ┃ ┗ timetable.json
 ┣ LICENSE
 ┣ main.py
 ┣ README.md
 ┗ requirements.txt
```

## Getting started

To try the app, download the repository from <https://github.com/bag1s3k/AutoBaka>

## Installation

```bash
git clone https://github.com/bag1s3k/AutoBaka.git
```

## Requirements

These are the versions that I currently use.
You can try others, but compatibility is not guaranteed. **(I'm regularly updating my system, so the older ones can work)**

![Static Badge](https://img.shields.io/badge/Python-3.13.7-blue)
![Static Badge](https://img.shields.io/badge/Pip-25.2-orange)  
![Static Badge](https://img.shields.io/badge/Windows_11-24H2-lightblue)
![Static Badge](https://img.shields.io/badge/Chrome-Updated-yellow)

> ⚠️ **Chrome Required**: This app uses Chromedriver via WebDriverManager. Make sure you have Google Chrome installed and keep it up to date, because the driver is matched automatically to your installed Chrome version.

## Usage

### Run main script

Just get your average grades without any interface  

#### Procedure with WINDOWS 

Set your login details to `config\.env`

  ```dotenv
  BAKA_USERNAME=username
  BAKA_PASSWORD=password
  ```

Setup config to `config\config.ini`

```ini
[PATHS]
result_path = c:\example\result.txt 
```
>💡 **idea**: You can export the result file to your cloud, so you can access it on your phone as well.



```ini
[URLS]
login_url = https://baka.website/login # login page
marks_url = https://baka.website/next/prubzna.aspx?s=chrono
```

`marks_url` Login to your bakaláři website interface > Grade > Interim Grading > Chronological button and **copy url**


<p><img src="docs/screenshot_chronological.png" alt="Chronological button" style="width:100%;"/></p>

```ini
[SETTINGS]
timeout = 15 # default and required but you can try different
headless_mode = True # Wanna see what is happening
quit_driver = True # If you wanna close the window after the program end
export_format = json # there are grades stored ["json", "txt", "xaml", "csv"]
```

- **Using virtual environment `.venv`**

Download all required libraries from `requirements.txt` ⚠️*while you are installing requirements you have to be in project root*

```bash
pip install -r requirements.txt
```

Activate virtual enviroment `.venv`

```bash
cd C:\example\autobaka 
```

```bash
.\.venv\Scripts\activate.ps1
```

You should see `(.venv)` before your path: `(.venv) C:\example\autobaka>`

Run script `main.py` using login details from `.env`

```bash
python main.py
```

***Possible options:***  
- `"--login", "-l"` by using this one you have to enter your login details **username password**

```bash
python main.py --login username password # --login or -l to use login details from cmd
```

## Examples

```bash
PS C:\local\work\Download> cd C:\local\work\autobaka # Move to the project root
PS C:\local\work\autobaka> .\.venv\Scripts\activate.ps1 # Activate .venv
````

**Login details from `.env`**

```bash
(.venv) PS C:\local\work\autobaka> python main.py
........ Successfully
(.venv) PS C:\local\work\autobaka>
```

**Login details from cmd**

```bash
(.venv) PS C:\local\work\autobaka> python main.py -l username password
........ Successfully
(.venv) PS C:\local\work\autobaka>
```

## Features

- Your average grades

## Contributing

Contributions are welcome! Open an issue, fork the repository, make improvements, and create a pull request.



## Known Issues

- while running only a main script it shows `DevTools listening on ws://127.0.0.1:xxxxx/devtools/browser/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, and there is 1 dot before this message, I wanna delete it
- there are for sure a lot of improvements and issues in the repository, but I'm still adding new features, I'm not interested in finding bugs and improvements

## Planned

- UI
- CLI
- mobile version?
- absence planner


## FAQ


## License

See [LICENSE](LICENSE) for details.

## Authors

<div style="display: flex; align-items: center; gap: 10px;">

  <img src="https://github.com/bag1s3k.png" alt="Author avatar" style="width:60px; border-radius: 50%;" />

  <p style="margin: 0; font-size: 15pt;">
    Created by <a href="https://github.com/bag1s3k" style="font-weight:bold;">bag1s3k</a>
  </p>
  
</div>

<br>