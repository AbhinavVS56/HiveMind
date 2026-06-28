import { useState } from "react"
import "./App.css"

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
    <div className="app">
      <h1 className="title">HiveMind</h1>
      <textarea className="query-input"
              placeholder="Ask anything" 
              value={query} 
              onChange={(event)=>setQuery(event.target.value)}>
      </textarea>
      <button className="ask-button"
              onClick={sendQuestion} 
              disabled={loading}>{loading?"Thinking...":"Ask HiveMind"}</button>
      <h2 className="convo-title">Conversation</h2>
      <div className="convo">  
        {messages.map((message,index)=>(
        <div key={index} className={`message ${message.sender === "You" ? "user" : "hivemind"}`}>
          <h3 className="sender">{message.sender}</h3>
          <p className="content">{message.text}</p>
        </div>
      ))
      }
      </div>
    </div>
  )
}

export default App