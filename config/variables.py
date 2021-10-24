from yaml import load, dump
from yaml import Loader, Dumper

user_path = './config/user.yml'

# load user variables
with open(user_path, 'r') as file:
    user = load(file, Loader)

