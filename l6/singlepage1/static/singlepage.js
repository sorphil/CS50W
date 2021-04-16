
function showSection(section)
{
    fetch(`/section/${section}`)
    .then(response => response.text())
    .then(text=>{
        document.querySelector("#result").innerHTML = text;
    })
}

window.onpopstate = function(event){
    // From the pushState first parameter ie ({section: section})
    console.log(event.state.section)
    showSection(event.state.section)
}

document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('button').forEach(button =>{
        button.onclick = function(){
            const section = this.dataset.section
            history.pushState({section:section}, "", `section${section}`)
            showSection(section)
        }
    })
})