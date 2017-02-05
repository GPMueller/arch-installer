#  !  /usr/bin/env python3
import fileinput
import subprocess
from subprocess import run
from collections import defaultdict

def sed_inplace(fileToSearch, textToSearch, textToReplace):
    with fileinput.FileInput(fileToSearch, inplace=True) as file:
        for line in file:
            print(line.replace(textToSearch, textToReplace), end='')

def install_packages(user_input):
    ### Setup Package List
    print(" >> Creating package list")

    misc_packages = ['base',
                     'base-devel',
                     'sudo',
                     'wget',
                     'git',
                     'vim',
                     'zsh',
                     'powerline-fonts',
                     'p7zip',
                     'unrar',
                     'fortune-mod',
                     'reflector',
                     'tree']
    packages = {
        'minimal': {
            'desktop' : [],
            'server'  : ['openssh']},
        'developer': defaultdict(lambda:
                                 ['cmake',
                                  'boost',
                                  'eigen',
                                  'opencl-headers',
                                  'ocl-icd',
                                  'openmpi',
                                  'hdf5-cpp-fortran',
                                  'python-pip',
                                  'ipython',
                                  'python-h5py',
                                  'python-scipy',
                                  'python-matplotlib',
                                  'python-pillow',
                                  'python-pylint',
                                  'autopep8',
                                  'doxygen']),
        'office': defaultdict(lambda:
                              ['texlive-most',
                               'texlive-lang']),
        'media': defaultdict(lambda:
                             ['gnuplot',
                              'graphviz',
                              'ffmpeg'])
    }

    desktop_distros = {
        "KDE plasma": ['xorg-server',
                       'xorg-server-utils',
                       'xorg-apps',
                       'yakuake',
                       'plasma-meta',
                       'kde-applications']
    }

    gui_packages = {
        'minimal': {
            'desktop': ['qtox',
                        'owncloud-client',
                        'xclip'],
            'server': []},
        'developer': defaultdict(lambda: []),
        'office': defaultdict(lambda:
                              ['texstudio',
                               'libreoffice-fresh']),
        'media': {
            'desktop': ['teamspeak3',
                        'gimp',
                        'inkscape',
                        'blender',
                        'handbrake',
                        'vlc'],
            'server': ['vlc',
                       'teamspeak3-server',
                       'owncloud-server']}
    }

    graphics_driver_packages = {
        'default': ['mesa', 'mesa-libgl', 'xf86-video-vesa', 'opencl-mesa'],
        'intel':   ['mesa', 'mesa-libgl', 'xf86-video-intel', 'opencl-mesa'],
        'nvidia':  ['nvidia', 'nvidia-libgl', 'opencl-nvidia'],
        'amd':     ['mesa', 'mesa-libgl', 'xf86-video-vesa', 'opencl-mesa'],
        'vbox':    ['virtualbox-guest-modules-arch', 'virtualbox-guest-utils', 'opencl-mesa']}

    package_list = misc_packages
    package_list += graphics_driver_packages[user_input['graphics driver']]

    if 'full' in user_input['packages']:
        package_list += [
            package for package in value[user_input['system type']]
            for key, value in packages]
        if user_input['desktop'] != 'none':
            package_list += desktop_distros[user_input['desktop']]
            package_list += [
                package for package in value[user_input['system type']]
                for key, value in gui_packages]
    else:
        for package_type in user_input:
            package_list += packages[package_type][user_input['system type']]
            if user_input['desktop'] != 'none':
                package_list += packages[user_input['desktop']]
                package_list += gui_packages[package_type][user_input['system type']]

    package_string = " ".join(package_list)



    ### Nicer formatting for pacstrap
    sed_inplace("/etc/pacman.conf", "#Color", "Color")
    sed_inplace("/etc/pacman.conf", "#TotalDownload", "TotalDownload")

    ### Update mirrorlist
    print(" >> Updating mirror list")
    try:
        run(
            ['reflector --latest 100 --sort rate --protocol https --save /etc/pacman.d/mirrorlist'],
            shell=True,
            check=True)
    except subprocess.CalledProcessError as error:
        print('Updating package mirrorlist failed with message: ', error.output)



    print(" >> Going to install arch packages")
    try:
        run(['pacstrap /mnt '+ package_string], shell=True, check=True)
    except subprocess.CalledProcessError as error:
        print('Error installing packages. Message: ', error.output)

    print(" >> Installed arch packages")


    ### Nicer formatting for pacstrap on installed system
    sed_inplace("/mnt/etc/pacman.conf", "#Color", "Color")
    sed_inplace("/mnt/etc/pacman.conf", "#TotalDownload", "TotalDownload")