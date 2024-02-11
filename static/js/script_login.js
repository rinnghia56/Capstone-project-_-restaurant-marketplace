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

function checkFileUpload() {
    var fileInput = document.getElementById('file__input');
    var file_upload = document.querySelector('.file-upload');
  
    if (fileInput.files.length > 0) {
      // Người dùng đã chọn tệp để tải lên
      file_upload.style.backgroundColor = '#1da1f2a1'
       file_upload.textContent =  fileInput.files[0].name
    }
  }