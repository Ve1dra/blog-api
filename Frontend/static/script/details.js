const update = document.getElementById("Update-posts")
const heading = document.getElementById("heading")
const content = document.getElementById("content")
const patchBody = {
    id: localStorage.getItem("postId"),
    heading: heading.value,
    content: content.value,
}
const urls = `https://blog-api-n1d5.onrender.com/api/v1/users/patch/${localStorage.getItem("postId")}/`
update.addEventListener("click", async (e) =>{
    e.preventDefault();
    console.log("Updating this post for this user...")
    await fetch(urls, {
        method: "PATCH",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(patchBody)
    }).then(Response => {
        if (!Response.ok) throw new Error("API could not be fetched")
            return Response.json()
    }).then(data =>{
        console.log(data)
    }).catch(e => {alert(e.message)})
})