const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item => {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i => i.parentElement.classList.remove('active'));
		li.classList.add('active');
	});
});

const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
});

const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if (window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		searchButtonIcon.classList.toggle('bx-search');
		searchButtonIcon.classList.toggle('bx-x');
	}
});

if (window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if (window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}

window.addEventListener('resize', function () {
	if (this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
});

const switchMode = document.getElementById('switch-mode');
switchMode.addEventListener('change', function () {
	document.body.classList.toggle('dark', this.checked);
});

function toggleProfileDropdown() {
		const dropdown = document.getElementById("profileDropdown");
		dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
	}

	window.onclick = function (e) {
		if (!e.target.matches('.profile-img')) {
			const dropdown = document.getElementById("profileDropdown");
			if (dropdown && dropdown.style.display === "block") {
				dropdown.style.display = "none";
			}
		}
	}

function toggleNotification() {
    const panel = document.getElementById("notifPanel");
    panel.style.display = (panel.style.display === "block") ? "none" : "block";
  }

  // Close panel jika klik di luar area
  window.onclick = function (e) {
    if (!e.target.closest('.notification-dropdown')) {
      const panel = document.getElementById("notifPanel");
      if (panel && panel.style.display === "block") {
        panel.style.display = "none";
      }
    }
  }