import { useState } from "react"
import "./App.css"
import logo from "./assets/logo.png"

function App(){
  const[query,setQuery]=useState("")
  const[messages,setMessages]=useState([])
  const[loading,setLoading]=useState(false)
  const[chatStarted,setChatStarted]=useState(false)

  async function sendQuestion(){
    if(query.trim()===""){
      return
    }
    setChatStarted(true)
    setLoading(true)
    const response=await fetch("http://127.0.0.1:8000/research",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({query:query})
    })
    const data=await response.json()
    console.log(data)
    setMessages([...messages,
      {sender:"You",text:query},
      {sender:"HiveMind",text:data.answer}])
    setQuery("")
    setLoading(false)
  }

  return(
    <div className={`app ${chatStarted ? "chat-mode" : ""}`}>
        <div className="header">
            <img src={logo} alt="HiveMind Logo" className="logo"/>
        </div>

        <div className="conversation-area">
            <div className="conversation">
                {
                    messages.map(
                        (message,index)=>(
                            <div key={index}
                            className={`message ${message.sender==="You" ? "user" : "hivemind"}`}
                            >
                                <p>{message.text}</p>
                            </div>
                        )
                    )
                }
            </div>
        </div>

        <div className="input-area">
            <div className="input-section">
                <textarea
                    className="query-input"
                    placeholder="What's on your mind?"
                    value={query}
                    onChange={(event)=>setQuery(event.target.value)}
                />
                <div className="button">
                    <button
                        className="ask-button"
                        onClick={sendQuestion}
                        disabled={loading}
                    >
                    {loading ? "Thinking..." : "Ask HiveMind"}
                    </button>
                </div>
            </div>
        </div>

        <p className="quote">
            <em>
                "I am on a curiosity voyage, and I need my paddles to travel.
                These books... these books are my paddles."
            </em>
            <br/>
            <span>— Dustin Henderson</span>
        </p>
    </div>
)
}

export default App