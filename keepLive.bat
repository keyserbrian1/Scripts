@setlocal enableextensions enabledelayedexpansion
@echo off
set connectionTries=0
set restarts=0
:loop
echo Testing Connection...
set state=down
for /f "tokens=1,3" %%a in ('ping -n 1 8.8.8.8') do (
    if %%a==Reply if %%b==8.8.8.8: set state=up
)
if %state%==down (
    echo Failure^^!
    echo Restarting...    
    netsh wlan disconnect >nul:
    set found=no
    for /f "tokens=4" %%n in ('netsh wlan show network') do (
        if "%%n"=="KEYSER-family5.0" set found=yes
    )
    if "%found%"=="no" (
        echo Target Wi-fi not found^^!
        set /a connectionTries=connectionTries+1
        echo Connection Failure #!connectionTries!^^!
        if !connectionTries!==3 (
            echo Quitting...
            goto :end
        ) else (
            echo Retrying...
        )
    ) else (
        for /f "tokens=1" %%q in ('netsh wlan connect KEYSER-family5.0') do (set res=%%q)
        ping -n 1 -t 10000 0.0.0.0 >nul: 2>nul:
        if not "!res!"=="Connection" (
            echo Error in connection^^!
            set /a connectionTries=connectionTries+1
            echo Connection Failure #!connectionTries!^^!
            if !connectionTries!==3 (
                echo Quitting...
                goto :end
            ) else (
                echo Retrying...
            )
        ) else (
            echo Restarted^^!
            set connectionTries=0
            set /a restarts=restarts+1
        )
    )
) else (
    echo OK^^!
    set connectionTries=0
)

choice /c Qqwertyuiopasdfghjklzxcvbnm1234567890 /cs /n /t 2 /d Q >nul: 2>nul:
if not !errorlevel!==1 (
    echo Restarted connection !restarts! times.
)
goto :loop
:end
endlocal