document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(reply_info) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#messages').style.display = 'none';

  const compose_recipients = document.querySelector('#compose-recipients')
  const compose_subject = document.querySelector('#compose-subject')
  const compose_body = document.querySelector('#compose-body')

  // Clear out composition fields
  compose_recipients.value = '';
  compose_subject.value = '';
  compose_body.value = '';
  document.querySelector('#compose-form').addEventListener('submit', send);

  //if replying
  if(reply_info!=null)
  {
    compose_recipients.value = reply_info['sender'];
    compose_recipients.disabled = true;
    
    //To check if the email is already a "replied" email (ie, it has "Re:" in its subject)
    if (reply_info['subject'].split(' ')[0] != "Re:")
    {
      //add the "Re:"
      compose_subject.value = `Re: ${reply_info['subject']}`
    }
    else
    {
      //leave it as it is
      compose_subject.value = reply_info['subject']
    }

    compose_body.value = `On ${reply_info['timestamp']} ${reply_info['sender']} wrote: ${reply_info['body']}`

  }

  
}

function load_mailbox(mailbox, event_message) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  //if an event_message was not passed, clear the message
  if(!event_message)
  {  
    document.querySelector('#messages').style.display = 'none';
    document.querySelector('#messages').className = ''
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  //Fetch the emails from a given mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => 
    {

      for(let i = 0; i < emails.length; i++)
      {
        //to mark an email as read/unread
        let read_or_unread = ''
        emails[i].read == true ? read_or_unread = 'Mark as Unread' : read_or_unread = 'Mark as Read';
        
        let email = document.createElement('div')
        email.innerHTML = `<div class = "email" id = "email_${emails[i].id}">
                          <div class = "email_clickable" id = "email_clickable_${emails[i].id}">
                            <div class = "sender"><b>From: </b>${emails[i].sender}</div>
                            <div class = "recipient"><b>To: </b>${emails[i].recipients[0]}</div>
                            <div class = "subject"><b>Subject: </b>${emails[i].subject} </div>
                            <div class = "timestamp"><b>Timestamp: </b>${emails[i].timestamp}</div>
                          </div>
                          <div class = "read" id = "read_${emails[i].id}">Read ✓</div>
                          <div class = "markread"><button class = "btn btn-sm btn-outline-primary" id = "markreadbutton_${emails[i].id}">${read_or_unread}</button></div>
                          </div>`

        document.querySelector('#emails-view').innerHTML+= email.innerHTML
      }

      //shows the recipient instead of the sender if in the sent mailbox
      //also removes the mark read button and the read icon
      if (mailbox=='sent')
      {
        document.querySelectorAll('.sender').forEach((sender)=>{
            sender.style.display = 'none'
        });
        document.querySelectorAll('.read').forEach((read)=>{
          read.style.display = 'none'
        });
        document.querySelectorAll('.markread').forEach((markread)=>{
          markread.style.display = 'none'
        });
      }

      else
      {
        document.querySelectorAll('.recipient').forEach((recipient)=>{
          recipient.style.display = 'none'
      })
      }

      //to add the event listeners for the email and mark read/unread button
      for (let i = 0; i<emails.length; i++)
      {
        document.querySelector(`#read_${emails[i].id}`).style.display = "none"

        //if not read, don't display read icon
        if(emails[i].read && mailbox!='sent')
        {
          document.querySelector(`#read_${emails[i].id}`).style.display = "block"
          document.querySelector(`#email_${emails[i].id}`).style.backgroundColor = "rgb(250, 250, 250)";
        }
        document.querySelector(`#markreadbutton_${emails[i].id}`).addEventListener('click', () => mark_email(emails[i]))
        document.querySelector(`#email_clickable_${emails[i].id}`).addEventListener('click', () => openEmail(emails[i].id, mailbox));
      }

    });

}

