// The goal here is to make a tiny little library for storing/manipulating
// 3d shapes in JS, in a class called 'Shape'. The Shape class will be used
// for the initial loading of shapes (from OBJ files or hard-coded data) into
// webgl

var icos;
// assumes 'vertices' and 'faces' are each either arrays of arrays (one array for each v/f), or flat 1-d arrays representing 3-vectors. In either case, the Shape's V and F are stored as arrays of 3-arrays.
function Shape (vertices, faces) {
	// typeof(array)='object' in JS
	if (typeof(vertices[0])=='object'){
		this.V = vertices;
	} else {
		this.V = [];
		for (i=0; i<vertices.length; i+=3){
			this.V.push(vertices.slice(i,i+3));
		}
	} if (typeof(faces[0])=='object'){
		this.F = faces;
	} else {
		this.F = [];
		for (i=0;i<faces.length;i+=3){
			this.F.push(faces.slice(i,i+3));
		}
	}
}

// LOAD SHAPE FROM OBJ: allows plain names, name.obj (assumed to be in the same directory as index.html), or full web link starting with http


var OBJ_name_parse = function(fname) {
    fullname = fname;
    if (fname.substring(fname.length-4,fname.length) != '.obj') {
        fullname = fullname.concat('.obj');
    }
    // remember, a user of the webpage doesn't want JS to open a local file, but one hosted somewhere online (assumed to be in the current directory on my page if not specified). Assumed: any url would start with http
    if (fname.substring(0,4) != 'http') {
        var loc = window.location.pathname; 
        var dir = loc.substring(0, loc.lastIndexOf('/'));
        fullname = dir.concat('/'.concat(fullname));
    }
    return fullname
}


// how do I make the output of this function the output of the callback function
// below??

var get_OBJ_string = function(fname, saveStr) {
    fullname = OBJ_name_parse(fname);
    var ret = $.get(fullname, function(data) {
        saveStr = data.toString();
        icos_string = saveStr;
        console.log('in ret saveStr = ' + saveStr);
        return 6
        
    })
    console.log('ret = ' + ret);
}

var icos_string = '';
get_OBJ_string('icosahedron', icos_string);
console.log('icos_string = ' + icos_string);
setTimeout(function(){ console.log('@3 secs icos_string = ' + icos_string); }, 3000);

var fromOBJ = function(fname) {
    
    fullname = OBJ_name_parse(fname);
    var out2 = jQuery.get(fullname, function(data) {
        //console.log(data);
        var text = data.toString();
        var lines = text.split('\n');
        var vertices = [];
        var faces = [];
        // adds vertices and faces, and ignores all else for now
        for( i=0; i<lines.length; i++ ){
            var words = lines[i].split(/[ ,]+/); //regexp for any num of commas/spaces
            var firstLetter = words[0][0];
            if (firstLetter == 'v' || firstLetter == 'V') {
                var vect = [];
                for( j=1;j<words.length;j++ ){
                    vect[j-1] = parseFloat(words[j]);    
                }
                vertices.push(vect);
            } else if (firstLetter == 'f' || firstLetter == 'F') {
                var fac = [];
                for( j=1;j<words.length;j++ ){
                    fac[j-1] = parseInt(words[j]);    
                }
                faces.push(fac);
            }
        };
        var out = new Shape(vertices, faces);
        console.log('out is a ' + out);
        
        //console.log('inner: '+out.V);
        icos = out;
        return out;
    });
    console.log('out2 is a ' + out2);

    return out2;
};


// in efforts to isolate the asynchronous ajax section of the code:
// fstring is expected to be the OBJ file contents in string form
var fromOBJ_string = function(fstring) {
        var lines = fstring.split('\n');
        var vertices = [];
        var faces = [];
        // adds vertices and faces, and ignores all else for now
        for( i=0; i<lines.length; i++ ){
            var words = lines[i].split(/[ ,]+/); //regexp for any num of commas/spaces
            var firstLetter = words[0][0];
            if (firstLetter == 'v' || firstLetter == 'V') {
                var vect = [];
                for( j=1;j<words.length;j++ ){
                    vect[j-1] = parseFloat(words[j]);    
                }
                vertices.push(vect);
            } else if (firstLetter == 'f' || firstLetter == 'F') {
                var fac = [];
                for( j=1;j<words.length;j++ ){
                    fac[j-1] = parseInt(words[j]);    
                }
                faces.push(fac);
            }
        };
        var out = new Shape(vertices, faces);
        console.log('out is a ' + out);
        
        //console.log('inner: '+out.V);
        icos = out;
        return out;
    console.log('out2 is a ' + out2);

    return out2;
};





