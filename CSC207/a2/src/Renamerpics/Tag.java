package Renamerpics;


public class Tag {
	
	/** The string of a tag. */
	public String tag;
	/** All tags start with PREFIX. */
	public final static String PREFIX = "@";
	
	/**
     * Creates a Tag of the string. Tag starts with @.
     */
	public Tag(String name){
		this.tag = PREFIX + name;
	}
	
	/**
     * Give the string of the tag.
     * @return the string format of the tag.
     */
	public String toString(){
		return this.tag;
	}
	
	/**
    public static void main(String[] args) {
    	Tag tag = new Tag("see");
    	System.out.println(tag.toString());
	}*/

}
