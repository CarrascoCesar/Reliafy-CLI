" Reliafy minimal .vimrc for simple YAML editing (portable)

" Enable filetype detection and plugins
filetype plugin indent on

" Use UTF-8
set encoding=utf-8
set fileencoding=utf-8

" Syntax highlighting
syntax on

" Colors and UI
set number
set showmatch

" Indentation
set expandtab
set shiftwidth=2
set tabstop=2
set smartindent

" YAML specific: 2-space indent, fold markers disabled
augroup yaml_settings
  autocmd!
  autocmd FileType yaml setlocal shiftwidth=2 tabstop=2 expandtab
augroup END

" Highlight overlong lines at column 121 (optional)
" Optional: uncomment to mark column 121
" set colorcolumn=121

" Search
set ignorecase
set smartcase
set hlsearch
set incsearch

" Status line
set laststatus=2

" Better backspace
set backspace=indent,eol,start

" Disable swap/backup in repo (optional)
" Keep defaults for swap/backup to avoid surprises across environments

" Map :W to :w
command! W w

" YAML filetype detection for .yaml/.yml
augroup filetypedetect
  autocmd!
  autocmd BufRead,BufNewFile *.yml,*.yaml setfiletype yaml
augroup END
