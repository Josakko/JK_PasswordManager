#define Name "JK Password Manager"
#define Version "6.6.1"
#define Publisher "Josakko"
#define AppUrl "https://github.com/Josakko/JK_PasswordManager"
#define Executable "JK_PasswordManager.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{15F8CA47-4A96-4B97-B546-95A40F93C10B}
AppName={#Name}
AppVersion={#Version}
;AppVerName={#Name} {#Version}
AppPublisher={#Publisher}
AppPublisherURL={#AppUrl}
AppSupportURL={#AppUrl}
AppUpdatesURL={#AppUrl}
DefaultDirName={autopf}\JK_PasswordManager
DefaultGroupName={#Name}
AllowNoIcons=yes
LicenseFile=LICENSE
; C:\Users\Korisnik\Documents\Programs\JK Password Manager\SetupFile\LICENSE
; Remove the following line to run in administrative install mode (install for all users.)
; PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer
; C:\Users\Korisnik\Desktop
OutputBaseFilename=JK_PasswordManagerSetupFile
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Korisnik\Documents\Programs\JK Password Manager\JK Password Manager\{#Executable}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Korisnik\Documents\Programs\JK Password Manager\JK Password Manager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#Name}"; Filename: "{app}\{#Executable}"
Name: "{group}\{cm:UninstallProgram,{#Name}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Name}"; Filename: "{app}\{#Executable}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#Executable}"; Description: "{cm:LaunchProgram,{#StringChange(Name, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

