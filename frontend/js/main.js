function getData(event) {
    event.preventDefault();
    let ip = document.getElementById("ip-input").value;
    if (!ip) {
        window.alert("O campo de entrada de IP está vazio. Por favor, insira um endereço IP válido.");
        return;
    }
    fetchData(ip);
}

function fetchData(ip) {
    data = [];
    let tableBody = document.getElementById('data-body');
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
      }

    fetch(`http://localhost:8000/${ip}/users`)
      .then(response => response.json())
      .then(data => {
        console.log(data);

        // Limpa a tabela antes de adicionar novos conteúdos

        if (data["detail"]["status"] === "nok") {
            // Exibe uma mensagem de erro em vez de adicionar a tabela
            let message = data["detail"]["message"];
            window.alert(`Erro: ${message}`);
        } else {
            // E aqui você pode usar os dados para preencher a tabela
            data["detail"]["users"].forEach(item => {
              let row = document.createElement('tr');
              row.innerHTML = `
                <td>${item.username}</td>
                <td>${item.uid}</td>
                <td>${item.comment}</td>
                <td>${item.locked}</td>
              `;
              tableBody.appendChild(row);
            });
        }
      })
      .catch(error => {
        console.error(error);
        window.alert("Não foi possível obter dados do backend.");
        });
}