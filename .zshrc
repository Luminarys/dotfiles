# Path to your oh-my-zsh installation.
export ZSH=/home/luminarys/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="kardan"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder
#
# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git zsh-syntax-highlighting)

# User configuration

export PATH="/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl/:/home/luminarys/Scripts:/home/luminarys/Programming/Go/bin/"
# export MANPATH="/usr/local/man:$MANPATH"

source $ZSH/oh-my-zsh.sh

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi
export EDITOR='vim'

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
 export SSH_KEY_PATH="~/.ssh/"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias update="sudo pacman -Syu && yaourt -Syua"
alias pstall="sudo pacman -S"
alias astall="makepkg -s && sudo pacman -U *.xz"
alias terminal="gnome-terminal"
alias shutdown="sudo shutdown 0"
alias open="xdg-open"
alias login-to-homeserv="ssh luminarys@luminarys.com -i ~/.ssh/HomeServ"
alias gcc="gcc -pedantic"
alias fcow="fortune | cowsay"
alias dm="sh /home/luminarys/Scripts/DM.sh"
alias ranger='python /usr/bin/ranger'
alias ssh='TERM=linux ssh'
alias latex-clone='cp -r ~/Documents/Latex/latex-boilerplate'
alias platex-clone='cp -r ~/Documents/Latex/latex-physics-bp'
alias gpo='git push origin master'
alias gpu='git push upstream master'
alias vpn='sudo openvpn /etc/openvpn/pia/US_Midwest.ovpn'
alias gac='git add . && git commit -m'
alias mpd-update='mpc update Music'
alias msync='rsync -P -a eumen@rt.luminarys.com:/media/500g/Music/ ~/Music/ && mpd-update'
alias viz='cava -i fifo -p /tmp/mpd.fifo'
alias tfortune='shuf -n 1 ~/Scripts/theo-quotes'
alias nsm='xrandr --output eDP1 --off --output VGA1 --left-of HDMI1'
alias sm='xrandr --output eDP1 --left-of VGA1 --output VGA1 --left-of HDMI1'
#alias tmux="TERM=screen-256color-bce tmux -2"
TERM=xterm-256color

export PATH=/home/luminarys/torch/install/bin:$PATH  # Added automatically by torch-dist
export LD_LIBRARY_PATH=/home/luminarys/torch/install/lib:/usr/local/lib/:$LD_LIBRARY_PATH  # Added automatically by torch-dist
export DYLD_LIBRARY_PATH=/home/luminarys/torch/install/lib:$DYLD_LIBRARY_PATH  # Added automatically by torch-dist
export GOPATH=/home/luminarys/Programming/Go
export GOBIN=/home/luminarys/Programming/Go/bin
export GOMAXPROCS=8
#export GTK_THEME=Adwaita
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
