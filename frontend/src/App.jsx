import { useState } from "react"
import "./App.css"
import logo from "./assets/logo.png"
import background from "./assets/background.jpg"
import mindflayer from "./assets/mindflayer.jpg"

function App(){
  const[query,setQuery]=useState("")
  const[messages,setMessages]=useState([])
  const[loading,setLoading]=useState(false)

  async function sendQuestion(){
    if(query.trim()===""){
      return
    }
    setLoading(true)
    const response=await fetch("http://127.0.0.1:8000/research",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({query:query})
    })
    const data=await response.json()
    setMessages([...messages,
      {sender:"You",text:query},
      {sender:"HiveMind",text:data.answer}])
      setQuery("")
    setLoading(false)
  }

  return(
    messages.length===0?(
    <div className="landing-page">
      <img src={logo} alt="HiveMind Logo" className="logo"/>
      <div className="input-section">
        <textarea className="query-input"
                placeholder="What's on your mind?" 
                value={query} 
                onChange={(event)=>setQuery(event.target.value)}>
        </textarea>
        <div className="button">
          <button className="ask-button"
                  onClick={sendQuestion} 
                  disabled={loading}>{loading?"Thinking...":"Ask HiveMind"}</button>
        </div>
      </div>
      <p className="quote">
        <em>"I am on a curiosity voyage, and I need my paddles to travel.
        These books... these books are my paddles."
        </em>
        <br/>
        <span>- Dustin Henderson</span>
      </p>
    </div>
    ):(
    <div className="chat-page">
        Chat Page
    </div>
    )
  )
}

export default App