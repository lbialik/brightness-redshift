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
        with open('persistent_storage.json','w') as storage:
            SETTINGS = {}
            json.dump(SETTINGS, storage)
    if SETTINGS == {}:
        SETTINGS = {
            'brightness': 1,
            'redshift': 6500
        }
    ARG = sys.argv[1] # direction
    # current settings values
    brightness = SETTINGS['brightness']
    redshift = SETTINGS['redshift']
    # determine flags (make adjustments)
    if ARG == 'up':
        brightness = 1 if (brightness + 0.1 > 1) else brightness + 0.1
    elif ARG == 'down':
        brightness = 0.1 if (brightness - 0.1 < 0.1) else brightness-0.1
    elif ARG == 'right':
        redshift = 13000 if (redshift + 500 > 13000) else redshift + 500
    elif ARG == 'left':
        redshift = 0 if (redshift - 500 < 0) else redshift - 500
    # return settings values
    SETTINGS['brightness'] = brightness
    SETTINGS['redshift'] = redshift
    # default is no change to SETTINGS
    flags = ['redshift', '-O', str(SETTINGS['redshift']), '-b', str(SETTINGS['brightness'])]
    # make redshift call
    run(flags)
    # write changes to storage
    with open('persistent_storage.json', 'w') as storage:
        json.dump(SETTINGS, storage)
        storage.close()
    exit(0)
    sys.exit(0)
