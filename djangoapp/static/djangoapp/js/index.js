'use scrict';

input = document.querySelector('.load__input');
button = document.querySelector('.load__button');

filezone = document.querySelector('.file-zone__file-list');

input.addEventListener('input', () => {
	if (input.value) {
		button.disabled = false;
		button.classList.add('load__button--active');
	} else {
		button.disabled = true;
		button.classList.remove('load__button--active');
	}

	if (input.files.length > 0 && filezone) {
		[...input.files].forEach((element, index) => {
			const newFileTag = document.createElement('p');
			newFileTag.textContent = `${index + 1}. ${element.name}`;
			newFileTag.classList.add('file-zone__file');
			filezone.appendChild(newFileTag);
		});
	}
});
