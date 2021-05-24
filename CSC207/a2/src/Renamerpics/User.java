package Renamerpics;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

public class User{
	
	/**An ArrayList contains all User's current tags*/
	private ArrayList<Tag> currentList;
	
	protected static final Logger logger = Logger.getLogger(User.class.getName());
    
	/**
     * Creat a New User with a new ArrayList of default tags. 
	 * @throws IOException 
	 * @throws SecurityException 
     */
    public User(ArrayList<Tag> tags) throws SecurityException, IOException{
    	logger.setLevel(Level.ALL);
    	currentList = tags;
    }
    
    /**
     * Creat a New User with a empty ArrayList of tags. 
     */
    public User(){
    	logger.setLevel(Level.ALL);
    	currentList = new ArrayList<Tag>();
    }

    /**
     * User can add tags to their currentags. 
     * @param tag the tag that User want to add.
     */
	public void addUserTag(String tag){
		if (currentList == null){
			currentList = new ArrayList<Tag>();
		}else{
		    if(!this.currentList.contains(tag)){
			    Tag newTag = new Tag(tag);
			    this.currentList.add(newTag);
		    }
		}
	}
    /**
     * User can delete tags to their currentags. 
     * @param tag the tag that User want to delete.
     */
	public void delUserTag(Tag tag){
		if(this.currentList.contains(tag)){
			this.currentList.remove(tag);
		}
	}
	
	/**
     * User can view all their curretn tags. 
     * @return a string of all the current tag seperated by ; .
     */
	public String viewTags(){
		String r = new String();
		for (Tag tag:  currentList){
			r += tag.toString() + ";";
		}
		return r;
	}
	
	/**
     * User can view the entire log history. 
     * @throws IOException 
     * @return ArrayList<String> of 
     */
	@SuppressWarnings("finally")
	public String viewLogFile() throws IOException{
		String r = "";
		try{
			String workingDir = System.getProperty("events.log");
			File logfile = new File(workingDir);
			BufferedReader br = new BufferedReader(new FileReader(logfile));
		    String s;
		    while ((s = br.readLine()) != null) {
		    	r += s + "\n";
		    }
		    br.close();
		} catch (NullPointerException o) {
			r += "No Log to be viewed";
		} finally{
			return r;
		}
	}
	
	/**
	public static void main(String[] args) throws SecurityException, IOException {
		Tag tag1 = new Tag("1");
		Tag tag2 = new Tag("2");
		Tag tag3 = new Tag("3");
		ArrayList<Tag> tags = new ArrayList<Tag>();
		tags.add(tag1);
		tags.add(tag2);
		tags.add(tag3);
		User userA = new User();
		User userB = new User(tags);
		userA.addUserTag("a");
		userA.addUserTag("b");
		userB.delUserTag(tag2);
		userB.delUserTag(tag3);
		System.out.println(userA.viewTags());
		System.out.println(userB.viewTags());
		System.out.println(userB.viewLogFile());
	}*/
}
