execute pathogen#infect()
execute pathogen#helptags() 
syntax on
filetype plugin indent on

:let mapleader = "\<space>"

map <leader>n :NERDTreeToggle<CR>
map <leader>p :CtrlP<CR>
map <leader>w :w<CR>
map <leader>s :Ag<space>

let g:neocomplete#enable_at_startup = 1
let g:neocomplete#enable_smart_case = 1

inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"

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
set backspace=indent,eol,start
set grepprg=grep\ -nH\ $*
let g:tex_flavor = "latex"

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_cpp_compiler = 'g++'
let g:syntastic_cpp_compiler_options = ' -std=c++11 -stdlib=libc++'

au FileType haskell nnoremap <buffer> <F1> :HdevtoolsType<CR>
au FileType haskell nnoremap <buffer> <silent> <F2> :HdevtoolsClear<CR>
au FileType haskell nnoremap <buffer> <silent> <F3> :HdevtoolsInfo<CR>

" The Silver Searcher
if executable('ag')
  " Use ag over grep
  set grepprg=ag\ --nogroup\ --nocolor

  " Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
  let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'

  " ag is fast enough that CtrlP doesn't need to cache
  let g:ctrlp_use_caching = 0
  nnoremap K :grep! "\b<C-R><C-W>\b"<CR>:cw<CR>
endif
autocmd BufEnter *.php set ai sw=2 ts=2 sta et fo=croql
autocmd BufRead,BufNewFile *.twig set filetype=jinja
autocmd BufEnter *.twig set ai sw=4 ts=4 sta et fo=croql
