document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  // 화면에 Inbox, Sent  큰 글자로 보여주는것
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox == 'show_mail') {
    show_mail()
    return;
  }


  // Now fetch the json to see mails I have
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then((emails) => {
    emails.forEach((element) => {

      if (mailbox == 'sent') {
        sender_recipients = element.recipients;
      } else {
        sender_recipients = element.sender;
      }

      if (mailbox == 'inbox') {
        if (element.read) is_read = 'read';
        else is_read = '';
      } else {
        is_read = '';
      }

      // Now, make a variable to display the mails I have in the mailbox I select
      var item = document.createElement('div');
      item.className = `card   ${is_read} my-1 items`;
      item.innerHTML = `<div class="card-body" id="item-${element.id}">
      ${element.subject} | ${sender_recipients} | ${element.timestamp}
      <br>
      ${element.body.slice(0, 100)}
      </div>`;

      document.querySelector('#emails-view').appendChild(item);
      item.addEventListener('click', () => {
        show_mail(element.id, mailbox);
      });
    });
  });
}


function show_mail(id, mailbox) {
  fetch(`/emails/${id}`)
  .then((response) => response.json())
  .then((email) => {
    // Before we display the contents of a mail, let's erase previous display like when we click inbox
    document.querySelector('#emails-view').innerHTML = "";
    // Now, make a variable to display the contents of a mail
    var item = document.createElement("div");
    item.className = `card`;
    item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
    Sender: ${email.sender}
    Recipients: ${email.recipients}
    Subject: ${email.subject}
    Time: ${email.timestamp}
    <br>
    ${email.body}
    </div>`;
    document.querySelector('#emails-view').appendChild(item);
    // 만약 선택한 mail이 sent에 해당하는 것이었다면 따로 archive나 reply 버튼이 필요없기때문에 바로 return;으로 function을 끝내버림.
    if (mailbox == "sent") return;
    // sent가 아닐시 archive와 reply 버튼을 생성해줌
    let archive = document.createElement("btn");
    archive.className = `btn btn-outline-info my-2`;
    // When you click archive button
    archive.addEventListener('click', () => {
      // use toggle archive function to change the state of archive(True or False) when you click it
      toggle_archive(id, email.archived);
      if (archive.innerText == 'Archive') archive.innerText = 'Unarchive';
      else archive.innerText = 'Archive';
    });

    // 왜 필요함 ??? 위에 꺼랑 둘중에 하나는 필요없어보임 ???
    if (email.archived) archive.textContent = 'Unarchive';
    else archive.textContent = 'Archive';
    document.querySelector('#emails-view').appendChild(archive);

    let reply = document.createElement('btn');
    reply.className = `btn btn-outline-success m-2`;
    reply.textContent =  "Reply";
    reply.addEventListener('click', () => {
      reply_mail(email.sender, email.subject, email.body, email.timestamp);
    });
    document.querySelector('#emails-view').appendChild(reply);
    // Change the status of read to 'true'
    make_read(id);
  });
}

function toggle_archive(id, state) {
  fetch(`/email/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !state,
    }),
  });
}

function make_read(id) {
  fetch(`/email/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true,
    }),
  });
}

function reply_mail(sender, subject, body, timestamp) {
  // use compose email function to display the form
  compose_email();
  if (subject.slice(0,3) != 'Re:') subject = `Re: ${subject}`;
  document.querySelector('#compose-recepients').value = sender;
  document.querySelector('#compose-subject').value = subject;

  pre_fill = `On ${timestamp} ${sender} wrote:\n${body}\n`;
  document.querySelector('#compose-body').value = pre_fill;
}


// !!!!!!!!!!!!!!!! 여기 연습파트!!!!!!!!!!

document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archived'));

  load_mailbox('inbox');

});


function compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recepients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  if (mailbox == 'show_mail') {
    show_mail()
    return;
  }

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then((emails) => {
    emails.forEach((element) => {


      if (mailbox == 'sent') {
        sender_recepients = element.recepients;
      } else {
        sender_recepients = element.sender;
      }

      // Check read status of the element to display its color in inbox
      if (mailbox == 'inbox') {
        if (element.read) is_read = 'read';
        else is_read = '';
      } else {
        is_read = '';
      }

      // Now make a variable to display mailbox
      var item = document.createElement('div');
      item.className = `card ${is_read} my-1 items`;
      item.innerHTML = `<div class='card-body' id='item-${element.id}'>
      ${element.subject} | ${sender_recepients} | ${element.timestamp}
      <br>
      ${element.body}
      </div>`;

      document.querySelector('#emails-view').appendChild(item);
      item.addEventListener('click', () => {
        show_mail(element.id, mailbox);
      });

    });
  });
}

function show_mail(id, mailbox) {
  fetch(`/emails/${id}`)
  .then((response) => response.json())
  .then((email) => {
    document.querySelector('#emails-view').innerHTML = '';
    var item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">

    `
  });
}