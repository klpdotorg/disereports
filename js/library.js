var info;
var translations;

// Load the Visualization API and the piechart package.
google.load('visualization', '1', {'packages':['corechart','table','imagechart']});
var table1;

var levels = ['GREEN','RED','ORANGE','WHITE','BLUE','YELLOW']
var languages = ['ENGLISH','KANNADA','E/K','URDU','HINDI','E/H','TAMIL','TELUGU']

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
  consttype=info["const_type"];
  translations = info['transdict'];
  now = new Date()
  document.getElementById("reportdate").innerHTML = now.toDateString();
  document.getElementById("rephead").innerHTML = "<img src=\'/images/" + info["logo_link"] + "\' width='300px' vertical-align='bottom' border=0 />";

 document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'/images/arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"
                                                 + info['const_name'] + "</h1>";
  constinfo =  "<dl class='header-def'><dt>";
  if(consttype=='MP Constituency' || consttype=='MLA Constituency' || consttype=='Ward'){
    constinfo = constinfo + "<dt>" + translations['H8'] + "</dt><dd>" + info["const_code"] + "</dd>"
                                                 + "<dt>" + translations['H9'] + "</dt><dd>" + info["const_rep"] + "</dd>"
                                                + "<dt>" + translations['H10'] + "</dt><dd>" + info["const_party"] + "</dd>";
  }
  else if(consttype=='BLOCK' || consttype=='PROJECT'){
    constinfo =constinfo  + "<dt>" + translations["DISTRICT"] + "</dt><dd>" + info["const_dist"] + "</dd>";
  }
  else if(consttype=='CLUSTER' || consttype=='CIRCLE'){
    constinfo = constinfo + "<dt>" + translations["DISTRICT"] + "</dt><dd>" + info["const_dist"] + "</dd>"
                                                + "<dt>" + translations["BLOCK"]+"/"+translations["PROJECT"] + "</dt><dd>" + info["const_blck"] + "</dd>";
  }
  document.getElementById("constinfo").innerHTML = constinfo + "</dl>";;
  document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
          '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
          '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
          '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;
  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'><dt>' + translations['H11'] + '</dt><dd>' + info["inst_counts"]["schcount"] + '</dd>'
                                                  + '<dt>' + translations['H12'] + '</dt><dd>' + info["inst_counts"]["preschcount"] + '</dd></dl>';


/*  document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'/images/af_arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"  
                                               + info['const_name'] + "</h1>";
  document.getElementById("constinfo").innerHTML =  "<dl class='header-def'><dt>" + translations['H8'] + "</dt><dd>"
                           + info["const_code"] + "</dd>"
                           + "<dt>" + translations['H9'] + "</dt><dd>" + info["const_rep"] + "</dd>"
                           + "<dt>" + translations['H10'] + "</dt><dd>" + info["const_party"] + "</dd>"
			   + "</dl>";
  document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
  '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
  '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
  '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;*/

  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'>' 
			   + '<dt style="font-size:9pt">' + translations['H11'] + '</dt>'
                           + '<dd>' + info["inst_counts"]["abs_schcount"] + '</dd>'
			   + '<dt style="font-size:9pt">' + translations['H95'] + '</dt>'
                           + '<dd>' + info["lib_count"] + '</dd>'
			   + '<dt style="font-size:9pt">' + translations['H96'] + '</dt>'
                           + '<dd>' + ConvertToIndian(info["lib_stucount"],false) + '</dd></dl>'
  if(parseInt(info["lib_count"]) != 0){
  
    document.getElementById("libintrohead").innerHTML = translations['H84'];
    document.getElementById('libintro_txt').innerHTML = (info['libintro_txt'] == 'undefined') ? translations['H60'] : info['libintro_txt'];
    //lib_summary_chart();

    document.getElementById("libstatushead").innerHTML = translations['H85'];
    document.getElementById('libstatus_txt').innerHTML = (info['libstatus_txt'] == 'undefined') ? translations['H60'] : info['libstatus_txt'];
    lib_status_chart();

    document.getElementById("libinfrahead").innerHTML = translations['H86'];
    document.getElementById('libinfra_txt').innerHTML = (info['libinfra_txt'] == 'undefined') ? translations['H60'] : info['libinfra_txt'];
    document.getElementById('libexp_txt').innerHTML = (info['libexp_txt'] == 'undefined') ? translations['H60'] : info['libexp_txt'];
    lib_infra_chart();

    document.getElementById("libtxnlanghead").innerHTML = translations['H87'];
    document.getElementById("libtxnlevelhead").innerHTML = '<br><br>'+translations['H89'];
    document.getElementById('libtxn_txt').innerHTML = (info['libtxn_txt'] == 'undefined') ? translations['H60'] : info['libtxn_txt'];

    document.getElementById('libtxnlevel_txt').innerHTML = (info['libtxnlevel_txt'] == 'undefined') ? translations['H60'] : info['libtxnlevel_txt'];
    document.getElementById('libtxnlang_txt').innerHTML = (info['libtxnlang_txt'] == 'undefined') ? translations['H60'] : info['libtxnlang_txt'];
    document.getElementById("lib_graphic").innerHTML = "<img src=\'/images/lib_graphic.png\' width=\'95px\' style=\'padding-top:60px\'/>" ;
    lib_txnclass_table();
    lib_txntime_chart();
  if(Object.keys(info["neighbours_lib"]).length > 0) {
    libneighbours_chart();
  }
    document.getElementById("libneighhead").innerHTML = translations['H88'];
    document.getElementById('libneighbours_txt').innerHTML = (info['libneighbours_txt'] == 'undefined') ? translations['H60'] : info['libneighbours_txt'];


    document.getElementById('source_txt').innerHTML = (info['source_txt'] == 'undefined') ? translations['H60'] : info['source_txt'];
    document.getElementById('collab_txt').innerHTML = (info['collab_txt'] == 'undefined') ? translations['H60'] : info['collab_txt'];
  }
}

