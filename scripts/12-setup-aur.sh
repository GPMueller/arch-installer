### Install yaourt
# chmod +x arch-installer/yaourt.sh
# cp arch-installer/yaourt.sh /mnt/
# arch-chroot /mnt ./yaourt.sh

### Install aura
chmod +x arch-installer/aura.sh
cp arch-installer/aura.sh /mnt/
arch-chroot /mnt ./aura.sh

### Install packages from AUR
# arch-chroot /mnt yaourt -S visual-studio-code --noconfirm
arch-chroot /mnt aura -S visual-studio-code