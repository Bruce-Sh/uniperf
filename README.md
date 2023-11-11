/etc/systemd/system/uniperf.service
[Unit]
Description=Gunicorn instance to serve uniperf
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/logsDB/uniperf
Environment="PATH=/logsDB/env/bin"
ExecStart=/logsDB/env/bin/gunicorn --workers 3 --bind unix:uniperf.sock -m 007 run

[Install]
WantedBy=multi-user.target


