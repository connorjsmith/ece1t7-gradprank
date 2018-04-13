from time import strftime, localtime
from neopixel import *

# LED strip configuration:
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FLAGS      = NEO_KHZ800 + NEO_GRB # TODO might not be the right place
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Special Time configurations
EASTEREGG_MINUTES = 17
HALLOWEEN_ORANGE = Color(0xFF, 0x91, 0x00)
WHITE = Color(255, 255, 255)

# TODO replace with rpi stuff
word_to_indices = {
    'it': [0, 1],
    'is': [0, 1],
    'twenty': [0, 1],
    'half': [0, 1],
    'quarter': [0, 1],
    'ten_m': [0, 1],
    'five_m': [0, 1],
    'to': [0, 1],
    'past': [0, 1],
    'one': [0, 1],
    'two': [0, 1],
    'three': [0, 1],
    'eleven': [0, 1],
    'twelve': [0, 1],
    'seven': [0, 1],
    'six': [0, 1],
    'nine': [0, 1],
    'ten_h': [0, 1],
    'eight': [0, 1],
    'four': [0, 1],
    'five_h': [0, 1],
    "o'clock": [0, 1],
    'noon': [0, 1],
    'midnight': [0, 1],
    'am': [0, 1],
    'pm': [0, 1],
    'ece1t7': [0, 1],
    'easteregg': [0, 1],
}

def parse_words(time):
    # TODO check if we are at ~55s and round up to avoid small drifts in the clock
    minutes = time.tm_min
    if minutes == EASTEREGG_MINUTES and time.tm_sec < 1:
        return ['easteregg']

    hour_12 = int(strftime("%I", time))
    hour_24 = time.tm_hour

    words = ['it', 'is', 'ece1t7']
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

def get_color_for_word(w):
    t = localtime()
    if t.tm_mon == 10 and t.tm_mday == 31: # Oct 31
        return HALLOWEEN_ORANGE

    elif w in ['ece1t7', 'it', 'is']:
        return WHITE # these words are always white

    # NOTE: insert other special times or words here
    else:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        while r == 0 and g == 0 and b == 0:
            # Never use black
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

        return Color(r,g,b)

last_words = set()
def activate_words(strip, words):

    # Nothing to do if words haven't changed
    if last_words == set(words):
        return

    # Words have changed
    last_words = set(words)

    # Turn off all pixels
    for p in range(strip.numPixels()):
        strip.setPixelColor(p, Color(0,0,0))

    # Turn on appropriate words
    for w in words:
        pins_for_word = words_to_indices[w]
        color = get_color_for_word(w)
        for p in pins_for_word:
            strip.setPixelColor(p, color)

    # Show changes on strip
    strip.show()


def main():
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FLAGS, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    while True:
        t  = localtime()
        words = parse_words(t)
        activate_words(words)


def test():
    for i in range(24*60):
        t = localtime(i*60)
        t_str = strftime("%H:%M %p", t)
        words=parse_words(t)
        print(t_str, words)
