#!/usr/bin/env bash
yabai_state=$(brew services|rg --pcre2 -o '(?<=yabai)\s+\w+'|sed 's/ //g')
if [ "$yabai_state" == "started" ]; then
	eval 'brew services stop yabai'
elif [ "$yabai_state" == "stopped" ]; then
	eval 'brew services start yabai'
fi
