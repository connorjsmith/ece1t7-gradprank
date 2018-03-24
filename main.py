from time import strftime, localtime

EASTEREGG_MINUTES = 17

# TODO replace with rpi stuff
GPIO1 = 1
GPIO2 = 2
GPIO3 = 3
GPIO4 = 4
GPIO5 = 5
GPIO6 = 6
GPIO7 = 7
GPIO8 = 8
GPIO9 = 9
GPIO10 = 10
GPIO11 = 11
GPIO12 = 12
GPIO13 = 13
GPIO14 = 14
GPIO15 = 15
GPIO16 = 16
GPIO17 = 17
GPIO18 = 18
GPIO19 = 19
GPIO20 = 20
GPIO21 = 21
GPIO22 = 22
GPIO23 = 23
GPIO24 = 24
GPIO25 = 25
GPIO26 = 26
GPIO27 = 27

word_to_gpio = {
    'it': GPIO1,
    'is': GPIO2,
    'twenty': GPIO3,
    'half': GPIO4,
    'quarter': GPIO4,
    'ten_m': GPIO5,
    'five_m': GPIO6,
    'to': GPIO7,
    'past': GPIO8,
    'one': GPIO9,
    'two': GPIO10,
    'three': GPIO11,
    'eleven': GPIO12,
    'twelve': GPIO13,
    'seven': GPIO14,
    'six': GPIO15,
    'nine': GPIO16,
    'ten_h': GPIO17,
    'eight': GPIO18,
    'four': GPIO19,
    'five_h': GPIO20,
    "o'clock": GPIO21,
    'noon': GPIO22,
    'midnight': GPIO23,
    'am': GPIO24,
    'pm': GPIO25,
    'ece1t7': GPIO26,
    'easteregg': GPIO27
}

def parse_words(time):
    # TODO check if we are at ~55s and round up to avoid small drifts in the clock
    minutes = time.tm_min
    if minutes == EASTEREGG_MINUTES and time.tm_sec < 1:
        return ['easteregg']

    hour_12 = int(strftime("%I", time))
    hour_24 = time.tm_hour

    words = ['it', 'is']
    # round minutes to nearest 5, capped at 55
    r_minutes = round(minutes/5)*5 % 60
    if r_minutes == 5 or r_minutes == 55:
        words.append('five_m')
    elif r_minutes == 10 or r_minutes == 50:
        words.append('ten_m')
    elif r_minutes == 15 or r_minutes == 45:
        words.append('quarter')
    elif r_minutes == 20 or r_minutes == 40:
        words.append('twenty')
    elif r_minutes == 25 or r_minutes == 35:
        words.append('twenty')
        words.append('five_m')
    elif r_minutes == 30:
        words.append('half')

    # get to/past, or null
    if r_minutes > 30:
        words.append('to')
    elif r_minutes > 0:        #if  minutes == 0, add nothing
        words.append('past') # prefer "half past noon" over "half to one"

    # get hours, or midnight/noon
    if minutes >= 33: # round up the hour
        hour_12 = (hour_12 + 1) % 12
        hour_12 = max(hour_12, 1) # roll over 12 to 1, not 0
        hour_24 = (hour_24+1) % 24
    if hour_24 == 12:
        words.append('noon')
    elif hour_24 == 0:
        words.append('midnight')
    elif hour_12 == 1:
        words.append('one')
    elif hour_12 == 2:
        words.append('two')
    elif hour_12 == 3:
        words.append('three')
    elif hour_12 == 4:
        words.append('four')
    elif hour_12 == 5:
        words.append('five_h')
    elif hour_12 ==  6:
        words.append('six')
    elif hour_12 == 7:
        words.append('seven')
    elif hour_12 == 8:
        words.append('eight')
    elif hour_12 == 9:
        words.append('nine')
    elif hour_12 == 10:
        words.append('ten_h')
    elif hour_12 == 11:
        words.append('eleven')

    # get am_pm, or null if midnight/noon
    if (hour_24 % 12 != 0):
        if hour_24 < 12:
            words.append('am')
        else:
            words.append('pm')

    return words

def activate_pins(pins):
    for p in range(32): # TODO how many pins should we set low?
        if p in pins:
            GPIO.output(p, GPIO.HIGH)
        else:
            GPIO.output(p, GPIO.LOW)

def main():
    while True:
        t  = localtime()
        words = parse_words(t)
        pins = [word_to_gpio[w] for w in words]
        activate_pins(pins)
                  

def test():
    for i in range(24*60):
        t = localtime(i*60)
        t_str = strftime("%H:%M %p", t)
        words=parse_words(t)
        print(t_str, words)
