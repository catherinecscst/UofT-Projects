package Renamerpics;

import java.io.BufferedReader;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.SimpleFormatter;


public class PhotoRenamer {
	
	/** An order for the action of adding a tag. */
	protected static final String ADDTAG = "Rename the file by adding a tag.";
	/** An order for the action of deleting tags. */
	protected static final String DELTAG = "Rename the file by deleting a tag.";
	/** A new FileHandler to log info into the log File. */
	private static FileHandler fh;
	/** An arraylist to store this photo's old names. */
	private ArrayList<String> history;
	/** The working file. */
	private File file;
	
	
	/**
     * Creates a new PhotoRenamer for the image file.
     * @throws IOException 
     * @throws SecurityException
     */
	public PhotoRenamer(File file) throws SecurityException, IOException{
		this.file = file;
		fh = new FileHandler("events.log");
		fh.setFormatter(new SimpleFormatter());
        fh.setLevel(Level.INFO);
		User.logger.addHandler(fh);
		this.history = new ArrayList<String>();
	}
	
	/**
	 * Rename a file base on a tag.
	 * @param tag the tag want to be added or deleted.
	 * @param order the action of adding tags or deleting tags. Only accept String ADDTAG or String DELTAG.
	 * @throws IOException 
     */
	public void renameImage(Tag tag, String order){
		String prechange = new String(this.file.getName());
		if (order == ADDTAG){
			String[] lstr = this.file.toString().split("\\.");
			String rr = "";
			 for(int i=0; i<(lstr.length-1); i++){
				 rr += lstr[i];
			 }
			 rr += tag.toString() + "." +lstr[lstr.length-1];
			File n = new File(this.file.getPath().replaceAll(this.file.toString(), rr));
			this.file.renameTo(n);
			this.file = n;
		} else {
			File n = new File(file.getPath().replaceAll(tag.toString(), ""));
			this.file.renameTo(n);
			this.file = n;
		}
		java.util.Date date= new java.util.Date();
		String msg = String.valueOf(date.getTime()) + ": " + prechange+ " > "+ this.file.getName().toString();
		User.logger.log(Level.INFO, msg);
		
	}
	
	/**
	 * Rename a file base on a list of tags.
	 * @param tags the list of tags want to be added or deleted.
	 * @param order the action of adding tags or deleting tags. Only accept String ADDTAG or String DELTAG.
     */
	public void renameImageTags(ArrayList<Tag> tags, String order){
		for (Tag tag: tags){
			renameImage(tag, order);
		}
	}

	/**
	 * Get the renaming hisotry of this image and store all the old names into this.History.
	 * @throws IOException 
     */
	public void getOddName() throws IOException{
		ArrayList<String> list = new ArrayList<>();
		String fileName = this.file.getName();
		BufferedReader br = new BufferedReader(new FileReader("events.log"));
	    String s;
	    while ((s = br.readLine()) != null) {
	    	if(s.startsWith("INFO")){
	    		list.add(0, s);
	    	}
	    }
	    br.close();
	    for(String n : list){
	    	if(n.contains(fileName)){
	    		fileName = n.split(" > ")[0].split(" ")[2];
	    		if(!history.contains(fileName)){
	    			history.add(fileName);   			
	    		}
	    	}
	    }
	}
	
	public String FileName(){
		return this.file.getName();
	}

	/**
	public static void main(String[] args) throws SecurityException, IOException {
		File file = new File("/Users/kasipinkii/Documents/Computer Science/CSC207/FileTester/LevelA.jpg");
		PhotoRenamer r = new PhotoRenamer(file);
		Tag tag = new Tag("s");
		Tag tag1 = new Tag("p");
		Tag tag2 = new Tag("ppppp");
		r.renameImage(tag, ADDTAG);
		r.renameImage(tag1, ADDTAG);
		r.renameImage(tag2, ADDTAG);
		r.getOddName();
		System.out.println(r.history);
		r.renameImage(tag2, DELTAG);
		r.getOddName();
		System.out.println(r.history);
		
		Tag tag21 = new Tag("21");
		Tag tag22 = new Tag("22");
		Tag tag23 = new Tag("23");
		ArrayList<Tag> r2 = new ArrayList<Tag>();
		r2.add(tag21);
		r2.add(tag22);
		r2.add(tag23);
		r.renameImageTags(r2, ADDTAG);
		System.out.println(r.FileName());
		r.renameImageTags(r2, DELTAG);
		System.out.println(r.FileName());
	}*/

}
