import sys
import json
from subprocess import run

# sys.argv - variables (array)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected 2 arguments. Exiting.')
        sys.exit(1)
    # parse from storage file
    try:
        with open('persistent_storage.json', 'r') as storage:
            SETTINGS = json.load(storage) # dictionary, {redshift:value, brightness:value}
    except FileNotFoundError:
        with open('persistent_storage.json', 'w') as storage:
            SETTINGS = {
                'brightness': 1,
                'redshift': 6500
            }
            json.dump(SETTINGS, storage)
    # direction
    ARG = sys.argv[1]
    # current settings values
    BRIGHTNESS = SETTINGS['brightness']
    REDSHIFT = SETTINGS['redshift']
    # brightness range
    B_MIN = 0.1
    B_MAX = 1
    B_DELTA = 0.05
    # mins
    R_MIN = 0
    R_MAX = 10000
    R_DELTA = 500
    # determine FLAGS (make adjustments)
    if ARG == 'up':
        BRIGHTNESS = B_MAX if (BRIGHTNESS + B_DELTA >
                               B_MAX) else BRIGHTNESS + B_DELTA
    elif ARG == 'down':
        BRIGHTNESS = B_DELTA if (BRIGHTNESS - B_DELTA < B_DELTA) else BRIGHTNESS-B_DELTA
    elif ARG == 'right':
        REDSHIFT = R_MAX if (REDSHIFT + R_DELTA >
                             R_MAX) else REDSHIFT + R_DELTA
    elif ARG == 'left':
        REDSHIFT = R_MIN if (REDSHIFT - R_DELTA <
                             R_MIN) else REDSHIFT - R_DELTA
    # return settings values
    SETTINGS['brightness'] = BRIGHTNESS
    SETTINGS['redshift'] = REDSHIFT
    # default is no change to SETTINGS
    FLAGS = ['redshift', '-O', str(SETTINGS['redshift']), '-b', str(SETTINGS['brightness'])]
    # make system call
    run(FLAGS)
    # write changes to storage
    with open('persistent_storage.json', 'w') as storage:
        json.dump(SETTINGS, storage)
        storage.close()
    exit(0)
    sys.exit(0)
