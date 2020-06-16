if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$pwd'; & '$PSCommandPath';`"";
    exit;
}

if(-not(Test-Path ./vc_redist.x64.exe -PathType Leaf))
{
    Invoke-WebRequest https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile vc_redist.x64.exe
}
Start-Process ./vc_redist.x64.exe /passive -NoNewWindow -Wait
if(-not($?)) {
    if (Test-Path ./vc_redist.x64.exe)
    {
      Remove-Item ./vc_redist.x64.exe
    }
    Write-Host "C++ Redistributable install failed. Please try again." -foreground red
    Exit(1)
}


python -V
if(-not($?)) {
    Write-Host "Please make sure Python is installed and command 'python -V' is callable." -foreground red
    Exit(1)
}

pip -V
if(-not($?)) {
    Write-Host "Please make sure Python-pip is installed and command 'pip -V' is callable." -foreground red
    Exit(2)
}

if(-not(Test-Path ./live.zip -PathType Leaf))
{
    Invoke-WebRequest https://github.com/planBLICK/easy2track_terminal/archive/live.zip -OutFile live.zip
    Expand-Archive ./live.zip -DestinationPath ./
    Rename-Item -Path ./easy2track_terminal-live ./easy2track_terminal
}



& pip install -r ./easy2track_terminal/requirements.txt

$file = (Get-Location).Path + "\easy2track_terminal\app\"
Write-Host $file
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\easy2track_terminal.lnk")
$Shortcut.TargetPath = $file + "run.bat"
$Shortcut.WorkingDirectory = $file
$shortcut.IconLocation= $file + "easy2track_terminal.ico"
$Shortcut.Save()

Write-Host "Installation successfull. cd now into ./easy2track_terminal/app and run 'run.bat'" -foreground green
Write-Host $pwd
read-host Press ENTER to continue...