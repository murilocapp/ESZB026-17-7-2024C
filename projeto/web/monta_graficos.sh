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
gera_pagina_alarme() {
    local status=$(cat "$ARQUIVO_STATUS")
    
    echo '<!DOCTYPE html>' > "$ARQUIVO_ALARME"
    echo '<html>' >> "$ARQUIVO_ALARME"
    echo '<head>' >> "$ARQUIVO_ALARME"
    echo '    <meta http-equiv="refresh" content="10">' >> "$ARQUIVO_ALARME"
    echo '    <title>Status do Alarme</title>' >> "$ARQUIVO_ALARME"
    echo '    <style>' >> "$ARQUIVO_ALARME"
    echo '        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }' >> "$ARQUIVO_ALARME"
    echo '        .status { font-size: 1.5em; margin-top: 50px; }' >> "$ARQUIVO_ALARME"
    echo '    </style>' >> "$ARQUIVO_ALARME"
    echo '</head>' >> "$ARQUIVO_ALARME"
    echo '<body>' >> "$ARQUIVO_ALARME"
    echo '    <h1>Status do Alarme</h1>' >> "$ARQUIVO_ALARME"

    if [[ "$status" == "Alarme Ativado" ]]; then
        echo '    <div class="status" style="color: red; font-weight: bold;">⚠️ Alarme Disparado! Paciente em Risco!</div>' >> "$ARQUIVO_ALARME"
    else
        echo '    <div class="status" style="color: green; font-weight: bold;">✅ Status Normal. Paciente Estável.</div>' >> "$ARQUIVO_ALARME"
    fi

    echo '</body>' >> "$ARQUIVO_ALARME"
    echo '</html>' >> "$ARQUIVO_ALARME"
}

# Chamar as funções
gera_graficos
atualiza_status
gera_pagina_alarme
