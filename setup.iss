[Setup]
AppName=quimge
AppVerName=quimge 0.1.2-0
AppPublisher=apkawa
AppPublisherURL=http://github.com/Apkawa/quimge/
DefaultDirName={pf}\quimge
DefaultGroupName=quimge
DisableProgramGroupPage=true
OutputBaseFilename=setup
Compression=lzma
SolidCompression=true
AllowUNCPath=false
VersionInfoVersion=1.0
VersionInfoCompany=Apkawa Inc
VersionInfoDescription=quimge - Qt GUI for uimge muiltiuploaders image to different imagehostings


[Dirs]
Name: {app}; Flags: uninsalwaysuninstall

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: {group}\quimge; Filename: {app}\quimge.exe; WorkingDir: {app}
Name: {group}\Uinstall; Filename: {app}\unins000.exe; WorkingDir: {app}

[Run]
Filename: {app}\quimge.exe; Description: {cm:LaunchProgram,guimge}; Flags: nowait postinstall skipifsilent

