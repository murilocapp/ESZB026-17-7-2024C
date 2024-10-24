#!/ bin / bash
2
3 # script baseado no có digo disponibilizado em:
4 # Derek Molloy , Exploring Raspberry Pi: Interfacing to the Real World with Embedded Linux ,
5 # Wiley 2016 , ISBN 978 -1 -119 -1868 -1 , http :// www. exploringrpi . com /
6 #
7 # Script usado para chavear um pino da GPIO na frequencia mais alta
8 # possivel usando Bash
9 echo 23 > / sys / class / gpio / export
10 sleep 0.5
11 echo " out" > / sys / class / gpio / gpio23 / direction
12 COUNTER =0
13 while [ $COUNTER -lt 20000 ]; do
14 echo 1 > / sys / class / gpio / gpio23 / value
15 let COUNTER = COUNTER +1
16 echo 0 > / sys / class / gpio / gpio23 / value
17 done
18 echo 23 > / sys / class / gpio / unexport