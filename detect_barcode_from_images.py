#i recommend you to search how's code working
import cv2
from pyzbar.pyzbar import decode
from termcolor import colored
from time import sleep
from rich.console import Console
import os 
os.system('cls|clear')
print(colored('----------------------','green'), colored('Extract Bar Code From Images','red'), colored('----------------------','green'))
print(colored('Created', 'red'), colored('By', 'green'), colored('Ahmed Abd','red'))
print("")

print(colored('NOTE','red'), ': PATH SHOULD BE DIRECTORY HAS BAR_CODE IMAGES !!  ')
path = input('Enter Path :')
console = Console()
tasks = [f"Code {n}" for n in range(1, 11)]
barcode_world = []
try : 
    with console.status("[bold green] Extracting Bar Code ") as status:
        for i in range(1,9375):
            image = cv2.imread(path+str(i)+'.png')
            detectedBarcodes = decode(image)
            for barcode in detectedBarcodes:
                barcode_world += barcode.data
        while tasks:
            task = tasks.pop(0)
            sleep(1)
            console.log(f"{task} Sorting ... ")
except : 
    print('--------! Path unavailable !-----------')



barcode_world_conChar = "".join(map(chr, barcode_world))
print('"'+barcode_world_conChar+'"')
        

