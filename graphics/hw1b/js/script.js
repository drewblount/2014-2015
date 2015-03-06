// from here to about line 100 is close to copied from the tutorial on learningwebgl.com
var gl;

function initGL(canvas) {
    try {
        gl = canvas.getContext("experimental-webgl");
        gl.viewportWidth = canvas.width;
        gl.viewportHeight = canvas.height;
    } catch (e) {
    }
    if (!gl) {
        alert("Could not initialise WebGL, sorry :-(");
    }
}

// gets the shader scripts from index.html
function getShader(gl, id) {
    var shaderScript = document.getElementById(id);
    if (!shaderScript) {
        return null;
    }

    var str = "";
    var k = shaderScript.firstChild;
    while (k) {
        if (k.nodeType == 3) {
            str += k.textContent;
        }
        k = k.nextSibling;
    }

    var shader;
    if (shaderScript.type == "x-shader/x-fragment") {
        shader = gl.createShader(gl.FRAGMENT_SHADER);
    } else if (shaderScript.type == "x-shader/x-vertex") {
        shader = gl.createShader(gl.VERTEX_SHADER);
    } else {
        return null;
    }

    gl.shaderSource(shader, str);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert(gl.getShaderInfoLog(shader));
        return null;
    }

    return shader;
}

// Global var for passing to webGL
var shaderProgram;
// self-explanatory, boring and essentially copied from lessons1-4 of learningwebgl.com
function initShaders() {
    var fragmentShader = getShader(gl, "shader-fs");
    var vertexShader = getShader(gl, "shader-vs");

    shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert("Could not initialise shaders");
    }

    gl.useProgram(shaderProgram);

    shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
    gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

    shaderProgram.vertexColorAttribute = gl.getAttribLocation(shaderProgram, "aVertexColor");
    gl.enableVertexAttribArray(shaderProgram.vertexColorAttribute);

    shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
    shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
}


// the model-view matrix. Most of the matrix stuff is taken from the example code at learningwebgl.com, lessons 1-4
var mvMatrix = mat4.create();
var mvMatrixStack = [];
var pMatrix = mat4.create();

function mvPushMatrix() {
    var copy = mat4.create();
    mat4.set(mvMatrix, copy);
    mvMatrixStack.push(copy);
}

function mvPopMatrix() {
    if (mvMatrixStack.length == 0) {
        throw "Invalid popMatrix!";
    }
    mvMatrix = mvMatrixStack.pop();
}


function setMatrixUniforms() {
    gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, false, pMatrix);
    gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, mvMatrix);
}


function degToRad(degrees) {
    return degrees * Math.PI / 180;
}

// everything from here on was written or heavily modified by me


// angles of rotation for different shapes
var r1 = 0;
var r2 = 0;
var r3 = 0;

function drawScene() {
	resizeCanvas();
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

	// gives a nice perspective
    // 2/18/15:: I don't quite understand what's up here
    mat4.perspective(45, gl.viewportWidth / gl.viewportHeight, 0.1, 100.0, pMatrix);

    mat4.identity(mvMatrix);

	// moves to position to draw first shape, rotates and draws it.

	// now draw two more cubes farther back
    if (drawIcos) {
        icos.drawShape(gl);
    }
    mat4.translate(mvMatrix, [0.0, 0.0, -10.0]);
    mvPushMatrix();
    mat4.rotate(mvMatrix, degToRad(r2), [1, 1, 1]);
	cubit.drawShape(gl);
    mvPopMatrix();
	

}

// animate uses Date().getTime() to ensure that animated movement happens at a regular speed independent of framerate.
var lastTime = 0;
function animate() {
    var timeNow = new Date().getTime();
    if (lastTime != 0) {
        var elapsed = timeNow - lastTime;

        r1 += (180 * elapsed) / 1000.0;
        r2 -= (75 * elapsed) / 1000.0;
		r3 += (30 * elapsed) / 1000.0;
    }
    lastTime = timeNow;
}

// called once per frame
function tick() {
	// arranges for tick to be called again
    requestAnimFrame(tick);
	// draws everything
    drawScene();
	// changes vars for next frame
    animate();
}

var canvas = document.getElementById("webGL-canvas");
function webGLStart() {
	resizeCanvas();
    initGL(canvas);
    initShaders();
	cubit.initBuffs(gl);	
    //icos.initBuffs(gl);	   

    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.enable(gl.DEPTH_TEST);

    tick();
	
}

function resizeCanvas() {
   // only change the size of the canvas if the size it's being displayed has changed.
	var width = $(window).width();
	var height = $(window).height();
	
   if (canvas.width != width || canvas.height != height) {
	   canvas.width = width;
       canvas.height = height;	 
   }
}

// is this good practice?
var drawIcos = false;


$('body').click(function(){
    //icos = 
    alert('outer: ' + icos.V);
    drawIcos = true;
});





