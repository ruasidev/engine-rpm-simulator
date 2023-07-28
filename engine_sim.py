import keyboard
import random
import time
import threading
import colorama
from colorama import Fore

colorama.init()

MIN_RPM = 820
MAX_RPM = 8600
RPM_COLORS = [Fore.GREEN, Fore.YELLOW, Fore.RED]

# GEAR_RATIOS = [40, 60, 80, 100, 120, 140]
GEAR_COLORS = [Fore.GREEN, Fore.MAGENTA, Fore.LIGHTBLUE_EX, Fore.YELLOW, Fore.LIGHTRED_EX, Fore.RED]
GEAR_RANGES = [(80, 90), (70, 80), (60, 70), (40, 50), (20, 30), (15, 20)]


#           -- > Future idea :3
# engine_type = {
#     "supercar": {
#         "gear-ranges": [(150, 170), (100, 110), (80, 90), (60, 70), (20, 25), (15, 20)],
#         "min-rpm": 1020,
#         "max-rpm": 13000,
#         "brake-decays": [0.08, 0.1, 0.15, 0.3, 0.4, 0.4]
#     }
# }

BRAKE_DECAYS = [0.05, 0.08, 0.1, 0.2, 0.3, 0.3]

DOWNSHIFT_JUMP = 2000

car_on = False
gear = 1
rpm = 0

IDLE = random.randint(MIN_RPM, MIN_RPM + 20)

def print_data(rpm, gear):
    rpm_color = RPM_COLORS[0]
    gear_color = GEAR_COLORS[gear - 1]
    if rpm > 4000:
        rpm_color = RPM_COLORS[1]
        if rpm > 8520:
            rpm_color = RPM_COLORS[2]
    
    print(f"   RPM: {rpm_color}{rpm:4}{Fore.RESET}   GEAR: {gear_color}{gear}{Fore.RESET}", end='\r')

def idle():
    global IDLE
    global rpm
    if rpm != IDLE:
        if rpm < IDLE:
            for _ in range(IDLE - rpm):
                rpm += 1
                time.sleep(0.001)
                print_data(rpm, gear)
        else:
            for _ in range(rpm - IDLE):
                rpm -= 1
                time.sleep(0.001)
                print_data(rpm, gear)
    else:
        IDLE = random.randint(MIN_RPM, MIN_RPM + 20)

def start_engine():
    global rpm
    global gear
    global car_on
    while rpm < 2000:
        rpm += random.randint(40, 50)
        print_data(rpm, gear)
    
    while rpm > 830:
        diff = rpm - 700
        DECAY = 0.01
        # function of decay since an abrupt stop at the min RPM through braking looks VERY unnatural
        change_rate = min(abs(diff), diff * DECAY)
        rpm -= int(change_rate)
        if rpm <= 830:
            car_on = True
            break
        print_data(rpm, gear)

    
def throttle():
    global rpm
    global gear
    redline = random.randint(MAX_RPM - 100, MAX_RPM)
    min_range, max_range = GEAR_RANGES[gear - 1]
    if rpm <= MAX_RPM:
        rpm += random.randint(min_range, max_range)
        print_data(rpm, gear)
    
    else:
        rpm = redline
        print_data(rpm, gear)
    

def engine_brake():
    global rpm
    rpm -= random.randint(27, 33)
    time.sleep(0.01)
    print_data(rpm, gear)


def brake():
    global rpm
    global gear
    diff = rpm - (MIN_RPM + 143)
    DECAY = BRAKE_DECAYS[gear - 1]
    # function of decay since an abrupt stop at the min RPM through braking looks VERY unnatural
    change_rate = min(abs(diff), diff * DECAY)
    rpm -= int(change_rate)

    time.sleep(0.01)
    print_data(rpm, gear)


def trans():
    global gear
    global rpm

    while True:
        if keyboard.is_pressed('p'):
            if not gear + 1 > len(GEAR_RANGES) and not rpm - 1750 < 860:
                gear += 1
                if rpm > 7000:
                    target = rpm - 4000
                if rpm < 7000 and rpm > 6000:
                    target = rpm - 3000
                if rpm < 6000:
                    target = rpm - 2000
                while rpm > target:
                    rpm -= random.randint(75, 85)
                    if rpm < target:
                        rpm = target
                    print_data(rpm, gear)
            time.sleep(0.2)
        
        if keyboard.is_pressed(';'):
            if not gear - 1 < 1 and not rpm + 2000 > 13000:
                gear -= 1
                target = rpm + 2000
                while rpm < target:
                    rpm += random.randint(75, 85)
                    if rpm > target:
                        rpm = target 
                    print_data(rpm, gear)
            time.sleep(0.2)


transmission = threading.Thread(target=trans)
transmission.daemon = True
transmission.start()


print_data(rpm, gear)

while True:
    if keyboard.is_pressed("f") and car_on == False:
        start_engine()
    if car_on:
        time.sleep(0.0001)

        if keyboard.is_pressed('l'):
            brake()

        if keyboard.is_pressed('w'):
            throttle()
        else:
            if rpm >= MIN_RPM + 21:
                engine_brake()
            else:
                idle()