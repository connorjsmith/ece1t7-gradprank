from time import strftime, gmtime

EASTEREGG_MINUTES = 17

word_to_gpio = {
    'it': GPIO1,
    'is': GPIO2,
    'twenty': GPIO3,
    'half': GPIO4,
    'quarter': GPIO4,
    'ten': GPIO5,
    'five': GPIO6,
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
    'ten': GPIO17,
    'eight': GPIO18,
    'four': GPIO19,
    'five': GPIO20,
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
    minutes = int(strftime("%M", time))
    if minutes == EASTEREGG_MINUTES:
        return ['easteregg']

    hour = int(strftime("%I", time))
    is_midnight = (int(strftime("%H", time)) == 0)
    am_pm = strftime("%p", time).lower()

    words = []
    # round minutes

    # get hours, or midnight/noon

    # get to/past, or null

    # get am_pm, or null if midnight/noon


    return words

def activate_pins(pins):
    for p in range(32): # TODO how many pins should we set low?
        if p in pins:
            GPIO.output(p, GPIO.HIGH)
        else:
            GPIO.output(p, GPIO.LOW)

def main():
    while True:
        t  = gmtime()
        words = parse_words(t)
        pins = [word_to_gpio[w] for w in words]
        activate_pins(pins)
        time.sleep(10) # our clock will be at most 10 seconds delayed from the real time
                  
