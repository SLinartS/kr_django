'use scrict';

input = document.querySelector('.load__input');
button = document.querySelector('.load__button');

input.addEventListener('input', () => {
	if (input.value) {
		button.disabled = false;
    button.classList.add('load__button--active');
	} else {
		button.disabled = true;
    button.classList.remove('load__button--active');
	}
});
