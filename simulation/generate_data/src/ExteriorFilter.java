//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.util.LinkedList;

public class ExteriorFilter implements ImageFilter {
    public ExteriorFilter() {
    }

    public BufferedImage filter(BufferedImage input) {
        int exteriorColor = input.getRGB(0, 0);
        BufferedImage extendedImage = new BufferedImage(input.getWidth() + 2, input.getHeight() + 2, input.getType());
        extendedImage.getGraphics().drawImage(input, 1, 1, (ImageObserver)null);

        for(int rowIdx = 0; rowIdx < extendedImage.getWidth(); ++rowIdx) {
            extendedImage.setRGB(rowIdx, 0, exteriorColor);
            extendedImage.setRGB(rowIdx, extendedImage.getHeight() - 1, exteriorColor);
        }

        for(int rowIdx = 1; rowIdx < extendedImage.getHeight() - 1; ++rowIdx) {
            extendedImage.setRGB(0, rowIdx, exteriorColor);
            extendedImage.setRGB(extendedImage.getWidth() - 1, rowIdx, exteriorColor);
        }

        boolean[][] exterior = this.getExterior(extendedImage, exteriorColor);
        BufferedImage result = new BufferedImage(input.getWidth(), input.getHeight(), input.getType());

        for(int rowIdx = 0; rowIdx < input.getHeight(); ++rowIdx) {
            for(int colIdx = 0; colIdx < input.getWidth(); ++colIdx) {
                if (!exterior[colIdx + 1][rowIdx + 1]) {
                    result.setRGB(colIdx, rowIdx, 16777215);
                } else {
                    result.setRGB(colIdx, rowIdx, exteriorColor);
                }
            }
        }

        return result;
    }

    private boolean[][] getExterior(BufferedImage image, int color) {
        boolean[][] exterior = new boolean[image.getWidth()][image.getHeight()];
        LinkedList<Point> points = new LinkedList();
        points.add(new Point(0, 0));
        exterior[0][0] = true;
        this.visit2(image, color, exterior, points);
        return exterior;
    }

    private void visit(BufferedImage image, int color, int x, int y, boolean[][] exterior) {
        exterior[x][y] = true;
        if (x > 0 && !exterior[x - 1][y] && color == image.getRGB(x - 1, y)) {
            this.visit(image, color, x - 1, y, exterior);
        }

        if (x < image.getWidth() - 1 && !exterior[x + 1][y] && color == image.getRGB(x + 1, y)) {
            this.visit(image, color, x + 1, y, exterior);
        }

        if (y > 0 && !exterior[x][y - 1] && color == image.getRGB(x, y - 1)) {
            this.visit(image, color, x, y - 1, exterior);
        }

        if (y < image.getHeight() - 1 && !exterior[x][y + 1] && color == image.getRGB(x, y + 1)) {
            this.visit(image, color, x, y + 1, exterior);
        }

    }

    private void visit2(BufferedImage image, int color, boolean[][] exterior, LinkedList<Point> points) {
        while(!points.isEmpty()) {
            Point current = (Point)points.removeLast();
            int x = current.getX();
            int y = current.getY();
            if (x > 0 && !exterior[x - 1][y] && color == image.getRGB(x - 1, y)) {
                points.addFirst(new Point(x - 1, y));
                exterior[x - 1][y] = true;
            }

            if (x < image.getWidth() - 1 && !exterior[x + 1][y] && color == image.getRGB(x + 1, y)) {
                points.addFirst(new Point(x + 1, y));
                exterior[x + 1][y] = true;
            }

            if (y > 0 && !exterior[x][y - 1] && color == image.getRGB(x, y - 1)) {
                points.addFirst(new Point(x, y - 1));
                exterior[x][y - 1] = true;
            }

            if (y < image.getHeight() - 1 && !exterior[x][y + 1] && color == image.getRGB(x, y + 1)) {
                points.addFirst(new Point(x, y + 1));
                exterior[x][y + 1] = true;
            }
        }

    }
}
