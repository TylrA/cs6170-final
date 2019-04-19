//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.imageio.ImageIO;
import javax.imageio.stream.FileImageOutputStream;

public class FinalProject {
    public FinalProject() {
    }

    public static void main(String[] args) {
        if (args.length > 1 && args[0].equals("-bi")) {
            getBoundaryPointsFull(args[1], args[2], args[3], 5);
        } else if (args.length <= 1 || !args[0].equals("-b")) {
            if (args.length > 1 && args[0].equals("-d")) {
                double[][] pointCloud = readPointFile(args[1]);
                double[][] distMatrix = calculateDistanceMatrix(pointCloud);
                writeDistanceMatrix(distMatrix, args[2]);
            } else {
                int radius;
                String s;
                if (args.length > 1 && args[0].equals("-phbars")) {
                    radius = Integer.parseInt(args[1]);
                    int count = Integer.parseInt(args[2]);
                    String[] var14;
                    int var13 = (var14 = getOldestPersistantBars(radius, count, args[3])).length;

                    for(int var12 = 0; var12 < var13; ++var12) {
                        s = var14[var12];
                        System.out.println(s);
                    }
                } else if (args.length > 1 && args[0].equals("-uni")) {
                    radius = Integer.parseInt(args[1]);
                    String imagePath = args[2];
                    s = args[3];
                    String outputTxtPath = args[4];
                    ArrayList points = getUniformPoints(imagePath, radius, 7, s);

                    try {
                        BufferedWriter writer = new BufferedWriter(new FileWriter(outputTxtPath));

                        for(int i = 0; i < points.size(); ++i) {
                            writer.write(((Integer[])points.get(i))[0] + " " + ((Integer[])points.get(i))[1] + "\n");
                        }

                        writer.close();
                    } catch (IOException var8) {
                        var8.printStackTrace();
                    }
                } else {
                    System.out.println("FinalProject is a simple tool for manipulating files for the final project, in Computational Topology");
                    System.out.println("Usage:");
                    System.out.println("    -bi <inputfile> <outputfile> <outputimage> produce boundary (including interior boundaries)");
                    System.out.println("    -d <inputfile> <outputfile> produce distance matrix of point cloud (text file, each row a point, with values separated by spaces)");
                    System.out.println("    -phbars <interval dim> <count> <ripserfile> print the 'count' number of the longest living persistant intervals");
                    System.out.println("    -uni <radius> <inputfile> <outputimagefile> <outputtxtfile> produce point cloud of boundary with uniform points");
                }
            }
        }

    }

