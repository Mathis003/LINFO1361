#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <nom_fichier.csv>"
    exit 1
fi

if [[ ! "$1" =~ \.csv$ ]]; then
    echo "Le nom du fichier doit se terminer par '.csv'"
    exit 1
fi

name_csv="$1"

echo "Instance, Temps1, Temps2, Temps3, Temps4, Temps5, Temps6, Temps7, Temps8, Temps9, Temps10" > $name_csv

for i in {1..10}; do
    instance="./Instances/i$(printf "%02d" $i)"

    for j in {1..10}; do
        runtime=$( { time python3 pacman.py "$instance" > /dev/null; } 2>&1 | grep real | awk '{print $2}' )
        
        if [ $j -eq 1 ]; then
            echo -n "i$(printf "%02d" $i), $runtime" >> $name_csv
        else
            echo -n ", $runtime" >> $name_csv
        fi
    done

    echo "" >> $name_csv
done

echo "Terminé."
echo "Les temps d'exécution ont été enregistrés dans $name_csv."
