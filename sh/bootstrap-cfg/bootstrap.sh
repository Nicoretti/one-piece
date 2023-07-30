#!/bin/sh

# configuration
CONFIG_SOURCE="git@github.com:Nicoretti/terminal-config.git"
CONFIG_DESTIONATION="${HOME}/.cfg"
OH_MY_ZSH_SOURCE="https://github.com/robbyrussell/oh-my-zsh.git"
OH_MY_ZSH_DESTINATION="${HOME}/.oh-my-zsh"

# adjust configuration for read only setup
if [ $1 ] && [ $1 -eq "readonly" ]; then
    CONFIG_SOURCE="https://github.com/Nicoretti/terminal-config.git"
fi

say() {
	echo "bootstrap-cfg: ${1}"
}

# commonly used functions
err() {
    say "$1" >&2
    exit 1
}

need_cmd() {
    if ! command -v "$1" > /dev/null 2>&1
    then err "need '$1' (command not found)"
    fi
}

run() {
    "$@"
    if [ $? != 0 ]; then
        err "command failed: $*"
    fi
}

# check if all command are available commands
need_cmd mv
need_cmd git
need_cmd zsh

# Back up existing configurations
if [ -d ${OH_MY_ZSH_DESTINATION} ]; then
    run mv "${OH_MY_ZSH_CONFIG_DESTINATION}" "${OH_MY_ZSH_DESTINATION}.bak"
fi

if [ -d ${CONFIG_DESTIONATION} ]; then
    run mv "${CONFIG_DESTIONATION}" "${CONFIG_DESTIONATION}.bak"
fi

# check out configurations
run git clone ${OH_MY_ZSH_SOURCE} ${OH_MY_ZSH_DESTINATION}
run git clone --bare ${CONFIG_SOURCE} ${CONFIG_DESTIONATION}

# prepare config command
GIT_PATH=`command -v git`
CONFIG_COMMAND="${GIT_PATH} --git-dir=${CONFIG_DESTIONATION} --work-tree=${HOME}"

# prevent git from showing entire home as untracked
# -> we will add relavant config files manualy (opt-in)
run ${CONFIG_COMMAND} checkout -f master 
run ${CONFIG_COMMAND} config --local status.showUntrackedFiles no

