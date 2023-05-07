fetch("/api/orders")
  .then(function (resp) {
    return resp.json();
  })
  .then(function (data) {
    const orderId = data.data.number;
    document.querySelector(".order_number").innerHTML = orderId;
  });
