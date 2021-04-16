document.addEventListener("DOMContentLoaded", () =>{

    document.querySelector('form').onsubmit = () => {
        //to get httpresponse from some page
        fetch('https://api.exchangeratesapi.io/latest?base=USD')
        .then(response => response.json())
        .then(data =>{
            console.log(data)
            let currency = document.querySelector('#currency').value.toUpperCase();
            let rate = data.rates[currency];
            if (rate !== undefined)
            {
                document.querySelector('#result').innerHTML = `1 USD is equal to ${rate.toFixed(3)} ${currency}`;
            }
            else
            {
                document.querySelector('#result').innerHTML = 'Invalid currency'
            }
            
        })
        .catch(error => {
            console.log('Error:', error)
            });
            
        return false;
    } 
});