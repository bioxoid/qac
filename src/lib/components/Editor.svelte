<script>
// @ts-nocheck
import { onMount } from 'svelte';
export let png;
export let disable;
const canvas_size = {x: 300, y: 300};
onMount(() => {
  const canvas = document.getElementById("canvas")
  let mode = "pen";
  let isDrawing = false;
  let isDown = false;
  let x = 0;
  let y = 0;
  var ctx = canvas.getContext('2d');
  ctx.strokeStyle = "#FFFF80";
  ctx.lineWidth = 3;
  canvas.addEventListener('mousedown', e => {
    switch (mode) {
      case "pen":
      case "eraser":
        isDrawing = true;
        x = e.offsetX;
        y = e.offsetY;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y);
        ctx.stroke();
        break;
      case "fill":
        break;
    }
  });
  canvas.addEventListener('mousemove', e => {
    switch (mode) {
      case "pen":
      case "eraser":
        x = e.offsetX;
        y = e.offsetY;
        if (isDrawing && !isDown) {
          ctx.lineTo(x, y);
          ctx.stroke();
        }
        break;
      case "fill":
        break;
      }
  });
  canvas.addEventListener('mouseup', e => {
    switch (mode) {
      case "pen":
      case "eraser":
        if (isDrawing) {
          x = e.offsetX;
          y = e.offsetY;
          ctx.lineTo(x, y);
          ctx.stroke();
          isDrawing = false;
        }
        break;
      case "fill":
        x = e.offsetX;
        y = e.offsetY;
        floodFill(ctx, x, y, [255, 255, 128, 255])
        break;
    }
    png=canvas.toDataURL("image/png", 1)
  });
  function floodFill(ctx, x, y, fillColor) {
    // read the pixels in the canvas
    const imageData = ctx.getImageData(0, 0, ctx.canvas.width, ctx.canvas.height);
    // get the color we're filling
    const targetColor = getPixel(imageData, x, y);
    // check we are actually filling a different color
    if (!colorsMatch(targetColor, fillColor)) {
      fillPixel(imageData, x, y, targetColor, fillColor);
      // put the data back
      ctx.putImageData(imageData, 0, 0);
    }
  }
  function colorsMatch(a, b) {
    return a[0] === b[0] && a[1] === b[1] && a[2] === b[2] && a[3] === b[3];
  }
  function getPixel(imageData, x, y) {
    if (x < 0 || y < 0 || x >= imageData.width || y >= imageData.height) {
      return [-1, -1, -1, -1];  // impossible color
    } else {
      const offset = (y * imageData.width + x) * 4;
      return imageData.data.slice(offset, offset + 4);
    }
  }
  function setPixel(imageData, x, y, color) {
    const offset = (y * imageData.width + x) * 4;
    imageData.data[offset + 0] = color[0];
    imageData.data[offset + 1] = color[1];
    imageData.data[offset + 2] = color[2];
    imageData.data[offset + 3] = color[0];
  }
  function fillPixel(imageData, x, y, targetColor, fillColor) {
    const currentColor = getPixel(imageData, x, y);
    if (colorsMatch(currentColor, targetColor)) {
      setPixel(imageData, x, y, fillColor);
      fillPixel(imageData, x + 1, y, targetColor, fillColor);
      fillPixel(imageData, x - 1, y, targetColor, fillColor);
      fillPixel(imageData, x, y + 1, targetColor, fillColor);
      fillPixel(imageData, x, y - 1, targetColor, fillColor);
    }
  }
  document.getElementById("enable_pen").addEventListener("click", () => {
    mode = "pen"
    ctx.strokeStyle = "#FFFF80"
    ctx.globalCompositeOperation = 'source-over'
  })
  document.getElementById("enable_eraser").addEventListener("click", () => {
    mode = "eraser"
    ctx.globalCompositeOperation = 'destination-out'
  })
  document.getElementById("enable_fill").addEventListener("click", () => {
    mode = "fill"
  })
  document.getElementById("all_eraser").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  })
});
</script>
<svelte:head>
  <!-- This page is created using https://github.com/mukti107/Method-Draw-->
</svelte:head>
<div style="pointer-events: {disable? "none" : "auto"}">
  <canvas id="canvas" width="{canvas_size.x}px" height="{canvas_size.y}px"></canvas>
  <button id="enable_pen">ペン</button>
  <button id="enable_eraser">消しゴム</button>
  <button id="all_eraser">全消し</button>
  <button id="enable_fill">塗りつぶし</button>
</div>
<style>
#canvas {
  border: 2px solid black;
}
</style>
