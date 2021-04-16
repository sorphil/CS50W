document.addEventListener("DOMContentLoaded", ()=>{
    const submit = document.querySelector('#submit')
    const task = document.querySelector('#task');
    submit.disabled = true;
    
    task.onkeyup = () =>{
        
        if (task.value != "")
        {
            submit.disabled = false;
        }
        else
        {
            submit.disabled = true;
        }
    };


    document.querySelector('#tasks').onsubmit = ()=>
    {
        const li = document.createElement('li');
        li.innerHTML = task.value;
        document.querySelector('#tasks').append(li);
        task.value = ""
       
        return false;
    }
});