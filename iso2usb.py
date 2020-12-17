import argparse
import os
import subprocess
import sys


parser = argparse.ArgumentParser(
    description='For MacOS, iso2usb can make a bootable USB from a Linux ISO.')
parser.add_argument(
    'usb', help='Full path to USB, e.g.: /dev/disk2')
parser.add_argument(
    'iso', help='Full path to ISO e.g.: /Users/username/ubuntu-amd64.iso')
args = parser.parse_args()

def main(args):
    iso = False
    usb = False
    file_img = '/tmp/tempfile.img'
    file_dmg = file_img + '.dmg'
    p_status = 0
    u_status = 0
    dd_status = 0
    
    # Check if ISO and USB exists:
    if os.path.isfile(args.iso):
        iso = True
    else:
        print('  - wrong path to ISO')

    if os.path.lexists(args.usb):
        usb = True
    else:
        print('  - wrong path to USB, check by typing "diskutil list"')

    if iso and usb:
        # Remove a previously save .img.dmg
        if os.path.lexists(file_dmg):
            os.remove(file_dmg)

        # convert to image in OSX (it may look like this: /tmp/tempfile.img.dmg)
        print('  - converting ISO to image...')
        cmd_convert = 'hdiutil convert -format UDRW ' + args.iso + ' -o ' + file_img
        p = subprocess.Popen(cmd_convert, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()
        
        # unmount USB
        if p_status == 0:
            cmd_unmount = 'diskutil unmountDisk ' + args.usb
            u = subprocess.Popen(cmd_unmount, stdout=subprocess.PIPE, shell=True)
            u_status = u.wait()
        
        # check before continuing
        if u_status == 0:
            cont = input('Overwrite all at '+args.usb+', [Y/n] ')
        
        # write to USB, this step requires admin password
        if cont == 'Y':
            print('  - writing usb...this can take some time.')
            cmd_dd = 'sudo dd if='+file_dmg+' of='+args.usb+' bs=1m'
            w = subprocess.Popen(cmd_dd, stdout=subprocess.PIPE, shell=True)
            dd_status = w.wait()
        else:
            print('  - aborted!')
            return


if __name__== "__main__":
    subprocess.call('clear', shell=True)
    print('iso2usb running ...')
    main(args)
    print('... Done!')
