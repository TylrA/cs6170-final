package f;

import java.awt.image.BufferedImage;

public class ContrastFilter implements ImageFilter {

	@Override
	public BufferedImage filter(BufferedImage input) {
		// TODO Auto-generated method stub
		BufferedImage result = new BufferedImage(input.getWidth(), input.getHeight(), BufferedImage.TYPE_INT_RGB);
		int pixel, r, g, b;
		
		for (int y = 0; y < input.getHeight(); y++)
			for (int x = 0; x < input.getWidth(); x++) {
				pixel = input.getRGB(x, y);
				
				r = (pixel >> 16) & 0xff;
				g = (pixel >> 8) & 0xff;
				b = pixel & 0xff;
			}
		return null;
	}

}
