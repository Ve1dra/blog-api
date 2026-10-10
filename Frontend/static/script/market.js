const URL = "https://blog-api-n1d5.onrender.com/api/v1/users/posts/"

const feed = document.getElementById("feed-post")
const postForm = document.getElementById("post-form")

const heading = document.getElementById("head")
const content = document.getElementById("body")
const update_btn = document.querySelector(".get")

function loadPosts() {
    console.log("Getting all posts in the database...")
    fetch(URL, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            "Content-Type": "application/json"
        },
    }).then(Response => {
        if (!Response.ok) throw new Error("API could not be fetched")
        return Response.json()
    }).then(data => {
        console.log(data);
        let dat = data.results
        for (let i = 0; i < dat.length; i++) {
            const block = document.createElement('div')
            block.className = 'feed-post';

            const title = document.createElement("h3");
            title.textContent = dat[i].heading;

            const body = document.createElement("p")
            body.textContent = dat[i].content;

            const btnDiv = document.createElement('div')

            const editBtn = document.createElement('button');
            editBtn.id = 'edit'
            editBtn.className = 'edit'
            editBtn.textContent = 'Edit'

            const delBtn = document.createElement("button")
            delBtn.id = 'delete';
            delBtn.className = 'delete';
            delBtn.textContent = 'Delete'

            btnDiv.appendChild(editBtn)
            btnDiv.appendChild(delBtn)

            block.appendChild(title)
            block.appendChild(body)
            block.appendChild(btnDiv)

            feed.appendChild(block)

            editBtn.addEventListener('click', async () => {
                window.scrollTo({ top: 0, behavior: 'smooth' })
                heading.value = dat[i].heading
                content.textContent = dat[i].content

                update_btn.addEventListener('click', async (e) => {
                    e.preventDefault()
                    const body = {
                        heading: heading.value,
                        content: content.value,
                    }
                    fetch(`https://blog-api-n1d5.onrender.com/api/v1/users/patch/${dat[i].id}/`, {
                        method: "PATCH",
                        headers: {
                            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(body)
                    }).then(Response => {
                        if (!Response.ok) throw new Error("API could not be fetched")
                        return Response.json()
                    }).then(data => {
                        console.log(data)
                        loadPosts()
                        location.reload()
                    }).catch(e => { alert(e.message) })
                })
            })

            delBtn.addEventListener('click', async (e) => {
                fetch(`https://blog-api-n1d5.onrender.com/api/v1/users/patch/${dat[i].id}/`, {
                    method: "DELETE",
                    headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}`, }
                }).then(Response => {
                    if (!Response.ok) { throw new Error("Delete couldn't happen") }
                    else {
                        loadPosts()
                        location.reload()
                    }

                }).catch(e => { console.log(e.message) })
            })

        }
    }).catch(e => { console.log(e.message) })
}

setTimeout(loadPosts(), 1000);


postForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Loading...")
    const body = {
        heading: heading.value,
        content: content.value,
    }

    await fetch(URL, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    }).then(Response => {
        if (!Response.ok) throw new Error("API could not be fetched")
        return Response.json()
    }).then(data => {
        console.log(data)
        loadPosts()
        location.reload()
    }).catch(e => { alert(e.message) })
})


