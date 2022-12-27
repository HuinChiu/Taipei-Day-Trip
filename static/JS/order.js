//設定Display ccv field
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: '#card-expiration-date',
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style focus state
        ':focus': {
            'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})



const submitButton = document.querySelector(".order_btn")
submitButton.addEventListener("click", onSubmit)

var entry = {
    "prime": "", "order": { "price": "", "trip": { "attraction": {} }, "date": "", "time": "" },
    "contact": { "name": "", "email": "", "phone": "" }
}



async function onSubmit(event) {
    event.preventDefault()
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

    // Get prime
    TPDirect.card.getPrime(function (result) {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        else {
            const prime = result.card.prime
            entry.prime = prime
            console.log("thisis" + JSON.stringify(entry.prime))
            console.log("this is " + entry)
            const name = document.querySelector(".input_name").value
            const email = document.querySelector(".input_email").value
            const phone = document.querySelector(".input_phone").value
            const price = document.querySelector(".item_price").innerText
            const date = document.querySelector(".item_date_time").innerText
            const time = document.querySelector(".item_time_time").innerText
            entry.contact.name = name
            entry.contact.email = email
            entry.contact.phone = phone
            entry.order.price = price
            entry.order.date = date
            entry.order.time = time
            fetch("/api/booking").then(function (resp) {
                return resp.json();
            }).then(function (data) {
                const attraction = data.data.attraction
                entry.order.trip.attraction = attraction
                fetch("/api/orders", {
                    method: "POST",
                    body: JSON.stringify(entry),
                    headers: new Headers({
                        "content-Type": "application/json" //request Header
                    })
                }).then(function (resp) {
                    return resp.json();
                }).then(function (data) {
                    console.log(data)
                    if (data.data.payment.status == 0) {
                        console.log(data)
                        console.log(data.data.number)
                        window.location.href = `/thankyou?number=${data.data.number}`
                    }
                    else {
                        alert("付款失敗!請重新輸入!")
                    }
                })
            })


        }

    })

}


