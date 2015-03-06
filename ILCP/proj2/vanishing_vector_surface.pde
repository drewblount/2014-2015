
     int originX, originY;
     
     boolean pause = true;
     
     void setup() {
       size(window.innerWidth, window.innerHeight);
       stroke(255);
       background(192, 64, 0);
       originX = width/3;
       originY = height/4;
     } 
	 

     void draw() {
       if (!pause) {
         line(originX, originY, mouseX, mouseY);
       }  
     }
     
     void mousePressed() {
       if (mouseButton == LEFT) {
         pause = !pause;
       }
       if (mouseButton == RIGHT) {
         originX = mouseX;
         originY = mouseY;
       }
     }
     void keyPressed() {
       if (key == ' ') {
         background(192, 64, 0);         
       }
       if (key == 's' || key == 'S') {
         saveFrame("vanishing_vector_surface_####.png");
       }
	   if (key == 'r' || key == 'R') {
		   setup()
	   }
     }

