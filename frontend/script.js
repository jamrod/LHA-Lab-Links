const form = document.querySelector('#form')
const cwinput = document.querySelector('#codeword')
const url = "https://k7mdz0megh.execute-api.us-west-2.amazonaws.com/prod"
const results =document.querySelector('#results')

form.addEventListener("submit", sendSyncRequest)

function validatePwd(t){
    let valid = /^[^{}\[\]\(\)\*\&\^%\$\s]+$/
    return t.match(valid)
}

function showResults(response) {
    if (response.errorMessage){
        results.textContent = response["errorMessage"]
    } else {
        results.textContent = response["body"]
    }
}

function sendSyncRequest (){
    let codeword = cwinput.value
    results.textContent = ""
    if (validatePwd(codeword)){
        cwinput.value = ""
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(`${codeword}`)
        })
        .then(res => res.json())
        .then(data => showResults(data))
        .catch(err => showResults(err))
    } else {
        cwinput.value = ""
        results.textContent = "Invalid input, try again"
    }
}