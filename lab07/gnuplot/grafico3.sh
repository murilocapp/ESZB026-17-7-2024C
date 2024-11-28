#!/bin/sh
ARQUIVODADOS=/home/pi/sist_embarcados_git/lab07/gnuplot/dados3.txt
ARQUIVOSAIDA=/home/pi/sist_embarcados_git/lab07/gnuplot/dados3.png

gnuplot << EOF
set title "Grafico Grupo 7 - 3"
set ylabel "Eixo Y"
set xlabel "Eixo X"
set terminal png
set output "$ARQUIVOSAIDA"
plot "$ARQUIVODADOS" \
     linecolor rgb '#ff0000' \
     linetype 2 \
     linewidth 1 \
     pointtype 5 \
     pointsize 0 \
     title "meus dados" \
     with linespoints
EOF
