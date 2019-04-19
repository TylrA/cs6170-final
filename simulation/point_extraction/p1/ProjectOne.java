//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package p1;

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

public class ProjectOne {
    public ProjectOne() {
    }

    public static void main(String[] args) {
        if (args.length > 1 && args[0].equals("-bi")) {
            getBoundaryPointsFull(args[1], args[2], 3);
        } else if (args.length > 1 && args[0].equals("-b")) {
            getBoundaryPointsOuter(args[1], args[2], 3);
        } else if (args.length > 1 && args[0].equals("-d")) {
            double[][] pointCloud = readPointFile(args[1]);
            double[][] distMatrix = calculateDistanceMatrix(pointCloud);
            writeDistanceMatrix(distMatrix, args[2]);
        } else if (args.length > 1 && args[0].equals("-phbars")) {
            int dim = Integer.parseInt(args[1]);
            int count = Integer.parseInt(args[2]);
            String[] var6;
            int var5 = (var6 = getOldestPersistantBars(dim, count, args[3])).length;

            for(int var4 = 0; var4 < var5; ++var4) {
                String s = var6[var4];
                System.out.println(s);
            }
        } else {
            System.out.println("ProjectOne is a simple tool for manipulating files for project 1, in Computational Topology");
            System.out.println("Usage:");
            System.out.println("    -bi <inputfile> <outputfile> produce boundary (including interior boundaries)");
            System.out.println("    -b <inputfile> <outputfile> produce boundary (only outer boundary)");
            System.out.println("    -d <inputfile> <outputfile> produce distance matrix of point cloud (text file, each row a point, with values separated by spaces)");
            System.out.println("    -phbars <interval dim> <count> <ripserfile> print the 'count' number of the longest living persistant intervals");
        }

    }

    private static void getBoundaryPointsFull(String inputPath, String outputPath, int blurFactor) {
        try {
            BufferedImage tempImage = ImageIO.read(new File(inputPath));
            BufferedImage rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), 1);
            rawImage.getGraphics().drawImage(tempImage, 0, 0, (ImageObserver)null);
            getBoundaryPointsRaw(rawImage, outputPath, blurFactor);
        } catch (Exception var5) {
            var5.printStackTrace();
        }

    }

    private static void getBoundaryPointsOuter(String inputPath, String outputPath, int blurFactor) {
        try {
            BufferedImage tempImage = ImageIO.read(new File(inputPath));
            BufferedImage rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), 1);
            rawImage.getGraphics().drawImage(tempImage, 0, 0, (ImageObserver)null);
            ExteriorFilter filter = new ExteriorFilter();
            getBoundaryPointsRaw(filter.filter(rawImage), outputPath, blurFactor);
        } catch (Exception var6) {
            var6.printStackTrace();
        }

    }

    private static void getBoundaryPointsRaw(BufferedImage rawImage, String outputPath, int blurFactor) {
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
                    pixel1 = pixel1 > pixel2 ? pixel1 - pixel2 : pixel2 - pixel1;
                    diffImage.setRGB(colIdx, rowIdx, pixel1);
                    if (pixel1 > 0) {
                        total += (double)(pixel1 & 255);
                        ++totalCnt;
                    }

                    if (pixel1 > 0) {
                        nonTrivials.add(new Point(colIdx, rowIdx));
                    }
                }
            }

            Random r = new Random();
            double factor = factor(totalCnt);
            int cnt = false;
            LinkedList<Point> pointCloud = new LinkedList();
            Iterator var19 = nonTrivials.iterator();

            while(var19.hasNext()) {
                Point p = (Point)var19.next();
                colIdx = diffImage.getRGB(p.getX(), p.getY()) & 255;
                if (r.nextDouble() < factor * (double)totalCnt * (double)colIdx / total) {
                    pointCloud.add(new Point(p.getX(), p.getY()));
                }
            }

            BufferedWriter output = new BufferedWriter(new FileWriter(outputPath));
            Iterator var20 = pointCloud.iterator();

            while(var20.hasNext()) {
                Point p = (Point)var20.next();
                output.write(p.getX() + " " + p.getY() + "\n");
            }

            output.close();
        } catch (Exception var21) {
            var21.printStackTrace();
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
        if (pointCount < 1000) {
            return 0.8D;
        } else if (pointCount < 2000) {
            return 0.6D;
        } else if (pointCount < 5000) {
            return 0.3D;
        } else {
            return pointCount < 6000 ? 0.25D : 0.18D;
        }
    }
}
