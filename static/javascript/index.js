// Assumindo que você está usando jQuery e um banco de dados MySQL
const tableName = "http://suntechsupplies170773.protheus.cloudtotvs.com.br:1907/rest/restqry";

$.ajax({
  url: "http://suntechsupplies170773.protheus.cloudtotvs.com.br:1907/rest/restqry",
  method: "POST",
  data: {
    query: `SELECT COUNT(*) AS total FROM ${tableName}`
  },
  success: function(response) {
    const totalData = response.total;

    // O restante do código para a paginação...
  }
});

// Defina a quantidade de resultados por página
const resultsPerPage = 15;

// Função para atualizar a tabela com os dados da página selecionada
function updateTable(page) {
  // Calcule o índice inicial e final dos dados a serem exibidos
  const startIndex = (page - 1) * resultsPerPage;
  const endIndex = startIndex + resultsPerPage;

  // Obtenha os dados da página selecionada
  $.ajax({
    url: "http://suntechsupplies170773.protheus.cloudtotvs.com.br:1907/rest/restqry",
    method: "POST",
    data: {
      query: `SELECT * FROM ${tableName} LIMIT ${startIndex}, ${resultsPerPage}`
    },
    success: function(response) {
      // Atualize a tabela com os dados recebidos
      const tableBody = document.querySelector('table tbody');
      tableBody.innerHTML = '';
      response.forEach(row => {
        const tr = document.createElement('tr');
        // Crie as células da linha com os dados da linha
        //...
        tableBody.appendChild(tr);
      });
    }
  });
}

// Chame a função updateTable para carregar os dados da primeira página
updateTable(1);