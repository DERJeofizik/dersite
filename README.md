# Static Web Site Creator for DER Jeofizik

Downloads data from YouTube and creates a static web site.


## Installation

Clone the repository:

    git clone --recursive https://github.com/DERJeofizik/dersite
    cd dersite

Create a virtual environment and activate it:

    python3 -m venv env
    source env/bin/activate

Install required packages

    pip install -r requirements.txt


## Running

Download data from YouTube (channel_id should be set in config file).

    python run.py download config.toml data.json

Create the web site:

    python run.py create config.toml data.json

Deploy using git (updates the submodule and commits the changes)

    python run.py deploy config.toml


## Local development

You can change the base URL for local testing

    python run.py create config.toml data.json -b http://localhost:8000

You can run local server:

    python run.py server config.toml


You can go to http://localhost:8000 to visit the web site.
