<script>
import { onMount } from 'svelte';
export let canvas;
export let div;
let canvas_container
let btn;
let ctx;
let x_btn;
onMount(() => {
  let isDrawing = false;
  let x = 0;
  let y = 0;
  ctx = canvas.getContext('2d');
  document.addEventListener('mousedown', e => {
    isDrawing = true;
    x = e.offsetX;
    y = e.offsetY/2;
    ctx.moveTo(x, y);
    ctx.lineTo(x, y);
    ctx.stroke();
  });
  window.addEventListener('mousemove', e => {
    x = e.offsetX;
    y = e.offsetY/2;
    if (isDrawing && !isDown) {
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  });
  document.addEventListener('mouseup', e => {
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
  btn.addEventListener("click", (e) => {
    getPixels();
  })
  function getPixels() {
    const style = canvas.style
    console.log(canvas);
    console.log(ctx.getImageData(0, 0, 300, 300));
    return ctx.getImageData(style.left, style.top, 300, 300);
  };
  x_btn.addEventListener("click", (e) => {
    canvas_container.style.visibility = "hidden"
  })
});
</script>
<svelte:head>
  <!-- This page is created using https://github.com/mukti107/Method-Draw-->
</svelte:head>
<div id="canvas_container" bind:this={canvas_container}>
  <canvas id="canvas" bind:this={canvas}></canvas>
  <button bind:this={btn}>dataurl</button>
  <input />
  <button bind:this={btn}>send</button>
  <button id="x_btn" bind:this={x_btn}>x</button>
</div>
<style>
#canvas_container {
  border: 2px solid black;
  position: absolute;
  width: 300px;
  height: 300px;
  padding: 20px;
  right: left( 95vw - 300px );
  top: 10px;
  background-color: rgba(244, 244, 244, 0.5);
  z-index: 1;
}
#canvas {
  border: 2px solid black;
  width: 300px;
  height: 300px;
}
#x_btn {
  position: absolute;
  top: 0;
  right: 0;
  border: none;
  border-radius: 50%;
  background: none;
  /* font-size: 1.2rem; */
  width: 1.2rem;
  height: 1.2rem;
}
#x_btn:hover {
  background: #ccc
}
</style>
