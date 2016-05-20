ECHO OFF
for %%G in (*.mkv) do (
if not exist "%%~dpnG.mp4" (
"C:\Program Files\HandBrake-0.10.2-x86_64-Win_CLI\HandBrakeCLI.exe" -i "%%~G" -o "%%~dpnG.mp4" -s "1" --subtitle-burn 1
)
)
ECHO on