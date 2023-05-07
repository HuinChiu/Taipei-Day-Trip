let nextPage = 0;
let header_search = "";

//觀察對象設定當對象可看見便執行
const options = {
  root: null,
  threshold: 0,
  rootMargin: "0px",
};
const footer = document.querySelector(".footer-item");

let observer = new IntersectionObserver(function (entries, observer) {
  // 每當目標元素進入畫面後就新增20筆，並且重置觀察的元素
  if (entries[0].isIntersecting) {
    callback(nextPage);
    observer.observe(footer);
  }
}, options);
observer.observe(footer);

async function callback() {
  if (nextPage == null) {
    return;
  } else {
    let url = "";
    if (search.value == "") {
      url = `/api/attractions?page=${nextPage}`;
    } else {
      url = `/api/attractions?page=${nextPage}&keyword=${header_search}`;
    }
    const response = await fetch(url);
    const result = await response.json();
    if (result.erro == true) {
      let main = document.querySelector("main");
      let boxDiv = document.createElement("div");
      boxDiv.innerText = result.message;
      main.appendChild(boxDiv);
    } else {
      const loading = document.querySelector(".loading");
      loading.style.display = "flex";
      nextPage = result.nextPage;
      let data = result.data;
      let count = 0;
      for (let i = 0; i < data.length; i++) {
        let name = data[i].name;
        let mrt = data[i].mrt;
        let category = data[i].category;
        let images = data[i].images[0];
        let id = data[i].id;
        let main = document.querySelector("main");
        let aTag = document.createElement("a");
        aTag.className = "a-tag";
        aTag.href = `/attraction/${id}`;
        let boxDiv = document.createElement("div");
        boxDiv.className = "box";
        let itemDiv = document.createElement("div");
        itemDiv.className = "item";
        // let itemImg = document.createElement("img");
        let itemImg = new Image();
        itemImg.className = "item-img";
        itemImg.src = images;
        itemImg.onload = function () {
          loading.style.display = "none";
        };
        let itemTitle = document.createElement("div");
        itemTitle.className = "item-title";
        itemTitle.innerText = name;
        let itemDescrip = document.createElement("div");
        itemDescrip.className = "item-descrip";
        let itemMrt = document.createElement("div");
        itemMrt.className = "item-mrt";
        itemMrt.innerText = mrt;
        let itemCategory = document.createElement("div");
        itemCategory.className = "item-category";
        itemCategory.innerText = category;
        main.appendChild(aTag);
        aTag.appendChild(boxDiv);
        boxDiv.appendChild(itemDiv);
        boxDiv.appendChild(itemDescrip);
        itemDiv.appendChild(itemImg);
        itemDiv.appendChild(itemTitle);
        itemDescrip.appendChild(itemMrt);
        itemDescrip.appendChild(itemCategory);
      }
    }
  }
}

//點擊搜尋圖片後搜尋資料
let searchBtn = document.querySelector(".header_btn");
searchBtn.addEventListener("click", () => {
  document.querySelector("main").innerHTML = "";
  nextPage = 0;
  header_search = document.querySelector(".header_search").value;
  observer.unobserve(footer);
  observer.observe(footer);
});

//點擊搜尋匡後為點選景點列表匡點選外面網頁讓景點列表匡消失，並將字顯示在搜尋匡上
document.addEventListener(
  "click",
  function () {
    let search = document.querySelector(".header_search");
    let categoryItem = document.querySelectorAll(".cat-item");
    for (let i = 0; i < categoryItem.length; i++) {
      categoryItem[i].addEventListener("click", function () {
        let catItemStr = categoryItem[i].innerText;
        search.value = catItemStr;
        document.querySelector(".category").style.display = "none";
      });
    }
  },
  true
);

//點擊搜尋匡出現景點列表匡
let search = document.querySelector(".header_search");
search.addEventListener("click", function () {
  let categoryDiv = document.querySelector(".category");
  categoryDiv.innerHTML = "";
  document.querySelector(".category").style.display = "grid";

  fetch("/api/categories")
    .then(function (resp) {
      return resp.json();
    })
    .then(function (result) {
      let data = result.data;
      for (let i = 0; i < data.length; i++) {
        let catItem = document.createElement("div");
        catItem.className = "cat-item";
        catItem.innerText = data[i];
        categoryDiv.appendChild(catItem);
      }
    });
});

//點擊搜尋匡後為點選景點列表匡點選外面網頁讓景點列表匡消失
document.addEventListener(
  "click",
  function () {
    document.querySelector(".category").style.display = "none";
  },
  true
);

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

checkcookie();

async function signin() {
  let cookie = "";
  const email = document.querySelector("#signin_email").value;
  const password = document.querySelector("#signin_password").value;
  let entry = { email: email, password: password };
  const url = "/api/user/auth";
  try {
    await fetch(url, {
      method: "PUT",
      body: JSON.stringify(entry),
      headers: new Headers({
        "content-Type": "application/json",
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
