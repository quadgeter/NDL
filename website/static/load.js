const loader = document.querySelector(".loader");
const loadingMsg = document.querySelector(".loading-msg");


window.addEventListener('load', () => {
    loader.classList.add("loader-hidden");
    loadingMsg.classList.add("loading-msg-hidden");
});

const searchBtn = document.querySelector("#search-btn");
searchBtn.addEventListener('click', () => {
    alert();
    loader.classList.remove("loader-hidden");
    loadingMsg.classList.remove("loading-msg-hidden");
});

const loadMore = document.querySelector("#load-more");
loadMore.addEventListener('click', () => {
    alert();
    loader.classList.remove("loader-hidden");
    loadingMsg.classList.remove("loading-msg-hidden");
});