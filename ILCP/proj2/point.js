// here's a little point class I made to help with some geometry


var point = function (x,y) {
	this.x = x || 0;
	this.y = y || 0;
}

point.prototype = {
	
	
	// returns a vector (a point) pointing from this point to other point p
	pointTo : function(p) {
		return new point( p.x - this.x, p.y - this.y );
	},
		
	heading: function() {
		return Math.atan2(this.y,this.x);
	},
	
	// increases it by radians and degrees;
	plusEqPolar : function(dist, ang){
		this.x += dist*Math.cos(ang);
		this.y += dist*Math.sin(ang);
	},
	
	length: function() {
	  return Math.sqrt(Math.pow(this.x, 2), Math.pow(this.y, 2))
	}
	
}

