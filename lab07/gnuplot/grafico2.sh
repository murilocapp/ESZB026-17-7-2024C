#!/bin/sh
ARQUIVODADOS=/home/pi/sist_embarcados_git/lab07/gnuplot/dados2.txt
ARQUIVOSAIDA=/home/pi/sist_embarcados_git/lab07/gnuplot/dados2.png

gnuplot << EOF
set title "Grafico Grupo 7 - 2"
set ylabel "Eixo Y"
set xlabel "Eixo X"
set terminal png
set output "$ARQUIVOSAIDA"
plot "$ARQUIVODADOS" \
     linecolor rgb '#00ff00' \
     linetype 0 \
     linewidth 0 \
     pointtype 5 \
     pointsize 1.0 \
     title "meus dados" \
     with linespoints
EOF
