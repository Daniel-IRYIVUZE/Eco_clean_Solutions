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

document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        counter.innerText = '0';

        const updateCounter = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;

            const increment = target / 200; // Adjust this value for speed

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCounter, 10);
            } else {
                counter.innerText = target;
            }
        };

        updateCounter();
    });
});
function updateStatus(selectElement) {
    const statusCell = selectElement.parentElement.previousElementSibling;
    const statusValue = selectElement.value;

    statusCell.textContent = statusValue;

    switch(statusValue) {
        case "Completed":
            statusCell.style.backgroundColor = "green";
            statusCell.style.color = "white";
            break;
        case "Pending":
            statusCell.style.backgroundColor = "yellow";
            statusCell.style.color = "black";
            break;
        case "Declined":
            statusCell.style.backgroundColor = "red";
            statusCell.style.color = "white";
            break;
        default:
            statusCell.style.backgroundColor = "";
            statusCell.style.color = "black";
            break;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const districtSelect = document.getElementById('district');
    const sectorSelect = document.getElementById('sector');
    const cellSelect = document.getElementById('cell');
    const villageSelect = document.getElementById('village');

    const sectors = {
      Gasabo: ['Sector1', 'Sector2'],
      Kicukiro: ['Sector3', 'Sector4'],
      Nyarugenge: ['Sector5', 'Sector6'],
      Muhanga: ['Sector7', 'Sector8']
      // Add more sectors as needed
    };

    const cells = {
      Sector1: ['Cell1', 'Cell2'],
      Sector2: ['Cell3', 'Cell4'],
      Sector3: ['Cell5', 'Cell6'],
      Sector4: ['Cell7', 'Cell8'],
      Sector5: ['Cell9', 'Cell10'],
      Sector6: ['Cell11', 'Cell12'],
      Sector7: ['Cell13', 'Cell14'],
      Sector8: ['Cell15', 'Cell16']
      // Add more cells as needed
    };

    const villages = {
      Cell1: ['Village1', 'Village2'],
      Cell2: ['Village3', 'Village4'],
      Cell3: ['Village5', 'Village6'],
      Cell4: ['Village7', 'Village8'],
      Cell5: ['Village9', 'Village10'],
      Cell6: ['Village11', 'Village12'],
      Cell7: ['Village13', 'Village14'],
      Cell8: ['Village15', 'Village16'],
      Cell9: ['Village17', 'Village18'],
      Cell10: ['Village19', 'Village20'],
      Cell11: ['Village21', 'Village22'],
      Cell12: ['Village23', 'Village24'],
      Cell13: ['Village25', 'Village26'],
      Cell14: ['Village27', 'Village28'],
      Cell15: ['Village29', 'Village30'],
      Cell16: ['Village31', 'Village32']
      // Add more villages as needed
    };

    districtSelect.addEventListener('change', function() {
      const selectedDistrict = this.value;
      sectorSelect.innerHTML = '<option value="">Select Sector</option>';
      cellSelect.innerHTML = '<option value="">Select Cell</option>';
      villageSelect.innerHTML = '<option value="">Select Village</option>';
      
      if (selectedDistrict && sectors[selectedDistrict]) {
        sectors[selectedDistrict].forEach(function(sector) {
          const option = document.createElement('option');
          option.value = sector;
          option.textContent = sector;
          sectorSelect.appendChild(option);
        });
      }
    });

    sectorSelect.addEventListener('change', function() {
      const selectedSector = this.value;
      cellSelect.innerHTML = '<option value="">Select Cell</option>';
      villageSelect.innerHTML = '<option value="">Select Village</option>';

      if (selectedSector && cells[selectedSector]) {
        cells[selectedSector].forEach(function(cell) {
          const option = document.createElement('option');
          option.value = cell;
          option.textContent = cell;
          cellSelect.appendChild(option);
        });
      }
    });

    cellSelect.addEventListener('change', function() {
      const selectedCell = this.value;
      villageSelect.innerHTML = '<option value="">Select Village</option>';

      if (selectedCell && villages[selectedCell]) {
        villages[selectedCell].forEach(function(village) {
          const option = document.createElement('option');
          option.value = village;
          option.textContent = village;
          villageSelect.appendChild(option);
        });
      }
    });

    document.getElementById('registrationForm').addEventListener('submit', function(event) {
      event.preventDefault();

      let isValid = true;

      // Clear previous errors
      document.querySelectorAll('.error').forEach(function(element) {
        element.textContent = '';
      });

      // Validate Registration ID
      const registrationId = document.getElementById('registrationId').value.trim();
      if (registrationId === '') {
        document.getElementById('registrationIdError').textContent = 'Registration ID is required.';
        isValid = false;
      }

      // Validate Company Name
      const companyName = document.getElementById('companyName').value.trim();
      if (companyName === '') {
        document.getElementById('companyNameError').textContent = 'Company Name is required.';
        isValid = false;
      }

      // Validate CEO
      const ceo = document.getElementById('ceo').value.trim();
      if (ceo === '') {
        document.getElementById('ceoError').textContent = 'CEO is required.';
        isValid = false;
      }

      // Validate District
      const district = document.getElementById('district').value.trim();
      if (district === '') {
        document.getElementById('districtError').textContent = 'District is required.';
        isValid = false;
      }

      // Validate Sector
      const sector = document.getElementById('sector').value.trim();
      if (sector === '') {
        document.getElementById('sectorError').textContent = 'Sector is required.';
        isValid = false;
      }

      // Validate Cell
      const cell = document.getElementById('cell').value.trim();
      if (cell === '') {
        document.getElementById('cellError').textContent = 'Cell is required.';
        isValid = false;
      }

      // Validate Village
      const village = document.getElementById('village').value.trim();
      if (village === '') {
        document.getElementById('villageError').textContent = 'Village is required.';
        isValid = false;
      }

      // Validate Email
      const email = document.getElementById('email').value.trim();
      if (email === '') {
        document.getElementById('emailError').textContent = 'Email is required.';
        isValid = false;
      } else if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        document.getElementById('emailError').textContent = 'Invalid email format.';
        isValid = false;
      }

      // Validate Phone Number
      const countryCode = document.getElementById('countryCode').value;
      const phoneNumber = document.getElementById('phoneNumber').value.trim();
      if (phoneNumber === '') {
        document.getElementById('phoneNumberError').textContent = 'Phone Number is required.';
        isValid = false;
      } else if (!phoneNumber.match(/^[0-9]{9}$/)) {
        document.getElementById('phoneNumberError').textContent = 'Phone number must be 9 digits.';
        isValid = false;
      }

      if (isValid) {
        // Submit the form
        const fullPhoneNumber = countryCode + phoneNumber;
        alert(`Company registered successfully! Phone number: ${fullPhoneNumber}`);
        document.getElementById('registrationForm').reset();
      }
    });
  });
