// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

document.getElementById('viewAllBtn').addEventListener('click', function(event) {
    event.preventDefault();
    var table = document.getElementById('orderTable');
    if (table.style.display === 'none' || table.style.display === '') {
        table.style.display = 'table';
        this.textContent = 'Hide';
    } else {
        table.style.display = 'none';
        this.textContent = 'View';
    }
});

document.querySelectorAll('.action-dropdown').forEach(function(dropdown) {
    dropdown.addEventListener('change', function() {
        var selectedValue = this.value;
        var statusSpan = this.closest('tr').querySelector('.status');
        statusSpan.className = 'status ' + selectedValue;
        statusSpan.textContent = selectedValue.charAt(0).toUpperCase() + selectedValue.slice(1);
    });
});