# Razen
## Random Zen Meditation App

## Installation
git clone https://github.com/ifrit98/razen.git
sudo apt-get install $(grep -vE "^\s*#" dependencies | tr "\n" " ")
pip install -r requirements

## Usage
python razen.py # opens up GUI

## Balls
[]("mainpage.jpg")
[]("settingspage.jpg")


xargs -a $(awk '/^\s*[^#]/' "$requirements") -r -- sudo apt-get -y install
xargs -a <(awk '! /^ *(#|$)/' "$packagelist") -r -- sudo apt-get install

