if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <nom_fichier.csv>"
    exit 1
fi

if [[ ! "$1" =~ \.csv$ ]]; then
    echo "Le nom du fichier doit se terminer par '.csv'"
    exit 1
fi

name_csv="$1"

echo "Instance, Time, ExploredNodes, RemainingNodes" > $name_csv

for i in {1..10}; do
    instance="./Instances/i$(printf "%02d" $i)"

    output=$(python pacman.py $instance)

    execution_time=$(echo "$output" | grep "Execution time" | awk '{print $4}')
    nodes_explored=$(echo "$output" | grep "# Nodes explored" | awk '{print $5}')
    queue_size=$(echo "$output" | grep "Queue size at goal" | awk '{print $6}')
    
    echo -n "i$(printf "%02d" $i), $execution_time, $nodes_explored, $queue_size" >> $name_csv
    echo "" >> $name_csv
done

echo "Terminé."
echo "Les temps d'exécution ont été enregistrés dans $name_csv."