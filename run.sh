#!/bin/sh

ROOT="$(dirname $(realpath $0))"

if [ $1 -eq "player" ]; then
    python $ROOT/tss-player.py
elif [ $1 -eq "recorder" ]; then
    python $ROOT/tss-recorder.py
else
    echo '引数にはplayerかrecorderを指定してください'
fi