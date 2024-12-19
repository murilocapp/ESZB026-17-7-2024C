#!/bin/bash

# Caminhos dos arquivos
ARQUIVO_DADOS="data/leitura_sensor.csv"
ARQUIVO_EVENTOS="data/eventos.csv"
ARQUIVO_STATUS="data/status_alarme.txt"
ARQUIVO_ALARME="/var/www/html/alarme.html"  

# Diretório para gráficos
DIR_GRAFICOS="/var/www/html/graficos"
mkdir -p "$DIR_GRAFICOS"

# Função para gerar os gráficos
gera_graficos() {
    gnuplot <<-EOF
        set terminal png
        set output "${DIR_GRAFICOS}/rasterplot.png"
        set title "Rasterplot de Eventos"
        set xlabel "Tempo (s)"
        set ylabel "Eventos"
        plot "${ARQUIVO_EVENTOS}" using 1:2 with impulses title "Eventos"

        set output "${DIR_GRAFICOS}/dispersao.png"
        set title "Gráfico de Dispersão"
        set xlabel "Tempo (s)"
        set ylabel "Valor"
        plot "${ARQUIVO_DADOS}" using 1:2 with points title "Valores"
EOF
}


# Função para gerar a página de status do alarme
gera_pagina() {
    local status=$(cat "$ARQUIVO_STATUS")

    cat <<EOF > "$ARQUIVO_ALARME"
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="10"> <!-- Atualiza a página a cada 10 segundos -->
    <title>Monitor de Apneia</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #c4ae69;
            text-align: center;
            margin: 0;
            padding: 20px;
            color: #11161b;
        }
        img {
            max-width: 90%;
            height: auto;
            margin: 20px 0;
        }
        .status {
            font-size: 1.2em;
            margin: 20px;
            display: inline-block;
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Monitor de Apneia</h1>
    <h2>Rasterplot</h2>
    <img src="/graficos/rasterplot.png" alt="Rasterplot de Eventos">

    <h2>Gráfico de Dispersão</h2>
    <img src="/graficos/dispersao.png" alt="Gráfico de Dispersão">

    <h2>Status do Paciente</h2>
EOF

    if [[ "$status" == "Alarme Ativado" ]]; then
        cat <<EOF >> "$ARQUIVO_ALARME"
    <div class="status" style="color: red; font-weight: bold;">⚠️ Alarme Disparado! Paciente em Risco!</div>
EOF
    else
        cat <<EOF >> "$ARQUIVO_ALARME"
    <div class="status" style="color: green; font-weight: bold;">✅ Status Normal. Paciente Estável.</div>
EOF
    fi

    cat <<EOF >> "$ARQUIVO_ALARME"
</body>
</html>
EOF
}

# Chamar as funções
gera_graficos
atualiza_status
gera_pagina