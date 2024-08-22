#define Name "JK_PasswordManager"
#define Version "7.0.0"
#define Publisher "Josakko"
#define AppUrl "https://github.com/Josakko/JK_PasswordManager"
#define Executable "JK_PasswordManager.exe"

[Setup]
AppId={{15F8CA47-4A96-4B97-B546-95A40F93C10B}
AppName={#Name}
AppVersion={#Version}
AppVerName={#Name}-{#Version}
AppPublisher={#Publisher}
AppPublisherURL={#AppUrl}
AppSupportURL={#AppUrl}
AppUpdatesURL={#AppUrl}
DefaultDirName={autoappdata}\{#Name}
DefaultGroupName={#Name}
AllowNoIcons=yes
DisableDirPage=auto
DisableWelcomePage=no
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
SetupIconFile=..\assets\icon.ico
; WizardImageFile=wizardimage.bmp
UninstallDisplayIcon=..\assets\icon.ico
UninstallDisplayName={#Name}-Setup
ChangesAssociations=yes
LicenseFile=..\..\..\LICENSE
PrivilegesRequired=lowest
OutputDir=installer
OutputBaseFilename={#Name}-installer-{#Version}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "..\..\..\out\windows-out\{#Executable}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\..\src\assets"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#Name}"; Filename: "{app}\{#Executable}"
Name: "{group}\{cm:UninstallProgram,{#Name}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Name}"; Filename: "{app}\{#Executable}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#Executable}"; Description: "{cm:LaunchProgram,{#StringChange(Name, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

