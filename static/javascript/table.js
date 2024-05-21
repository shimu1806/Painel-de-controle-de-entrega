let currentPage = 1
const itemsPerPage = 25
let totalItems = 0
let tableData = []

// colhe dados da endpoint
function fetchTableData() {
    fetch('/fetch_data/')
    .then(response => response.json())
    .then(data => {
        tableData = data
        totalItems = tableData.length
        displayTableData()             // constroi tabela
        updateNavigationButtons()      // constroi navegação
        updatePageInfo()               // auxilia navegação 'qtd de paginas'
    })
    .catch(error => console.error('Error:', error))
}


const tableHeaders = document.querySelectorAll('.table-head')
tableHeaders.forEach(header => {
  header.addEventListener('click', () => {
    const column = header.getAttribute('data-column')
    if (column) {
      tableData.sort((a, b) => a[column].localeCompare(b[column]))
      currentPage = 1
      displayTableData()
      updateNavigationButtons()
      updatePageInfo()
    }
  })
})


function displayTableData() {
    const tableBody = document.querySelector('.table-group-divider')
    tableBody.innerHTML = '' // Limpa a tabela
    const start = (currentPage - 1) * itemsPerPage
    const end = start + itemsPerPage
    const pageData = tableData.slice(start, end)

    pageData.forEach(item => {
        const row = document.createElement('tr')
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
        `
        tableBody.appendChild(row)
    })
}

function updateNavigationButtons() {
    document.getElementById('previous').disabled = currentPage === 1
    document.getElementById('next').disabled = currentPage === Math.ceil(totalItems / itemsPerPage)
    document.getElementById('first').disabled = currentPage === 1
    document.getElementById('last').disabled = currentPage === Math.ceil(totalItems / itemsPerPage)
}

function updatePageInfo() {
    const pageInfo          = document.getElementById('page-info')
    const totalPages        = Math.ceil(totalItems / itemsPerPage)
    pageInfo.textContent    = `Página ${currentPage} de ${totalPages}`
}

document.getElementById('previous').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--
        displayTableData()
        updateNavigationButtons()
        updatePageInfo()
    }
})

document.getElementById('next').addEventListener('click', () => {
    if (currentPage < Math.ceil(totalItems / itemsPerPage)) {
        currentPage++
        displayTableData()
        updateNavigationButtons()
        updatePageInfo()
    }
})

document.getElementById('first').addEventListener('click', () => {
    currentPage = 1
    displayTableData()
    updateNavigationButtons()
    updatePageInfo()
})

document.getElementById('last').addEventListener('click', () => {
    currentPage = Math.ceil(totalItems / itemsPerPage)
    displayTableData()
    updateNavigationButtons()
    updatePageInfo()
})
function updateStatusCounts() {
    fetch('/update_status_counts/')
        .then(response => response.json())
        .then(data => {
        const statusContainer = document.getElementById('status-container')
  
            // Update the status counts in the HTML element
            statusContainer.querySelector('.box2 p').textContent = data['1']
            statusContainer.querySelector('.box3 p').textContent = data['2']
            statusContainer.querySelector('.box4 p').textContent = data['0']
            statusContainer.querySelector('.box5 p').textContent = data['3']
            statusContainer.querySelector('.box6 p').textContent = data['4']
        })
    .catch(error => {
        console.error('Error fetching status counts:', error)
        })
    }
    
    // Ciclo das funções
    updateStatusCounts()
    setInterval(updateStatusCounts, 20000)
    fetchTableData()
    setInterval(fetchTableData, 20000)

    // Recarrega a página depois de 20 minutos
    setTimeout(function() {
        location.reload() 

    }, 1200000)