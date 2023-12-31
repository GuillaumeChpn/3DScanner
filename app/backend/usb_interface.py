import subprocess
from shutil import move, copy2
from time import sleep

def get_usb_drives_list() -> list:
    '''
    Returns a list of all mounted USB storage devices. Filters the internal storage of the RPi.
    '''
    listdrives = subprocess.Popen('mount', shell=True, stdout=subprocess.PIPE)
    listdrivesout, _ = listdrives.communicate()
    listdrivesout = str(listdrivesout)[2:]
    listdrivesout = listdrivesout.split('\\n')
    listdrivesout = listdrivesout[:-1]

    usb_drives = []
    for line in listdrivesout:
        if (line.find('/sys') == -1 and 
            line.find('/run') == -1 and 
            line.find('on /dev') == -1 and 
            line.find('/boot') == -1 and 
            line.find('/proc') == -1 and
            line.find('on / type')) == -1:
            path = line.split()[2]
            
            usb_drives.append(path)
    return usb_drives

class USBStorage():
    def __init__(self, name: str):
        '''
        Creates a USBStorage object.
        
        :param name: The name of the USB storage device. For example, if the device is mounted on /media/pi/USBSTORAGE, then the name is USBSTORAGE.
        '''
        self.mounted = False
        self.name = name

        self.loc = None
        locs = get_usb_drives_list()
        for loc in locs:
            if loc.find(self.name) != -1:
                self.loc = loc + '/'
                break

        if self.loc is not None:
            self.mounted = True
            

    def move_file_to(self, file_path: str, dest_folder: str) -> None:
        '''
        Moves a file to the specified destination folder.

        :param file_path: The path of the file to be moved.
        :param dest_folder: The destination folder.
        '''
        file_dest = dest_folder + file_path.split('/')[-1]
        move(file_path, file_dest)

    def copy_file_to(self, file_path: str, dest_folder: str) -> None:
        '''
        Copies a file to the specified destination folder.

        :param file_path: The path of the file to be copied.
        :param dest_folder: The destination folder.
        '''
        file_dest = dest_folder + file_path.split('/')[-1]
        copy2(file_path, file_dest)

    def umount(self) -> None:
        '''
        Safely unmounts the USB storage device.
        '''
        cmd = 'sudo umount ' + self.loc
        subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE)
        sleep(1)
        self.mounted = False


if __name__ == '__main__':
    usb_drives = get_usb_drives_list()
    if len(usb_drives) >= 1:
        for l in usb_drives:
            print(l)
    else:
        print('No device found.')
        exit()

    st = USBStorage(usb_drives[0])
    st.umount()

    usb_drives = get_usb_drives_list()
    if len(usb_drives) >= 1:
        for l in usb_drives:
            print(l)
    else:
        print('No device found.')
    
    exit()




