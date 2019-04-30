package f;

import java.awt.image.BufferedImage;
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
import java.util.LinkedList;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.imageio.ImageIO;
import javax.imageio.stream.FileImageOutputStream;

public class FinalProject {

	public static void main(String[] args) {
		if (args.length > 1 && args[0].equals("-bi")) {
			getBoundaryPointsFull(args[1], args[2], args[3], 5);
		}
		else if (args.length > 1 && args[0].equals("-d")) {
			double[][] pointCloud = readPointFile(args[1]);
			double[][] distMatrix = calculateDistanceMatrix(pointCloud);
			writeDistanceMatrix(distMatrix, args[2]);
		}
		else if (args.length > 1 && args[0].equals("-phbars")) {
			int dim = Integer.parseInt(args[1]);
			int count = Integer.parseInt(args[2]);
			for(String s : getOldestPersistantBars(dim, count, args[3]))
				System.out.println(s);
		}
		else if (args.length > 1 && args[0].equals("-uni")) {
			int radius = Integer.parseInt(args[1]);
			String imagePath = args[2];
			String outputImagePath = args[3];
			String outputTxtPath = args[4];
			
			ArrayList<Integer[]> points = getUniformPoints(imagePath, radius, 7, outputImagePath, false, 0);
			
			BufferedWriter writer;
			try {
				writer = new BufferedWriter(new FileWriter(outputTxtPath));
				for (int i = 0; i < points.size(); i++)
					writer.write(points.get(i)[0] + " " + points.get(i)[1] + "\n");
				writer.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else if (args.length > 1 && args[0].equals("-rb")) {
			RedBlueFilter filter = new RedBlueFilter();
			try {
				BufferedImage input_temp = ImageIO.read(new File(args[1]));
				BufferedImage input = new BufferedImage(input_temp.getWidth(), input_temp.getHeight(), BufferedImage.TYPE_INT_RGB);
				input.getGraphics().drawImage(input_temp, 0, 0, null);
				BufferedImage output = filter.filterEdgeWrap(input);
				ImageIO.write(output, "PNG", new FileImageOutputStream(new File(args[2])));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
		else if (args.length > 1 && args[0].equals("-unig")) {
			int radius = Integer.parseInt(args[1]);
			String imagePath = args[2];
			String outputImagePath = args[3];
			String outputTxtPath = args[4];
			
			ArrayList<Integer[]> points = getUniformPoints(imagePath, radius, 5, outputImagePath, true, 0);
			
			BufferedWriter writer;
			try {
				writer = new BufferedWriter(new FileWriter(outputTxtPath));
				for (int i = 0; i < points.size(); i++)
					writer.write(points.get(i)[0] + " " + points.get(i)[1] + "\n");
				writer.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else if (args.length > 1 && args[0].equals("-unic")) {
			int radius = Integer.parseInt(args[1]);
			int blurFactor = Integer.parseInt(args[2]);
			String imagePath = args[3];
			String outputImagePath = args[4];
			String outputTxtPath = args[5];
			
			ArrayList<Integer[]> points = getUniformPoints(imagePath, radius, blurFactor, outputImagePath, true, 0);
			
			BufferedWriter writer;
			try {
				writer = new BufferedWriter(new FileWriter(outputTxtPath));
				for (int i = 0; i < points.size(); i++)
					writer.write(points.get(i)[0] + " " + points.get(i)[1] + "\n");
				writer.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else if (args.length > 1 && args[0].equals("-unirichcustom")) {
			int radius = Integer.parseInt(args[1]);
			int blurFactor = Integer.parseInt(args[2]);
			int startPos = Integer.parseInt(args[3]);
			String imagePath = args[4];
			String outputImagePath = args[5];
			String outputTxtPath = args[6];
			
			ArrayList<Integer[]> points = getUniformPoints(imagePath, radius, blurFactor, outputImagePath, true, startPos);
			
			BufferedWriter writer;
			try {
				writer = new BufferedWriter(new FileWriter(outputTxtPath));
				for (int i = 0; i < points.size(); i++)
					writer.write(points.get(i)[0] + " " + points.get(i)[1] + "\n");
				writer.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else {
			System.out.println("FinalProject is a simple tool for manipulating files for the final project, in Computational " +
					"Topology");
			System.out.println("Usage:");
			System.out.println("    -bi <inputfile> <outputfile> <outputimage> produce boundary (including interior boundaries)");
			System.out.println("    -d <inputfile> <outputfile> produce distance matrix of point cloud (text file, " +
					"each row a point, with values separated by spaces)");
			System.out.println("    -phbars <interval dim> <count> <ripserfile> print the 'count' number of the " +
					"longest living persistant intervals");
			System.out.println("    -uni <radius> <inputfile> <outputimagefile> <outputtxtfile> produce point cloud of boundary with uniform points");
			System.out.println("    -rb <inputfile> <outputfile> inverts the blue channel and creates a black and white image.");
			System.out.println("    -unig <radius> <inputfile> <outputimagefile> produce point cloud of boundary with uniform points, green2red filter.");
			System.out.println("    -unic <radius> <blurfactor> <inputfile> <outputimagefile> produce point cloud of boundary with uniform points, green2red filter.");
			System.out.println("    -unirichcustom <radius> <blurfactor> <startpos> <inputfile> <outputimagefile> produce point cloud of boundary with uniform points, green2red filter.");
		}
	}
	
	private static void getBoundaryPointsFull(String inputPath, String outputPath, String imagePath, int blurFactor) {
		try {
			BufferedImage tempImage = ImageIO.read(new File(inputPath));
			BufferedImage rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(),
					BufferedImage.TYPE_INT_RGB);
			rawImage.getGraphics().drawImage(tempImage, 0, 0, null);
			getBoundaryPointsRaw(rawImage, outputPath, imagePath, blurFactor);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	private static void getBoundaryPointsRaw(BufferedImage rawImage, String outputPath, String imagePath, int blurFactor) {
		try {
			BlurFilter filter = new BlurFilter(blurFactor);
			BufferedImage blurImage = filter.filter(rawImage);
			
			BufferedImage diffImage = new BufferedImage(rawImage.getWidth(), rawImage.getHeight(), rawImage.getType());
			int pixel1;
			int pixel2;
			int value1;
			int value2;
			double total = 0;
			int totalCnt = 0;
			LinkedList<Point> nonTrivials = new LinkedList<>();
			
			for(int rowIdx = 0; rowIdx < diffImage.getHeight(); rowIdx++) {
				for(int colIdx = 0; colIdx < diffImage.getWidth(); colIdx++) {
					pixel1 = rawImage.getRGB(colIdx, rowIdx);
					pixel2 = blurImage.getRGB(colIdx, rowIdx);
					value1 = ((pixel1 & 0xff) + ((pixel1 >> 8) & 0xff) + ((pixel1 >> 16) & 0xff)) / 3;
					value2 = ((pixel2 & 0xff) + ((pixel2 >> 8) & 0xff) + ((pixel2 >> 16) & 0xff)) / 3;
					value1 = value1 > value2 ? value1 - value2 : value2 - value1;
					pixel1 = (value1 << 16) | (value1 << 8) | value1;
					
					diffImage.setRGB(colIdx, rowIdx, pixel1);
					if(value1 > 0) {
						total += value1;
						totalCnt++;
						nonTrivials.add(new Point(colIdx, rowIdx));
					}
				}
			}
			
			Random r = new Random();
			int temp;
			double factor = factor(totalCnt);
			LinkedList<Point> pointCloud = new LinkedList<>();
			for(Point p : nonTrivials) {
				temp = diffImage.getRGB(p.getX(), p.getY()) & 0xff;
				
				if(r.nextDouble() < factor * totalCnt * temp / total) {
					pointCloud.add(new Point(p.getX(), p.getY()));
					diffImage.setRGB(p.getX(), p.getY(), 0xff0000);
				}
			}
			
			ImageIO.write(diffImage, "PNG", new FileImageOutputStream(new File(imagePath)));
			BufferedWriter output = new BufferedWriter(new FileWriter(outputPath));
			for(Point p : pointCloud)
				output.write(p.getX() + " " + p.getY() + "\n");
			
			output.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static ArrayList<Integer[]> getUniformPoints(String imagePath, int radius, int blurFactor, String outputPath, boolean greenRed, int startPos) {
		BlurFilter filter = new BlurFilter(blurFactor);
		BufferedImage tempImage;
		BufferedImage rawImage;
		BufferedImage blurredImage;
		BufferedImage diffImage;
		
		try {
			tempImage = ImageIO.read(new File(imagePath));
			rawImage = new BufferedImage(tempImage.getWidth(), tempImage.getHeight(), BufferedImage.TYPE_INT_RGB);
			rawImage.getGraphics().drawImage(tempImage, 0, 0, null);
			if(greenRed)
				rawImage = (new GreenToRedFilter()).filter(rawImage);
			blurredImage = filter.filterEdgeWrap(rawImage);
			diffImage = new BufferedImage(rawImage.getWidth(), rawImage.getHeight(), BufferedImage.TYPE_INT_RGB);
			diffImage.getGraphics().drawImage(rawImage, 0, 0, null);
			
			int[][] mat = getDiffImage(rawImage, blurredImage, diffImage, startPos);
			
			ArrayList<Integer[]> result = getUniformPoints(mat, diffImage, radius, startPos);
			ImageIO.write(diffImage, "PNG", new FileImageOutputStream(new File(outputPath)));
			
			return result;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	
	private static ArrayList<Integer[]> getUniformPoints(int[][] valueMatrix, BufferedImage diffImage, int radius, int startPos) {
		int maxValue;
		Integer[] maxPos = new Integer[2];
//		maxValue = diffImage.getRGB(0, 5) & 0xffffff;
		maxValue = valueMatrix[startPos][5];
		maxPos[0] = startPos;
		maxPos[1] = 5;
//		int width = diffImage.getWidth();
//		int height = diffImage.getHeight();
		int width = valueMatrix.length;
		int height = valueMatrix[0].length;
		
		for (int i = 6; i < height - 5; i++) {
//			if (diffImage.getRGB(0, i) > maxValue) {
			if (valueMatrix[startPos][i] > maxValue) {
//				maxValue = diffImage.getRGB(0, i);
				maxValue = valueMatrix[startPos][i];
				maxPos[1] = i;
			}
		}
		
		ArrayList<Integer[]> result = new ArrayList<>();
		// TODO: remove following line:
		diffImage.setRGB(maxPos[0], maxPos[1], 0x00ff00);
		result.add(maxPos.clone());
		flushNeighbors(valueMatrix, maxPos, radius, 2, 3);
		
		Integer[] currentPos = maxPos.clone();
//		maxValue = diffImage.getRGB(0, currentPos[1] - radius);
		maxValue = valueMatrix[startPos][currentPos[1] - radius];
		maxPos[1] = currentPos[1] - radius;
		
		// North & South sides
		for (int x = startPos; x <= startPos + radius; x++) {
//			if (currentPos[1] - radius >= 0 && diffImage.getRGB(x, currentPos[1] - radius) > maxValue) {
			if (currentPos[1] - radius >= 0 && valueMatrix[x][currentPos[1] - radius] > maxValue) {
//				maxValue = diffImage.getRGB(x, currentPos[1] - radius);
				maxValue = valueMatrix[x][currentPos[1] - radius];
				maxPos[0] = x;
				maxPos[1] = currentPos[1] - radius;
			}
//			if (currentPos[1] + radius < height && diffImage.getRGB(x, currentPos[1] + radius) > maxValue) {
			if (currentPos[1] + radius < height && valueMatrix[x][currentPos[1] + radius] > maxValue) {
//				maxValue = diffImage.getRGB(x, currentPos[1] + radius);
				maxValue = valueMatrix[x][currentPos[1] + radius];
				maxPos[0] = x;
				maxPos[1] = currentPos[1] + radius;
			}
		}
		
		// East side
		for (int y = currentPos[1] - radius + 1; y < currentPos[1] + radius; y++) {
//			if (y >= 0 && diffImage.getRGB(radius, y) > maxValue) {
			if (y >= 0 && y < height && valueMatrix[radius][y] > maxValue) {
//				maxValue = diffImage.getRGB(radius, y);
				maxValue = valueMatrix[startPos + radius][y];
				maxPos[0] = startPos + radius;
				maxPos[1] = y;
			}
		}
		
		diffImage.setRGB(maxPos[0], maxPos[1], 0x00ff00);
		result.add(maxPos.clone());
		flushNeighbors(valueMatrix, maxPos, radius, 2, 3);
		Integer[] prevPos = currentPos;
		currentPos = maxPos.clone();
		
		while (!(width - mod(currentPos[0] - startPos, width) <= 2 * radius && Math.abs(currentPos[1] - result.get(0)[1]) <= 2 * radius)) {
			maxValue = -1;
			
			// North & South sides
			for (int x = currentPos[0] - radius; x <= currentPos[0] + radius; x++) {
				if (currentPos[1] - radius >= 0 //&& angleDifference(prevAngle, currentPos, x, currentPos[1] - radius) > Math.PI / 8 
						&& valueMatrix[mod(x, width)][currentPos[1] - radius] > maxValue) {
					maxValue = valueMatrix[mod(x, width)][currentPos[1] - radius];
					maxPos[0] = x;
					maxPos[1] = currentPos[1] - radius;
				}
				if (currentPos[1] + radius < height
						&& valueMatrix[mod(x, width)][currentPos[1] + radius] > maxValue) {
					maxValue = valueMatrix[mod(x, width)][currentPos[1] + radius];
					maxPos[0] = x;
					maxPos[1] = currentPos[1] + radius;
				}
			}
			
			// East & West sides
			for (int y = currentPos[1] - radius + 1; y < currentPos[1] + radius; y++) {
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
			
			diffImage.setRGB(mod(maxPos[0], width), maxPos[1], 0x00ff00);
			result.add(new Integer[] {mod(maxPos[0], width), maxPos[1]});
			prevPos = currentPos;
			currentPos = maxPos.clone();
		}
		
		return result;
	}
	
	/**
	 * Sets all points in the "space" matrix in the disk of radius "radius" * "n" / "d"
	 * (integer division), centered at "point" to 0.
	 * @param space
	 * @param point (x,y) coordinate pair
	 * @param radius
	 * @param n
	 * @param d
	 */
	private static void flushNeighbors(int[][] space, Integer[] point, int radius, int n, int d) {
		for (int x = point[0] - (radius * n) / d; x < point[0] + (radius * n) / d; x++) {
			for (int y = point[1] - (radius * n) / d; y < point[1] + (radius * n) / d; y++) {
				if (y >= 0 && y < space[0].length)
					space[mod(x, space.length)][y] = 0;
			}
		}
	}
	
	private static double[][] readPointFile(String path) {
		double[][] result = null;
		LinkedList<String[]> lines = new LinkedList<>();
		try {
			BufferedReader file = new BufferedReader(new FileReader(path));
			while(file.ready())
				lines.add(file.readLine().split(" "));
			file.close();
			
			int width = lines.getFirst().length;
			result = new double[lines.size()][width];
			int lineIdx = 0;
			
			for(String[] line : lines) {
				for(int idx = 0; idx < width; idx++) {
					result[lineIdx][idx] = Double.parseDouble(line[idx]);
				}
				lineIdx++;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		return result;
	}
	
	private static double[][] calculateDistanceMatrix(double[][] points) {
		int width = points[0].length;
		
		double[][] result = new double[points.length - 1][points.length - 1];
		double[] temp1;
		double[] temp2;
		double distance;
		
		for(int i = 1; i < points.length; i++) {
			for(int j = 0; j < i; j++) {
				temp1 = points[i];
				temp2 = points[j];
				distance = 0;
				
				for(int v = 0; v < width; v++)
					distance += Math.pow(temp1[v] - temp2[v], 2);
				
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
			for(int i = 0; i < distanceMatrix.length; i++) {
				for(int j = 0; j <= i; j++)
					output.write(df.format(distanceMatrix[i][j]) + ",");
				
				output.write("\n");
			}
			
			output.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private static String[] getOldestPersistantBars(int dimension, int barCount, String ripserPath) {
		String[] result = null;
		try {
			BufferedReader file = new BufferedReader(new FileReader(ripserPath));
			String line = file.readLine();
			while(file.ready() && !line.equals("persistence intervals in dim " + dimension + ":")) {
				line = file.readLine();
			}
			
			Pattern pattern = Pattern.compile("\\[(\\d+(?:\\.\\d+)?), ?(\\d+(?:\\.\\d+)?)?\\)"); // \[(\d+(?:\.\d+)?), ?(\d+(?:\.\d+)?)?\)
			Matcher matcher;
			ArrayList<Interval> intervals = new ArrayList<>();
			double start;
			double duration;
			
			while(file.ready()) {
				line = file.readLine();
				matcher = pattern.matcher(line);
				
				if(matcher.find()) {
					start = Double.parseDouble(matcher.group(1));
					if(matcher.groupCount() < 2)
						duration = -1;
					else
						duration = Double.parseDouble(matcher.group(2));
					intervals.add(new Interval(start, duration));
				}
			}
			file.close();
			
			Collections.sort(intervals);
			
			result = new String[barCount];
			for(int i = 0; i < barCount; i++)
				result[i] = intervals.get(intervals.size() - 1 - i).toString();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return result;
	}
	
	public static double factor(int pointCount) {
		System.out.println(pointCount);
		if(pointCount < 1000)
			return 0.8;
		else if(pointCount < 2000)
			return 0.6;
		else if(pointCount < 5000)
			return 0.3;
		else if(pointCount < 6000)
			return 0.25;
		else if(pointCount < 200000)
			return 0.02;
		return 0.018;
	}
	
	/**
	 * Measures the absolute angle difference between two vectors in a way that makes sense.
	 * @param angle One of the vectors (as if it were theta for a point in polar coordinates)
	 * @param origin The "tail" of the vector making the other angle
	 * @param x coordinate offset from origin, used to define second vector
	 * @param y coordinate offset from origin, used to define second vector
	 * @return a positive number between 0 and pi that reflects the difference between the two angles.
	 */
	public static double angleDifference(double angle, Integer[] origin, int x, int y) {
		double angle2 = Math.atan2(x - origin[0], y - origin[1]);
		double result = angle2 - angle;
		while (result < -Math.PI / 2)
			result += 2 * Math.PI;
		while (result > Math.PI / 2)
			result -= 2 * Math.PI;
		if (result < 0)
			return -result;
		return result;
	}
	
	public static int[][] getDiffImage(BufferedImage imgA, BufferedImage imgB, BufferedImage diffImage, int startPos) {
		int pixel1;
		int pixel2;
		int value1;
		int value2;
		int[][] result = new int[imgA.getWidth()][imgA.getHeight()];
		
		for(int rowIdx = 0; rowIdx < diffImage.getHeight(); rowIdx++) {
//			pixel1 = imgA.getRGB(0, rowIdx);
//			pixel2 = imgB.getRGB(0, rowIdx);
//			value1 = ((pixel1 & 0xff) + ((pixel1 >> 8) & 0xff) + ((pixel1 >> 16) & 0xff)) / 3;
//			value2 = ((pixel2 & 0xff) + ((pixel2 >> 8) & 0xff) + ((pixel2 >> 16) & 0xff)) / 3;
//			value1 = value1 > value2 ? value1 - value2 : value2 - value1;
//			if (diffImage.getHeight() - rowIdx <= 40)
//				value1 = value1 * (diffImage.getHeight() - rowIdx) / 80;
//			pixel1 = (value1 << 16) | (value1 << 8) | value1;
//			
//			diffImage.setRGB(0, rowIdx, pixel1);
//			result[0][rowIdx] = value1;

			for(int colIdx = 0; colIdx < diffImage.getWidth(); colIdx++) {
				pixel1 = imgA.getRGB(colIdx, rowIdx);
				pixel2 = imgB.getRGB(colIdx, rowIdx);
				value1 = ((pixel1 & 0xff) + ((pixel1 >> 8) & 0xff) + ((pixel1 >> 16) & 0xff)) / 3;
				value2 = ((pixel2 & 0xff) + ((pixel2 >> 8) & 0xff) + ((pixel2 >> 16) & 0xff)) / 3;
				value1 = value1 > value2 ? value1 - value2 : value2 - value1;
				pixel1 = (value1 << 16) | (value1 << 8) | value1;
				
				if (colIdx == startPos && diffImage.getHeight() - rowIdx <= 40)
					value1 = value1 * (diffImage.getHeight() - rowIdx) / 80;
				diffImage.setRGB(colIdx, rowIdx, pixel1);
				result[colIdx][rowIdx] = value1;
			}
		}
		
		return result;
	}
	
	public static int mod(int a, int b) {
		int result = a % b;
		if (result < 0)
			result += b;
		return result;
	}
}