function lib_summary_chart()
{
      /*
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Medium of Instruction');
      data.addColumn('number', 'Number');
      for (var key in info["lib_moicount"]){
        data.addRow([key , parseInt(info["lib_moicount"][key])]);
      }
      var chart1 = new google.visualization.PieChart(document.getElementById('libsch_moi_gph'));
      chart1.draw(data, {width: 450, height: 200, title: translations['H90'],colors:['0b2465','5c82ff','c6d5ff','98b1ff','96afff']});
      document.getElementById("lib_count").innerHTML = translations['H95'] + ':' + info["lib_count"];
      document.getElementById("libstu_count").innerHTML = translations['H96'] + ':' + info["lib_stucount"];
      document.getElementById("libsch_count").innerHTML = translations['H94'] + ':' + info["inst_counts"]["abs_schcount"] ;
     */ 
}

function lib_status_chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string' , translations['H85']);
      data.addColumn('number', translations['H99']);
      for (var key in info["lib_status"]){
        data.addRow([key , info["lib_status"][key]]);
      }
      data.sort([{column:1,desc:true}]);
      var table1 = new google.visualization.Table(document.getElementById('libstatus_tb'));
      table1.draw(data, {width: 450, allowHtml: true});
}

function lib_infra_chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string' , translations['H100']);
      data.addColumn('string', translations['H99']);
      for (var key in info["lib_summary"]){
        data.addRow([key , ConvertToIndian(info["lib_summary"][key],false)]);
      }
      data.sort([{column:1,desc:true}]);
      var table2 = new google.visualization.Table(document.getElementById('libinfra_tb'));
      table2.draw(data, {width: 450, allowHtml: true});

      data = new google.visualization.DataTable();
      data.addColumn('string' , translations['H104']);
      data.addColumn('string', translations['H99']);
      data.addRow([translations['H105'] , ConvertToIndian(info["teachers_count"],false)]);
      data.addRow([translations['H106'] , ConvertToIndian(info["librarian_count"],false)]);
      data.sort([{column:1,desc:true}]);
      var table5 = new google.visualization.Table(document.getElementById('libtraining_tb'));
      table5.draw(data, {width: 450, allowHtml: true});
}

