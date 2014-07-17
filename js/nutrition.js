var info;
var translations;

// Load the Visualization API and the piechart package.
google.load('visualization', '1', {'packages':['corechart','table','imagechart']});
var table1;

String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){
      if(txt.indexOf('/')>0)
        return txt;
      else
	return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};
    
function initialise(data)
{
  info = data;
  translations = info['transdict'];
  now = new Date()
  document.getElementById("reportdate").innerHTML = now.toDateString();
  document.getElementById("rephead").innerHTML = "<img src=\'/images/KLP_logo2.png\' width='130px' vertical-align='top' border=0 />" + '<br/>' + translations['H56'];

  document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'/images/arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"  
                                               + info['const_name'].toUpperCase() + "</h1>";
  document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
  '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
  '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
  '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;
  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'>' 
			   + '<dt style="font-size:9pt">' + translations['H108']+ '</dt>'
                           + '<dd style="font-size:9pt">' + info["sch_count"]["totsch"] + '</dd>'
			   + '<dt style="font-size:9pt">' + translations['H109'] + '</dt>'
                           + '<dd style="font-size:9pt">' + ConvertToIndian(info["sch_count"]["mdmsch"],false) + '</dd></dl>'
  if(parseInt(info["lib_count"]) != 0){
  

    document.getElementById("nutinfohead").innerHTML = translations['H110'];
    document.getElementById('nutinfo_txt').innerHTML = (info['nutinfo_txt'] == 'undefined') ? translations['H60'] : info['nutinfo_txt'];
    nutinfo_chart();

    document.getElementById('source_txt').innerHTML = (info['source_txt'] == 'undefined') ? translations['H60'] : info['source_txt'];
    document.getElementById('collab_txt').innerHTML = (info['collab_txt'] == 'undefined') ? translations['H60'] : info['collab_txt'];
  }
}

function nutinfo_chart()
{
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Month_Week');
      data.addColumn('number', 'Food Indent');
      data.addColumn('number', 'Attendance');
      data.addColumn('number', 'DISE-enrollment');
      data.addColumn('number', 'KLP-enrollment');
      var months = ['January','February','March','April','May','June','July','August','September','October','November','December']
      for (var each in months ){
        if(months[each] in info["mdm_agg"]) {
          mon = months[each];
          for(var wk=1; wk<5;wk++) {
            data.addRow([mon + ' (Week ' + wk + ')', info["mdm_agg"][mon][wk][0], info["mdm_agg"][mon][wk][1], parseInt(info["dise_enrol"]["numboys"])+parseInt(info["dise_enrol"]["numgirls"]),parseInt(info["klp_enrol"]["numgirls"])+ parseInt(info["klp_enrol"]["numboys"])]);
          }
        }
      }
      var chart = new google.visualization.LineChart(document.getElementById('nutinfo_chart'));
      chart.draw(data, {width: 800, height: 500, chartArea:{width:'60%'}, title:  translations['H111'], backgroundColor: 'transparent', pieSliceText:'label', pointSize:5, colors: ['purple','orange','blue','green'],vAxis:{title:translations['H112']},hAxis:{slantedText:true, slantedTextAngle:45}});

}

//UTILITY FUCTIONS----------------------------

function sortDict(unsortedObj)
{
  var sortable = [];
  for (var key in unsortedObj)
  sortable.push([key, unsortedObj[key]]);
  var sortedDict = sortable.sort(function(a, b) {return b[1] - a[1]});
  return sortedDict;
}

function roundNumber(rnum, rlength) { // Arguments: number to round, number of decimal places
  var newnumber = Math.round(rnum*Math.pow(10,rlength))/Math.pow(10,rlength);
  return parseFloat(newnumber); // Output the result to the form field (change for your purposes)
}


function isEmpty(ob){
  for(var i in ob){ return false;}
  return true;
}

function ConvertToIndian(inputString,colour_code) { 
      cc_str = '';
      if( inputString == undefined || inputString == null)
        inputString = '0'
      if(colour_code){
        val = parseFloat(inputString[0]);
        bm = parseFloat(inputString[1]);
        /*if (val >= bm) {*/
        if (val >= 70) {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#43AD2C;">' 
        }
        else {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#CD4306;">' 
        }
      }
      inputString = inputString.toString(); 
      var numberArray = inputString.split('.', 2); 
      var pref = parseInt(numberArray[0]); 
      var suf = numberArray[1]; 
      var outputString = ''; 
      if (isNaN(pref)) return ''; 
      var minus = ''; 
      if (pref < 0) minus = '-'; 
      pref = Math.abs(pref).toString(); 
      if (pref.length > 3) { 
      var lastThree = pref.substr(pref.length - 3, pref.length); 
      pref = pref.substr(0, pref.length - 3); 
      if (pref.length % 2 > 0) { 
      outputString += pref.substr(0, 1) + ','; 
      pref = pref.substr(1, pref.length - 1); 
      } 

      while (pref.length >= 2) { 
      outputString += pref.substr(0, 2) + ','; 
      pref = pref.substr(2, pref.length); 
      } 

      outputString += lastThree; 
      } else { 

      outputString = minus + pref; 
      } 

      if (!isNaN(suf)) outputString += '.' + suf; 
      if(colour_code) {
        outputString = cc_str + outputString + '</span>%' 
        outputString = outputString + '<span style="font-size:8pt">&nbsp;&nbsp;&nbsp;' + translations['Bangalore Avg'] + ': ' + bm + '%</span></span>';
        return outputString; 
      } else {
        return outputString; 
      }
}

function ColourIcon(value,key) { 

      val = parseFloat(value[0]);
      /*bm = parseFloat(value[1]);
      if (val >= bm) {*/
      if (val >= 70) {
        return key;
      }
      else {
        return key.replace('.png','n.png');
      }
}
