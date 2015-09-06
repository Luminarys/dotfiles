execute pathogen#infect()
syntax on
filetype plugin indent on
map <C-n> :NERDTreeToggle<CR>
let g:neocomplete#enable_at_startup = 1
inoremap <C-d> <C-h>
imap <C-j> <down>
imap <C-k> <up>
inoremap <C-h> <left>
imap <C-l> <right>
imap <C-e> <Esc>
noremap <C-e> <Esc>
map <S-p> :bprev<CR>
map <S-n> :bnext<CR>
map <S-e> :bdelete<CR>
map <S-h> :wincmd h<CR>
map <S-l> :wincmd l<CR>
map <S-j> :wincmd j<CR>
map <S-k> :wincmd k<CR>
let g:airline#extensions#tabline#enabled = 1
set laststatus=2
set autochdir
set smarttab
set tabstop=4
set shiftwidth=4
set expandtab
set grepprg=grep\ -nH\ $*
let g:tex_flavor = "latex"
