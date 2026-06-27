import { useState } from "react"

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
    <div>
      <h1>HiveMind</h1>
      <input type="text" placeholder="Ask anything" value={query} onChange={(event)=>setQuery(event.target.value)}/>
      <button onClick={sendQuestion} disabled={loading}>{loading?"Thinking...":"Ask HiveMind"}</button>
      <h2>Conversation</h2>
      {messages.map((message,index)=>(
        <div key={index}>
          <h3>{message.sender}</h3>
          <p>{message.text}</p>
        </div>

      ))
      }
    </div>
  )
}

export default App