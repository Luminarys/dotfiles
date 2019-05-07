" execute pathogen#infect()
" execute pathogen#helptags() 
"
call plug#begin('~/.vim/plugged')

Plug 'scrooloose/nerdtree'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'mileszs/ack.vim'
Plug 'vim-airline/vim-airline'
Plug 'elixir-lang/vim-elixir'
Plug 'othree/yajs.vim'
Plug 'mxw/vim-jsx'
Plug 'pangloss/vim-javascript'
Plug 'embear/vim-localvimrc'
Plug 'rust-lang/rust.vim'
Plug 'racer-rust/vim-racer'
Plug 'kchmck/vim-coffee-script'
Plug 'Chiel92/vim-autoformat'
Plug 'Shougo/vimproc'
Plug 'Shougo/unite.vim'
Plug 'cespare/vim-toml'
Plug 'mbbill/undotree'
Plug 'airblade/vim-gitgutter'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-rhubarb'
Plug 'majutsushi/tagbar'
Plug 'tikhomirov/vim-glsl'

call plug#end()

syntax enable

let mapleader = "\<space>"
map <leader>n :NERDTreeToggle<CR>
map <leader>p :CtrlP<CR>
map <leader>t :CtrlPTag<CR>
map <leader>b :TagbarToggle<CR>
map <leader>w :w<CR>
map <leader>af :Autoformat<CR>
map <leader>q :b#<CR>
map <leader>u :UndotreeToggle<CR>
nnoremap <Leader>a :Ack!<Space>


" inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
" inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
" inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"
if executable('rg')
  let g:ackprg = 'rg --vimgrep'
endif

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
set smarttab
set autoindent
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set backspace=indent,eol,start
set grepprg=grep\ -nH\ $*
let g:tex_flavor = "latex"

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

" au FileType haskell nnoremap <buffer> <F1> :HdevtoolsType<CR>
" au FileType haskell nnoremap <buffer> <silent> <F2> :HdevtoolsClear<CR>
" au FileType haskell nnoremap <buffer> <silent> <F3> :HdevtoolsInfo<CR>

if executable('rg')
  let g:ctrlp_user_command = 'rg -l --color never "" %s'
endif
let g:jsx_ext_required = 0

"" let g:tagbar_type_rust = {
""    \ 'ctagstype' : 'rust',
""    \ 'kinds' : [
""        \'T:types,type definitions',
""        \'f:functions,function definitions',
""        \'g:enum,enumeration names',
""        \'s:structure names',
""        \'m:modules,module names',
""        \'c:consts,static constants',
""        \'t:traits',
""        \'i:impls,trait implementations',
""    \]
""    \}

let g:localvimrc_persistent = 1

autocmd BufEnter *.go set ai noexpandtab ts=4 sw=4
autocmd BufEnter *.php set ai sw=2 ts=2 sta et fo=croql
autocmd BufEnter *.js set ai sw=2 ts=2 sta et fo=croql
autocmd BufEnter *.jsx set ai sw=2 ts=2 sta et fo=croql
autocmd BufEnter *.coffee set ai sw=2 ts=2 sta et fo=croql
autocmd BufRead,BufNewFile *.twig set filetype=jinja
autocmd BufEnter *.twig set ai sw=2 ts=2 sta et fo=croql
autocmd BufRead *.rs :setlocal tags=./rusty-tags.vi;/,$RUST_SRC_PATH/rusty-tags.vi
autocmd BufWrite *.rs :silent! exec "!rusty-tags vi --quiet --start-dir=" . expand('%:p:h') . "&" <bar> redraw!
autocmd BufEnter *.java set tags=.tags
