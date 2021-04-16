

document.addEventListener('DOMContentLoaded', function()
{   
    let name = document.querySelector('#name')
    let submit = document.querySelector('#submit')
    submit.disabled = true;

    name.onkeyup = () =>
    {
        if(name.value !="")
        {
            submit.disabled = false;
        }
        else
        {
            submit.disabled = true;
        }
    }



    document.querySelector('form').onsubmit = function()
    {
        
        const heading = document.querySelector('h1')
        let head = heading.innerHTML.split(" ");
        let headname = head[1];
        nameValue = name.value
        nameValue = nameValue.charAt(0).toUpperCase() + nameValue.slice(1).toLowerCase()
        let str = heading.innerHTML;
        let words = str.split(" ");
        if(headname != undefined)
            {
                if(words[0] === "Hello" && headname === nameValue)
                {
                    heading.innerHTML = `Goodbye ${headname}`;
                    
                    document.querySelector("#name").value = "";
                }
                else if(words[0] === "Hello" && headname != nameValue)
                {
                    heading.innerHTML = `Hello ${nameValue}`;
                    
                    document.querySelector("#name").value = "";
                }
                else if(words[0] === "Goodbye" && headname === nameValue)
                {
                    heading.innerHTML = `Hello ${headname}`;
                    
                    document.querySelector("#name").value = "";
                   
                }
            }
        else
        {
            heading.innerHTML = `Hello ${nameValue}`;
            document.querySelector("#name").value = "";
            submit.disabled = true;
        }
        return false;
    };
} );