    private static void getBoundaryPointsFull(String inputPath, String outputPath, String imagePath, int blurFactor) {
        try {
            BufferedImage tempImage = ImageIO.read(new File(inputPath));
            BufferedImage rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), 1);
            rawImage.getGraphics().drawImage(tempImage, 0, 0, (ImageObserver)null);
            getBoundaryPointsRaw(rawImage, outputPath, imagePath, blurFactor);
        } catch (Exception var6) {
            var6.printStackTrace();
        }

    }

    private static void getBoundaryPointsOuter(String inputPath, String outputPath, String imagePath, int blurFactor) {
        try {
            BufferedImage tempImage = ImageIO.read(new File(inputPath));
            BufferedImage rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), 1);
            rawImage.getGraphics().drawImage(tempImage, 0, 0, (ImageObserver)null);
            ExteriorFilter filter = new ExteriorFilter();
            getBoundaryPointsRaw(filter.filter(rawImage), outputPath, imagePath, blurFactor);
        } catch (Exception var7) {
            var7.printStackTrace();
        }

    }

    private static void getBoundaryPointsRaw(BufferedImage rawImage, String outputPath, String imagePath, int blurFactor) {
        try {
            BlurFilter filter = new BlurFilter(blurFactor);
            BufferedImage blurImage = filter.filter(rawImage);
            BufferedImage diffImage = new BufferedImage(rawImage.getWidth(), rawImage.getHeight(), rawImage.getType());
            double total = 0.0D;
            int totalCnt = 0;
            LinkedList<Point> nonTrivials = new LinkedList();

            int colIdx;
            for(int rowIdx = 0; rowIdx < diffImage.getHeight(); ++rowIdx) {
                for(colIdx = 0; colIdx < diffImage.getWidth(); ++colIdx) {
                    int pixel1 = rawImage.getRGB(colIdx, rowIdx);
                    int pixel2 = blurImage.getRGB(colIdx, rowIdx);
                    int value1 = ((pixel1 & 255) + (pixel1 >> 8 & 255) + (pixel1 >> 16 & 255)) / 3;
                    int value2 = ((pixel2 & 255) + (pixel2 >> 8 & 255) + (pixel2 >> 16 & 255)) / 3;
                    value1 = value1 > value2 ? value1 - value2 : value2 - value1;
                    pixel1 = value1 << 16 | value1 << 8 | value1;
                    diffImage.setRGB(colIdx, rowIdx, pixel1);
                    if (value1 > 0) {
                        total += (double)value1;
                        ++totalCnt;
                        nonTrivials.add(new Point(colIdx, rowIdx));
                    }
                }
            }

            Random r = new Random();
            double factor = factor(totalCnt);
            int cnt = 0;
            LinkedList<Point> pointCloud = new LinkedList();
            Iterator var22 = nonTrivials.iterator();

            while(var22.hasNext()) {
                Point p = (Point)var22.next();
                colIdx = diffImage.getRGB(p.getX(), p.getY()) & 255;
                if (r.nextDouble() < factor * (double)totalCnt * (double)colIdx / total) {
                    pointCloud.add(new Point(p.getX(), p.getY()));
                    diffImage.setRGB(p.getX(), p.getY(), 16711680);
                }
            }

            ImageIO.write(diffImage, "PNG", new FileImageOutputStream(new File(imagePath)));
            BufferedWriter output = new BufferedWriter(new FileWriter(outputPath));
            Iterator var23 = pointCloud.iterator();

            while(var23.hasNext()) {
                Point p = (Point)var23.next();
                output.write(p.getX() + " " + p.getY() + "\n");
            }

            output.close();
        } catch (Exception var24) {
            var24.printStackTrace();
        }

    }

    public static ArrayList<Integer[]> getUniformPoints(String imagePath, int radius, int blurFactor, String outputPath) {
        BlurFilter filter = new BlurFilter(blurFactor);

        try {
            BufferedImage tempImage = ImageIO.read(new File(imagePath));
            BufferedImage rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), 1);
            rawImage.getGraphics().drawImage(tempImage, 0, 0, (ImageObserver)null);
            BufferedImage blurredImage = filter.filterEdgeWrap(rawImage);
            BufferedImage diffImage = new BufferedImage(rawImage.getWidth(), rawImage.getHeight(), 1);
            diffImage.getGraphics().drawImage(rawImage, 0, 0, (ImageObserver)null);
            int[][] mat = getDiffImage(rawImage, blurredImage, diffImage);
            ArrayList<Integer[]> result = getUniformPoints(mat, diffImage, radius);
            ImageIO.write(diffImage, "PNG", new FileImageOutputStream(new File(outputPath)));
            return result;
        } catch (IOException var11) {
            var11.printStackTrace();
            return null;
        }
    }

    private static ArrayList<Integer[]> getUniformPoints(int[][] valueMatrix, BufferedImage diffImage, int radius) {
        Integer[] maxPos = new Integer[2];
        maxPos[0] = 0;
        maxPos[1] = 5;
        int maxValue = valueMatrix[0][5];
        int width = valueMatrix.length;
        int height = valueMatrix[0].length;

        for(int i = 6; i < height - 5; ++i) {
            if (valueMatrix[0][i] > maxValue) {
                maxValue = valueMatrix[0][i];
                maxPos[1] = i;
            }
        }

        ArrayList<Integer[]> result = new ArrayList();
        diffImage.setRGB(maxPos[0], maxPos[1], 65280);
        result.add((Integer[])maxPos.clone());
        flushNeighbors(valueMatrix, maxPos, radius, 2, 3);
        Integer[] currentPos = (Integer[])maxPos.clone();
        maxValue = valueMatrix[0][currentPos[1] - radius];
        maxPos[1] = currentPos[1] - radius;

        for(int y = 0; y <= radius; ++y) {
            if (currentPos[1] - radius >= 0 && valueMatrix[y][currentPos[1] - radius] > maxValue) {
                maxValue = valueMatrix[y][currentPos[1] - radius];
                maxPos[0] = y;
                maxPos[1] = currentPos[1] - radius;
            }

            if (currentPos[1] + radius < height && valueMatrix[y][currentPos[1] + radius] > maxValue) {
                maxValue = valueMatrix[y][currentPos[1] + radius];
                maxPos[0] = y;
                maxPos[1] = currentPos[1] + radius;
            }
        }

        for(int y = currentPos[1] - radius + 1; y < currentPos[1] + radius; ++y) {
            if (y >= 0 && y < height && valueMatrix[radius][y] > maxValue) {
                maxValue = valueMatrix[radius][y];
                maxPos[0] = radius;
                maxPos[1] = y;
            }
        }

        diffImage.setRGB(maxPos[0], maxPos[1], 65280);
        result.add((Integer[])maxPos.clone());
        flushNeighbors(valueMatrix, maxPos, radius, 2, 3);

        for(currentPos = (Integer[])maxPos.clone(); width - mod(currentPos[0], width) > 2 * radius || Math.abs(currentPos[1] - ((Integer[])result.get(0))[1]) > 2 * radius; currentPos = (Integer[])maxPos.clone()) {
            maxValue = -1;

            for(int y = currentPos[0] - radius; y <= currentPos[0] + radius; ++y) {
                if (currentPos[1] - radius >= 0 && valueMatrix[mod(y, width)][currentPos[1] - radius] > maxValue) {
                    maxValue = valueMatrix[mod(y, width)][currentPos[1] - radius];
                    maxPos[0] = y;
                    maxPos[1] = currentPos[1] - radius;
                }

                if (currentPos[1] + radius < height && valueMatrix[mod(y, width)][currentPos[1] + radius] > maxValue) {
                    maxValue = valueMatrix[mod(y, width)][currentPos[1] + radius];
                    maxPos[0] = y;
                    maxPos[1] = currentPos[1] + radius;
                }
            }

            for(int y = currentPos[1] - radius + 1; y < currentPos[1] + radius; ++y) {
                if (y >= 0 && y < height) {
                    if (valueMatrix[mod(currentPos[0] - radius, width)][y] > maxValue) {
                        maxValue = valueMatrix[mod(currentPos[0] - radius, width)][y];
                        maxPos[0] = currentPos[0] - radius;
                        maxPos[1] = y;
                    }

                    if (valueMatrix[mod(currentPos[0] + radius, width)][y] > maxValue) {
                        maxValue = valueMatrix[mod(currentPos[0] + radius, width)][y];
                        maxPos[0] = currentPos[0] + radius;
                        maxPos[1] = y;
                    }
                }
            }

            flushNeighbors(valueMatrix, currentPos, radius, 2, 3);
            diffImage.setRGB(mod(maxPos[0], width), maxPos[1], 65280);
            result.add(new Integer[]{mod(maxPos[0], width), maxPos[1]});
        }

        return result;
    }

    private static void flushNeighbors(int[][] space, Integer[] point, int radius, int n, int d) {
        for(int x = point[0] - radius * n / d; x < point[0] + radius * n / d; ++x) {
            for(int y = point[1] - radius * n / d; y < point[1] + radius * n / d; ++y) {
                if (y >= 0 && y < space[0].length) {
                    space[mod(x, space.length)][y] = 0;
                }
            }
        }

    }

    private static double[][] readPointFile(String path) {
        double[][] result = null;
        LinkedList lines = new LinkedList();

        try {
            BufferedReader file = new BufferedReader(new FileReader(path));

            while(file.ready()) {
                lines.add(file.readLine().split(" "));
            }

            file.close();
            int width = ((String[])lines.getFirst()).length;
            result = new double[lines.size()][width];
            int lineIdx = 0;

            for(Iterator var7 = lines.iterator(); var7.hasNext(); ++lineIdx) {
                String[] line = (String[])var7.next();

                for(int idx = 0; idx < width; ++idx) {
                    result[lineIdx][idx] = Double.parseDouble(line[idx]);
                }
            }
        } catch (Exception var9) {
            var9.printStackTrace();
        }

        return result;
    }

    private static double[][] calculateDistanceMatrix(double[][] points) {
        int width = points[0].length;
        double[][] result = new double[points.length - 1][points.length - 1];

        for(int i = 1; i < points.length; ++i) {
            for(int j = 0; j < i; ++j) {
                double[] temp1 = points[i];
                double[] temp2 = points[j];
                double distance = 0.0D;

                for(int v = 0; v < width; ++v) {
                    distance += Math.pow(temp1[v] - temp2[v], 2.0D);
                }

                distance = Math.sqrt(distance);
                result[i - 1][j] = distance;
            }
        }

        return result;
    }

    private static void writeDistanceMatrix(double[][] distanceMatrix, String outputPath) {
        try {
            BufferedWriter output = new BufferedWriter(new FileWriter(outputPath));
            output.write("\n");
            DecimalFormat df = new DecimalFormat("#.####");

            for(int i = 0; i < distanceMatrix.length; ++i) {
                for(int j = 0; j <= i; ++j) {
                    output.write(df.format(distanceMatrix[i][j]) + ",");
                }

                output.write("\n");
            }

            output.close();
        } catch (IOException var6) {
            var6.printStackTrace();
        }

    }

    private static String[] getOldestPersistantBars(int dimension, int barCount, String ripserPath) {
        String[] result = null;

        try {
            BufferedReader file = new BufferedReader(new FileReader(ripserPath));

            String line;
            for(line = file.readLine(); file.ready() && !line.equals("persistence intervals in dim " + dimension + ":"); line = file.readLine()) {
            }

            Pattern pattern = Pattern.compile("\\[(\\d+(?:\\.\\d+)?), ?(\\d+(?:\\.\\d+)?)?\\)");
            ArrayList intervals = new ArrayList();

            while(file.ready()) {
                line = file.readLine();
                Matcher matcher = pattern.matcher(line);
                if (matcher.find()) {
                    double start = Double.parseDouble(matcher.group(1));
                    double duration;
                    if (matcher.groupCount() < 2) {
                        duration = -1.0D;
                    } else {
                        duration = Double.parseDouble(matcher.group(2));
                    }

                    intervals.add(new Interval(start, duration));
                }
            }

            file.close();
            Collections.sort(intervals);
            result = new String[barCount];

            for(int i = 0; i < barCount; ++i) {
                result[i] = ((Interval)intervals.get(intervals.size() - 1 - i)).toString();
            }
        } catch (FileNotFoundException var14) {
            var14.printStackTrace();
        } catch (IOException var15) {
            var15.printStackTrace();
        }

        return result;
    }

    public static double factor(int pointCount) {
        System.out.println(pointCount);
        if (pointCount < 1000) {
            return 0.8D;
        } else if (pointCount < 2000) {
            return 0.6D;
        } else if (pointCount < 5000) {
            return 0.3D;
        } else if (pointCount < 6000) {
            return 0.25D;
        } else {
            return pointCount < 200000 ? 0.02D : 0.018D;
        }
    }

    public static double angleDifference(double angle, Integer[] origin, int x, int y) {
        double angle2 = Math.atan2((double)(x - origin[0]), (double)(y - origin[1]));

        double result;
        for(result = angle2 - angle; result < -1.5707963267948966D; result += 6.283185307179586D) {
        }

        while(result > 1.5707963267948966D) {
            result -= 6.283185307179586D;
        }

        return result < 0.0D ? -result : result;
    }

    public static int[][] getDiffImage(BufferedImage imgA, BufferedImage imgB, BufferedImage diffImage) {
        int[][] result = new int[imgA.getWidth()][imgA.getHeight()];

        for(int rowIdx = 0; rowIdx < diffImage.getHeight(); ++rowIdx) {
            for(int colIdx = 0; colIdx < diffImage.getWidth(); ++colIdx) {
                int pixel1 = imgA.getRGB(colIdx, rowIdx);
                int pixel2 = imgB.getRGB(colIdx, rowIdx);
                int value1 = ((pixel1 & 255) + (pixel1 >> 8 & 255) + (pixel1 >> 16 & 255)) / 3;
                int value2 = ((pixel2 & 255) + (pixel2 >> 8 & 255) + (pixel2 >> 16 & 255)) / 3;
                value1 = value1 > value2 ? value1 - value2 : value2 - value1;
                pixel1 = value1 << 16 | value1 << 8 | value1;
                diffImage.setRGB(colIdx, rowIdx, pixel1);
                result[colIdx][rowIdx] = value1;
            }
        }

        return result;
    }

    public static int mod(int a, int b) {
        int result = a % b;
        if (result < 0) {
            result += b;
        }

        return result;
    }
}
