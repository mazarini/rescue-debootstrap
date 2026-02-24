set mouse=
" --- Interface et Visuel ---
set showcmd             " Affiche la commande en cours en bas à droite
set cursorline          " Souligne la ligne où se trouve le curseur
set showmatch           " Surligne la parenthèse correspondante
syntax on               " Active la coloration syntaxique
set termguicolors       " Couleurs 24-bits si ton terminal le supporte

" --- Tabulations et Indentation ---
set expandtab           " Remplace les tabulations par des espaces
set shiftwidth=4        " Taille de l'indentation (4 espaces)
set tabstop=4           " Une tabulation affiche 4 espaces
set smartindent         " Indentation intelligente (pour le C, Python, etc.)

" --- Recherche ---
set hlsearch            " Surligne les résultats de recherche
set incsearch           " Recherche au fur et à mesure de la saisie
set ignorecase          " Ignore la casse lors de la recherche...
set smartcase           " ...sauf si on utilise une majuscule

" --- Comportement Système ---
set hidden              " Permet de changer de buffer sans sauvegarder
set undofile            " Garde l'historique des 'undo' même après fermeture
set encoding=utf-8      " Encodage standard (important pour tes locales !)
