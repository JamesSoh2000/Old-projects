document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

// inbox, sent, or archive 3종류의 mail

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

// inbox, sent, or archive 3종류의 mailbox

// 여기가 inbox를 눌렀을 때 나오는 화면(첫화면)
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  // 화면에 Inbox, Sent  큰 글자로 보여주는것
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  if (mailbox == "show_mail") {
    show_mail();
    return;
  }


  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // console.table(emails);
      // for (const email in emails) {
      //   console.log(email)
      // }
      // 여기서 emails는 [{id: 3, sender: 'justlikethat17@gmail.com', ...}, {...}] 이런식으로 된 array임.
      // element는 위 emails 안에 있는 각 key의 value {id: 3, sender: 'justlikethat17@gmail.com', recipients: Array(1), subject: 'Count', body: '2', …}
      emails.forEach((element) => {

        console.log(emails)

        if (mailbox != "sent") {
          sender_recipients = element.sender;
        } else {
          sender_recipients = element.recipients;
        }
        if (mailbox == "inbox") {
          if (element.read) is_read = "read";
          else is_read = "";
        } else is_read = "";
        var item = document.createElement("div");
        item.className = `card   ${is_read} my-1 items`;

        item.innerHTML = `<div class="card-body" id="item-${element.id}">

        ${element.subject} | ${sender_recipients} | ${element.timestamp}
        <br>
        ${element.body.slice(0, 100)}
        </div>`;
        document.querySelector("#emails-view").appendChild(item);
        item.addEventListener("click", () => {
          show_mail(element.id, mailbox);
        });
      });
    });
}


// 여기가 특정하나의 mail을 눌렀을 때 그 메일의 내용들이 나오는 파트 sfsfsf
function show_mail(id, mailbox) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      // Print email
      // console.log(email);
      document.querySelector("#emails-view").innerHTML = "";
      var item = document.createElement("div");
      item.className = `card`;
      // white-space: pre-wrap을 사용하면 html에서 이렇게 한줄한줄 whitespace사용한게 그대로 적용됨(원래는 저렇게 한줄한줄써도 전부 같은줄에 배치됨) https://www.codingfactory.net/10597
      // 여기서 Sender 줄 이렇게 뒤로 빼면 차이가 있음!!
      item.innerHTML = `<div class="card-body" style="white-space: pre-wrap;">
  Sender: ${email.sender}
  Recipients: ${email.recipients}
  Subject: ${email.subject}
  Time: ${email.timestamp}
  <br>${email.body}
      </div>`;
      document.querySelector("#emails-view").appendChild(item);
      if (mailbox == "sent") return;
      let archive = document.createElement("btn");
      archive.className = `btn btn-outline-info my-2`;
      archive.addEventListener("click", () => {

        // <span>Hello <span style="display: none;">World</span></span>, innerText will return 'Hello', while textContent will return 'Hello World'.
        // innerText - When you only need to see what’s in the element — with zero formatting.
        toggle_archive(id, email.archived);
        if (archive.innerText == "Archive") archive.innerText = "Unarchive";
        else archive.innerText = "Archive";
      });
      // textContent - When you want to see what’s in the element, plus any styling on it.
      if (!email.archived) archive.textContent = "Archive";
      else archive.textContent = "Unarchive";
      document.querySelector("#emails-view").appendChild(archive);

      let reply = document.createElement("btn");
      reply.className = `btn btn-outline-success m-2`;
      reply.textContent = "Reply";
      reply.addEventListener("click", () => {
        reply_mail(email.sender, email.subject, email.body, email.timestamp);
      });
      document.querySelector("#emails-view").appendChild(reply);
      make_read(id);
    });
}

function toggle_archive(id, state) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !state,
    }),
  });
}

function make_read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function reply_mail(sender, subject, body, timestamp) {
  compose_email();
  // if (!/^Re:/.test(subject)) subject = `Re: ${subject}`;
  // if ('Re:' in subject === false) {
  //   subject = `Re: ${subject}`;
  // }
  if (subject.slice(0,3) != 'Re:') subject = `Re: ${subject}`;
  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subject;

  pre_fill = `On ${timestamp} ${sender} wrote:\n${body}\n`;

  document.querySelector("#compose-body").value = pre_fill;
}


// 여러가지 사용법들
// white-space: pre-wrap을 사용하면 html에서 이렇게 한줄한줄 whitespace사용한게 그대로 적용됨(원래는 저렇게 한줄한줄써도 전부 같은줄에 배치됨) https://www.codingfactory.net/10597