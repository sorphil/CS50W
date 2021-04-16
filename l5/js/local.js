if(!localStorage.getItem('counter'))
{
    localStorage.setItem('counter', 0);
}

function count()
{
    let value = localStorage.getItem('counter')
    value++;
    document.querySelector('h1').innerHTML = value;
    localStorage.setItem('counter', value);
}

document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelector('h1').innerHTML = localStorage.getItem('counter')
    document.querySelector('#button').onclick = count;
})