function lib_txnclass_table()
{
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Class');
      for (var i in levels) {
          data.addColumn('number', levels[i].toTitleCase());
      }
      for (var key in info["lib_class_level"]){
        row = ['Class ' + key]
        for (var i in levels) {
          row.push(info["lib_class_level"][key][levels[i]]);
        }
        data.addRow(row);
      }
      data.sort([{column:0,desc:false}]);
      var chart5 = new google.visualization.ColumnChart(document.getElementById('libtxnclasslevel_tb'));
      chart5.draw(data, {width: 750, height: 250, chartArea:{width:'72%'},  title: translations['H97'],colors:['green','red','orange','grey','blue','yellow'],hAxis:{slantedText:true}});
      //var table3 = new google.visualization.Table(document.getElementById('libtxnclasslevel_tb'));
      //table3.draw(data, {width: 600, allowHtml: true});
      /* 
      data = new google.visualization.DataTable();
      data.addColumn('string' , 'Class');
      for (var j in languages) {
        data.addColumn('number', languages[j]);
      }
      for (var key in info["lib_class_lang"]){
        row = ['Class ' + key]
        for (var j in languages) {
          row.push(info["lib_class_lang"][key][languages[j]]);
        }
        data.addRow(row);
      }
      data.sort([{column:0,desc:false}]);
      var chart6 = new google.visualization.ColumnChart(document.getElementById('libtxnclasslang_tb'));
      chart6.draw(data, {width: 750, height: 350, chartArea:{width:'65%'},  title: translations['H98'],colors:['CF4328','FE8F01','F1978F','78448C','7A94D1','BABAD4','B9A2B4','DDB2AB'],hAxis:{slantedText:true}});
      //var table4 = new google.visualization.Table(document.getElementById('libtxnclasslang_tb'));
      //table4.draw(data, {width: 600, allowHtml: true});
      */
}

function lib_txntime_chart()
{
      var months=['Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Month');
      for (var i in levels) {
          data.addColumn('number', levels[i].toTitleCase());
      }
      for (var key in months){
        row = [months[key]]
        for (var i in levels) {
          if(months[key] in info["lib_level"]) 
            row.push(info["lib_level"][months[key]][levels[i]]);
          else
            row.push(0);
        }
        data.addRow(row);
      }
      var chart2 = new google.visualization.LineChart(document.getElementById('libtxntimelevel_gph'));
      chart2.draw(data, {width: 750, height: 250, chartArea:{width:'72%'},  title: translations['H91'],colors:['green','red','orange','grey','blue','yellow'],hAxis:{slantedText:true},pointSize:3,lineWidth:2});

      data = new google.visualization.DataTable();
      data.addColumn('string' , 'Month');
      for (var j in languages) {
        data.addColumn('number', languages[j].toTitleCase());
      }
      for (var key in months){
        row = [months[key]]
        for (var j in languages) {
          if(months[key] in info["lib_lang"]) 
            row.push(info["lib_lang"][months[key]][languages[j]]);
          else
            row.push(0)
        }
        data.addRow(row);
      }
      var chart3 = new google.visualization.LineChart(document.getElementById('libtxntimelang_gph'));
      chart3.draw(data, {width: 850, height: 350, chartArea:{width:'70%'},  title: translations['H92'],colors:['CF4328','FE8F01','F1978F','78448C','7A94D1','BABAD4','B9A2B4','DDB2AB'],hAxis:{slantedText:true},pointSize:3,lineWidth:2});
}

function libneighbours_chart()
{
      data = new google.visualization.DataTable();
      data.addColumn('string' , translations['H6']);
      data.addColumn('string' , translations['H101']);
      data.addColumn('string' , translations['H102']);
      data.addColumn('string' , translations['H107']);
      data.addColumn('string' , translations['H103']);
      data.addColumn('number' , translations['H101']);
      data.addColumn('number' , translations['H103']);
      
      for (var key in info["neighbours_lib"]){
        data.addRow([key, ConvertToIndian(info["neighbours_lib"][key]["libtxn"],false), ConvertToIndian(info["neighbours_lib"][key]["libinfra"],false), ConvertToIndian(info["neighbours_lib"][key]["libschcount"]),ConvertToIndian(info["neighbours_lib"][key]["libstu"],false),info["neighbours_lib"][key]["libtxn"],info["neighbours_lib"][key]["libstu"]]);
      }
      data.sort([{column:1,desc:true}]);

      var chartview = new google.visualization.DataView(data);
      chartview.setColumns([0,5,6]);
      var tableview = new google.visualization.DataView(data);
      tableview.setColumns([0,1,2,3,4]);
      var chart4 = new google.visualization.BarChart(document.getElementById('libneighbours_gph'));
      chart4.draw(chartview, {width: '100%', height: 300, chartArea:{width:'68%'}, title: translations['H93'],colors:['242c60','96afff','b5e1ff']});
      var table5 = new google.visualization.Table(document.getElementById('libneighbours_tb'));
      table5.draw(tableview, {width: 750, allowHtml: true});


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
