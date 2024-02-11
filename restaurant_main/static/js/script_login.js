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


function checkFileUpload(id_elemnt){
    document.getElementById(id_elemnt).addEventListener('change', function(){
        if (this.files.length > 0) {
            file_upload = document.querySelector('.file-upload');
            file_upload.style.backgroundColor = '#1da1f2a1'
            file_upload.textContent =  this.files[0].name
          }
    })
}

checkFileUpload('file__input')