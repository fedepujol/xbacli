""" 
    Goal: Change the current system brightness value.
    Motivation: Learn to use argparse.
    Notes: Check if your system has an intel_backlight. 
        Run the following command:
            ls /sys/class/backlight
"""
import argparse


""" Const  """
INTEL_PATH = '/sys/class/backlight/intel_backlight/'

""" Get the current and max value of brightness """
def getValue(fileName):
    f_file = open(fileName, 'r')
    file_val = f_file.readline()
    f_file.close()

    return file_val

""" Change the value of file """
def saveValue(newValue):
    with open(INTEL_PATH + 'brightness', 'r+') as f_bright:
        data = f_bright.seek(0)
        f_bright.write(str(newValue))
        f_bright.truncate()
        f_bright.close()

def change_brightness(v_inc):
    """ Get the current values of Brightness """
    c_bright = float(getValue(INTEL_PATH + 'brightness'))
    m_bright = float(getValue(INTEL_PATH + 'max_brightness'))

    """ Calculate the integer part of the percentage """
    c_bright += ((v_inc * m_bright) / 100)

    """ 
        Limit the value to the boundries.
        Min: 0
        Max: 4882 (Max Brightness)
    """
    if c_bright > m_bright:
        c_bright = m_bright

    if c_bright < 0:
        c_bright = 0

    """ Change the brightness value """
    saveValue(round(c_bright))

""" Main function of program """
def main():
    """ Create the main argument parser """
    xba_parser = argparse.ArgumentParser(prog="xba-cli", description="Custom cli-tool to manage brightness")

    """ Flags """
    xba_parser.add_argument('-inc', metavar='', type=int, nargs=1, dest='inc', help='Increase brightness')
    xba_parser.add_argument('-dec', metavar='', type=int, nargs=1, dest='dec', help='Decrease brightness')

    """ Get arguments """
    xba_args = xba_parser.parse_args()

    """ Need to change the sign if decrease flag is passed """
    if xba_args.inc != None:
        change_brightness(xba_args.inc[0])

    if xba_args.dec != None:
        change_brightness(xba_args.dec[0] * (-1))

if __name__ == "__main__":
    main()
