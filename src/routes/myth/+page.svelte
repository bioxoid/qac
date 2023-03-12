<script>
const OPENAI_API_KEY = "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";
let c_name = "";
let added_content = "";
let content = "";
// let unavailable_words=["殺す"]
function getContent() {
  if (added_content == "") {
    return `「${c_name}座」という新たな星座を思いつきました。その星座に関する神話を嘘を交えながら図鑑のように最後まで書いてください。`
  } else {
    return `「${c_name}座」という新たな星座を思いつきました。その星座に関する神話を嘘を交えながら、文章中に「${added_content}」という単語を入れつつ、図鑑のように最後まで書いてください。`
  }
}
async function gptIt() {
  console.log("Sending content to ChatGPT...")
  console.log(getContent());
  content = "waiting response..."
  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'model': 'gpt-3.5-turbo',
      'messages': [
        {
          'role': 'user',
          'content':  getContent()
        }
      ]
    })
  })
  const data = await res.json();
  content = data.choices[0].message.content;
  console.log("Content received!")
}

</script>
<div>
  <div>
    <span>星座名</span><input type="text" bind:value={c_name}>
  </div>
  <div>
    <span>文章中に入れたい単語</span><input type="text" bind:value={added_content}>
  </div>
<button on:click={gptIt}>send</button>
</div>
<div>
  <textarea id="result">{content}</textarea>
</div>
<style>
  :global(body) {
    margin: 10px
  }
  #result {
    width: 90vw;
    margin-left: calc(5vw - 10px);
    height: 50vh;
  }
</style>