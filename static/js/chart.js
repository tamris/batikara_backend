// Login Chart - Bulanan
const loginCtx = document.getElementById('loginChart').getContext('2d');
new Chart(loginCtx, {
	type: 'bar',
	data: {
		labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
		datasets: [{
			label: 'User Login',
			data: [120, 98, 135, 150, 123, 140, 160, 148, 130, 145, 138, 110],
			backgroundColor: '#3C91E6',
			borderRadius: 6,
			barThickness: 28,
		}]
	},
	options: {
		responsive: true,
		scales: {
			y: {
				beginAtZero: true,
				suggestedMax: 200,
				ticks: { stepSize: 50 }
			}
		},
		plugins: {
			legend: { display: false }
		}
	}
});

// Gender Chart - Pie
document.addEventListener("DOMContentLoaded", function () {
  const genderCanvas = document.getElementById('genderChart');
  if (genderCanvas) {
    fetch('/gender-data')
      .then(res => res.json())
      .then(data => {
        new Chart(genderCanvas.getContext('2d'), {
          type: 'doughnut',
          data: {
            labels: data.labels,
            datasets: [{
              data: data.data,
              backgroundColor: ['#3C91E6', '#FD7238'],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'bottom' }
            }
          }
        });
      })
      .catch(err => console.error('Gagal ambil data gender:', err));
  }
});

