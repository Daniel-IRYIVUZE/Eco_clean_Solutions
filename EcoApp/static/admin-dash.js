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
            statusCell.style.color = "green";
            break;
        case "Pending":
            statusCell.style.color = "yellow";
            break;
        case "Declined":
            statusCell.style.color = "red";
            break;
        default:
            statusCell.style.backgroundColor = "";
            statusCell.style.color = "black";
            break;
    }
}
