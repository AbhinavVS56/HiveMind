import { useState, useRef, useEffect } from "react"
import "./App.css"
import logo from "./assets/logo.png"
import mindflayer from "./assets/mindflayer1.jpg"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

function App(){
  const[query,setQuery]=useState("")
  const[messages,setMessages]=useState([])
  const[loading,setLoading]=useState(false)
  const[chatStarted,setChatStarted]=useState(false)

  const conversationRef=useRef(null)

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
  useEffect(()=>{
    if(conversationRef.current)
    {
        conversationRef.current.scrollTo({
            top:conversationRef.current.scrollHeight,
            behavior:"smooth"
        })
    }
  },[messages])

  const handleKeyDown = (event) => {
    if (loading) return;
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion();
    }
}

  return(
    <div className={`app ${chatStarted ? "chat-mode" : ""}`}>
        <div className="header">
            <img src={logo} alt="HiveMind Logo" className="logo"/>
        </div>

        <div className="conversation-area" ref={conversationRef}>
            <div className="conversation">
                {
                    messages.map(
                        (message,index)=>(
                            <div key={index}
                            className={`message ${message.sender==="You" ? "user" : "hivemind"}`}
                            >
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {message.text}
                                </ReactMarkdown>
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
                    onKeyDown={handleKeyDown}
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
        <img src={mindflayer} alt="Mind Flayer" className="mindflayer"/>
    </div>
)
}

export default App