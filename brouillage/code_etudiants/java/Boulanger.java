import java.io.*;
import java.awt.image.*;
import javax.imageio.*;

class Boulanger {
    
    public static Point boulanger(int x, int y, int w, int h) {
	if (x<w/2) return new Point(2*x+y%2,y/2);
	else return new Point(2*(w-1-x)+(1-y%2),h-1-y/2);
    }

    public static void transforme(BufferedImage img_src, BufferedImage img_dst, int w, int h) {
	for (int i=0; i<w; ++i)
	    for (int j=0; j<h; ++j) {
		Point p = boulanger(i,j,w,h);
		img_dst.setRGB(p.x,p.y,img_src.getRGB(i,j));
	    }
    }

    public static void main(String[] args) throws IOException {
	BufferedImage img = ImageIO.read(new File(args[0]));
	int w = img.getWidth();
	int h = img.getHeight();
	BufferedImage img2 = new BufferedImage(img.getWidth(),img.getHeight(),img.getType());
	transforme(img,img2,w,h);
	ImageIO.write(img2,"png",new File("out.png"));
    }

}