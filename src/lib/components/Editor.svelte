<script>
// @ts-nocheck
import { onMount } from 'svelte';
export let canvas;
export let png;
let canvas_container
export let im_file;
let closed = false;
const canvas_size = {x: 300, y: 300};
onMount(() => {
  const canvas = document.getElementById("canvas")
  let isDrawing = false;
  let x = 0;
  let y = 0;
  var ctx = canvas.getContext('2d');
  ctx.strokeStyle = "#fff";
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
  document.getElementById("btn_toggle_closed").addEventListener("click", (e) => {
    const rect = canvas_container.getBoundingClientRect();
    if (closed) {
      canvas_container.style.left = 0 + "px"
    } else {
      canvas_container.style.left = -rect.width + "px"
    }
    closed = !closed
  })
  document.getElementById("send").addEventListener("click", () => {
    let image_data = getPixels();
    const data = image_data.data
    const drawn_pixels = [];
    const drawn_pixel_ids = [];
    var row = 0;
    for (let i=3; i <= data.length; i+=4) {
      let pixel_number = Math.floor(i/4);
      if (pixel_number>=canvas_size.x*row) { drawn_pixels.push([]); row += 1; }
      if (data[i] !== 0) {
        drawn_pixels[row-1].push(1)
        drawn_pixel_ids.push(pixel_number)
      } else {
        drawn_pixels[row-1].push(0)
      }
    }
    png=canvas.toDataURL("image/png", 1)
    console.log(png);
  })
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
<div id="canvas_container" bind:this={canvas_container}>
  <span>お絵描き</span>
  <canvas id="canvas" width="{canvas_size.x}px" height="{canvas_size.y}px" bind:this={canvas}></canvas>
  <!-- <button bind:this={btn}>dataurl</button> -->
  <label for="name">星座名</label>
  <input id="name" />
  <button id="send">生成</button>
  <input type="file" accept="image/png" bind:this={im_file}>
  <button id="btn_toggle_closed">{closed? ">": "<"}</button>
  <!-- <button id="enable_pen">ペン</button>
  <button id="enable_eraser">消しゴム</button>
  <button id="all_eraser">全消し</button> -->
</div>
<style>
#canvas_container {
  border: 2px solid black;
  position: absolute;
  width: 300px;
  height: 400px;
  padding: 10px;
  left: 0px;
  top: 10px;
  background-color: rgba(244, 244, 244, 0.5);
  z-index: 1;
  transition: all 0.3s ease;
}
#canvas {
  border: 2px solid black;
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
