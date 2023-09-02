const logo = document.querySelector('.logo');
const body = document.body;

if (logo) {
    logo.addEventListener('click', changeTheme);
}
console.log('algo')
if (localStorage.getItem('mode')) changeTheme();

function changeTheme() {
    body.classList.toggle('lightmode');
    if (body.classList.contains('lightmode')) localStorage.setItem('mode', 'lightmode');
    else localStorage.removeItem('mode');
}