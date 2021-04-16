let counter = 1;

//load 10 posts at a time
const quantity = 10;

//When DOM is loaded
document.addEventListener("DOMContentLoaded", load())


//When reaching the end of the window/or bottom, load next posts
window.onscroll = () => 
{
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight)
    {
        load();
        return false;
    }
}

//Load next set of posts
function load()
{
    //set start and end numbers, update counter
   
    const start = counter;
    const end = start + quantity - 1
    counter = end + 1;
    console.log(start)
    console.log(end)

    //Fetch new posts and add it
    fetch(`/post?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data=>{
        data.posts.forEach(add_post)
    })

}

function add_post(contents)
{
    const post = document.createElement('div');
    post.innerHTML = contents;
    post.className = 'post'
    document.querySelector('#posts').append(post)
}