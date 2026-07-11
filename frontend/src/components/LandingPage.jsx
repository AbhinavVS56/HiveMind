function LandingPage({
    query,
    setQuery,
    loading,
    sendQuestion,
    logo
}){

    return(
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
                    <span>— Dustin Henderson</span>
                  </p>
                </div>

    )

}

export default LandingPage