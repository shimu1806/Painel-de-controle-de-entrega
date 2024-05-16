function updateStatusCounts() {
  fetch('http://127.0.0.1:8000/update_status_counts/')
      .then(response => response.json())
      .then(data => {
      const statusContainer = document.getElementById('status-container');

          // Update the status counts in the HTML element
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

  // Call the function to update the status counts
  updateStatusCounts();
  // setInterval(updateStatusCounts, 5000);