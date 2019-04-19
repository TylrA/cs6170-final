//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package f;

import java.awt.image.BufferedImage;

public class BlurFilter implements ImageFilter {
    private int factor;

    public BlurFilter(int _factor) {
        if (_factor % 2 == 0) {
            throw new IllegalArgumentException("Blur factor must be a positive odd number.");
        } else {
            this.factor = _factor;
        }
    }

    public BufferedImage filter(BufferedImage i) {
        BufferedImage result = new BufferedImage(i.getWidth(), i.getHeight(), i.getType());

        for(int y = 0; y < i.getHeight(); ++y) {
            for(int x = 0; x < i.getWidth(); ++x) {
                if (y >= 7 && i.getHeight() - y >= 7) {
                    int rowLowCutOff = -this.factor / 2;
                    if (y < -rowLowCutOff) {
                        rowLowCutOff = -y;
                    }

                    int rowHighCutOff = this.factor / 2;
                    if (y > i.getHeight() - 1 - rowHighCutOff) {
                        rowHighCutOff = i.getHeight() - 1 - y;
                    }

                    int colLowCutOff = -this.factor / 2;
                    if (x < -colLowCutOff) {
                        colLowCutOff = -x;
                    }

                    int colHighCutOff = this.factor / 2;
                    if (x > i.getWidth() - 1 - colHighCutOff) {
                        colHighCutOff = i.getWidth() - 1 - x;
                    }

                    int neighbors = 0;
                    int redValue = 0;
                    int greenValue = 0;
                    int blueValue = 0;

                    int colOffset;
                    for(colOffset = colLowCutOff; colOffset <= colHighCutOff; ++colOffset) {
                        for(int rowOffset = rowLowCutOff; rowOffset <= rowHighCutOff; ++rowOffset) {
                            int pixel = i.getRGB(x + colOffset, y + rowOffset);
                            redValue += pixel >> 16 & 255;
                            greenValue += pixel >> 8 & 255;
                            blueValue += pixel >> 0 & 255;
                            ++neighbors;
                        }
                    }

                    redValue /= neighbors;
                    greenValue /= neighbors;
                    blueValue /= neighbors;
                    colOffset = redValue << 16 | greenValue << 8 | blueValue;
                    result.setRGB(x, y, colOffset);
                } else {
                    result.setRGB(x, y, i.getRGB(x, y));
                }
            }
        }

        return result;
    }

    public BufferedImage filterEdgeWrap(BufferedImage i) {
        BufferedImage result = new BufferedImage(i.getWidth(), i.getHeight(), i.getType());

        for(int y = 0; y < i.getHeight(); ++y) {
            for(int x = 0; x < i.getWidth(); ++x) {
                if (y >= 7 && i.getHeight() - y >= 7) {
                    int rowLowCutOff = -this.factor / 2;
                    if (y < -rowLowCutOff) {
                        rowLowCutOff = -y;
                    }

                    int rowHighCutOff = this.factor / 2;
                    if (y > i.getHeight() - 1 - rowHighCutOff) {
                        rowHighCutOff = i.getHeight() - 1 - y;
                    }

                    int neighbors = 0;
                    int redValue = 0;
                    int greenValue = 0;
                    int blueValue = 0;

                    int colOffset;
                    for(colOffset = -this.factor / 2; colOffset <= this.factor / 2; ++colOffset) {
                        for(int rowOffset = rowLowCutOff; rowOffset <= rowHighCutOff; ++rowOffset) {
                            int pixel = i.getRGB(this.mod(x + colOffset, i.getWidth()), y + rowOffset);
                            redValue += pixel >> 16 & 255;
                            greenValue += pixel >> 8 & 255;
                            blueValue += pixel >> 0 & 255;
                            ++neighbors;
                        }
                    }

                    redValue /= neighbors;
                    greenValue /= neighbors;
                    blueValue /= neighbors;
                    colOffset = redValue << 16 | greenValue << 8 | blueValue;
                    result.setRGB(x, y, colOffset);
                } else {
                    result.setRGB(x, y, i.getRGB(x, y));
                }
            }
        }

        return result;
    }

    public void setBlurFactor(int _factor) {
        if (_factor % 2 == 0) {
            throw new IllegalArgumentException("Blur factor must be a positive odd number.");
        } else {
            this.factor = _factor;
        }
    }

    public String toString() {
        return "Blur";
    }

    public String getDescription() {
        return "Blurs the image.";
    }

    private int mod(int a, int b) {
        int result = a % b;
        if (result < 0) {
            result += b;
        }

        return result;
    }
}
