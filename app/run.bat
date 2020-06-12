if not  exist ./login_data.json (
    rem file exists
    echo "No login-credentials found, asking now..."
    python ./init_app.py
)

:loop
python ./main.py
timeout /t 3 > NUL
goto loop