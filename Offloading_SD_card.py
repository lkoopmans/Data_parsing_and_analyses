import sys
import time
import psutil
import shutil
import os
from datetime import date
import pathlib
t0 = time.time()
today = date.today()
d1 = today.strftime("%d/%m/%Y")
store_path = '/Volumes/HD_C8'

tst = psutil.disk_partitions()
num_of_cards = int(input("Enter the number of cards: "))

card_names = [None] * num_of_cards
c = int(0)

for info in psutil.disk_partitions():
    if 'Card' in info.mountpoint:
        card_names[c] = info.mountpoint
        c += 1
print(c, 'Cards found with names', card_names)

if c != num_of_cards:
    print("Error: only " + str(c) + " instead of " + str(num_of_cards) + " cards were found")
    sys.exit()
else:
    print('Copying started')


for j in range(c):
    if j == 2 or j == 4 or j == 6:
        time.sleep(3600/2)
    print('Card', j+1)
    files = os.listdir(card_names[j] + '/DCIM')

    today = date.today()
    d = today.strftime("%d_%m_%Y")

    temp = card_names[j].split('/')

    cd = ''
    output_path = cd + '/' + store_path+'/'+d+'/'+temp[-1]

    os.makedirs(output_path)
    print('Write to ' + output_path)
    # shutil.copytree(card_names[j]+'/DCIM', output_path)
    os.system('cp -R ' + card_names[j] + '/DCIM ' + output_path +' &')


