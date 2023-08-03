#! /bin/bash
source /opt/anaconda/etc/profile.d/conda.sh
conda activate telegram-personal-bot
export TUNNEL_DOMAIN=http://localhost:3000
python bot.py
