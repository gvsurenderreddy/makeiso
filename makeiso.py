#! python3
#! /usr/bin/python3

# This is a test of the sync to GitHub

import os, sys, logging, traceback

logging.basicConfig(filename='./MakeISO.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

tmp_dir = ('/tmp')
present_dir = os.getcwd()
working_dir = ('/dicom/latest_version/livecdtmp')
latest_dir = ('/dicom/latest_version')

if os.geteuid() != 0:
    os.execvp("sudo", ["sudo"] + sys.argv)

if present_dir != (working_dir):
    logging.debug('Not in correct directory. Must change from ' + present_dir + ' to ' + working_dir + ' directory.')
    print ('Changing to ' + working_dir + ' directory.')
    os.chdir(working_dir)


def manifest_mod():
    logging.info('Start of manifest file chmod.')
    print ('Setting +W permissions to manifest file.')
    os.system("chmod +w ./extract-cd/casper/filesystem.manifest")
    logging.info('manifest_mod complete.')
    try:
        raise Exception ('An error has occured')
    except:
        errorFile = open(working_dir + '/' + 'errors.txt', 'a')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        print ('The traceback error information was written to ' + str(errorFile))

def manifest_update():
    logging.info('Start of manifest file write.')
    print ('Writing update to manifest file.')
    os.system("sudo chroot edit dpkg-query -W --showformat='${Package} ${Version}\n' > ./extract-cd/casper/filesystem.manifest")
    logging.info('manifest_update complete.')

def manifest_copy():
    logging.info('Start of manifest file copy.')
    print ('Copying manifest file.')
    os.system("sudo cp ./extract-cd/casper/filesystem.manifest extract-cd/casper/filesystem.manifest-desktop")
    logging.info('manifest_copy complete.')

def manifest_ubi_edit():
    logging.info('Editing ubiquity manifest.')
    print ('Editing ubiquity manifest file.')
    os.system("sudo sed -i '/ubiquity/d' ./extract-cd/casper/filesystem.manifest-desktop")
    logging.info('ubiquity edit complete.')

def casper_manifest():
    logging.info('Editing the casper manifest.')
    print ('Editing the casper manifest file.')
    os.system("sudo sed -i '/ubiquity/d' ./extract-cd/casper/filesystem.manifest-desktop")
    logging.info('Casper manifest edit complete.')


def rm_squashfs():
    logging.info('Removing filesystem.squashfs file.')
    print ('Deleting squashfs file.')
    if os.path.isfile('./extract-cd/casper/filesystem.squashfs'):
        os.remove('./extract-cd/casper/filesystem.squashfs')
    logging.info('filesystem.squashfs file deleted.')


def compress_newfs():
    logging.info('Compress new filesystem.squashfs file.')
    print ('Compressing new filesystem.')
    os.system("sudo mksquashfs edit ./extract-cd/casper/filesystem.squashfs -comp xz -e edit/boot")
    logging.info('Compression of filesystem complete.')

def update_newfs():
    logging.info('Updating size of filesystem.')
    print ('Updating the size of the new filesystem.')
    os.system("printf $(sudo du -sx --block-size=1 edit | cut -f1) > ./extract-cd/casper/filesystem.size")
    logging.info('Update of filesystem complete.')

def remove_md5sum ():
    logging.info('Removing old MD5SUM.')
    print ('Delting old MD5SUM file.')
    if os.path.isfile('./extract-cd/md5sum.txt'):
        os.remove('./extract-cd/md5sum.txt')
    logging.info('Deleted extract-cd/md5sum.txt.')

def create_md5sum():
    logging.info('Creating new MD5SUM file.')
    print ('Creating a new MD5SUM text file.')
    os.system("find -type f -print0 | sudo xargs -0 md5sum | grep -v extract-cd/isolinux/boot.cat | sudo tee extract-cd/md5sum.txt")
    logging.info('Created extract-cd/md5sum.txt.')


manifest_mod()
manifest_update()
manifest_copy()
manifest_ubi_edit()
casper_manifest()
rm_squashfs()
compress_newfs()
update_newfs()
remove_md5sum()
create_md5sum()

print ('Creating ISO image')
os.chdir(working_dir + '/extract-cd')
os.system("sudo mkisofs -D -r -V '$IMAGE_NAME' -cache-inodes -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o ../../latest_version.iso .")


# print ('Enter name of iso image file:')
isoname = input('Enter name of iso image file: ')

#if present_dir != (latest_dir):
#    logging.info('Change to latest version dir.')
#    print ('Changing from ' + present_dir + ' to ' + latest_dir + '.')
#    os.chdir(latest_dir)

if os.path.isfile != (latest_dir + '/' + isoname):
    logging.info('Renaming file to ' + isoname)
    os.chdir(latest_dir)
    os.system("chown brit:brit latest_version.iso")
    os.rename('latest_version.iso', isoname)
    print ('ISO file renamed to ' + isoname)
else:
    print ('File exists.')

if os.path.isfile(latest_dir + '/' + isoname):
    logging.info('ISO created successfully.')
    print (' ISO creation COMPLETE ')
else:
    logging.error('ISO rename FAILED.')
    print ('ISO rename failed')