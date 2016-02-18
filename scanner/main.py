import pymysql

def connect_to_db():
    pass

def main():
    while True:
        barcode = input("Please scan a barcode")
        # Is this code a command code (add, subtract, bottle, change db)
        if barcode[0:6] == '$CODE$':
            mode = barcode.split('$')[1]
            # If yes- change mode
        else:
            pass
        # If no- Check if code exists in database
            # If code exists, add to data base
            # If code does not exist, queue to be added to db

def add(code):
    # First, find out if this code is already 'identified'. If so, add +1 to quantity
    # If not, add new item to db function, and then add +1 to quantity
    pass

def remove(code):
    pass

def select_schema(code):
    pass

MODE= {'add': add,
       'remove': remove,
       'change': select_schema,
       }