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
OutputDir=installer
OutputBaseFilename={#Name}-web_installer-{#Version}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "7za.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
; Source: "{tmp}\{#Name}-win_portable\*"; DestDir: "{app}"; Flags: ignoreversion external

[Icons]
Name: "{group}\{#Name}"; Filename: "{app}\{#Executable}"
Name: "{group}\{cm:UninstallProgram,{#Name}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Name}"; Filename: "{app}\{#Executable}"; Tasks: desktopicon

[Run]
Filename: "{tmp}\7za.exe"; Parameters: "x '{tmp}\{#Name}.zip' -o'{app}\' * -r -aoa"; Flags: runascurrentuser runhidden
Filename: "{app}\{#Executable}"; Description: "{cm:LaunchProgram,{#StringChange(Name, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var 
  DownloadPage: TDownloadWizardPage;

procedure InitializeWizard; begin
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), nil);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if CurPageID = wpReady then begin
    DownloadPage.Clear;

    DownloadPage.Add('https://github.com/{#Publisher}/{#Name}/releases/download/v{#Version}/{#Name}-win_portable-{#Version}.zip', '{#Name}.zip', '');

    DownloadPage.Show;
    try
      try
        DownloadPage.Download;
        Result := True;
      except
          SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
        Result := False;
      end;
    finally
      DownloadPage.Hide;
    end;
  end else
    Result := True;
end;


procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep); begin
  if CurUninstallStep = usPostUninstall then begin
    if MsgBox('Do you want to delete all the user data (all saved passwords) ?', mbConfirmation, MB_YESNO) = IDYES then begin
        if DelTree(ExpandConstant('{app}/'), True, True, True) then begin 
        end 
        else begin
            MsgBox('Error deleting user data. Please delete it manually.', mbError, MB_OK);
        end;
    end;
  end;
end;
