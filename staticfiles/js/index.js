
const chatBtn = document.getElementById('chatBtn');
const chatModal = document.getElementById('chatModal');
const closeBtn = document.getElementById('closeBtn');

chatBtn.addEventListener('click', () => {
  chatModal.classList.toggle('translate-x-full');
});

closeBtn.addEventListener('click', () => {
  chatModal.classList.add('translate-x-full');
});


