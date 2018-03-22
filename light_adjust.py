"""
Program designed to allow users to incrementally adjust light settings on screen.

Uses redshift package supported by Jon Lund Steffensen at: http://jonls.dk/redshift/

Appropriate terminal command would look like:
"python3 /home/<user>/brightness-redshift/light_adjust.py up"
"""
import sys # used to parse arguments to program
import json # used to write persistent settings to file
from subprocess import run # used to run redshift terminal command

B_DEFAULT = 1
R_DEFAULT = 6500

def adjust_light(settings, direction, persistent):
    """
    Main functional method.

    Adjusts current settings read in by main method,
    Makes adjustment call to system (redshift must be installed)
    Writes changes to file.
    """
    # current settings values
    brightness = settings['brightness']
    redshift = settings['redshift']
    # brightness range values
    b_min = 0.1
    b_max = 1.0
    b_delta = 0.05
    # redshift range values
    r_min = 1000
    r_max = 10000
    r_delta = 250
    # adjust settings
    if direction == 'up':
        brightness = b_max if (brightness + b_delta >
                               b_max) else brightness + b_delta
    elif direction == 'down':
        brightness = b_min if (brightness - b_delta <
                               b_min) else brightness - b_delta
    elif direction == 'right':
        redshift = r_max if (redshift + r_delta >
                             r_max) else redshift + r_delta
    elif direction == 'left':
        redshift = r_min if (redshift - r_delta <
                             r_min) else redshift - r_delta
    # return adjusted settings values
    settings['brightness'] = brightness
    settings['redshift'] = redshift
    # default is no change to settings
    flags = ['redshift',
             '-O', str(settings['redshift']),
             '-b', str(settings['brightness']),
             '-r']
    # make system call
    run(flags)
    # notification of location in brightness-redshift
    if brightness == B_DEFAULT and redshift == R_DEFAULT:
        notification = ['notify-send',
                        'Light Adjustment Neutral',
                        'Redshift: ' + str(redshift) + ', Brightness: ' + str(brightness)]
        run(notification)
    # write changes to storage
    with open(persistent, 'w') as storage:
        json.dump(settings, storage)
        storage.close()
    # close
    exit(0)
    sys.exit(0)

if __name__ == '__main__':
    PERSISTENT = '.persistent_storage.json'
    # handle calling errors
    if len(sys.argv) != 2:
        print('Expected 2 arguments. Exiting.')
        sys.exit(1)
    # parse settings from storage file
    try:
        with open(PERSISTENT, 'r') as storage:
            SETTINGS = json.load(storage) # dictionary, {redshift:value, brightness:value}
    except FileNotFoundError:
        with open(PERSISTENT, 'w') as storage:
            SETTINGS = {
                'brightness': B_DEFAULT,
                'redshift': R_DEFAULT,
                # 'time' :  time set for notifications so only one appears after 3 seconds
            }
            json.dump(SETTINGS, storage)
    # direction
    DIRECTION = sys.argv[1]
    # make function call
    adjust_light(SETTINGS, DIRECTION, PERSISTENT)
    
