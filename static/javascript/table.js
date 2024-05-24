// Variáveis para paginação
let currentPage = 1;
const itemsPerPage = 25;
let totalItems = 0;
let tableData = [];

// Endpoints
const endpointTable = '/fetch_data/';
const endpointMural = '/update_status_counts/';

// Função para obter dados do endpoint
function fetchTableData() {
    fetch(endpointTable)
        .then(response => response.json())
        .then(data => {
            tableData = data;
            totalItems = tableData.length;
            displayTableData(); // Constrói os dados da tabela
            updateNavigationButtons(); // Atualiza os botões de navegação
            updatePageInfo(); // Atualiza as informações da página
        })
        .catch(error => console.error('Error:', error));
}

// Função para renderizar a tabela com os dados da página atual
function displayTableData() {
    const tableBody = document.querySelector('.table-group-divider');
    tableBody.innerHTML = ''; // Limpa a tabela
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = tableData.slice(start, end);

    pageData.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><span class="status-${item.CB7_STATUS}"></span></td>
            <td>${item.CB7_FILIAL}</td>
            <td>${item.CB7_ORDSEP}</td>
            <td>${item.CB7_PEDIDO}</td>
            <td>${item.CB7_CLIENT}</td>
            <td>${item.CB7_LOJA}</td>
            <td>${item.A1_NOME}</td>
            <td>${item.CB7_DTEMIS}</td>
            <td>${item.CB7_HREMIS}</td>
            <td>${item.CB7_DTINIS}</td>
            <td>${item.CB7_HRINIS}</td>
            <td>${item.CB7_DTFIMS}</td>
            <td>${item.CB7_HRFIMS}</td>
            <td>${item.CB7_NOTA}</td>
            <td>${item.CB7_SERIE}</td>
            <td>${item.CB8_PROD}</td>
            <td>${item.B1_DESC}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Função para ordenar os dados e renderizar a tabela
function filterTable(columnIndex) {
    let direction = "asc"; // Define a direção inicial como ascendente
    let clicks = parseInt(document.querySelector(".table-hover").getAttribute("data-clicks-" + columnIndex) || 0);

    clicks++;
    if (clicks % 3 === 1) {
        direction = "asc"; // Primeiro clique: do menor para o maior
    } else if (clicks % 3 === 2) {
        direction = "desc"; // Segundo clique: do maior para o menor
    } else {
        direction = "orig"; // Terceiro clique: volta ao normal (sem classificação)
    }
    document.querySelector(".table-hover").setAttribute("data-clicks-" + columnIndex, clicks);

    if (direction === "asc") {
        tableData.sort((a, b) => (a[columnIndex] > b[columnIndex]) ? 1 : -1);
    } else if (direction === "desc") {
        tableData.sort((a, b) => (a[columnIndex] < b[columnIndex]) ? 1 : -1);
    } else {
        // Se a direção for "orig", você pode redefinir a ordem original dos dados
        fetchTableData(); // Recarrega os dados originais
        return;
    }

    displayTableData();
    updateNavigationButtons();
    updatePageInfo();
}

// Adicione um evento de clique genérico para todos os cabeçalhos da coluna
document.querySelectorAll("thead th").forEach(function(th, index) {
    th.addEventListener("click", function() {
        filterTable(index); // Chame a função de filtragem com o índice da coluna clicada
    });
});

// Função para atualizar os botões de navegação
function updateNavigationButtons() {
    document.getElementById('previous').disabled = currentPage === 1;
    document.getElementById('next').disabled = currentPage === Math.ceil(totalItems / itemsPerPage);
    document.getElementById('first').disabled = currentPage === 1;
    document.getElementById('last').disabled = currentPage === Math.ceil(totalItems / itemsPerPage);
}

// Função para atualizar as informações da página
function updatePageInfo() {
    const pageInfo = document.getElementById('page-info');
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
}

// Função para mudar de página
function changePage(newPage) {
    if (newPage < 1 || newPage > Math.ceil(totalItems / itemsPerPage)) return;
    currentPage = newPage;
    displayTableData();
    updateNavigationButtons();
    updatePageInfo();
}

// Adicione eventos para os botões de paginação
document.getElementById('previous').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        displayTableData();
        updateNavigationButtons();
        updatePageInfo();
    }
});

document.getElementById('next').addEventListener('click', () => {
    if (currentPage < Math.ceil(totalItems / itemsPerPage)) {
        currentPage++;
        displayTableData();
        updateNavigationButtons();
        updatePageInfo();
    }
});

document.getElementById('first').addEventListener('click', () => {
    currentPage = 1;
    displayTableData();
    updateNavigationButtons();
    updatePageInfo();
});

document.getElementById('last').addEventListener('click', () => {
    currentPage = Math.ceil(totalItems / itemsPerPage);
    displayTableData();
    updateNavigationButtons();
    updatePageInfo();
});

// Função para atualizar os contadores de status
function updateStatusCounts() {
    fetch(endpointMural)
        .then(response => response.json())
        .then(data => {
            const statusContainer = document.getElementById('status-container');

            // Atualiza os contadores de status no elemento HTML
            statusContainer.querySelector('.box2 p').textContent = data['1'];
            statusContainer.querySelector('.box3 p').textContent = data['2'];
            statusContainer.querySelector('.box4 p').textContent = data['0'];
            statusContainer.querySelector('.box5 p').textContent = data['3'];
            statusContainer.querySelector('.box6 p').textContent = data['4'];
        })
        .catch(error => {
            console.error('Error fetching status counts:', error);
        });
}

// Ciclo das funções
updateStatusCounts();
setInterval(updateStatusCounts, 20000);
fetchTableData();
setInterval(fetchTableData, 20000);

// Recarrega a página depois de 20 minutos
setTimeout(function() {
    location.reload();
}, 1200000);