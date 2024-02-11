
// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})

const toast = document.querySelector('.toast')
const close = document.querySelector('.close-error')
const error_list = document.querySelector('.error-list')

if(close) {
close.addEventListener('click',function() {
    error_list.remove();
})}

setTimeout(function() {
    if (toast) {
     toast.remove();
    }
}, 3000)