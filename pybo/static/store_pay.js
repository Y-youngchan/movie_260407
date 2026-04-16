document.addEventListener("DOMContentLoaded", function () {

    const clientKey = "test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm";
    const tossPayments = TossPayments(clientKey);

    document.getElementById("payment-button").addEventListener("click", function (e) {

        e.preventDefault();

        tossPayments.requestPayment("카드", {
            amount: amount,
            orderId: "order_" + new Date().getTime(),
            orderName: orderName,
            customerName: "홍길동",

            successUrl: "http://localhost:5000/film/success",
            failUrl: "http://localhost:5000/film/fail"
        });
    });

});