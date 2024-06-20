// add hovered class to selected list item
let list = document.querySelectorAll('.navigation li');

function activeLink() {
  list.forEach((item) => {
    item.classList.remove('hovered');
  });
  this.classList.add('hovered');
}

list.forEach((item) => item.addEventListener('mouseover', activeLink));

// Menu Toggle
let toggle = document.querySelector('.toggle');
let navigation = document.querySelector('.navigation');
let main = document.querySelector('.main');

toggle.onclick = function () {
  navigation.classList.toggle('active');
  main.classList.toggle('active');
};

document.addEventListener('DOMContentLoaded', () => {
  const counters = document.querySelectorAll('.counter');
  counters.forEach((counter) => {
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

  // Retrieve orderId from data attribute
  const orderId = selectElement.parentElement.dataset.orderId;

  statusCell.textContent = statusValue;

  switch (statusValue) {
    case 'Completed':
      statusCell.style.color = 'green';
      break;
    case 'Pending':
      statusCell.style.color = 'orange';
      break;
    case 'Declined':
      statusCell.style.color = 'red';
      break;
    default:
      statusCell.style.backgroundColor = '';
      statusCell.style.color = 'black';
      break;
  }

  fetch(`/update-order-status/${orderId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: statusValue }),
  })
    .then((response) => {
      if (response.ok) {
        console.log('Status updated successfully.');
        // Optionally handle any UI or additional logic upon successful update
      } else {
        console.log('Failed to update status.');
        // Handle error or retry logic if needed
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Error updating status.');
    });
}
