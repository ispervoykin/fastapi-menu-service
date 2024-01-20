menu = {"1": 1, "2": 2, "3": 3}
db_menu = {"1": 2, "2": 3, "3": 1}
for key in menu.keys():
    db_menu[key] = menu[key] 

print(db_menu)       