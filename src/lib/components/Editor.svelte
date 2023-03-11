<script>
import { onMount } from 'svelte';
export let canvas;
let div;
let canvas_container
let btn;
let ctx;
let btn_send
let btn_toggle_closed;
let closed = false;
onMount(() => {
  let isDrawing = false;
  let x = 0;
  let y = 0;
  ctx = canvas.getContext('2d');
  canvas.addEventListener('mousedown', e => {
    isDrawing = true;
    x = e.offsetX;
    y = e.offsetY/2;
    ctx.moveTo(x, y);
    ctx.lineTo(x, y);
    ctx.stroke();
  });
  canvas.addEventListener('mousemove', e => {
    x = e.offsetX;
    y = e.offsetY/2;
    if (isDrawing && !isDown) {
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  });
  canvas.addEventListener('mouseup', e => {
    if (isDrawing) {
      x = e.offsetX;
      y = e.offsetY/2;
      ctx.lineTo(x, y);
      ctx.stroke();
      isDrawing = false;
    }
  });
  let offset = [0,0];
  var isDown = false;
  // div.addEventListener('mousedown', function(e) {
  //   console.log("pressed");
  //   if (!isDrawing) { isDown = true };
  //   offset = [
  //     div.offsetLeft - e.clientX,
  //     div.offsetTop - e.clientY
  //   ];
  // }, true);
  // document.addEventListener('mouseup', function() {
  //   isDown = false;

  // }, true);
  // document.addEventListener('mousemove', (e) => {
  //   e.preventDefault();
  //   if (isDown) {
  //     let mousePosition = {
  //       x : e.clientX,
  //       y : e.clientY
  //     };
  //     div.style.left = (mousePosition.x + offset[0]) + 'px';
  //     div.style.top = (mousePosition.y + offset[1]) + 'px';
  //   }
  // });
  // btn.addEventListener("click", (e) => {
  //   getPixels();
  // })
  function getPixels() {
    const style = canvas.style
    console.log(canvas);
    console.log(ctx.getImageData(0, 0, 300, 300));
    return ctx.getImageData(style.left, style.top, 300, 300);
  };
  btn_toggle_closed.addEventListener("click", (e) => {
    if (closed) {
      canvas_container.style.left = 0 + "px"
    } else {
      canvas_container.style.left = -322 + "px"
    }
    closed = !closed
  })
  btn_send.addEventListener("click", (e) => {
    alert("まだできてません...")
  })
});
</script>
<svelte:head>
  <!-- This page is created using https://github.com/mukti107/Method-Draw-->
</svelte:head>
<div id="canvas_container" bind:this={canvas_container}>
  <span>お絵描き</span>
  <canvas id="canvas" bind:this={canvas}></canvas>
  <!-- <button bind:this={btn}>dataurl</button> -->
  <label for="name">星座名</label>
  <input id="name" />
  <button bind:this={btn_send}>生成</button>
  <button id="btn_toggle_closed" bind:this={btn_toggle_closed}>{closed? ">": "<"}</button>
</div>
<style>
#canvas_container {
  border: 2px solid black;
  position: absolute;
  width: 300px;
  height: 342px;
  padding: 10px;
  left: 0px;
  top: 10px;
  background-color: rgba(244, 244, 244, 0.5);
  z-index: 1;
  transition: all 0.3s ease;
}
#canvas {
  border: 2px solid black;
  width: 300px;
  height: 300px;
}
#btn_toggle_closed {
  position: absolute;
  top: 0;
  right: -1.2rem;
  border: none;
  background: rgb(244, 244, 244, 0.5);
  width: 1.2rem;
  height: 1.2rem;
  color: white;
}
#btn_toggle_closed:hover {
  background: #333
}
</style>
