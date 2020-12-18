# Razen
## Random Zen Meditation App

## Installation
```{bash}
git clone https://github.com/ifrit98/razen.git
sudo apt-get install $(grep -vE "^\s*#" dependencies | tr "\n" " ")
pip install -r requirements
```
## Usage  
```{bash}
python razen.py # opens up GUI
```

[Logo]("/razen_logo.jpg")

### Examples of install cmds
```{bash}
xargs -a $(awk '/^\s*[^#]/' "$requirements") -r -- sudo apt-get -y install
xargs -a <(awk '! /^ *(#|$)/' "$packagelist") -r -- sudo apt-get install
```
