python3 backend/manage.py &
cd frontend; npm start &
cd ../rasa ;python3 -m rasa_core_sdk.endpoint --actions chat_actions