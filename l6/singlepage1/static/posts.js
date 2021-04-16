//Start with first post
let counter = 1;

//load 4 posts at a time
const quantity = 4;

//When dom content is loaded, render first 20 posts
document.addEventListener('DOMContentLoaded', load)

function load()
{
    //Set start and end post numbers, update counter
    const start = counter;
    const end = start+quantity - 1;
    counter = end+1;


    //get new posts and add posts
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json)
    .then(data =>{
        console.log(data.posts)
        data.posts.forEach(add_post)
    })
}

function add_post(contents)
{
    //Create new post
    const post = document.createElement('div');
    post.className = 'post'
    post.innerHTML = contents

    //Add post to DOM
    document.querySelector('#posts').append(post)
}