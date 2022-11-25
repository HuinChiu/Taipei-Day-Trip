let nextPage = 0;
let url = `http://127.0.0.1:3000/api/attractions?page=${nextPage}`
//首頁獲取資料
getData(url);
//於首頁取得所有資料並顯示
function getData(url) {
    console.log(url)
    fetch(url).then(function (response) {
        return response.json();
    }).then(function (result) {
        nextPage = result["nextPage"];
        console.log(nextPage)
        let data = result["data"]
        for (let i = 0; i < data.length; i++) {
            let name = data[i]["name"];
            let mrt = data[i]["mrt"];
            let category = data[i]["category"];
            let images = data[i]["images"][0];
            let main = document.querySelector("main");
            let boxDiv = document.createElement("div");
            boxDiv.className = "box";
            let itemDiv = document.createElement("div");
            itemDiv.className = "item";
            let itemImg = document.createElement("img");
            itemImg.className = "item-img";
            itemImg.src = images;
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
            main.appendChild(boxDiv);
            boxDiv.appendChild(itemDiv);
            boxDiv.appendChild(itemDescrip);
            itemDiv.appendChild(itemImg);
            itemDiv.appendChild(itemTitle);
            itemDescrip.appendChild(itemMrt);
            itemDescrip.appendChild(itemCategory);
        } return nextPage
    }).then(function (nextPage) {
        if (nextPage == null) { //停止取得資料
            return
        } else {
            let url = `http://127.0.0.1:3000/api/attractions?page=${nextPage}`
            const options = {
                root: null,
                threshold: 0.75,
                rootMargin: "0px"
            }
            const footer = document.querySelector("footer");
            const observer = new IntersectionObserver(function (entries) {
                if (entries[0].isIntersecting) {
                    getData(url);
                    observer.unobserve(footer);
                }
            }, options);
            observer.observe(footer);
        }
    })
}



//get category data
function getCatData(url) {
    try {
        fetch(url).then(function (response) {
            return response.json();
        }).then(function (result) {
            if (result["erro"]) {
                document.querySelector("main").innerHTML = result["message"]
                return null
            } else {
                nextPage = result["nextPage"];
                let data = result["data"]
                for (let i = 0; i < data.length; i++) {
                    let name = data[i]["name"];
                    let mrt = data[i]["mrt"];
                    let category = data[i]["category"];
                    let images = data[i]["images"][0];
                    let main = document.querySelector("main");
                    let boxDiv = document.createElement("div");
                    boxDiv.className = "box";
                    let itemDiv = document.createElement("div");
                    itemDiv.className = "item";
                    let itemImg = document.createElement("img");
                    itemImg.className = "item-img";
                    itemImg.src = images;
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
                    main.appendChild(boxDiv);
                    boxDiv.appendChild(itemDiv);
                    boxDiv.appendChild(itemDescrip);
                    itemDiv.appendChild(itemImg);
                    itemDiv.appendChild(itemTitle);
                    itemDescrip.appendChild(itemMrt);
                    itemDescrip.appendChild(itemCategory);
                }
            } return nextPage
        }).then(function (nextPage) {
            if (nextPage == null) { //停止取得資料
                return
            } else {
                let search = document.querySelector(".header_search").value;
                let url = `http://127.0.0.1:3000/api/attractions?page=${nextPage}&keyword=${search}`
                console.log(url)
                //取得下一頁url
                const options = {
                    root: null,
                    threshold: 0.25,
                    rootMargin: "-10px"
                }
                const footer = document.querySelector("footer");
                const observer = new IntersectionObserver(function (entries) {
                    if (entries[0].isIntersecting) {
                        getCatData(url);
                        observer.unobserve(footer);
                    }
                }, options);
                observer.observe(footer);
            }
        })
    } catch (erro) {
        console.log(`Erro: ${erro}`)

    };
}



//取得搜尋景點關鍵字列表
let categoryUrl = "http://127.0.0.1:3000/api/categories"
async function getCategory(categoryUrl) {
    try {
        let response = await fetch(categoryUrl);
        let result = await response.json();
        let data = result["data"]
        for (let i = 0; i < data.length; i++) {
            let categoryDiv = document.querySelector(".category");
            let catItem = document.createElement("div");
            catItem.className = "cat-item";
            catItem.innerText = data[i];
            categoryDiv.appendChild(catItem);

        };
        //取得景點列表內文字並顯示在searchInput上
        let search = document.querySelector(".header_search");
        let categoryItem = document.querySelectorAll(".cat-item");
        for (let i = 0; i < categoryItem.length; i++) {
            categoryItem[i].addEventListener("click", function () {
                let catItemStr = categoryItem[i].innerText;
                search.value = catItemStr
                document.querySelector(".category").style.display = "none";
            })
        }
    } catch (erro) {
        console.log(`Erro: ${erro}`);
    }
};
getCategory(categoryUrl);
//點擊搜尋匡出現景點列表匡
let search = document.querySelector(".header_search");
search.addEventListener("click", function () {
    document.querySelector(".category").style.display = "grid";
});

//點擊特定景點類別後顯示景點類別資料
let searchImg = document.querySelector(".header_btn");
searchImg.addEventListener("click", function () {
    document.querySelector(".category").style.display = "none";
    document.querySelector("main").innerHTML = ""
    let search_str = search.value;
    let geturl = `http://127.0.0.1:3000/api/attractions?keyword=${search_str}`;
    getCatData(geturl);
})

//點擊搜尋匡後為點選景點列表匡點選外面網頁讓景點列表匡消失
document.addEventListener("click", function () {
    document.querySelector(".category").style.display = "none";
}, true)
