import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function TypingMessage({ text }){
    const[displayText, setDisplayText] = useState("");
    useEffect(() => {
        setDisplayText("");
        const words = text.split(" ");
        let index = 0;
        const interval = setInterval(() => {
           setDisplayText(words.slice(0, index + 1).join(" "));
            index++;
            if(index >= words.length){
                clearInterval(interval);
            } 
        },40);
        return ()=>clearInterval(interval);
    },[text]);

    return (
    <ReactMarkdown
        remarkPlugins={[remarkGfm]}
    >
        {displayText}
    </ReactMarkdown>
    );
}

export default TypingMessage;