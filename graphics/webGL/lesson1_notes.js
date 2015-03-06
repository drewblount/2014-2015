
// global var for webGL context
var gl;
function initGL(canvas) {
    try {
		// initialize the context. (At some point the 'experimental-' will be)
        gl = canvas.getContext("experimental-webgl");
		// below 2lines utilize JS's flexibility w/ defining new object properties
		// these are later used at beginning of drawScene
        gl.viewportWidth = canvas.width;
        gl.viewportHeight = canvas.height;
    } catch (e) {
    }
    if (!gl) {
        alert("Could not initialise WebGL, sorry :-(");
    }
}


// this function lets us load shaders as script files, just like
// loading a .js file in html
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


// SHADERS: "The reason that we’re introducing shaders in what is meant to be a simple WebGL example (they’re at least “intermediate” in OpenGL tutorials) is that we use them to get the WebGL system, hopefully running on the graphics card, to apply our model-view matrix and our projection matrix to our scene without us having to move around every point and every vertex in (relatively) slow JavaScript."


var shaderProgram;

function initShaders() {
	// "each program can hold one fragment and one vertex shader"
    var fragmentShader = getShader(gl, "shader-fs");
    var vertexShader = getShader(gl, "shader-vs");

	// a gl "program" is a way of specifying jobs to be done on the gfx card (i.e. by webGL, not JS)
    shaderProgram = gl.createProgram();
	// links the program/shaders/gl to each other
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

	// checks the above assignment
    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert("Could not initialise shaders");
    }

	// I wonder what's the difference between linkProgram and useProgram
    gl.useProgram(shaderProgram);

	// again using JS to add a new field to an object
    shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
	// lets gl know that we'll be loading vertices, as an array, from shaderProgram.vertex...
    gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

	// storing some more attributes in the program object for convenience
    shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
    shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
}

// "model-view matrix", "projection matrix". Zero-matrices at first. Later, mat4perspective
// will take the aspect ratio and FoV args to populate pMatrix
var mvMatrix = mat4.create();
var pMatrix = mat4.create();

function setMatrixUniforms() {
    gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, false, pMatrix);
    gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, mvMatrix);
}


// buffers hold info about the shapes in the canvas
// in real applications, there wouldn't be seperate buffers
// for each shape
// buffers are stored on the graphics card!

var triangleVertexPositionBuffer;
var squareVertexPositionBuffer;

function initBuffers() {
    triangleVertexPositionBuffer = gl.createBuffer();
	// tells GL what to set the active buffer (gl.ARRAY_BUFFER)
	// (functions don't take a buffer as argument, rather, the
	// GL instance always has an active buffer)
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleVertexPositionBuffer);
    var vertices = [
         0.0,  1.0,  0.0,
        -1.0, -1.0,  0.0,
         1.0, -1.0,  0.0
    ];
	// Float32Array is passable to webGL (JS list is not)
	// this adds the vertices to the graphics card
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
	// the following two lines are adding new attributes (JS shorthand)
	// that will be useful later for remembering the implied 2darray shape of
	// the 1d buffer
    triangleVertexPositionBuffer.itemSize = 3;
    triangleVertexPositionBuffer.numItems = 3;

    squareVertexPositionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, squareVertexPositionBuffer);
    vertices = [
         1.0,  1.0,  0.0,
        -1.0,  1.0,  0.0,
         1.0, -1.0,  0.0,
        -1.0, -1.0,  0.0
    ];
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
    squareVertexPositionBuffer.itemSize = 3;
    squareVertexPositionBuffer.numItems = 4;
}


function drawScene() {
	// (will be explained more later): this tells webGL
	// the size of the canvas we're drawing on
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
	// clears the canvas in prep for drawing
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

	// overrides the default (orthographic) 3d projection
	// variables are: vert. field of view (degrees), aspect ratio, low-depth cutoff, high-depth cutoff
    mat4.perspective(45, gl.viewportWidth / gl.viewportHeight, 0.1, 100.0, pMatrix);

	// this is a translation/rotation matrix (that does nothing)
	// the matrix used to represent the current translated/rotated
	// state of the gl state-machine is the MODEL-VIEW MATRIX mvMatrix
	// the following line "moves us to an origin point from which we can move to start drawing our 3D world"
    mat4.identity(mvMatrix);
	// the above line uses "Brandon Jones’s excellent glMatrix" LA library

	// translates to a starting point for drawing the triangle
	// "multiply the given matrix by a translation matrix with the following parameters"
    mat4.translate(mvMatrix, [-1.5, 0.0, -7.0]);
	
	// loads the triangle buffer
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleVertexPositionBuffer);
	// tell webGL that the values in it are vertices. Note the itemSize attribute is being used
    gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, triangleVertexPositionBuffer.itemSize, gl.FLOAT, false, 0, 0);
	
	// much of the matrix-manipulation has been purely in JS, so the
	// following function (defined above) moves the matrices to the graphics card
    setMatrixUniforms();
	
	// "draw the array of vertices I gave you earlier as triangles, starting with item 0 in the array and going up to the numItemsth element"
    gl.drawArrays(gl.TRIANGLES, 0, triangleVertexPositionBuffer.numItems);


	// move into position for drawing the square
    mat4.translate(mvMatrix, [3.0, 0.0, 0.0]);
    gl.bindBuffer(gl.ARRAY_BUFFER, squareVertexPositionBuffer);
    gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, squareVertexPositionBuffer.itemSize, gl.FLOAT, false, 0, 0);
    setMatrixUniforms();
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, squareVertexPositionBuffer.numItems);
	// a triangle strip is a special way of specifying vertices in a shape,
	// where the first three vertices are a triangle, then vertices 2,3,4, then vertices 2,4,5 etc
}



function webGLStart() {
    var canvas = document.getElementById("lesson01-canvas");
    initGL(canvas);
    initShaders();
	// Buffers contain info about the shapes
    initBuffers();

    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.enable(gl.DEPTH_TEST);

    drawScene();
}
