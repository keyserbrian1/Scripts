for %%G in (*.mkv) do (
if not exist "%%~dpnG_eng.mkv" (
"C:\Program Files\MKVToolNix\mkvmerge.exe" -o "%%~dpnG_eng.mkv" -a 2 -S "%%~G"
)
)