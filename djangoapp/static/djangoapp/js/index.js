'use scrict';

input = document.querySelector('.load__input');
button = document.querySelector('.load__button');

input.addEventListener('input', () => {
	if (input.value) {
		button.disabled = false;
	} else {
		button.disabled = true;
	}
});