// Function to send email
function send(event)
{
  const recipients = String(document.querySelector('#compose-recipients').value);
  const subject = String(document.querySelector('#compose-subject').value);
  const body =  String(document.querySelector('#compose-body').value);
  const messages = document.querySelector('#messages');

  //to check if recipient form is empty
  if (recipients != '')
  {
    //if more than one recipient, it should be split by a comma(,) else the recipient_validate function will return false
    const recipients_arr = recipients.split(', ')

    //flag to check if recipient is valid; initialized as true
    let result = true
    
    //validate each recipient (if more than one via commas)
    for (let i = 0; i < recipients_arr.length; i++)
    {
      result = recipient_validate(recipients_arr[i])
    }

    //if any recipient is invalid
    if (result == false)
     {
      messages.style.display = "block"
      messages.classList.add('alert', 'alert-danger')
      messages.innerHTML = "Recipient email(s) invalid; Make sure to add commas if more than one recipient"

      event.preventDefault();
      return false;
    }

    else
    {
      for (let i = 0; i<recipients_arr.length; i++)
      {  
        event.preventDefault();
        fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
              recipients: recipients_arr[i],
              subject: subject,
              body: body
          })
        })
        .then(response => response.json())
        .then(() => {

            messages.style.display = "block"
            messages.classList.add('alert', 'alert-success')
            messages.innerHTML = "Successfully sent"
            event.preventDefault();
            load_mailbox('sent', true)
            return false;
            
        })
      }
    }
  }
  else
  {
    messages.style.display = "block"
    messages.classList.add('alert', 'alert-danger')
    messages.innerHTML = "Recipient form cannot be left empty"
    event.preventDefault();
    return false;
  }
}

// Regex to validate the email address of the recipient(s) taken from https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
function recipient_validate(recipient)
{
  const valid_email = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return valid_email.test(recipient)
}

//to fetch and display a particular email's information
function openEmail(email_id, mailbox)
{
  //Marks the email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  

  //Fetches all the information of the email
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email =>{
    //to check if the opened email is archived or unarchived
    let archive_or_unarchived = ''
    email.archived == true ? archive_or_unarchived = 'Unarchive' : archive_or_unarchived = 'Archive';
    
    

    let detailed_email = document.createElement('div')
    detailed_email.innerHTML = `<div class = "detailed_email">
                                  <div class = "sender"><b>From: </b>${email.sender}</div>
                                  <div class = "recipient"><b>To: </b>${email.recipients}</div>
                                  <div class = "subject"><b>Subject: </b>${email.subject}</div>
                                  <div class = "timestamp"><b>Timestamp: </b>${email.timestamp}</div>
                                  <button class = "btn btn-sm btn-outline-primary reply">Reply</button>
                                  <button class = "btn btn-sm btn-outline-primary archive">${archive_or_unarchived}</button>
                                  <hr>
                                  <p class = "body">${email.body}</p>
                                </div>`
    document.querySelector('#emails-view').innerHTML = detailed_email.innerHTML
    document.querySelector('.archive').addEventListener('click', () => archive_email(email))

    //by default don't show all the buttons
    document.querySelector('.reply').style.display = "none"
    document.querySelector('.archive').style.display = "none"
    
    
    //Only emails not sent by the current user shall have the reply button
    if(mailbox=='inbox')
    {
      document.querySelector('.reply').style.display = "inline-block";
      const reply_info = {
        sender:email.sender, 
        subject:email.subject,
        body:email.body,
        timestamp:email.timestamp
      }
      document.querySelector('.reply').addEventListener('click', () => compose_email(reply_info));
    }
    
    //Likewise, albeit emails from both archived and inbox display all buttons
    if (mailbox!='sent')
    {
      document.querySelector('.archive').style.display = "inline-block";
    }
  })

}

//to archive an email
function archive_email(email)
{
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  })
  .then(()=>{
    if(email.archived==true)
    {
      messages.style.display = "block"
      messages.classList.add('alert', 'alert-primary')
      messages.innerHTML = "Email has been unarchived"
      load_mailbox('inbox', true)
    }
    else
    {
      messages.style.display = "block"
      messages.classList.add('alert', 'alert-primary')
      messages.innerHTML = "Email has been archived"
      load_mailbox('inbox', true)
    }
  })
  
}

//to mark an email as read/unread
function mark_email(email)
{
  console.log(email.id)
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: !email.read
    })
  })
  .then(()=>{
    if(email.read==true)
    {
      messages.style.display = "block"
      messages.classList.add('alert', 'alert-primary')
      messages.innerHTML = "Email has been marked as unread"
      load_mailbox('inbox', true)
    }
    else
    {
      messages.style.display = "block"
      messages.classList.add('alert', 'alert-primary')
      messages.innerHTML = "Email has been marked as read"
      load_mailbox('inbox', true)
    }
  })
  
}