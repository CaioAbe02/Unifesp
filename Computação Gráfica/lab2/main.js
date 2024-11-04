function main(){
  const canvas = document.querySelector("#canvas");
  const gl = canvas.getContext('webgl', { preserveDrawingBuffer: true });

  if (!gl) {
      throw new Error('WebGL not supported');
  }

  var vertexShaderSource = document.querySelector("#vertex-shader-2d").text;
  var fragmentShaderSource = document.querySelector("#fragment-shader-2d").text;

  var vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  var fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  var program = createProgram(gl, vertexShader, fragmentShader);

  gl.useProgram(program);

  const positionBuffer = gl.createBuffer();

  const positionLocation = gl.getAttribLocation(program, `position`);
  gl.enableVertexAttribArray(positionLocation);
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

  const matrixUniformLocation = gl.getUniformLocation(program, `matrix`);
  const colorUniformLocation = gl.getUniformLocation(program, `color`);
  const pointSizeUniformLocation = gl.getUniformLocation(program, `pointSize`);

  let matrix = [
      2/canvas.width, 0, 0, 0,
      0, -2/canvas.height, 0, 0,
      0, 0, 0, 0,
      -1, 1, 0, 1
  ];
  gl.uniformMatrix4fv(matrixUniformLocation, false, matrix);

  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.clearColor(1.0, 1.0, 1.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);
  let positionVector = [canvas.width/2,canvas.height/2];
  gl.bindBuffer(gl.ARRAY_BUFFER,positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positionVector), gl.STATIC_DRAW);
  let colorVector = [0.0,0.0,1.0];
  gl.uniform3fv(colorUniformLocation,colorVector);

  let pointSizeFloat = 5.0;
  gl.uniform1f(pointSizeUniformLocation, pointSizeFloat);

  canvas.addEventListener("mousedown",mouseClick,false);

  let x = canvas.width / 2;
  let y = canvas.height / 2;
  let mode = 'line';
  let color_mode = true;
  let count = 1;
  let point0 = [x, y];
  let point1 = [x, y];
  let point2 = [x, y];

  function mouseClick(event) {
    count += 1;
    x = event.offsetX;
    y = event.offsetY;
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([x,y]), gl.STATIC_DRAW);

    if (mode == 'line') {
      if (count == 2) {
        point1 = [x, y];
        drawLine(point0, point1)
      }
      else {
        gl.clear(gl.COLOR_BUFFER_BIT);
        point0 = [x, y];
        point1 = [x, y];
        count = 1;
      }
    }
    else if (mode == 'triangle') {
      if (count == 2) {
        point1 = [x, y];
      }
      else if (count == 3) {
        point2 = [x, y];
        drawLine(point0, point1);
        drawLine(point1, point2);
        drawLine(point0, point2);
      }
      else if (count > 3) {
        gl.clear(gl.COLOR_BUFFER_BIT);
        point0 = [x, y];
        count = 1;
      }
    }
    drawPoint();
    console.log(point0, point1, point2);
  }

  const bodyElement = document.querySelector("body");
  bodyElement.addEventListener("keydown",keyDown,false);

  function keyDown(event){
    switch(event.key){
      case "0":
        if (color_mode) {
          colorVector = [0.0,0.0,0.0];
          break;
        }
        break;
      case "1":
        if (color_mode) {
          colorVector = [1.0,0.0,0.0];
          break;
        }
        pointSizeFloat = 2.0;
        break;
      case "2":
        if (color_mode) {
          colorVector = [0.0,1.0,0.0];
          break;
        }
        pointSizeFloat = 3.0;
        break;
      case "3":
        if (color_mode) {
          colorVector = [0.0,0.0,1.0];
          break;
        }
        pointSizeFloat = 4.0;
        break;
      case "4":
        if (color_mode) {
          colorVector = [1.0,1.0,0.0];
          break;
        }
        pointSizeFloat = 5.0;
        break;
      case "5":
        if (color_mode) {
          colorVector = [0.0,1.0,1.0];
          break;
        }
        pointSizeFloat = 6.0;
        break;
      case "6":
        if (color_mode) {
          colorVector = [1.0,0.0,1.0];
          break;
        }
        pointSizeFloat = 7.0;
        break;
      case "7":
        if (color_mode) {
          colorVector = [1.0,0.5,0.5];
          break;
        }
        pointSizeFloat = 8.0;
        break;
      case "8":
        if (color_mode) {
          colorVector = [0.5,1.0,0.5];
          break;
        }
        pointSizeFloat = 9.0;
        break;
      case "9":
        if (color_mode) {
          colorVector = [0.5,0.5,1.0];
          break;
        }
        pointSizeFloat = 10.0;
        break;
      case "r":
      case "R":
        mode = 'line';
        break;
      case "t":
      case "T":
        mode = 'triangle';
        break;
      case "e":
      case "E":
        color_mode = false;
        break;
      case "k":
      case "K":
        color_mode = true;
        break;
    }
    gl.uniform3fv(colorUniformLocation,colorVector);
    gl.uniform1f(pointSizeUniformLocation, pointSizeFloat);
    if (mode == 'line') {
      drawPoint();
      drawLine(point0, point1);
    }
    else if (mode == 'triangle' && count == 3) {
      drawLine(point0, point1);
      drawLine(point1, point2);
      drawLine(point0, point2);
    }
  }

  function drawPoint(){
    gl.drawArrays(gl.POINTS, 0, 1);
  }

  function drawLine(vertex0, vertex1) {
    const linePoints = bresenhamLine(vertex0[0], vertex0[1], vertex1[0], vertex1[1]);
    const vertices = new Float32Array(linePoints.flat());

    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

    gl.drawArrays(gl.POINTS, 0, linePoints.length);
  }

  function bresenhamLine(x0, y0, x1, y1) {
    const points = [];
    let dx = Math.abs(x1 - x0);
    let dy = Math.abs(y1 - y0);
    let sx = x0 < x1 ? 1 : -1;
    let sy = y0 < y1 ? 1 : -1;
    let err = dx - dy;

    while (true) {
        points.push([x0, y0]);

        if (Math.abs(x0 - x1) < 1 && Math.abs(y0 - y1) < 1) break;
        let e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x0 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y0 += sy;
        }
    }
    return points;
  }

  drawPoint();
}

function createShader(gl, type, source) {
  var shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
  if (success) {
    return shader;
  }

  console.log(gl.getShaderInfoLog(shader));
  gl.deleteShader(shader);
}

function createProgram(gl, vertexShader, fragmentShader) {
  var program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  var success = gl.getProgramParameter(program, gl.LINK_STATUS);
  if (success) {
    return program;
  }

  console.log(gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
}

main();