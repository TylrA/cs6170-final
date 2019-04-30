package f;

import java.awt.image.BufferedImage;

/**
 * This image filter blurs the image by averaging 3x3 pixel values.
 * @author Tyler Adams, last updated 2019-02-19.
 *
 */
public class BlurFilter implements ImageFilter {

	private int factor;
//	private boolean wrapEdges;
	
	/**
	 * Creates a new BlurFilter object with an initial blur factor of 3.
	 */
	public BlurFilter(int _factor) {//, boolean _wrapEdges) {
		if(_factor % 2 == 0)
			throw new IllegalArgumentException("Blur factor must be a positive odd number.");
		
		factor = _factor;
//		wrapEdges = _wrapEdges;
	}
	
	@Override
	/**
	 * Blurs image by averaging each pixel with its 8 neighbors.
	 */
	public BufferedImage filter(BufferedImage i) {

		BufferedImage result = new BufferedImage(i.getWidth(), i.getHeight(), i.getType());

		for(int y = 0; y < i.getHeight(); y++)
			for(int x = 0; x < i.getWidth(); x++) {
				
				// TODO: Remove this first condition. It's a last minute hack for the 5 minute presentation:
				if(y < 7 || i.getHeight() - y < 7) {
					result.setRGB(x, y, i.getRGB(x, y));
				} else {
					//Set boundaries for the pixel's neighbors.
					//High and low cutoffs will prevent the filter from trying to blur edges and corners with 8 neighbors.
					int rowLowCutOff = -(factor) / 2;
					if(y < -rowLowCutOff)
						rowLowCutOff = -y;
					
					int rowHighCutOff = (factor) / 2;
					if(y > (i.getHeight() - 1) - rowHighCutOff)
						rowHighCutOff = (i.getHeight() - 1) - y;
					
					int colLowCutOff = -(factor) / 2;
					if(x < -colLowCutOff)
						colLowCutOff = -x;
					
					int colHighCutOff = (factor) / 2;
					if(x > (i.getWidth() - 1) - colHighCutOff)
						colHighCutOff = (i.getWidth() - 1) - x;
					
					int neighbors = 0;
					int redValue = 0;
					int greenValue = 0;
					int blueValue = 0;
					
					//Add values of this pixel and all of its neighbors
					for(int colOffset = colLowCutOff; colOffset <= colHighCutOff; colOffset++) {
						for(int rowOffset = rowLowCutOff; rowOffset <= rowHighCutOff; rowOffset++) {
							
							int pixel = i.getRGB(x + colOffset, y + rowOffset);
							
							redValue += (pixel >> 16) & 0xff;
							greenValue += (pixel >> 8) & 0xff;
							blueValue += (pixel >> 0) & 0xff;
							neighbors++;
						}
					}
					
					redValue = redValue / neighbors;
					greenValue = greenValue / neighbors;
					blueValue = blueValue / neighbors;
											
					int newPixel = (redValue << 16) | (greenValue << 8) | blueValue;
					
					result.setRGB(x, y, newPixel);
				}
			}
		
		return result;
	}
	
	/**
	 * Blurs image by averaging each pixel with its 8 neighbors.
	 */
	public BufferedImage filterEdgeWrap(BufferedImage i) {

		BufferedImage result = new BufferedImage(i.getWidth(), i.getHeight(), i.getType());

		for(int y = 0; y < i.getHeight(); y++)
			for(int x = 0; x < i.getWidth(); x++) {
				
				// TODO: Remove this first condition. It's a last minute hack for the 5 minute presentation:
				if(y < 7 || i.getHeight() - y < 7) {
					result.setRGB(x, y, i.getRGB(x, y));
				} else {
					//Set boundaries for the pixel's neighbors.
					//High and low cutoffs will prevent the filter from trying to blur edges and corners with 8 neighbors.
					int rowLowCutOff = -(factor) / 2;
					if(y < -rowLowCutOff)
						rowLowCutOff = -y;
					
					int rowHighCutOff = (factor) / 2;
					if(y > (i.getHeight() - 1) - rowHighCutOff)
						rowHighCutOff = (i.getHeight() - 1) - y;
					
//					int colLowCutOff = -(factor) / 2;
//					if(x < -colLowCutOff)
//						colLowCutOff = -x;
//					
//					int colHighCutOff = (factor) / 2;
//					if(x > (i.getWidth() - 1) - colHighCutOff)
//						colHighCutOff = (i.getWidth() - 1) - x;
					
					int neighbors = 0;
					int redValue = 0;
					int greenValue = 0;
					int blueValue = 0;
					
					//Add values of this pixel and all of its neighbors
					for(int colOffset = -factor / 2; colOffset <= factor / 2; colOffset++) {
						for(int rowOffset = rowLowCutOff; rowOffset <= rowHighCutOff; rowOffset++) {
							
							int pixel = i.getRGB(mod(x + colOffset, i.getWidth()), y + rowOffset);
							
							redValue += (pixel >> 16) & 0xff;
							greenValue += (pixel >> 8) & 0xff;
							blueValue += (pixel >> 0) & 0xff;
							neighbors++;
						}
					}
					
					redValue = redValue / neighbors;
					greenValue = greenValue / neighbors;
					blueValue = blueValue / neighbors;
											
					int newPixel = (redValue << 16) | (greenValue << 8) | blueValue;
					
					result.setRGB(x, y, newPixel);
				}
			}
		
		return result;
	}
	
	/**
	 * Sets the blur factor of the filter. This is the dimension of the box surrounding a pixel, from which an average will be produced.
	 * @param _factor dimension of the square surrounding a pixel - must be an odd integer at least 3.
	 * @throws IllegalArgumentException if factor is negative or less than 3.
	 */
	public void setBlurFactor(int _factor) {
		if(_factor % 2 == 0)
			throw new IllegalArgumentException("Blur factor must be a positive odd number.");
		
		factor = _factor;
	}

	/**
	 * Returns a String representing this filter.
	 */
	public String toString() {
		return "Blur";
	}

	/**
	 * Describes the function of the filter.
	 * @return description
	 */
	public String getDescription() {
		return "Blurs the image.";
	}

	private int mod(int a, int b) {
		int result = a % b;
		if (result < 0)
			result += b;
		return result;
	}
}
