// here's a little point class I made to help with some geometry


var point = function (x,y) {
	this.x = x || 0;
	this.y = y || 0;
}

  // offsets help with framing the window
var xl = 60;
var xr = 0;
var yt = 40;
var yb = 10;
var buffer = 100;
var posbuff = buffer + 100;
var numer = 100;
 


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
	  return Math.sqrt(Math.pow(this.x, 2), Math.pow(this.y, 2));
	},
	
	
	
	
	avoidWall: function() {
	  
	  if (this.x < buffer+xl) {
	  	this.x += numer/(this.x-xl);
	  }
	  if (this.x > $(window).width() - posbuff - xr) {
	  	this.x -= numer/($(window).width() - this.x + xr);
	  }
	  if (this.y < buffer+yt) {
	  	this.y += numer/(this.y-yt);
	  }
	  if (this.y > $(window).height() - posbuff - yt) {
	  	this.x -= numer/($(window).height() - this.y + yt);
	  }
	},
	
	correctEdge: function() {
		if (this.x < 0){
			this.x = this.x * -1;
		}
		if (this.x > $(window).width()) {
			this.x -= 2*(this.x-$(window).width());
		}
		if (this.y < 0){
			this.y = this.y * -1;
		}
		if (this.y > $(window).height()) {
			this.y -= 2*(this.y-$(window).height());
		}

	}
	
}

