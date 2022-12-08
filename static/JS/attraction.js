let url = `/api${location.pathname}`;

fetch(url).then(function (resp) {
    return resp.json();
}).then(function (data) {
    console.log(data)
    result = data["data"];
    let name = result["name"];
    let categoryMrt = `${result["category"]} at ${result["mrt"]}`;
    let imgList = result["images"];
    let imgCount = imgList.length
    console.log(categoryMrt)
    let itemName = document.querySelector(".item_name");
    itemName.innerText = name;
    let itemCategory = document.querySelector(".item_category");
    itemCategory.innerText = categoryMrt;
    let description = document.querySelector(".description");
    description.innerText = result["description"];
    let addressDiv = document.querySelector(".address_descrip");
    addressDiv.innerText = result["address"];
    let mrt = document.querySelector(".traffic_mrt");
    mrt.innerText = result["transport"];

    // 設置img
    let imgBox = document.querySelector(".img_box");
    imgBox.style.backgroundImage = `url(${imgList[0]})`
    for (let i = 0; i < imgCount; i++) {
        let radio = document.querySelector(".radio");
        let imgRadio = document.createElement("input");
        imgRadio.className = "img_radio";
        imgRadio.type = "radio";
        imgRadio.name = "radio";
        imgRadio.className = "img_radio";
        radio.appendChild(imgRadio);

        imgRadio.addEventListener("click", function () {
            let imgBox = document.querySelector(".img_box");
            imgBox.style.backgroundImage = `url(${imgList[i]})`
        }
        )
    }
    //第一張圖radio checked
    const imgRadio = document.querySelectorAll(".img_radio")
    imgRadio[0].checked = true;

    //左側箭頭切換
    let index = 0
    let img_left = document.querySelector(".btn_left")
    img_left.addEventListener("click", function () {
        index--;
        if (index < 0) {
            index = imgCount - 1;
        }
        let imgBox = document.querySelector(".img_box");
        imgBox.style.backgroundImage = `url(${imgList[index]})`
        let radios = document.querySelectorAll(".img_radio")
        radios[index].checked = true;

    })
    //右側箭頭切換
    let img_right = document.querySelector(".btn_right")
    img_right.addEventListener("click", function () {
        index++;
        if (index > imgCount - 1) {
            index = 0
        }
        let imgBox = document.querySelector(".img_box");
        imgBox.style.backgroundImage = `url(${imgList[index]})`
        let radios = document.querySelectorAll(".img_radio")
        radios[index].checked = true;
    })
})


//上半天 下半天費用變更
let Pm = document.querySelector(".PM")
Pm.addEventListener("click", function () {
    let feed = document.querySelector(".feed")
    feed.innerText = "新台幣2500元"
})
let Am = document.querySelector(".AM")
Am.addEventListener("click", function () {
    let feed = document.querySelector(".feed")
    feed.innerText = "新台幣2000元"
})

async function checkcookie() {
    await fetch("/api/user/auth").then(function (resp) {
        return resp.json()
    }).then(function (data) {
        console.log(data["data"])
        if (data["data"] !== null) {
            document.querySelector(".sign").style.display = "none"
            document.querySelector(".signin").style.display = "none"
            document.querySelector(".signout").style.display = "block"
        }
    })
}


checkcookie();

