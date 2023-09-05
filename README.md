# StrongMinds
###### Repository for "Pizza Pizza"

## How to run locally

**NOTE: This repository requires Python 3 to run locally. [Go here](https://www.python.org/downloads/release/python-381/) if you need to install Python 3.**

1. Clone the git repository into your local directory of choice
2. Run `pip3 install -r requirements.txt` in terminal
3. Run `flask db init`, `flask db stamp head`, `flask db migrate`, and `flask db upgrade` in that order in terminal
4. Run `flask run` in terminal
5. Navigate to the website through `http://127.0.0.1:5000` or `http://localhost:5000`

## Tests
1. Click Pizza Toppings Manager link
2. Fill in the topping name and amount inputs
3. Click Add Pizza Topping button
4. After topping is added, change amount field then click Update Amount button
5. Click Delete Topping button
6. Click Pizza List Manager link
7. Click Add Topping button for toppings you want added
8. Fill in Pizza Name field
9. Click Add New Pizza button
10. Click Delete Pizza button
11. Repeat steps 7-9
12. Click Edit Pizza link
13. Click Remove Topping button
14. Click Add Topping button
15. Change name of pizza in Pizza Name field
16. Click Update Pizza button

## Credits
- [Matthew Esqueda](https://github.com/matthewjw2007)