function get_OBJ_V_F(fname) {
    fullname = fname;
    if (fname.substring(fname.length-4,fname.length) != '.obj') {
        fullname = fullname.concat('.obj');
    }
    // remember, a user of the webpage doesn't want JS to open a local file, but one hosted somewhere online (assumed to be in the current directory on my page if not specified). Assumed: any url would start with http
    if (fname.substring(0,4) != 'http') {
        var loc = window.location.pathname; 
        var dir = loc.substring(0, loc.lastIndexOf('/'));
        fullname = dir.concat('/'.concat(fullname));
    }

    return jQuery.get(fullname, function(data) {
        var text = data.toString();
        var lines = text.split('\n');
        var vertices = [];
        var faces = [];
        // adds vertices and faces, and ignores all else for now
        for( i=0; i<lines.length; i++ ){
            var words = lines[i].split(/[ ,]+/); //regexp for any num of commas/spaces
            var firstLetter = words[0][0];
            if (firstLetter == 'v' || firstLetter == 'V') {
                var vect = [];
                for( j=1;j<words.length;j++ ){
                    vect[j-1] = parseFloat(words[j]);    
                }
                vertices.push(vect);
            } else if (firstLetter == 'f' || firstLetter == 'F') {
                var fac = [];
                for( j=1;j<words.length;j++ ){
                    fac[j-1] = parseInt(words[j]);    
                }
                faces.push(fac);
            }
        };
        return [vertices, faces];
    });
}


function shapeFromOBJ_url(url) {
    
};


// Shape.color should be a flat array of rgba values (4 array entries) for each vertex
Shape.prototype.setUniformColor = function(r,g,b,a) {
	this.color = [];
	var col = [r,g,b,a];
	for(i=0;i<this.V.length;i++){
		this.color=this.color.concat(col);
	}
};

Shape.prototype.setRandomGreyscale = function() {
	this.color = [];
	var l; //for lightness
	for(i=0;i<this.V.length;i++){
		l = Math.random(); 
		this.color = this.color.concat([l,l,l,1])
	}
};

Shape.prototype.getInfo = function() {
	return "Shape with " + this.V.length + " vertices and " + this.F.length + " faces.";
};

Shape.prototype.toString = function() {
	return this.getInfo();
};

Shape.prototype.valueOf = function() {
	return this.getInfo();
};

Shape.prototype.verbose = function() {
	var outS = "VERTICES:\n";
	for (i=0;i<this.V.length;i++){
		outS = outS.concat(Str(this.V[i])+',\n');
	}
	outS = outS.concat('FACES:\n')
	for (i=0;i<this.F.length;i++){
		outS = outS.concat(Str(this.F[i])+',\n');
	}
	return outS;
};

// helpful
function flatten(twoDarray){
	return twoDarray.reduce(function(a, b) {
	  return a.concat(b);
	});
};


// Aimed to recreate the functionality of the initBuffers() function. takes a gl instance argument
Shape.prototype.initBuffs = function(gl) {
	
    this.positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
	
	// hands vertex position data to webGL
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(flatten(this.V)), gl.STATIC_DRAW);
	// these parameters are used elsewhere in script.js
    this.positionBuffer.itemSize = 3;
    this.positionBuffer.numItems = this.V.length;
	
	this.colorBuffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
	
	// checks to see if color has been set; else makes the shape gray
	if(typeof this.color === 'undefined') {this.setUniformColor(0.5,0.5,0.5,0)}
	
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.color), gl.STATIC_DRAW);
    this.colorBuffer.itemSize = 4;
    this.colorBuffer.numItems = this.color.length/4;
    
	
	this.indexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.indexBuffer);
	
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(this.F)), gl.STATIC_DRAW);
	// not sure why the following two are "unflattened," but they were in the example
    this.indexBuffer.itemSize = 1;
    this.indexBuffer.numItems = this.F.length * 3;
	
};

// replicates the shape-specific action of the drawScene() function in script.js. It's assumed that gl has already translated/rotated and whatever, and all that's left is to draw the shape
Shape.prototype.drawShape = function(gl) {
	
	gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
	// shaderProgram is inherited from script.js. Assumes positions are 3-vectors
	gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, this.positionBuffer.itemSize, gl.FLOAT, false, 0, 0);
	
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
    gl.vertexAttribPointer(shaderProgram.vertexColorAttribute, this.colorBuffer.itemSize, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.indexBuffer);
    setMatrixUniforms();
    gl.drawElements(gl.TRIANGLES, this.indexBuffer.numItems, gl.UNSIGNED_SHORT, 0);
	
};


var cubeV = [
        // Front face
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,

        // Back face
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0, -1.0, -1.0,

        // Top face
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0, -1.0,

        // Bottom face
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        // Right face
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0,  1.0,  1.0,
         1.0, -1.0,  1.0,

        // Left face
        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0
    ];
	
var cubeF = [
	0, 1, 2,      0, 2, 3,    // Front face
	4, 5, 6,      4, 6, 7,    // Back face
	8, 9, 10,     8, 10, 11,  // Top face
	12, 13, 14,   12, 14, 15, // Bottom face
	16, 17, 18,   16, 18, 19, // Right face
	20, 21, 22,   20, 22, 23  // Left face
];
var cubit = new Shape(cubeV, cubeF);
cubit.setRandomGreyscale();
console.log('cubit is a ' + cubit.toString());
var icos = fromOBJ('icosahedron');;
console.log('icos is a ' + icos.toString());
/*
var icos_data = jQuery.get(fullname, function(data) {
        console.log(data);
        var text = data.toString();
*/


