function fetchTableData() {
    fetch('http://127.0.0.1:8000/fetch_data/')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('.table-group-divider')
        data.forEach(item => {
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
            tableBody.appendChild(row);
                })
            })
        .catch(error => console.error('Error:', error))
    }

fetchTableData();
setInterval(fetchTableData, 10000)