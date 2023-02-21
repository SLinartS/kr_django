'use scrict';

const label = document.querySelector('.load__label');
const input = document.querySelector('.load__input');
const button = document.querySelector('.load__button');

const teachersList = document.querySelectorAll('.menu__list-elem');

const filezone = document.querySelector('.file-zone__file-list');

if (input.dataset.isDisabled === 'True') {
  label.classList.remove('load__button--active');
  label.setAttribute('style', 'pointer-events: none');
}

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
