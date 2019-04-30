package f;

import java.awt.image.BufferedImage;

public class RedBlueFilter implements ImageFilter {

	public RedBlueFilter() {
		
	}
	
	@Override
	public BufferedImage filter(BufferedImage input) {
		// TODO Auto-generated method stub
		return null;
	}

	/**
	 * Blurs image by averaging each pixel with its 8 neighbors.
	 */
	public BufferedImage filterEdgeWrap(BufferedImage i) {

		BufferedImage result = new BufferedImage(i.getWidth(), i.getHeight(), i.getType());
		
		int pixel;
		int redValue, greenValue, blueValue, v;

		for(int y = 0; y < i.getHeight(); y++)
			for(int x = 0; x < i.getWidth(); x++) {
				pixel = i.getRGB(x, y);
				
				redValue = (pixel >> 16) & 0xff;
				greenValue = (pixel >> 8) & 0xff;
				blueValue = (pixel >> 0) & 0xff;
				
				v = ((0xff - blueValue) + redValue + greenValue) / 3;
				v = (v << 16) | (v << 8) | v;
				result.setRGB(x, y, v);
			}
		
		return result;
	}
}
