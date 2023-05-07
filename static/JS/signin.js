//sign in
const signInBtn = document.querySelector(".sign_btn1");
signInBtn.addEventListener("click", signin);

// signup
const sign_btn = document.querySelector(".sign_btn2");
sign_btn.addEventListener("click", sendData);

//按下預定行程按鈕確認有無登入
const bookingBtn = document.querySelector(".booking_btn");
bookingBtn.addEventListener("click", checksignin);

//點擊登入按鈕跑出輸入帳號密碼匡
let sigin = document.querySelector(".signin");
sigin.addEventListener("click", function () {
  document.querySelector(".sign").style.display = "block";
});

//點擊登入右上角close icon後關閉登入
let closeIcon = document.querySelectorAll(".close_icon");
for (let i = 0; i < closeIcon.length; i++) {
  closeIcon[i].addEventListener("click", function () {
    document.querySelector(".sign").style.display = "none";
  });
}

//點擊還沒有帳戶？更換註冊匡
let notice1 = document.querySelector(".notice-1");
notice1.addEventListener("click", function () {
  document.querySelector(".signup_box").style.display = "block";
  document.querySelector(".signbox").style.display = "none";
  message = document.querySelectorAll(".message");
  message[0].innerText = "";
});

//點擊已經有帳戶了？更換登入帳號匡
let notice2 = document.querySelector(".notice-2");
notice2.addEventListener("click", function () {
  document.querySelector(".signup_box").style.display = "none";
  document.querySelector(".signbox").style.display = "block";
  message = document.querySelectorAll(".message");
  message[1].innerText = "";
});
checkcookie();

// signup
function sendData() {
  const signupName = document.querySelector("#signup_name").value;
  const signupEmail = document.querySelector("#signup_email").value;
  const signupPassword = document.querySelector("#signup_password").value;
  let entry = {
    name: signupName,
    email: signupEmail,
    password: signupPassword,
  }; //將name放入字典{name:123}
  let url = "/api/user"; //api url
  fetch(url, {
    method: "POST",
    body: JSON.stringify(entry),
    headers: new Headers({
      "content-Type": "application/json", //request Header
    }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.ok === true) {
        let message = document.querySelectorAll(".message");
        message[1].style.display = "block";
        message[1].innerText = "帳號註冊成功，請點選登入";
      } else if (data.erro == true) {
        let returnMessage = data.message;
        let message = document.querySelectorAll(".message");
        message[1].style.display = "block";
        message[1].innerText = returnMessage;
      }
    });
}

//sign in
async function signin() {
  let cookie = "";
  const email = document.querySelector("#signin_email").value;
  const password = document.querySelector("#signin_password").value;
  let entry = { email: email, password: password }; //將name放入字典{name:123}
  const url = "/api/user/auth"; //api url
  try {
    await fetch(url, {
      method: "PUT",
      body: JSON.stringify(entry),
      headers: new Headers({
        "content-Type": "application/json", //request Header
      }),
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.erro == true) {
          const returnMessage = data.message;
          const message = document.querySelectorAll(".message");
          message[0].style.display = "block";
          message[0].innerText = returnMessage;
        } else {
          cookie = document.cookie;
        }
      });
    checkcookie();
  } catch (error) {
    const errorMsg = error;
  }
}
//signout
const signout = document.querySelector(".signout");
signout.addEventListener("click", function () {
  fetch("/api/user/auth", {
    method: "DELETE",
  })
    .then(function (resp) {
      return resp.json();
    })
    .then(function (data) {
      if (data.ok == true) {
        document.querySelector(".signin").style.display = "block";
        document.querySelector(".signout").style.display = "none";
      }
    });
});
//確認有無token
async function checkcookie() {
  await fetch("/api/user/auth")
    .then(function (resp) {
      return resp.json();
    })
    .then(function (data) {
      if (data.data !== null) {
        document.querySelector(".sign").style.display = "none";
        document.querySelector(".signin").style.display = "none";
        document.querySelector(".signout").style.display = "block";
      }
    });
}
// 預定行程
async function checksignin() {
  await fetch("/api/user/auth")
    .then(function (resp) {
      return resp.json();
    })
    .then(function (data) {
      if (data["data"] == null) {
        document.querySelector(".sign").style.display = "block";
      } else {
        window.location.href = "/booking";
      }
    });
}
