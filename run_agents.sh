tmux new-session -s snubi_zeus2022

tmux set -g mouse on


tmux split-window -h
tmux split-window -h

tmux select-pane -t 0
tmux send "source venv/bin/activate" C-m
tmux send "python vision_agent.py" C-m

tmux select-pane -t 1
tmux send "source venv/bin/activate" C-m
tmux send "python face_agent.py" C-m

tmux select-pane -t 2
tmux send "source venv/bin/activate" C-m
tmux send "cd zeusweb-master" C-m
tmux send "python manage.py runserver" C-m


