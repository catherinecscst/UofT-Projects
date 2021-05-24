package Renamerpics;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;

/**
 * Manages Files.
 */
public class FileManager {
	
    /**
     * Get all the images under the gievn directory file.
     * @param directory the directory you want to get images from.  
     * @throws IOException 
     * @return an arraylist of image files under the given direcory file
     */
	public ArrayList<File> getImages(File directory) throws IOException{
		ArrayList<File> r = new ArrayList<File>();
		if (directory.isDirectory()){
			File[] test = directory.listFiles();
			for (File item: test){
				if (isImage(item)){
					r.add(item);
				}
				if (item.isDirectory()){
					ArrayList<File> n = getImages(item);
					for (File i: n){
						r.add(i);
					}
				}
			}
		}
		return r;
	}
	
	/**
	 * Distinguish the file is an image file or not.
	 * @param file the file.
	 * @throws IOException 
	 * @return whether this file is an image file or not.
     */			
	public Boolean isImage(File file) throws IOException{
		String n = file.toPath().toString();
		if (n.endsWith("jpg")|| n.endsWith("jpeg") || n.endsWith("png") || n.endsWith("tiff") || n.endsWith("bmp")) {
		    return true;
		} else {
			return false;
		}
	}
	
	/**
	 * Give the Directory File that contain selected imageFile.
	 * @param imageFile the selected imagefile.
	 * @throws IOException 
	 * @return the Directory File that contain selected imageFile.
     */
	public File searchImage(File imageFile) throws IOException{
		String o = imageFile.getPath();
		String back = "/" + imageFile.getName();
		o = o.replaceAll(back, "");
		File r = new File(o);
		return r;
	}
	
	/**
	 * Find all the image files that are tagged by the given tag.
	 * @param Tag the tag we are searching with.
	 * @return An ArrayList of Files that are tagged by the given tag.
	 * @throws IOException 
     */
	public ArrayList<File> searchByTag(Tag tag) throws IOException{
		ArrayList<File> n = new ArrayList<File>();
		String p = System.getProperty("user.home");
		File homeFile = new File(p);
		ArrayList<File> r;
		r = getImages(homeFile);
		for (File file: r){
			if(file.getName().contains(tag.toString())){
				n.add(file);
			}
		}
		return n;
	}
	
	/**
	public static void main(String[] args) throws IOException {
		FileManager manager = new FileManager();
		File file  = new File("/Users/kasipinkii/Documents/Computer Science/CSC207/FileTester");
		System.out.println(manager.getImages(file));
		

		File o = new File("/Users/kasipinkii/Documents/Computer Science/CSC207/FileTester/LevelA.jpg");
		System.out.println(manager.searchImage(o));
		
		//Tag tag = new Tag("s");
		//System.out.println(manager.searchByTag(tag));
	}*/
}
