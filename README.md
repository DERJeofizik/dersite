# Static Web Site Creator for DER Jeofizik

Downloads data from YouTube and creates a static web site.


## Installation

Clone the repository:

```sh
git clone --recursive https://github.com/DERJeofizik/dersite.git
cd dersite
```

Create a virtual environment and activate it:

```sh
python3 -m venv env
source env/bin/activate
```

Install required packages

```sh
pip install -r requirements.txt
```


## Running

Download data from YouTube (channel_id should be set in config file `config.toml`).

```sh
./run.py download
```

Create the web site:

```sh
./run.py create
```

Deploy using git (updates the submodule and commits the changes)

```
./run.py deploy
```

## Local development

You can change the base URL for local testing

```sh
./run.py create -b http://localhost:8000
```
You can run local server:

```
./run.py server
```


You can go to http://localhost:8000 to visit the web site.
