function deleteFav(favId){
    fetch("/delete-fav", {
        method: "POST",
        body: JSON.stringify({ favId: favId }),
    }).then((_res) => {
        window.location.href = "/favorites"
    });
}

const viewGuideBtns = document.querySelectorAll("#rankings-btn")

viewGuideBtns.forEach(ele => {
    ele.addEventListener('click', () => {
        window.location.href = "/rankings"
    });
});

