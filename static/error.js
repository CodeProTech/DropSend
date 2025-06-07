const troubleshootHeader = document.getElementById('troubleshootHeader');
const troubleshootContent = document.getElementById('troubleshootContent');
const chevronIcon = document.getElementById('chevronIcon');

troubleshootHeader.addEventListener('click', () => {
    troubleshootContent.classList.toggle('active');
    chevronIcon.classList.toggle('active');
});