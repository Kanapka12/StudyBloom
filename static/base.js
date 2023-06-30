function getBrightness(color) {
  const r = parseInt(color.slice(1, 3), 16);
  const g = parseInt(color.slice(3, 5), 16);
  const b = parseInt(color.slice(5, 7), 16);

  return (r * 299 + g * 587 + b * 114) / 1000;
}

function getTextColor(backgroundColor) {
  return getBrightness(backgroundColor) > 128 ? '#000' : '#fff';
}

function adjustTextColor() {
  const backgroundColor = document.body.getAttribute('data-user-background-color');
  document.documentElement.style.setProperty('--background-color', backgroundColor);
  const textColor = getTextColor(backgroundColor);
  document.documentElement.style.setProperty('--text-color', textColor);
}

document.addEventListener('DOMContentLoaded', adjustTextColor);
