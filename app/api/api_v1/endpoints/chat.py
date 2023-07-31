from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <meta charset="UTF-8" />
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/get_tasks?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibG9naW4iOiJzdHJpbmciLCJiYWxhbmNlIjowLjAsImlzX3N1cGVyIjpmYWxzZSwiZXhwIjoxNjkwNTg4ODEzfQ.cWexLtJXn4LyAUW4d64RI6RilQ-rgpnslAc5S2FvyXk");
ws.onmessage = function (event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};

function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
        </script>
    </body>
</html>
"""


@router.get("")
async def get():
    return HTMLResponse(html)
