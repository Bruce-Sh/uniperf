source /logsDB/venv/bin/activate
#python /Interop/logsDB/uniperf/app.py
export FLASK_APP=/logsDB/uniperf/run.py
flask run --host=0.0.0.0 --port=8090

