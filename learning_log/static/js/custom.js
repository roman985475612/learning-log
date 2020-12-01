$(document).ready(function () {
    const editor = CKEDITOR.replaceAll()
    CKFINDER.setupCKEditor( editor )
  })


document.querySelectorAll('.nav-link').forEach(item => {
    if (item.href == location.href) {
        item.classList.add('active')
    }
})
 
const addTagModal = new bootstrap.Modal(document.getElementById('addTagModal'), {
    keyboard: false
})


document.querySelector('#addTagBtn').addEventListener('click', event => {
    event.preventDefault()
    event.stopPropagation()
    
    addTagModal.show()
})

document.querySelector('#addTagActionBtn').addEventListener('click', event => {
    event.preventDefault()
    event.stopPropagation()
      
    addTagModal.hide()

    let formData = new FormData(document.getElementById('addTagForm'))
    let data = {}
    formData.forEach((value, key) => data[key] = value)
    
    fetch(location.origin + '/api-tag/tags/',
    {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json() )
    .then(data => { console.log( JSON.stringify( data ) ) })

    changeTagList(data)
})


function changeTagList(data) {
    const select = document.querySelector('#id_tag')
    select.insertAdjacentHTML('afterbegin', `<option value="${data.color}">${data.title}</option>`) 
}

const generateListColors = colors => {

    let select = document.querySelector('.modal-body .form-select')

    colors.forEach(item => {
        select.insertAdjacentHTML('beforeend', `<option value="${item.key}">${item.value}</option>`)
    })
}

const colors = [
    {key: "primary", value: "Blue"},
    {key: "secondary", value: "Gray"},
    {key: "success", value: "Green"},
    {key: "info", value: "Cyan"},
    {key: "warning", value: "Yellow"},
    {key: "danger", value: "Red"},
    {key: "light", value: "White"},
    {key: "dark", value: "Black"},
]

generateListColors(colors)

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}