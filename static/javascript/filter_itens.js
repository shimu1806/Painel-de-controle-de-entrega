// Adicione um evento de clique genérico para todos os cabeçalhos da coluna
document.querySelectorAll("thead td").forEach(function(th, index) {
    th.addEventListener("click", function() {
        filterTable(index); // Chame a função de filtragem com o índice da coluna clicada
    });
});

function filterTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch, direction;
    table = document.querySelector(".table-hover");
    switching = true;
    direction = "asc"; // Define a direção inicial como ascendente
    var clicks = table.getAttribute("data-clicks-" + columnIndex) || 0; // Obtém o número de cliques nesta coluna
    clicks = parseInt(clicks);

    // Incrementa o número de cliques e ajusta a direção com base nisso
    clicks++;
    if (clicks % 3 === 1) {
        direction = "asc"; // Primeiro clique: do menor para o maior
    } else if (clicks % 3 === 2) {
        direction = "desc"; // Segundo clique: do maior para o menor
    } else {
        direction = "orig"; // Terceiro clique: volta ao normal (sem classificação)
    }
    table.setAttribute("data-clicks-" + columnIndex, clicks); // Atualiza o número de cliques

    // ... código de classificação ...

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[columnIndex];
            y = rows[i + 1].getElementsByTagName("td")[columnIndex];

            // Verifica a direção e se deve trocar as células
            if (direction === "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch= true;
                    break;
                }
            } else if (direction === "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch= true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}