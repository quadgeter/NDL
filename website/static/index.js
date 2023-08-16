function deleteFav(favId){
    fetch("/delete-fav", {
        method: "POST",
        body: JSON.stringify({ favId: favId }),
    }).then((_res) => {
        window.location.href = "/favorites"
    });
}

function addFav(favId, favName, favPpg){
    fetch("/add-fav", {
        method: "POST",
        body: JSON.stringify({ favId: favId,
        favName: favName,
        favPpg: favPpg }),
    }).then((_res) => {
        window.location.href = "/rankings"
    });
}