from ddgs import DDGS

with DDGS() as ddgs:
    result=list(ddgs.text(
        "Latest AI news",
        max_results=3
    ))

print(result)