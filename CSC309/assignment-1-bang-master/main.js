/*
 * HW1 API testing. You should implement following 3 functioins.
 * - getListsOfItems:
 * 	   Find a RESTFUL API and use GET to retrive a list of items.
 * - getOneItemById:
 *     Retrieve a single item by id based on the list you get from 
 * 	   getListsOfItems().
 * - getOneAttributeFromItem:
 *     Return any attribute from the retrieved item. 
 *     Ex: Return the temperature.
 */

var OK = 200;
var request = require('request');

var siteurl = 'https://www.metaweather.com/api/location/4118/2017/09/01/';
var idName = "id";

var app = {
	/*
	* Add blank lines
	*/
	addBlankLines: function(){
		var i=0;
		while(i<5){
			console.log("");
			i++;
		}
	},

	/*
	*return a rendom integer within the range [start,end)
	*/
	getRandInt: function (start,end){
    	return Math.floor(Math.random() * (end - start) + start);
	},

	/*
	* Returns a list of items from the API.
	*
	* @return a promis of an array of items
	*/
	getListsOfItems: function() {
		return new Promise(function (resolve,reject) {
        	request(siteurl,function (err,res,body) {
	            if(err){
	                return reject(err);
	            }else if(res.statusCode !== OK){
	                err = new Error("Unexpected status code: " + res.statusCode);
	                err.res = res;
	                return reject(err);
	            }else{
		            var fullData = JSON.parse(body);
		           	return resolve(fullData);
		        }
	        });
	    });
	},

	/*
	* Returns single item given single id, this function runs independently
	*
	* @return Item
	*/
	getOneItemById: function(id) {
		return new Promise(function (resolve,reject){
			request(siteurl,function (err,res,body) {
		        if(err){
		            return reject(err);
		        }else if(res.statusCode !== OK){
		            err = new Error("Unexpected status code: " + res.statusCode);
		            err.res = res;
		            return reject(err);
		        }else{
			        var fullData = JSON.parse(body);

			        for(var i=0; i<fullData.length; i++){
						if(!fullData[i].hasOwnProperty(idName)){
							console.log("no field ",idName, " in this data");
							return reject(null);
						}

						if(fullData[i][idName]==id) return resolve(fullData[i]);
					}	

					return reject(null);
		        }
		    });
	    });
	},

	/*
	* Returns a single attribute from a given item (promise).
	*
	* @return a string
	*/
	getOneAttributeFromItem: function(item) {
		return item.then(function(fullData){
			if(fullData==null){
				console.log("Nothing found with id: ", searchId);
				return;
			}

			var count=0;
			var arr = [];
			
			for (var foo in fullData){
				if (fullData.hasOwnProperty(foo)) {
					count++;
					arr.push(`${foo} : ${fullData[foo]}`);
				 } 
			}
			return arr[app.getRandInt(0,count-1)];
		});
	},

	showAllIds: function(items){
		items
		.then(fullData=>{
			for(var i=0; i<fullData.length; i++){
				if(fullData[i].hasOwnProperty(idName)){
					console.log(fullData[i][idName]);
				}
			}
		})
		.catch(err=>{
			console.log(err);
		});
	},

	/*
	* Show piece of data in given promise 
	*/
	showData: function(prom){
		prom
		.then(fullData=>{
			if(fullData==null) return;
			console.log(fullData);
		})
		.catch(err=>{
			console.log(err);
		});
	},

	/*
	* Show datas in array of promise one by one when all promises are ready
	*/
	showDatas: function(arr){
		Promise.all(arr)
		.then(fullData=>{
			for(var i=0; i<3; i++){
				console.log("***********************************************");
				switch(i){
					case(0): 
						console.log("\t\t LIST OF ",fullData[0].length," ITEMS: ");
						break;
					case(1):
						console.log("SINGLE ITEM WITH '",idName,"=",searchId,"': ");
						break;
					case(2):
						console.log("\t\tA RANDOM ATTRIBUTE: ");
						break;
					default: 
				}
				console.log("***********************************************");
				console.log(fullData[i]);
				app.addBlankLines();
			}
		})
		.catch(err=>{
			console.log(err);
		});
	}
}

/*-------------main-------------*/

/*
* we use id as serchID which refers to
* a unique piece of information of weather at a particular time of 
* a date (2017/09/01)
*
* following are some sample id that can be using to search:
*
* 4958687521144832,5179214764441600,5859335854882816
* 6247726392016896,6558316348047360,6584474645037056
*/

var searchId = 6647771993997312;

/*uncomment the method below to get a list of all existed id*/
// app.showAllIds(app.getListsOfItems());

var items = app.getListsOfItems();
var item = app.getOneItemById(searchId);
var singleAttribute = app.getOneAttributeFromItem(item);

/*
* print out datas in this three promises one by one
*/

app.showDatas([items, item, singleAttribute]);

/*
* uncomment following method to print out data in each promise
*/

// app.showData(items);
// app.showData(item);
// app.showData(singleAttribute);

/*
* uncomment following comment block to get
* random 10 attributes of a given item
*/

// console.log("***********************************************");
// console.log("\tFOLLOWINF ARE 10 RANDOM ATTRIBUTE: ");
// console.log("***********************************************");
// for(var i=0; i<10; i++){
// 	singleAttribute = app.getOneAttributeFromItem(item);
// 	app.showData(singleAttribute);
// };