/**
 document.addEventListener("DOMContentLoaded", () =>{
    document.querySelectorAll("button").forEach(function(button){
        button.onclick = () =>{
            document.querySelector('h1').style.color = button.dataset.color;

        }

    });
        
    }
)
**/

document.addEventListener("DOMContentLoaded", () =>{
    document.querySelector('select').onchange = function(){
        console.log(this)
        document.querySelector('h1').style.color = this.value;
    };
});