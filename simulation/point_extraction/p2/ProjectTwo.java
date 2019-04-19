//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package p2;

import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.imageio.ImageIO;
import javax.imageio.stream.FileImageOutputStream;

public class ProjectTwo {
    public ProjectTwo() {
    }

    public static void main(String[] args) {
        if (args.length > 1 && args[0].equals("-c")) {
            int dim = Integer.parseInt(args[1]);
            String ripserPath = args[2];
            String outputPath = args[3];
            convertRipser(dim, ripserPath, outputPath);
        } else if (args.length > 1 && args[0].equals("-s")) {
            scaleImage(Integer.parseInt(args[1]), args[2], args[3]);
        } else if (args.length <= 1 || !args[0].equals("-r")) {
            System.out.println("ProjectTwo is a tool for manipulating files for project 2, in Computational Topology");
            System.out.println("Usage:");
            System.out.println("    -c <interval dim> <ripserfile> <outputfile> convert ripser file into input file for Hera; only include homologies of dimension ~interval dim~");
            System.out.println("    -s <sidelength> <imagefile> <outputPNGfile> scale image to a square image with given sidelength.");
        }

    }

    public static double[][] getPersistentImage(int sideLength, String filePath) {
        ArrayList<PersistentPoint> rawPoints = new ArrayList();
        BufferedReader file = null;

        try {
            file = new BufferedReader(new FileReader(filePath));
            Pattern point = Pattern.compile("(\\d+(?:\\.(?:\\d*)?)?) (\\d+(?:\\.(?:\\d*)?)?)");
            double maxLifespan = 0.0D;

            while(file.ready()) {
                String line = file.readLine();
                Matcher matcher = point.matcher(line);
                if (matcher.find()) {
                    double birth = Double.parseDouble(matcher.group(1));
                    double death = Double.parseDouble(matcher.group(2));
                    rawPoints.add(new PersistentPoint(birth, death));
                    maxLifespan = death - birth > maxLifespan ? death - birth : maxLifespan;
                }
            }
        } catch (FileNotFoundException var23) {
            var23.printStackTrace();
        } catch (IOException var24) {
            var24.printStackTrace();
        } finally {
            try {
                file.close();
            } catch (IOException var22) {
                var22.printStackTrace();
            }

        }

        return null;
    }

    public static void scaleImage(int sidelength, String imagePath, String outputPath) {
        try {
            BufferedImage tempImage = ImageIO.read(new File(imagePath));
            BufferedImage image = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), 1);
            image.getGraphics().drawImage(tempImage, 0, 0, (ImageObserver)null);
            BufferedImage result = new BufferedImage(sidelength, sidelength, 1);
            int[] vpart = new int[sidelength];
            int[] hpart = new int[sidelength];
            double vFactor = (double)image.getHeight() / (double)sidelength;
            double hFactor = (double)image.getWidth() / (double)sidelength;

            int minX;
            for(minX = 0; minX < sidelength; ++minX) {
                vpart[minX] = (int)Math.round(vFactor * (double)minX);
                hpart[minX] = (int)Math.round(hFactor * (double)minX);
                if (vpart[minX] == image.getHeight()) {
                    vpart[minX] = image.getHeight() - 1;
                }

                if (hpart[minX] == image.getWidth()) {
                    hpart[minX] = image.getWidth() - 1;
                }
            }

            for(int i = 0; i < sidelength; ++i) {
                for(int j = 0; j < sidelength; ++j) {
                    minX = hpart[i];
                    int minY = vpart[j];
                    int maxX;
                    if (i == sidelength - 1) {
                        maxX = image.getWidth() - 1;
                    } else {
                        maxX = hpart[i + 1];
                    }

                    int maxY;
                    if (j == sidelength - 1) {
                        maxY = image.getHeight() - 1;
                    } else {
                        maxY = vpart[j + 1];
                    }

                    result.setRGB(i, j, averagePixel(image, minY, maxY, minX, maxX));
                }
            }

            ImageIO.write(result, "PNG", new FileImageOutputStream(new File(outputPath)));
        } catch (IOException var18) {
            var18.printStackTrace();
        }

    }

    public static int averagePixel(BufferedImage image, int minY, int maxY, int minX, int maxX) {
        int cnt = (maxY - minY + 1) * (maxX - minX + 1);
        int result = 0;

        for(int i = minX; i <= maxX; ++i) {
            for(int j = minY; j <= maxY; ++j) {
                result += image.getRGB(i, j) & 255;
            }
        }

        result /= cnt;
        return result << 16 | result << 8 | result;
    }

    public static double[][] getPersistentImage(double[][] points, double maxLife, double minLife, int sideLength) {
        return null;
    }

    public static double getIntensity(double x, double y, double[][] points) {
        return 0.0D;
    }

    private static void convertRipser(int dimension, String ripserPath, String outputPath) {
        BufferedReader file = null;
        BufferedWriter writer = null;

        try {
            file = new BufferedReader(new FileReader(ripserPath));

            String line;
            for(line = file.readLine(); file.ready() && !line.equals("persistence intervals in dim " + dimension + ":"); line = file.readLine()) {
            }

            writer = new BufferedWriter(new FileWriter(outputPath));
            Pattern pattern = Pattern.compile("\\[(\\d+(?:\\.\\d+)?), ?(\\d+(?:\\.\\d+)?)?\\)");
            Pattern dimPattern = Pattern.compile("persistence intervals in dim \\d+:");

            while(file.ready()) {
                line = file.readLine();
                Matcher matcher = pattern.matcher(line);
                if (matcher.find()) {
                    if (matcher.groupCount() == 2 && matcher.group(2) != null) {
                        double start = Double.parseDouble(matcher.group(1));
                        double end = Double.parseDouble(matcher.group(2));
                        writer.write(start + " " + end + "\n");
                    }
                } else if (dimPattern.matcher(line).find()) {
                    break;
                }
            }
        } catch (FileNotFoundException var23) {
            var23.printStackTrace();
        } catch (IOException var24) {
            var24.printStackTrace();
        } finally {
            try {
                file.close();
                writer.close();
            } catch (IOException var22) {
                var22.printStackTrace();
            }

        }

    }
}
