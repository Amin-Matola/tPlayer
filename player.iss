; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=tPlayer
AppVersion=1.0.0
AppVerName=tPlayer
UsePreviousAppDir=yes
DefaultDirName={autopf}\tPlayer
DefaultGroupName=Music
Uninstallable=yes
WizardStyle=modern
SetupIconFile=default.ico
OutputBaseFilename=tPlayer
Compression=lzma
SolidCompression=yes
AppId={{man-784-3477230138008-273}}

[Files]
Source: "tPlayer.exe"; DestDir: "{app}"; DestName: "tPlayer.exe"
Source: "default.ico"; DestDir: "{app}"; DestName: "default.ico"

[Icons]
Name: "{group}\tPlayer"; Filename: "{app}\tPlayer.exe"; IconFilename: "{app}\default.ico"