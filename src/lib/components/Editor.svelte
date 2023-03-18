<script>
// @ts-nocheck
import { onMount } from 'svelte';
export let canvas;
export let png;
const canvas_size = {x: 300, y: 300};
onMount(() => {
  const canvas = document.getElementById("canvas")
  let isDrawing = false;
  let x = 0;
  let y = 0;
  var ctx = canvas.getContext('2d');
  ctx.strokeStyle = "#FFFF80";
  ctx.lineWidth = 3;
  canvas.addEventListener('mousedown', e => {
    isDrawing = true;
    x = e.offsetX;
    y = e.offsetY;
    ctx.moveTo(x, y);
    ctx.lineTo(x, y);
    ctx.stroke();
  });
  canvas.addEventListener('mousemove', e => {
    x = e.offsetX;
    y = e.offsetY;
    if (isDrawing && !isDown) {
      ctx.lineTo(x, y);
      ctx.stroke();
    }
  });
  canvas.addEventListener('mouseup', e => {
    if (isDrawing) {
      x = e.offsetX;
      y = e.offsetY;
      ctx.lineTo(x, y);
      ctx.stroke();
      isDrawing = false;
    }
    png=canvas.toDataURL("image/png", 1)
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
  function getPixels() {
    return ctx.getImageData(0, 0, canvas_size.x, canvas_size.y);
  };
  // document.getElementById("enable_pen").addEventListener("click", () => {
  //   ctx.strokeStyle = "#FED75D"
  //   ctx.globalCompositeOperation = 'source-over'
  // })
  // document.getElementById("enable_eraser").addEventListener("click", () => {
  //   ctx.globalCompositeOperation = 'destination-out'
  // })
  // document.getElementById("all_eraser").addEventListener("click", () => {
  //   ctx.clearRect(0, 0, canvas.width, canvas.height);
  // })
});
</script>
<svelte:head>
  <!-- This page is created using https://github.com/mukti107/Method-Draw-->
</svelte:head>
<div>
  <canvas id="canvas" width="{canvas_size.x}px" height="{canvas_size.y}px" bind:this={canvas}></canvas>
  <!-- <button id="enable_pen">ペン</button>
  <button id="enable_eraser">消しゴム</button>
  <button id="all_eraser">全消し</button> -->
</div>
<style>
#canvas {
  border: 2px solid black;
}
</style>
