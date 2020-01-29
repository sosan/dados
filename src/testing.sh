if [ "${FLASK_ENV}" = "development" ]; then
    echo "development"
    gunicorn --bind 0.0.0.0:"${PORT}" --workers 3 main:app --reload
else
    echo "production"
    gunicorn --bind 0.0.0.0:"${PORT}" --workers 3 main:app
fi