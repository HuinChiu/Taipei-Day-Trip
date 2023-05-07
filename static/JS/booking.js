document.querySelector(".msg").style.display = "none";
checkcookie(); //確認有無登入
getOrderData(); //確認有無登入若無登入導回首頁，若點擊刪除圖案刪除此預定行程

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

async function getOrderData() {
  await fetch("/api/user/auth")
    .then(function (resp) {
      return resp.json();
    })
    .then(function (data) {
      if (data.data == null) {
        document.querySelector(".sign").style.display = "block";
        window.location.href = "/";
      } else {
        const name = data.data.name;
        const id = data.data.id;
        document.querySelector(".signin_name").innerText = name;
        fetch("/api/booking")
          .then(function (resp) {
            return resp.json();
          })
          .then(function (data) {
            if (data.error == true) {
              document.querySelector("main").style.display = "none";
              document.querySelector(".msg").style.display = "block";
              document.querySelector("footer").style.paddingBottom = "100%";
            } else {
              const attraction = data.data.attraction;
              document.querySelector(".item_img").src = attraction.image;
              document.querySelector(".item_title_attraction").innerText =
                attraction.name;
              document.querySelector(".item_date_time").innerText =
                data.data.date;
              document.querySelector(".item_time_time").innerText =
                data.data.time;
              document.querySelector(".item_price").innerText = data.data.price;
              document.querySelector(".item_location_address").innerText =
                attraction.address;
              document
                .querySelector(".delete_btn")
                .addEventListener("click", deleteOrder);

              async function deleteOrder() {
                let entry = {};
                const attractionId = attraction.id;
                const address = attraction.address;
                const date = data.data.date;
                const price = data.data.price;
                const time = data.data.time;
                entry.id = id;
                entry.attraction_id = attractionId;
                entry.address = address;
                entry.date = date;
                entry.price = price;
                entry.time = time;
                await fetch("/api/booking", {
                  method: "DELETE",
                  body: JSON.stringify(entry),
                  headers: new Headers({
                    "content-Type": "application/json", //request Header
                  }),
                })
                  .then(function (resp) {
                    return resp.json();
                  })
                  .then(function (data) {
                    if (data.ok == true) {
                      alert("刪除預定行程成功！");
                      window.location.href = "/booking";
                    } else {
                      alert(data.message);
                    }
                  });
              }
            }
          });
      }
    });
}
