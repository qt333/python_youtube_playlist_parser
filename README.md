# Youtube playlist parser

Python script that allow you to parse given youtube playlist titles

# Features
- Manually fetch playlist titles
- Save to txt or json file
- Send message with telegram bot upon successful update

# Adding Cron job
m h  dom mon dow

0 11 * * * /home/ubuntu/python_youtube_playlist_parser/start_parse.sh >> /home/ubuntu/python_youtube_playlist_parser/cron.log 2>&1

