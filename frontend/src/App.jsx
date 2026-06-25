import { useState } from "react"

function App(){
  const[query,setQuery]=useState("")
  const[answer,setAnswer]=useState("")

  async function sendQuestion(){
    const response=await fetch("http://127.0.0.1:8000/research",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({query:query})
    })
    const data=await response.json()
    setAnswer(data.answer)
  }

  return(
    <div>
      <h1>HiveMind</h1>
      <input type="text" value={query} onChange={(event)=>setQuery(event.target.value)}/>
      <button onClick={sendQuestion}>Ask HiveMind</button>
      <h2>Answer</h2>
      <p>{answer}</p>
    </div>
  )
}

export default App